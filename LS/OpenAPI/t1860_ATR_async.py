"""
LS Open API / 서버저장조건 실시간검색(t1860), API사용자조건검색실시간(AFR)
2024.11.29

설명:
이 모듈은 LS Open API를 사용하여 주식 종목 검색(t1860 TR)을 수행하고, 
실시간 검색 데이터를 비동기 방식으로 수신하는 기능을 제공합니다.
WebSocket을 통해 실시간 데이터를 지속적으로 수신하며, 사용자 중단시까지 동작합니다.

구성:
1. API 설정 클래스: APIConfig
2. 요청 및 응답 데이터 클래스: T1860Request, AFRRequest, APIResponse
3. LS Open API 클라이언트 클래스: LSOpenAPI
   - t1860 TR 요청 메서드: request_t1860
   - 실시간 AFR 데이터 수신 메서드: receive_afr_data
4. 메인 실행 함수: main

사용 예:
메인 실행 함수(main)에서 LSOpenAPI 클래스의 인스턴스를 생성하고,
t1860 TR 요청 후 받은 알림 번호로 실시간 AFR 데이터 수신을 시작합니다.

주의사항:
- 'oauth_3', 'request_tr_4', 'key' 모듈이 필요합니다.
- 'key' 모듈에 사용자 ID와 인증 정보가 저장되어 있어야 합니다.
- 실제 서버 사용 시 APIConfig의 is_real 값을 적절히 설정해야 합니다.

히스토리:
1   2024.11.29 최초 작성
"""

import pprint
import asyncio
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
import json
import aiohttp
import oauth_3 as oauth
from request_tr_4 import request_tr
import key

@dataclass
class APIConfig:
    """LS Open API 설정"""
    is_real: bool
    base_url: str
    websocket_url: str
    stock_item_search_url: str

@dataclass
class T1860Request:
    """T1860 TR 요청 구조"""
    sSysUserFlag: str
    sFlag: str
    sAlertNum: str
    query_index: str

@dataclass
class AFRRequest:
    """AFR (실시간) 데이터 요청 구조"""
    tr_type: str
    tr_cd: str
    tr_key: str

@dataclass
class APIResponse:
    """일반 API 응답 구조"""
    header: Dict[str, Any]
    body: Optional[Dict[str, Any]]

# API 설정
config = APIConfig(
    is_real=True,
    base_url="https://openapi.ls-sec.co.kr:8080",
    websocket_url="wss://openapi.ls-sec.co.kr:9443/websocket",
    stock_item_search_url="https://openapi.ls-sec.co.kr:8080/stock/item-search"
)

class LSOpenAPI:
    """LS Open API 클라이언트: 주식 데이터 요청 및 실시간 데이터 수신 처리"""

    def __init__(self):
        """API 클라이언트 초기화: 접근 토큰 및 헤더 설정"""
        self.access_token: str = oauth.oauth(_real=config.is_real)
        self.headers: Dict[str, str] = {
            "content-type": "application/json; charset=utf-8",
            "authorization": self.access_token
        }

    async def request_t1860(self, query_index: str) -> Optional[str]:
        """T1860 TR 데이터 요청 및 알림 번호 반환"""
        t1860_request = T1860Request(
            sSysUserFlag="U",
            sFlag="E",
            sAlertNum="",
            query_index=f"{key.USER_ID:8}{query_index}"
        )

        t1860_input: Dict[str, Any] = {
            "url": config.stock_item_search_url,
            "tr_name": "t1860",
            "body": {"t1860InBlock": asdict(t1860_request)},
            "out_block_tags": ["t1860OutBlock"],
            "shcode": ""
        }

        try:
            data_frames, _, _ = request_tr(t1860_input, _real=config.is_real)
            if data_frames and len(data_frames) > 0:
                return data_frames[0]['sAlertNum'].iloc[0]
        except Exception as e:
            print(f"request_t1860 오류: {e}")
        return None

    async def receive_afr_data(self, alert_num: str) -> None:
        """실시간 AFR 데이터 수신 및 출력"""
        async with aiohttp.ClientSession() as session:
            async with session.ws_connect(config.websocket_url, headers=self.headers) as ws:
                afr_request = AFRRequest(
                    tr_type="3",
                    tr_cd="AFR",
                    tr_key=alert_num
                )
                request_data: Dict[str, Any] = {
                    "header": {
                        "token": self.access_token,
                        "tr_type": afr_request.tr_type
                    },
                    "body": {
                        "tr_cd": afr_request.tr_cd,
                        "tr_key": afr_request.tr_key
                    }
                }
                await ws.send_json(request_data)
                try:
                    while True:
                        msg = await ws.receive()
                        if msg.type == aiohttp.WSMsgType.TEXT:
                            response = APIResponse(**json.loads(msg.data))
                            print("수신된 AFR 데이터:")
                            pprint.pprint(asdict(response))
                        elif msg.type in (aiohttp.WSMsgType.CLOSED, aiohttp.WSMsgType.ERROR):
                            print("WebSocket 연결 종료")
                            break
                except asyncio.CancelledError:
                    print("AFR 데이터 수신 취소됨")
                finally:
                    await ws.close()

async def main(_test: bool = False) -> None:
    """API 클라이언트 실행 메인 함수"""
    api = LSOpenAPI()
    alert_num = await api.request_t1860("0000")
    if alert_num:
        print(f"수신된 sAlertNum: {alert_num}")
        receive_task = asyncio.create_task(api.receive_afr_data(alert_num))
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            print("메인 태스크 취소됨")
        finally:
            receive_task.cancel()
            await asyncio.gather(receive_task, return_exceptions=True)
    else:
        print("sAlertNum 수신 실패")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("사용자에 의해 프로그램 종료됨")
