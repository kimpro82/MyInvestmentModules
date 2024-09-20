import sys
import asyncio
import aiohttp
import oauth_3 as oauth
import pprint

# API 요청을 위한 기본 URL 설정
URL      = "https://openapi.ls-sec.co.kr:9443/stock/websocket"
MOCK_URL = "https://openapi.ls-sec.co.kr:29443/stock/websocket"
ORDER_URL = "https://openapi.ls-sec.co.kr:8080/stock/order"


async def async_request_tr(params):
    """비동기식으로 TR 요청을 처리하는 함수"""
    async with aiohttp.ClientSession() as session:
        async with session.post(params['url'], headers=params['header'], json=params['body']) as response:
            response_data = await response.json()
            return response_data


async def request_template(_real=False, _body=None):
    """TR 요청을 위한 공통 템플릿 함수"""
    _tr_name = sys._getframe(1).f_code.co_name              # 호출한 함수명을 가져옴
    print(_tr_name)                                         # Ok

    _url = URL if _real else MOCK_URL

    _header = {
        "token": f"Bearer {oauth.oauth(_real=_real)}",
        "tr_type": "1",
    }

    if _body is None:
        _body = {
            "tr_cd": _tr_name,
            "tr_key": "",
        }

    _params = {
        'url': _url,
        'header': _header,
        'body': _body,
        'tr_name': _tr_name,
    }

    return await async_request_tr(_params)


# SC0 ~ SC4 호출용 함수들
async def SC0(_body=None, _real=False):
    return await request_template(_real=_real, _body=_body)

async def SC1(_body=None, _real=False):
    return await request_template(_real=_real, _body=_body)

async def SC2(_body=None, _real=False):
    return await request_template(_real=_real, _body=_body)

async def SC3(_body=None, _real=False):
    return await request_template(_real=_real, _body=_body)

async def SC4(_body=None, _real=False):
    return await request_template(_real=_real, _body=_body)


async def receive_order_response(_real=False):
    """주문 응답을 비동기식으로 수신하는 함수"""

    async def handle_response(sc_function):
        while True:
            try:
                result = await sc_function()  # 함수 실행
                pprint.pprint(result)
            except Exception as e:
                print(f"Error while receiving response from {sc_function.__name__}: {e}")
                await asyncio.sleep(1)  # 짧은 대기 후 재시도

    # 각각의 TR 요청을 독립적으로 실행
    await asyncio.gather(
        handle_response(SC0),
        handle_response(SC1),
        handle_response(SC2),
        handle_response(SC3),
        handle_response(SC4),
    )


async def send_order_async(_real=False, _IsuNo=None, _OrdQty=None, _OrdPrc1=None, _OrdprcPtnCode=None):
    """비동기 주문 발송 함수"""
    
    # OAuth 토큰 발급
    _access_token = oauth.oauth(_real=_real)

    # 요청 헤더 설정
    _header = {
        "content-type": "application/json; charset=utf-8",  # 콘텐츠 타입
        "authorization": f"Bearer {_access_token}",  # OAuth 토큰
        "tr_cd": "CSPAT00601",  # TR 코드 (주문 코드)
        "tr_cont": "N",  # 연속 조회 여부
        "tr_cont_key": "",  # 연속 조회 키 (필요시 사용)
        "mac_address": ""  # MAC 주소 (필요시 사용)
    }

    # 요청 본문 설정
    _cspat00601_body = {
        "CSPAT00601InBlock1": {
            "IsuNo": _IsuNo,
            "OrdQty": _OrdQty,
            "OrdPrc": _OrdPrc1,
            "BnsTpCode": "2",  # 매수/매도 구분 (2: 매도)
            "OrdprcPtnCode": _OrdprcPtnCode,  # 호가유형코드
            "MgntrnCode": "000",  # 신용거래코드 (필요시 변경)
            "LoanDt": "",  # 대출일자 (필요시 추가)
            "OrdCndiTpCode": "0",  # 주문조건유형코드 (기본값)
        }
    }

    # 올바른 URL로 API 요청
    async with aiohttp.ClientSession() as session:
        async with session.post(ORDER_URL, headers=_header, json=_cspat00601_body) as response:
            return await response.json()


async def main(_real=False, _IsuNo=None, _OrdQty=None, _OrdPrc1=None, _OrdprcPtnCode=None):
    # 주문 응답 수신
    receive_task = asyncio.create_task(receive_order_response(_real))

    # 주문 발송
    _cspat00601_params = await send_order_async(_real, _IsuNo, _OrdQty, _OrdPrc1, _OrdprcPtnCode)

    # 주문 요청 결과를 비동기로 처리
    # pprint.pprint(_cspat00601_params)

    # 주문 응답을 기다림
    await receive_task


if __name__ == "__main__":
    # 실제 환경 여부 설정 (False: 모의투자)
    IS_REAL = True

    # 주식 종목번호 설정 (삼성전자: A005930)
    IsuNo = "005930" if IS_REAL else "A005930"

    # 호가유형코드 및 주문가 설정
    OrdprcPtnCode = "82"  # 지정가
    OrdPrc1 = 60000.0     # 최초 주문가
    OrdQty = 1            # 주문 수량

    # 메인 실행
    asyncio.run(main(IS_REAL, IsuNo, OrdQty, OrdPrc1, OrdprcPtnCode))
