# [My `LS OPEN API` Application Modules](/README.md#ls-open-api)

Code with `OPEN API` from *LS Securities Co., Ltd.*



### \<Reference>

- LS OPEN API Portal ☞ https://openapi.ls-sec.co.kr/ 


### \<List>

#### TR
- [서버저장조건 실시간검색(`t1860`), API사용자조건검색실시간(`AFR`) (2024.11.29)](#서버저장조건-실시간검색t1860-api사용자조건검색실시간afr-20241129)
- [현물주문(`CSPAT00601`) 外 : 비동기식 (2024.09.30)](#현물주문cspat00601-外--비동기식-20240930)
- [현물주문(`CSPAT00601`) 外 : 동기식 (2024.09.06)](#현물주문cspat00601-外--동기식-20240906)
- [현물계좌 잔고내역(`CSPAQ12300`), 주식잔고2(`t0424`) (2024.08.26)](#현물계좌-잔고내역cspaq12300-주식잔고2t0424-20240826)
- [서버저장조건 조건검색 (`t1859`, 2024.08.22)](#서버저장조건-조건검색-t1859-20240822)
- [외인기관종목별동향 2 (`t1716`, 2023.07.25)](#외인기관종목별동향-2-t1716-20230725)
- [외인기관종목별동향 (`t1716`, 2023.07.21)](#외인기관종목별동향-t1716-20230721)
- [재무순위종합 (`t3341`, 2023.07.14)](#재무순위종합-t3341-20230714)
#### Request TR & Save to CSV
- [Request TR 4 (2024.08.26)](#request-tr-4-20240826)
- [Request TR 3 (2024.08.22)](#request-tr-3-20240822)
- [Request TR 2 (2023.07.25)](#request-tr-2-20230725)
- [Request TR (2023.07.21)](#request-tr-20230721)
#### OAuth
- [Oauth 3 (2024.08.22)](#oauth-3-20240822)
- [Oauth 2 (2023.07.21)](#oauth-2-20230721)
- [Oauth (2023.07.11)](#oauth-20230711)


## [서버저장조건 실시간검색(`t1860`), API사용자조건검색실시간(`AFR`) (2024.11.29)](#list)

- Receive real-time conditional search results by passing the real-time key (`sAlertNum`) value received from `t1860` TR to `AFR` TR
- Improve code readability and maintainability by applying `@dataclass` and `typing` library
- Be aware that search conditions are **only** available in the real environment
- Future Improvements
  - Make it independent of the `request_tr_4` module
  - Apply `@dataclass` to other TRs as well
- Code and Results
  <details>
    <summary>Code : t1860_ATR_async.py</summary>

  ```py
  import pprint
  import asyncio
  from dataclasses import dataclass, asdict
  from typing import Optional, Dict, Any
  import json
  import aiohttp
  import oauth_3 as oauth
  from request_tr_4 import request_tr
  import key
  ```
  ```py
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
  ```
  ```py
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
  ```
  ```py
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
  ```
  </details>
  <details open="">
    <summary>Results</summary>

  ```txt
  수신된 sAlertNum: 1639410200I
  수신된 AFR 데이터:
  {'body': None,
  'header': {'rsp_cd': '00000',
            'rsp_msg': '정상처리되었습니다',
            'tr_cd': 'AFR',
            'tr_type': '3'}}
  ```
  </details>


## [현물주문(`CSPAT00601`) 外 : 비동기식 (2024.09.30)](#list)

- Improved from [현물주문(CSPAT00601) 外 : 동기식 (2024.09.06)](#현물주문cspat00601-外--동기식-20240906) as asynchronous 
- Code : `tr_stock_order_async.py`
  <details>
    <summary>Import modules and Declare constants</summary>

  ```py
  import asyncio
  import pprint
  import aiohttp
  import oauth_3 as oauth
  ```
  ```py
  # API 요청을 위한 기본 URL 설정
  URL      = "https://openapi.ls-sec.co.kr:9443/stock/websocket"
  MOCK_URL = "https://openapi.ls-sec.co.kr:29443/stock/websocket"
  ORDER_URL = "https://openapi.ls-sec.co.kr:8080/stock/order"
  ```
  </details>
  <details>
    <summary>async def send_api_request()</summary>

  ```py
  async def send_api_request(url, headers, body):
      """
      API 요청을 비동기 방식으로 발송하고 응답을 반환하는 함수

      Args:
          url (str): 요청할 API의 URL.
          headers (dict): 요청 헤더.
          body (dict): 요청 본문.

      Returns:
          dict: API 응답을 포함한 JSON 객체.
      """
      async with aiohttp.ClientSession() as session:
          async with session.post(url, headers=headers, json=body) as response:
              return await response.json()
  ```
  </details>
  <details>
    <summary>async def send_order_async()</summary>

  ```py
  async def send_order_async(_real=False, _IsuNo=None, _OrdQty=None, _OrdPrc1=None, _OrdprcPtnCode=None):
      """
      비동기 주문 발송 함수

      주식 주문을 비동기 방식으로 LS Open API에 요청합니다.

      Args:
          _real (bool): 실제 환경 여부. True는 실제 환경, False는 모의 투자.
          _IsuNo (str): 종목 번호 (예: '005930').
          _OrdQty (int): 주문 수량.
          _OrdPrc1 (float): 주문 가격.
          _OrdprcPtnCode (str): 호가유형코드 (예: '00' - 지정가, '03' - 시장가).

      Returns:
          dict: 주문 결과를 포함한 JSON 응답. 응답에는 주문 번호 등이 포함됩니다.
      
      주의:
          - 네트워크 요청 실패 시 예외가 발생할 수 있으므로 try-except로 처리하는 것이 좋습니다.
      """

      # OAuth 토큰 발급
      _access_token = oauth.oauth(_real=_real)

      # 요청 헤더 설정
      _header = {
          "content-type": "application/json; charset=utf-8",  # 요청 데이터 형식
          "authorization": f"Bearer {_access_token}",         # OAuth 토큰
          "tr_cd": "CSPAT00601",                              # TR 코드 (주문)
          "tr_cont": "N",                                     # 연속 조회 여부 (연속조회 미사용)
          "tr_cont_key": "",                                  # 연속 조회 키 (없음)
          "mac_address": ""                                   # MAC 주소 (필요시 사용)
      }

      # 요청 본문 설정
      _cspat00601_body = {
          "CSPAT00601InBlock1": {
              "IsuNo": _IsuNo,
              "OrdQty": _OrdQty,
              "OrdPrc": _OrdPrc1,
              "BnsTpCode": "2",                               # 매수/매도 구분 ('2'는 매도)
              "OrdprcPtnCode": _OrdprcPtnCode,                # 호가유형코드
              "MgntrnCode": "000",                            # 신용거래코드 ('000' - 일반)
              "LoanDt": "",                                   # 대출일자 (필요시 사용)
              "OrdCndiTpCode": "0",                           # 주문조건유형코드 ('0' - 기본값)
          }
      }

      # API 요청 발송
      return await send_api_request(ORDER_URL, _header, _cspat00601_body)
  ```
  </details>
  <details>
    <summary>async def correct_order_async()</summary>

  ```py
  async def correct_order_async(_real=False, _IsuNo=None, _OrdNo=None, _OrdQty=None, _OrdPrc2=None, _OrdprcPtnCode=None):
      """
      비동기 정정 주문 함수

      이미 발송된 주식 주문을 정정하는 요청을 비동기 방식으로 처리합니다.

      Args:
          _real (bool): 실제 환경 여부.
          _IsuNo (str): 종목 번호 (예: '005930').
          _OrdNo (str): 주문 번호 (기존 주문 번호).
          _OrdQty (int): 정정할 주문 수량.
          _OrdPrc2 (float): 정정할 주문 가격.
          _OrdprcPtnCode (str): 호가유형코드 (예: '00' - 지정가, '03' - 시장가).

      Returns:
          dict: 정정 주문 결과를 포함한 JSON 응답.
      
      주의:
          - 정정 가능한 주문만 대상으로 합니다. 이미 체결된 주문은 정정할 수 없습니다.
      """

      # OAuth 토큰 발급
      _access_token = oauth.oauth(_real=_real)

      # 요청 헤더 설정
      _header = {
          "content-type": "application/json; charset=utf-8",  # 요청 데이터 형식
          "authorization": f"Bearer {_access_token}",         # OAuth 토큰
          "tr_cd": "CSPAT00701",                              # TR 코드 (정정 주문)
          "tr_cont": "N",                                     # 연속 조회 여부
          "tr_cont_key": "",                                  # 연속 조회 키
          "mac_address": ""                                   # MAC 주소
      }

      # 정정 주문 본문 설정
      _cspat00701_body = {
          "CSPAT00701InBlock1": {
              "IsuNo": _IsuNo,
              "OrgOrdNo": _OrdNo,                             # 원래 주문 번호
              "OrdQty": _OrdQty,                              # 정정할 주문 수량
              "OrdPrc": _OrdPrc2,                             # 정정할 가격
              "BnsTpCode": "2",                               # 매도 주문 ('2'는 매도)
              "OrdprcPtnCode": _OrdprcPtnCode,                # 호가유형코드
              "MgntrnCode": "000",                            # 신용거래코드 ('000' - 일반)
              "LoanDt": "",                                   # 대출일자 (필요시 사용)
              "OrdCndiTpCode": "0",                           # 주문조건유형코드 ('0' - 기본값)
          }
      }

      # API 요청 발송
      return await send_api_request(ORDER_URL, _header, _cspat00701_body)
  ```
  </details>
  <details>
    <summary>async def cancel_order_async()</summary>

  ```py
  async def cancel_order_async(_real=False, _IsuNo=None, _OrdNo=None, _OrdQty=None):
      """
      비동기 취소 주문 함수

      이미 발송된 주식 주문을 취소하는 요청을 비동기 방식으로 처리합니다.

      Args:
          _real (bool): 실제 환경 여부.
          _IsuNo (str): 종목 번호 (예: '005930').
          _OrdNo (str): 주문 번호 (취소할 주문 번호).
          _OrdQty (int): 취소할 주문 수량.

      Returns:
          dict: 취소 주문 결과를 포함한 JSON 응답.
      
      주의:
          - 취소할 수 있는 상태의 주문만 대상으로 합니다. 체결된 주문은 취소할 수 없습니다.
      """

      # OAuth 토큰 발급
      _access_token = oauth.oauth(_real=_real)

      # 요청 헤더 설정
      _header = {
          "content-type": "application/json; charset=utf-8",  # 요청 데이터 형식
          "authorization": f"Bearer {_access_token}",         # OAuth 토큰
          "tr_cd": "CSPAT00801",                              # TR 코드 (취소 주문)
          "tr_cont": "N",                                     # 연속 조회 여부
          "tr_cont_key": "",                                  # 연속 조회 키
          "mac_address": ""                                   # MAC 주소
      }

      # 취소 주문 본문 설정
      _cspat00801 = {
          "CSPAT00801InBlock1": {
              "IsuNo": _IsuNo,
              "OrgOrdNo": _OrdNo,                             # 취소할 주문 번호
              "OrdQty": _OrdQty,                              # 취소할 수량
          }
      }

      # API 요청 발송
      return await send_api_request(ORDER_URL, _header, _cspat00801)
  ```
  </details>
  <details>
    <summary>async def main()</summary>

  ```py
  async def main(_real=False, _IsuNo=None, _OrdQty=None, _OrdPrc1=None, _OrdPrc2=None, _OrdprcPtnCode=None):
      """
      메인 비동기 함수

      주식 주문, 정정 주문, 취소 주문을 순차적으로 비동기 방식으로 처리합니다.
      """

      # 주문 발송
      _cspat00601_params = await send_order_async(_real, _IsuNo, _OrdQty, _OrdPrc1, _OrdprcPtnCode)
      # 발송된 주문의 주문 번호를 추출하여 저장합니다.
      OrdNo1 = _cspat00601_params['CSPAT00601OutBlock2']['OrdNo']
      # pprint.pprint(_cspat00601_params)                     # 주문 결과 출력
      pprint.pprint(OrdNo1)

      # 예시: 1초 후에 정정 주문 발송
      await asyncio.sleep(1)
      _cspat00701_params = await correct_order_async(_real, _IsuNo, OrdNo1, _OrdQty, _OrdPrc2, _OrdprcPtnCode)
      # pprint.pprint(_cspat00701_params)                     # 정정 주문 결과 출력
      # 정정된 주문의 새로운 주문 번호를 추출하여 저장합니다.
      OrdNo2 = _cspat00701_params['CSPAT00701OutBlock2']['OrdNo']
      pprint.pprint(OrdNo2)

      # 예시: 2초 후에 취소 주문 발송
      await asyncio.sleep(2)
      _cspat00801_params = await cancel_order_async(_real, _IsuNo, OrdNo2, _OrdQty)
      # pprint.pprint(_cspat00801_params)                     # 취소 주문 결과 출력
  ```
  </details>
  <details>
    <summary>Run</summary>

  ```py
  if __name__ == "__main__":

      from datetime import datetime

      IS_REAL = True                              # 실제 환경 여부 설정 (False: 모의투자, True: 실제 환경)
      IsuNo = "005930" if IS_REAL else "A005930"  # 주식 종목번호 설정 (삼성전자: 005930, 모의투자는 A005930)

      # 현재 시간을 기준으로 호가유형코드 설정
      current_time = datetime.now().time()
      if current_time > datetime.strptime("15:30", "%H:%M").time():
          if current_time < datetime.strptime("16:00", "%H:%M").time():
              OrdprcPtnCode = "81"                # 15:30 ~ 16:00 사이
          else:
              OrdprcPtnCode = "82"                # 16:00 ~ 18:00 사이
      else:
          OrdprcPtnCode = "00"                    # 그 외 시간 (정규 거래 시간)

      # 주문 가격과 수량 설정
      OrdPrc1 = 60000.0                           # 최초 주문 가격 (예: 60,000원)
      OrdPrc2 = 60100.0                           # 정정 주문 가격 (예: 60,100원)
      OrdQty = 1                                  # 주문 수량 (1주)

      # 비동기 메인 함수 실행
      asyncio.run(main(IS_REAL, IsuNo, OrdQty, OrdPrc1, OrdPrc2, OrdprcPtnCode))
  ```
  </details>
- Results
  <details open="">
    <summary>Results : Successful</summary>

  ```csv
  "0","주문NO","종목명","매매구분","주문수량","주문가격","현재가","체결수량","체결가격","미체결량","확인수량","상태","원주문","주문유형","주문시간","매체",
  "","23763","삼성전자","매수취소","1","0","61,500","0","0","0","1","취소확인","23762","시간외단일가","16:29:51","OPEN API",
  "","23762","삼성전자","매수정정","1","60,100","61,500","0","0","0","1","정정확인","23761","시간외단일가","16:29:49","OPEN API",
  "","23761","삼성전자","매수","1","60,000","61,500","0","0","0","0","완료","0","시간외단일가","16:29:47","OPEN API",
  ```
  </details>


## [현물주문(`CSPAT00601`) 外 : 동기식 (2024.09.06)](#list)

- [LS증권 OPEN API](https://openapi.ls-sec.co.kr/) > [API가이드](https://openapi.ls-sec.co.kr/apiservice) > [[주식] 주문](https://openapi.ls-sec.co.kr/apiservice?api_id=d0e216e0-10d9-479f-8a4d-e175b8bae307) > 현물주문(`CSPAT00601`), 현물정정주문(`CSPAT00701`), 현물취소주문(`CSPAT00801`)
- Code : `tr_stock_order.py`
  <details>
    <summary>Import modules and Declare constants</summary>

  ```py
  import sys
  import request_tr_4 as request_tr
  ```
  ```py
  # API 요청을 위한 기본 URL 설정
  URL = "https://openapi.ls-sec.co.kr:8080/stock/order"
  ```
  </details>
  <details>
    <summary>CSPAT00601()</summary>

  ```py
  def CSPAT00601(_body):
      """
      CSPAT00601: 주식 매수 주문 요청을 위한 함수

      매수 주문을 위한 TR 요청을 생성하는 함수입니다. 
      해당 함수는 주식 매수 주문에 필요한 정보를 받아 TR 요청을 위해 필요한
      URL, TR 이름, 출력 블록 태그 등의 데이터를 딕셔너리 형태로 반환합니다.

      Args:
          _body (dict): 주문 요청에 필요한 데이터가 포함된 딕셔너리

      Returns:
          dict: TR 요청에 필요한 정보 (URL, body, TR 이름, 출력 블록 태그 등) 
      """

      # TR 요청을 위한 URL 설정
      _url = URL

      # 함수 이름으로 TR 이름 설정 (이 함수는 'CSPAT00601')
      _tr_name = sys._getframe().f_code.co_name

      # 출력 블록 태그 설정 (결과 데이터를 참조하기 위한 키)
      # _out_block_tags = ["rsp_cd", "rsp_msg"]
      _out_block_tags = []
      for i in range(1, 3):
          _out_block_tags.append(f"{_tr_name}OutBlock{i}")

      # TR 요청에 필요한 정보를 딕셔너리로 반환
      return {
          'url': _url,              # 요청 URL
          'body': _body,            # 요청 바디
          'tr_name': _tr_name,      # TR 코드 이름
          'out_block_tags': _out_block_tags,  # 출력 블록 태그
          'shcode': None,           # 종목 코드 (필요시 사용)
      }
  ```
  </details>
  <details>
    <summary>CSPAT00701()</summary>

  ```py
  def CSPAT00701(_body):
      """
      CSPAT00701: 주식 주문 정정 요청을 위한 함수

      주식 주문을 정정하기 위한 TR 요청을 생성하는 함수입니다. 
      기존 주문을 정정할 때 필요한 정보를 받아, TR 요청에 사용할 
      URL, TR 이름, 출력 블록 태그 등의 데이터를 딕셔너리 형태로 반환합니다.

      Args:
          _body (dict): 주문 정정 요청에 필요한 데이터가 포함된 딕셔너리

      Returns:
          dict: TR 요청에 필요한 정보 (URL, body, TR 이름, 출력 블록 태그 등) 
      """

      # TR 요청을 위한 URL 설정
      _url = URL

      # 함수 이름으로 TR 이름 설정 (이 함수는 'CSPAT00701')
      _tr_name = sys._getframe().f_code.co_name

      # 출력 블록 태그 설정 (결과 데이터를 참조하기 위한 키)
      # _out_block_tags = ["rsp_cd", "rsp_msg"]
      _out_block_tags = []
      for i in range(1, 3):
          _out_block_tags.append(f"{_tr_name}OutBlock{i}")

      # TR 요청에 필요한 정보를 딕셔너리로 반환
      return {
          'url': _url,              # 요청 URL
          'body': _body,            # 요청 바디
          'tr_name': _tr_name,      # TR 코드 이름
          'out_block_tags': _out_block_tags,  # 출력 블록 태그
          'shcode': None,           # 종목 코드 (필요시 사용)
      }
  ```
  </details>
  <details>
    <summary>CSPAT00801()</summary>

  ```py
  def CSPAT00801(_body):
      """
      CSPAT00801: 주식 주문 취소 요청을 위한 함수

      주식 주문을 취소하기 위한 TR 요청을 생성하는 함수입니다. 
      기존 주문을 취소할 때 필요한 정보를 받아, TR 요청에 사용할 
      URL, TR 이름, 출력 블록 태그 등의 데이터를 딕셔너리 형태로 반환합니다.

      Args:
          _body (dict): 주문 취소 요청에 필요한 데이터가 포함된 딕셔너리

      Returns:
          dict: TR 요청에 필요한 정보 (URL, body, TR 이름, 출력 블록 태그 등) 
      """

      # TR 요청을 위한 URL 설정
      _url = URL

      # 함수 이름으로 TR 이름 설정 (이 함수는 'CSPAT00801')
      _tr_name = sys._getframe().f_code.co_name

      # 출력 블록 태그 설정 (결과 데이터를 참조하기 위한 키)
      # _out_block_tags = ["rsp_cd", "rsp_msg"]
      _out_block_tags = []
      for i in range(1, 3):
          _out_block_tags.append(f"{_tr_name}OutBlock{i}")

      # TR 요청에 필요한 정보를 딕셔너리로 반환
      return {
          'url': _url,              # 요청 URL
          'body': _body,            # 요청 바디
          'tr_name': _tr_name,      # TR 코드 이름
          'out_block_tags': _out_block_tags,  # 출력 블록 태그
          'shcode': None,           # 종목 코드 (필요시 사용)
      }
  ```
  </details>
  <details>
    <summary>Run</summary>

  ```py
  if __name__ == "__main__":
      import pprint

      # 실제 환경 여부 설정 (False: 모의투자)
      IS_REAL = False

      # 주식 종목번호 설정 (삼성전자: A005930)
      IsuNo = "A005930"

      # 호가유형코드 및 주문가 설정
      OrdprcPtnCode = "00"  # 지정가
      OrdPrc1 = 60000.0     # 최초 주문가
      OrdPrc2 = 65000.0     # 정정 주문가
      OrdQty = 1            # 주문 수량

      # 매수 주문 요청 데이터 설정
      cspat00601_body = {
          "CSPAT00601InBlock1": {
              "IsuNo": IsuNo,                 # 종목번호 (모의투자: A+종목코드)
              "OrdQty": OrdQty,               # 주문수량
              "OrdPrc": OrdPrc1,              # 주문가
              "BnsTpCode": "2",               # 매매구분 (1:매도, 2:매수)
              "OrdprcPtnCode": OrdprcPtnCode, # 호가유형코드 (00:지정가, 03:시장가 등)
              "MgntrnCode": "000",            # 신용거래코드 (000:보통)
              "LoanDt": "",                   # 대출일
              "OrdCndiTpCode": "0",           # 주문조건구분 (0:없음, 1:IOC, 2:FOK)
          }
      }
      # 매수 주문 요청을 위한 TR 요청 데이터 생성
      cspat00601_params = CSPAT00601(cspat00601_body)
      # pprint.pprint(cspat00601_params)
      results1 = request_tr.request_tr(cspat00601_params, _real=IS_REAL, _timeout=3)
      pprint.pprint(results1)

      # 첫 번째 주문번호 추출
      OrdNo = int(results1[0][1]["OrdNo"].values[0])
      print(OrdNo)

      # 주문 정정 요청 데이터 설정
      cspat00701_body = {
          "CSPAT00701InBlock1": {
              "OrgOrdNo": OrdNo,              # 원주문번호
              "IsuNo": IsuNo,                 # 종목번호 (모의투자: A+종목코드)
              "OrdQty": OrdQty,               # 주문수량
              "OrdprcPtnCode": OrdprcPtnCode, # 호가유형코드 (00:지정가, 03:시장가 등)
              "OrdCndiTpCode": "0",           # 주문조건구분 (0:없음, 1:IOC, 2:FOK)
              "OrdPrc": OrdPrc2,              # 주문가 (정정된 가격)
          }
      }
      # 주문 정정 요청을 위한 TR 요청 데이터 생성
      cspat00701_params = CSPAT00701(cspat00701_body)
      # pprint.pprint(cspat00701_params)
      results2 = request_tr.request_tr(cspat00701_params, _real=IS_REAL, _timeout=3)
      pprint.pprint(results2)

      # 두 번째 주문번호 추출
      OrdNo2 = int(results2[0][1]["OrdNo"].values[0])
      print(OrdNo2)

      # 주문 취소 요청 데이터 설정
      cspat00801_body = {
          "CSPAT00801InBlock1": {
              "OrgOrdNo": OrdNo2,             # 원주문번호
              "IsuNo": IsuNo,                 # 종목번호 (모의투자: A+종목코드)
              "OrdQty": OrdQty,               # 주문수량
          }
      }
      # 주문 취소 요청을 위한 TR 요청 데이터 생성
      cspat00801_params = CSPAT00801(cspat00801_body)
      # pprint.pprint(cspat00801_params)
      results3 = request_tr.request_tr(cspat00801_params, _real=IS_REAL, _timeout=3)
      pprint.pprint(results3)

      # # 결과를 CSV 파일로 저장
      request_tr.save_csv(_data_frames=results1[0], _tr_name=results1[1])
      request_tr.save_csv(_data_frames=results2[0], _tr_name=results2[1])
      request_tr.save_csv(_data_frames=results3[0], _tr_name=results3[1])
  ```
  </details>
- Results
  <details open="">
    <summary>CSPAT00601()</summary>

  ```py
  RecCnt,AcntNo,InptPwd,IsuNo,OrdQty,OrdPrc,BnsTpCode,OrdprcPtnCode,PrgmOrdprcPtnCode,StslAbleYn,StslOrdprcTpCode,CommdaCode,MgntrnCode,LoanDt,MbrNo,OrdCndiTpCode,StrtgCode,GrpId,OrdSeqNo,PtflNo,BskNo,TrchNo,ItemNo,OpDrtnNo,LpYn,CvrgTpCode
  1,55503309601,0000,A005930,1,60000.00,2,00,00,0,0,40,000,,000,0,,,0,0,0,0,0,0,0,0
  ```
  ```py
  RecCnt,OrdNo,OrdTime,OrdMktCode,OrdPtnCode,ShtnIsuNo,MgempNo,OrdAmt,SpareOrdNo,CvrgSeqno,RsvOrdNo,SpotOrdQty,RuseOrdQty,MnyOrdAmt,SubstOrdAmt,RuseOrdAmt,AcntNm,IsuNm
  1,22609,145812026,40,00,A005930,,60000,0,0,0,1,0,0,0,0,김프로,삼성전자
  ```
  </details>
  <details open="">
    <summary>CSPAT00701()</summary>

  ```py
  RecCnt,OrgOrdNo,AcntNo,InptPwd,IsuNo,OrdQty,OrdprcPtnCode,OrdCndiTpCode,OrdPrc,CommdaCode,StrtgCode,GrpId,OrdSeqNo,PtflNo,BskNo,TrchNo,ItemNo
  1,22609,55503309601,0000,A005930,1,00,0,65000.00,40,,,0,0,0,0,0
  ```
  ```py
  RecCnt,OrdNo,PrntOrdNo,OrdTime,OrdMktCode,OrdPtnCode,ShtnIsuNo,PrgmOrdprcPtnCode,StslOrdprcTpCode,StslAbleYn,MgntrnCode,LoanDt,CvrgOrdTp,LpYn,MgempNo,OrdAmt,BnsTpCode,SpareOrdNo,CvrgSeqno,RsvOrdNo,MnyOrdAmt,SubstOrdAmt,RuseOrdAmt,AcntNm,IsuNm
  1,22610,22609,145812530,40,00,A005930,,,,000,,,,,65000,2,0,0,0,0,0,0,김프로,삼성전자
  ```
  </details>
  <details open="">
    <summary>CSPAT00801()</summary>

  ```py
  RecCnt,OrgOrdNo,AcntNo,InptPwd,IsuNo,OrdQty,CommdaCode,GrpId,StrtgCode,OrdSeqNo,PtflNo,BskNo,TrchNo,ItemNo
  1,22610,55503309601,0000,A005930,1,40,,,0,0,0,0,0
  ```
  ```py
  RecCnt,OrdNo,PrntOrdNo,OrdTime,OrdMktCode,OrdPtnCode,ShtnIsuNo,PrgmOrdprcPtnCode,StslOrdprcTpCode,StslAbleYn,MgntrnCode,LoanDt,CvrgOrdTp,LpYn,MgempNo,BnsTpCode,SpareOrdNo,CvrgSeqno,RsvOrdNo,AcntNm,IsuNm
  1,22611,22609,145813279,40,00,A005930,,,,,,,,,2,0,0,0,김프로,삼성전자
  ```
  </details>


## [현물계좌 잔고내역(`CSPAQ12300`), 주식잔고2(`t0424`) (2024.08.26)](#list)

- [LS증권 OPEN API](https://openapi.ls-sec.co.kr/) > [API가이드](https://openapi.ls-sec.co.kr/apiservice) > [[주식] 계좌](https://openapi.ls-sec.co.kr/apiservice?api_id=37d22d4d-83cd-40a4-a375-81b010a4a627) > 현물계좌 잔고내역(`CSPAQ12300`), 주식잔고2(`t0424`)
- Call the **CSPAQ12300** and **t0424** TR from *LS Open API* with `request_tr_4` and `oauth_3`
  - **CSPAQ12300** can distinguish between different accounts
  - **t0424** in XingAPI includes an `accno` field, but this field is absent in the Open API, ~~making it impossible to specify an account for trading~~ instead, each account is identified by its own unique keys
- Code : `tr_stock_accno.py`
  <details>
    <summary>Import modules and Declare constants</summary>

  ```py
  import sys
  import request_tr_4 as request_tr
  ```
  ```py
  # API 요청을 위한 기본 URL 설정
  URL = "https://openapi.ls-sec.co.kr:8080/stock/accno"
  ```
  </details>
  <details>
    <summary>CSPAQ12300()</summary>

  ```py
  def CSPAQ12300(_BalCreTp="0", _CmsnAppTpCode="0", _D2balBaseQryTp="0", _UprcTpCode="0"):
      """
      CSPAQ12300 TR 요청을 위한 함수.

      이 함수는 CSPAQ12300 TR에 필요한 요청 URL, 바디 및 출력 블록 태그를 설정하고 반환합니다.
      주식 계좌와 관련된 잔고 및 수수료 정보 조회에 사용됩니다.

      Args:
          _BalCreTp (str, optional): 잔고 구분 타입. 기본값은 '0'.
          _CmsnAppTpCode (str, optional): 수수료 적용 타입 코드. 기본값은 '0'.
          _D2balBaseQryTp (str, optional): D2잔고 기준 조회 타입. 기본값은 '0'.
          _UprcTpCode (str, optional): 단가 타입 코드. 기본값은 '0'.

      Returns:
          dict: CSPAQ12300 TR 요청에 필요한 정보가 담긴 딕셔너리.
      """

      # TR 요청을 위한 URL 설정
      _url = URL

      # 요청 바디 설정
      _body = {
          "t10424InBlock": {
              "BalCreTp": _BalCreTp,
              "CmsnAppTpCode": _CmsnAppTpCode,
              "D2balBaseQryTp": _D2balBaseQryTp,
              "UprcTpCode": _UprcTpCode,
          }
      }

      # 함수 이름으로 TR 이름 설정
      _tr_name = sys._getframe().f_code.co_name

      # 출력 블록 태그 (결과 데이터를 참조하기 위한 키) 설정
      _out_block_tags = []
      for i in range(1, 4):
          _out_block_tags.append(f"{_tr_name}OutBlock{i}")

      # TR 요청에 필요한 정보를 딕셔너리로 반환
      return {
          'url': _url,              # 요청 URL
          'body': _body,            # 요청 바디
          'tr_name': _tr_name,      # TR 코드 이름
          'out_block_tags': _out_block_tags,  # 출력 블록 태그
          'shcode': None,           # 종목 코드 (필요시 사용)
      }
  ```
  </details>
  <details>
    <summary>t0424()</summary>

  ```py
  def t0424(_cts_expcode=""):
      """
      t0424 TR 요청을 위한 함수.

      이 함수는 t0424 TR에 필요한 요청 URL, 바디 및 출력 블록 태그를 설정하고 반환합니다.
      주식 계좌와 관련된 정보 조회에 사용됩니다.
      
      Args:
          _cts_expcode (str, optional): 연속 조회를 위한 종목 코드. 기본값은 빈 문자열입니다.

      Returns:
          dict: t0424 TR 요청에 필요한 정보가 담긴 딕셔너리.
      """

      # TR 요청을 위한 URL 설정
      _url = URL

      # 함수 이름으로 TR 이름 설정
      _tr_name = sys._getframe().f_code.co_name

      # 요청 바디 설정
      _body = {
          "t10424InBlock": {
              "prcgb": "",  # 가격 구분
              "chegb": "",  # 체결 구분
              "dangb": "",  # 당일/전일 구분
              "charge": "",  # 수수료 구분
              "cts_expcode": _cts_expcode,  # 연속 조회를 위한 종목 코드
          }
      }

      # 출력 블록 태그 (결과 데이터를 참조하기 위한 키) 설정
      _out_block_tags = []
      for i in ["", "1"]:
          _out_block_tags.append(f"{_tr_name}OutBlock{i}")

      # TR 요청에 필요한 정보를 딕셔너리로 반환
      return {
          'url': _url,              # 요청 URL
          'body': _body,            # 요청 바디
          'tr_name': _tr_name,      # TR 코드 이름
          'out_block_tags': _out_block_tags,  # 출력 블록 태그
          'shcode': None,           # 종목 코드 (필요시 사용)
      }
  ```
  </details>
  <details>
    <summary>Run</summary>

  ```py
  if __name__ == "__main__":
      import pprint

      # CSPAQ12300 TR 요청을 위한 파라미터 설정 및 결과 출력
      cspaq12300_params = CSPAQ12300()
      # pprint.pprint(cspaq12300_params)
      results1 = request_tr.request_tr(cspaq12300_params, _real=False, _timeout=3)
      pprint.pprint(results1)

      # 결과를 CSV 파일로 저장
      request_tr.save_csv(_data_frames=results1[0], _tr_name=results1[1])

      # t0424 TR 요청을 위한 파라미터 설정 및 결과 출력
      t0424_params = t0424(_cts_expcode="")
      results2 = request_tr.request_tr(t0424_params, _real=False, _timeout=3)

      # 첫 번째 결과 블록의 첫 번째 데이터와 두 번째 데이터를 출력
      pprint.pprint(results2[0][0])
      pprint.pprint(results2[0][1])

      # 결과를 CSV 파일로 저장
      request_tr.save_csv(_data_frames=results2[0], _tr_name=results2[1])
  ```
  </details>
- Results
  <details open="">
    <summary>CSPAQ12300</summary>

  ```txt
  RecCnt,AcntNo,Pwd,BalCreTp,CmsnAppTpCode,D2balBaseQryTp,UprcTpCode
  1,55503048401,0000,,,,
  ```
  ```txt
  RecCnt,BrnNm,AcntNm,MnyOrdAbleAmt,MnyoutAbleAmt,SeOrdAbleAmt,KdqOrdAbleAmt,HtsOrdAbleAmt,MgnRat100pctOrdAbleAmt,BalEvalAmt,PchsAmt,RcvblAmt,PnlRat,InvstOrgAmt,InvstPlAmt,CrdtPldgOrdAmt,Dps,D1Dps,D2Dps,OrdDt,MnyMgn,SubstMgn,SubstAmt,PrdayBuyExecAmt,PrdaySellExecAmt,CrdayBuyExecAmt,CrdaySellExecAmt,EvalPnlSum,DpsastTotamt,Evrprc,RuseAmt,EtclndAmt,PrcAdjstAmt,D1CmsnAmt,D2CmsnAmt,D1EvrTax,D2EvrTax,D1SettPrergAmt,D2SettPrergAmt,PrdayKseMnyMgn,PrdayKseSubstMgn,PrdayKseCrdtMnyMgn,PrdayKseCrdtSubstMgn,CrdayKseMnyMgn,CrdayKseSubstMgn,CrdayKseCrdtMnyMgn,CrdayKseCrdtSubstMgn,PrdayKdqMnyMgn,PrdayKdqSubstMgn,PrdayKdqCrdtMnyMgn,PrdayKdqCrdtSubstMgn,CrdayKdqMnyMgn,CrdayKdqSubstMgn,CrdayKdqCrdtMnyMgn,CrdayKdqCrdtSubstMgn,PrdayFrbrdMnyMgn,PrdayFrbrdSubstMgn,CrdayFrbrdMnyMgn,CrdayFrbrdSubstMgn,PrdayCrbmkMnyMgn,PrdayCrbmkSubstMgn,CrdayCrbmkMnyMgn,CrdayCrbmkSubstMgn,DpspdgQty,BuyAdjstAmtD2,SellAdjstAmtD2,RepayRqrdAmtD1,RepayRqrdAmtD2,LoanAmt
  1,,김프로,100000000,100000000,0,0,0,100000000,0,0,0,0.000000,0,0,0,100000000,100000000,100000000,,0,0,0,0,0,0,0,0,100000000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  ```
  ```txt
  (No balance in the account)
  ```
  </details>
  <details open="">
    <summary>t0424</summary>

  ```txt
  sunamt,dtsunik,mamt,sunamt1,cts_expcode,tappamt,tdtsunik
  100000000,0,0,100000000,,0,0
  ```
  ```txt
  (No balance in the account)
  ```
  </details>


## [서버저장조건 조건검색 (`t1859`, 2024.08.22)](#list)

- [LS OPEN API > API가이드 > 주식 > [주식] 종목검색](https://openapi.ls-sec.co.kr/apiservice?api_id=6b67369a-dc7a-4cc7-8c33-71bb6336b6bf) > 서버저장조건 조건검색 (t1859)
- Call the **t1866** and **t1859** TR from *LS Open API* with `request_tr_3` and `oauth_3`
- Code : `t1859.py`
  <details>
    <summary>Import modules and Declare constants</summary>

  ```py
  import key
  import request_tr_3 as request_tr
  ```
  ```py
  # API 요청을 위한 기본 URL 설정
  URL = "https://openapi.ls-sec.co.kr:8080/stock/item-search"
  ```
  </details>
  <details>
    <summary>t1866()</summary>

  ```py
  def t1866(_gb="0", _cont=""):
      """
      종목 검색을 위한 t1866 TR 요청 정보를 생성하는 함수.

      Parameters:
          _gb (str): 검색 구분 코드 (기본값은 "0").
          _cont (str): 검색 내용 (기본값은 빈 문자열).

      Returns:
          dict: TR 요청에 필요한 URL, 헤더, 바디, 출력 블록 태그 등을 포함한 딕셔너리.
      """

      _url = URL

      # 요청에 필요한 헤더 설정
      _header = {
          "content-type": "application/json; charset=utf-8",
          "authorization": None,  # 인증 토큰. 이후 추가 필요
          "tr_cd": "t1866",  # TR 코드
          "tr_cont": "N",  # 연속 조회 여부
          "tr_cont_key": "",  # 연속 조회 키 (필요시 사용)
          "mac_address": ""  # MAC 주소 (필요시 사용)
      }

      # 요청 바디 설정
      _body = {
          "t1866InBlock": {
              "user_id": key.USER_ID,
              "gb": _gb,
              "group_name": "",
              "cont": _cont,
              "cont_key": "",
          }
      }

      # 출력 블록 태그 (결과 데이터를 참조하기 위한 키)
      _out_block_tag = ["OutBlock", "OutBlock1"]

      # TR 요청에 필요한 정보를 딕셔너리로 반환
      return {
          'url': _url,
          'header': _header,
          'body': _body,
          'tr_name': t1866.__name__,
          'out_block_tag': _out_block_tag,
          'shcode': None,
      }
  ```
  </details>
  <details>
    <summary>t1859()</summary>

  ```py
  def t1859(_query_index="0000"):
      """
      특정 기준에 따른 종목 리스트 조회를 위한 t1859 TR 요청 정보를 생성하는 함수.

      Parameters:
          _query_index (str): 조회할 기준 인덱스 (기본값은 "0000").

      Returns:
          dict: TR 요청에 필요한 URL, 헤더, 바디, 출력 블록 태그 등을 포함한 딕셔너리.
      """

      _url = URL

      # 요청에 필요한 헤더 설정
      _header = {
          "content-type": "application/json; charset=utf-8",
          "authorization": None,  # 인증 토큰. 이후 추가 필요
          "tr_cd": "t1859",  # TR 코드
          "tr_cont": "N",  # 연속 조회 여부
          "tr_cont_key": "",  # 연속 조회 키 (필요시 사용)
          "mac_address": ""  # MAC 주소 (필요시 사용)
      }

      # 요청 바디 설정
      _body = {
          "t1859InBlock": {
              "query_index": f"{key.USER_ID:8}{_query_index}",
          }
      }

      # 출력 블록 태그 (결과 데이터를 참조하기 위한 키)
      _out_block_tag = ["OutBlock", "OutBlock1"]

      # TR 요청에 필요한 정보를 딕셔너리로 반환
      return {
          'url': _url,
          'header': _header,
          'body': _body,
          'tr_name': t1859.__name__,
          'out_block_tag': _out_block_tag,
          'shcode': None,
      }
  ```
  </details>
  <details>
    <summary>Run</summary>

  ```py
  if __name__ == "__main__":
      import pprint

      # t1866 TR 요청 테스트
      t1866_params = t1866()
      # pprint.pprint(t1866_params)

      # t1866 결과 요청 및 출력
      t1866_results = request_tr.request_tr(t1866_params, _timeout=3)
      # pprint.pprint(t1866_results[0])
      # request_tr.save_csv(_data_frames=t1866_results[0], _tr_name="t1866")

      # t1859 TR 요청 테스트
      t1859_results = request_tr.request_tr(t1859("0000"))
      pprint.pprint(t1859_results[0][1])
      request_tr.save_csv(_data_frames=t1859_results[0], _tr_name="t1859")
  ```
  </details>
- Results
  <details open="">
    <summary>t1866</summary>

  ```txt
  result_count,cont,contkey
  4,,
  ```
  ```txt
  query_index,group_name,query_name
  ********0000,나의전략,데일리모멘텀
  ********0001,나의전략,ETF Trading
  ********0002,나의전략,TRIX 주봉
  ********0003,나의전략,TRIX 일봉
  ```
  </details>
  <details open="">
    <summary>t1859</summary>

  ```txt
  result_count,result_time,text
  8,230539,
  ```
  ```txt
  shcode,hname,price,sign,change,diff,volume
  295310,에이치브이엠,12700,2,1790,16.41,2256154
  228760,지노믹트리,19080,2,2440,14.66,901801
  007460,에이프로젠,1784,2,184,11.50,29403465
  249420,일동제약,18390,2,1690,10.12,2832893
  461030,아이엠비디엑스,19780,2,1730,9.58,5572316
  462350,이노스페이스,21250,2,1700,8.70,250265
  003060,에이프로젠바이오로직스,1085,2,85,8.50,4552968
  465770,STX그린로지스,12570,2,820,6.98,1046078
  ```
  </details>


## [외인기관종목별동향 2 (`t1716`, 2023.07.25)](#list)

- Advanced from `t1716.py` in [외인기관종목별동향 (t1716, 2023.07.21)](#외인기관종목별동향-t1716-20230721)
  - `t1716_2.py` : Change `t1716()`'s return type : *tuple* → *dictionary*
  - Import `request_tr_2`
- Code and Results
  - `t1716_2.py`
    <details>
      <summary>Code (Mainly changed part)</summary>

    ```python
    def t1716(shcode = "005930", todt = "", period = 366):
        """
        ……

        Returns     :
            dict                    : 함수 호출 시 반환되는 값들을 딕셔너리로 묶어 반환합니다.
        """

        ……

        return {
            'url'           : _url,
            'header'        : _header,
            'body'          : _body,
            'tr_name'       : t1716.__name__,
            'out_block_tag' : _out_block_tag,
            'shcode'        : shcode
        }
    ```
    ```py
    if __name__ == "__main__":

        ……

        results = t1716()                                       # 함수 호출 결과를 딕셔너리로 받음
        pprint.pprint(results)
    ```
    </details>
    <details open="">
      <summary>Results</summary>

    ```txt
    {'body': {'t1716InBlock': {'frggubun': '1',
                              'fromdt': '20220725',
                              'gubun': '0',
                              'orggubun': '1',
                              'prapp': 100,
                              'prgubun': '1',
                              'shcode': '005930',
                              'todt': '20230726'}},
    'header': {'authorization': None,
                'content-type': 'application/json; charset=UTF-8',
                'mac_address': '',
                'tr_cd': 't1716',
                'tr_cont': 'N',
                'tr_cont_key': ''},
    'out_block_tag': 'OutBlock',
    'shcode': '005930',
    'tr_name': 't1716',
    'url': 'https://openapi.ebestsec.co.kr:8080/stock/frgr-itt'}
    ```
    </details>
  - `request_t1716.py`
    <details>
      <summary>Code (New)</summary>

    ```py
    """
    eBest Open API / 외인기관종목별동향 (t1716) 실행
    2023.07.25

    이 코드는 eBest Open API에서 t1716 TR을 호출하여 주어진 종목 코드와 조회 기간에 따른 외인과 기관의 순매매 정보를 조회하고,
    이를 하나의 DataFrame으로 병합한 뒤 하나의 CSV 파일로 저장하는 작업을 수행합니다.

    Parameters  :
        TR_NAME (str)       : TR을 호출하는 함수의 이름으로 사용될 문자열입니다.
        shcodes (list)      : 조회할 종목 코드들이 담긴 리스트입니다.
        todts (list)        : 조회를 종료할 날짜들이 담긴 리스트입니다.
        YEARS (int)         : 조회 기간의 연도 수를 나타내는 정수입니다.
        PERIOD (int)        : 조회 기간을 나타내는 정수로, 최대 366일까지 조회가 가능합니다.
        unique_keys (list)  : 중복된 열을 제거하기 위해 사용될 DataFrame의 열 이름들이 담긴 리스트입니다.

    Returns     :
        None
    """
    ```
    ```py
    import time
    import t1716_2 as t1716
    import request_tr_2 as request_tr
    import pandas as pd
    ```
    ```py
    if __name__ == "__main__":

        TR_NAME = "t1716"
        shcodes = ["122630", "252670", "233740", "251340"]
        todts   = []
        YEARS   = 10
        for i in range(0, YEARS):
            todts.append(str(2022 - i) + "1231")
        PERIOD  = 366
            # It seems to have a maximum value of 366 (why not 365? considering leap years)
        unique_keys = ["shcode", "date"]                                            # to remove duplicated columns

        # print(todts)                                                              # Ok

        merged_df = pd.DataFrame()
        for shcode in shcodes:
            merged_df_2 = pd.DataFrame()
            for todt in todts:
                results = request_tr.request_tr(t1716.t1716(shcode=shcode, todt=todt, period=PERIOD))
                merged_df_2 = pd.concat([merged_df_2, results[0]])
                print(f"{TR_NAME} / {shcode} 종목 / {todt} 데이터를 수신하였습니다.")
                time.sleep(1)
            merged_df_2["shcode"] = shcode
            merged_df = pd.concat([merged_df, merged_df_2])
        merged_df.drop_duplicates(subset=unique_keys, keep='first', inplace=True)
        request_tr.save_csv(data_frame=merged_df, tr_name=TR_NAME)
    ```

    </details>
    <details open="">
      <summary>Results</summary>

    ```txt
    t1716 / 122630 종목 / 20221231 데이터를 수신하였습니다.
    t1716 / 122630 종목 / 20211231 데이터를 수신하였습니다.
    ……
    t1716 / 251340 종목 / 20131231 데이터를 수신하였습니다.
    파일 저장을 완료하였습니다. : Data/T1716_20230726_092217.csv
    ```
    ```csv
    date,close,sign,change,diff,volume,krx_0008,krx_0018,krx_0009,pgmvol,fsc_listing,fsc_sjrate,fsc_0009,gm_volume,gm_value,shcode
    20221229,12805,5,-480,-3.61,18306241,3703971,-3248809,-571027,0,56568,0.04,-171027,0,0,122630
    20221228,13285,5,-275,-2.03,16378432,2235121,-1599598,-688470,0,227595,0.16,-1088470,0,0,122630
    20221227,13560,2,185,1.38,17776955,-772417,805734,155566,0,1316065,0.91,155566,0,0,122630
    20221226,13375,3,0,0.00,10881566,-288532,-14282,294974,0,1160499,0.85,294974,0,0,122630
    ……
    20160810,9890,5,-110,-1.10,347391,41873,-41873,0,0,0,0.00,0,0,0,251340
    ```
    </details>


## [외인기관종목별동향 (`t1716`, 2023.07.21)](#list)

- [eBest OPEN API](https://openapi.ls-sec.co.kr) > [API 가이드 > 주식 > [주식] 외인/기관](https://openapi.ls-sec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=90378c39-f93e-4f95-9670-f76e5c924cc6) > 외인기관종목별동향 (t1716)
- Only save parameters, that will be called by `request_tr()` in [Request TR (2023.07.21)](#request-tr-20230721)
- Code and Results
  <details>
    <summary>Code : t1716.py</summary>

  ```py
  """
  eBest Open API / 외인기관종목별동향 (t1716)
  2023.07.21

  이 코드는 eBest Open API에서 t1716 TR을 호출하기 위한 예시 코드입니다.
  t1716 TR은 주식 시장의 기관 및 외인 순매매 정보를 조회하는 TR입니다.
  """
  ```
  ```py
  from datetime import datetime, timedelta
  import pytz
  ```
  ```python
  def t1716(shcode = "005930", todt = "", period = 365) :
      """
      eBest Open API에서 t1716 TR을 호출하기 위한 URL, 헤더 및 바디 정보를 반환하는 함수입니다.

      Parameters:
          shcode (str, optional)  : 종목코드를 지정하는 매개변수입니다. 기본값은 "005930"(삼성전자)로 설정됩니다.
          todt (str, optional)    : 조회를 종료할 날짜를 지정하는 매개변수입니다. 기본값은 오늘 날짜로 설정됩니다.
          period (int, optional)  : 조회 기간을 지정하는 매개변수입니다. 기본값은 365일(1년)입니다.

      Returns:
          tuple                   : url, 헤더, 바디 정보, 함수 이름, 반환 데이터 태그, 종목코드를 포함하는 튜플을 반환합니다.
      """

      _url_base   = "https://openapi.ebestsec.co.kr:8080"
      _path       = "stock/frgr-itt"
      _url        = f"{_url_base}/{_path}"

      _header     = {
          "content-type"  : "application/json; charset=UTF-8",
          "authorization" : None,                             # fill in RunTR()
          "tr_cd"         : "t1716",
          "tr_cont"       : "N",
          "tr_cont_key"   : "",
          "mac_address"   : ""
      }

      # 시작일자와 종료일자를 YYYYMMDD 형식으로 생성하기
      _seoul_timezone = pytz.timezone('Asia/Seoul')
      _seoul_dt       = datetime.now(_seoul_timezone)
      _todt           = _seoul_dt.strftime('%Y%m%d') if todt == "" else todt
      _todt_datetime = datetime.strptime(_todt, '%Y%m%d').astimezone(_seoul_timezone)
      _fromdt = (_todt_datetime - timedelta(period)).strftime("%Y%m%d")

      _body           = {
          "t1716InBlock" : {
              "shcode"    : shcode,                           # 종목코드
              "gubun"     : "1",                              # 0:일간순매수 1:기간내누적순매수
              "fromdt"    : _fromdt,                          # 시작일자 : YYYYMMDD (default : 종료일자로부터 1년 전)
              "todt"      : _todt,                            # 종료일자 : YYYYMMDD
              "prapp"     : 0,                                # 프로그램매매 감산 적용율 - %단위
              "prgubun"   : "0",                              # PR적용구분(0:적용안함1:적용)
              "orggubun"  : "1",                              # 기관적용(0:미적용 1:적용)
              "frggubun"  : "1"                               # 외인적용(0:미적용 1:적용)
          }
      }

      _out_block_tag = "OutBlock"

      return _url, _header, _body, t1716.__name__, _out_block_tag, shcode
  ```
  ```py
  if __name__ == "__main__":

      import pprint

      url, header, body, tr_name, out_block_tag, shcode_ = t1716()

      print("URL              :")
      pprint.pprint(url)
      print("\nheader           :")
      pprint.pprint(header)
      print("\nbody             :")
      pprint.pprint(body)
      print("\ntr name          :")
      pprint.pprint(tr_name)
      print("\nOutBlockTag      :")
      pprint.pprint(out_block_tag)
      print("\nshcode           :")
      pprint.pprint(shcode_)
  ```
  </details>
  <details open="">
    <summary>Results</summary>

  ```txt
  URL              :
  'https://openapi.ebestsec.co.kr:8080/stock/frgr-itt'

  header           :
  {'authorization': None,
  'content-type': 'application/json; charset=UTF-8',
  'mac_address': '',
  'tr_cd': 't1716',
  'tr_cont': 'N',
  'tr_cont_key': ''}

  body             :
  {'t1716InBlock': {'frggubun': '1',
                    'fromdt': '20220722',
                    'gubun': '1',
                    'orggubun': '1',
                    'prapp': 0,
                    'prgubun': '0',
                    'shcode': '005930',
                    'todt': '20230722'}}

  tr name          :
  't1716'

  OutBlockTag      :
  'OutBlock'

  shcode           :
  '005930'
  ```
  </details>


## [재무순위종합 (`t3341`, 2023.07.14)](#list)

- [eBest OPEN API](https://openapi.ls-sec.co.kr) > [API 가이드 > 주식 > [주식] 투자정보](https://openapi.ls-sec.co.kr/apiservice#G_73142d9f-1983-48d2-8543-89b75535d34c#A_580d2770-a7a9-49e3-9ec1-49ed8bc734a2) > 재무순위종합
- Code and Results
  <details>
    <summary>Code : T3341.py</summary>

  ```py
  # import pprint
  import datetime
  import json
  import pandas as pd
  import requests

  import OAuth
  ```
  ```py
  URL_BASE    = "https://openapi.ebestsec.co.kr:8080"
  PATH        = "stock/investinfo"
  URL         = f"{URL_BASE}/{PATH}"

  header      = {
      "content-type"  : "application/json; charset=UTF-8",
      "authorization" : f"Bearer {OAuth.ACCESS_TOKEN}",
      "tr_cd"         : "t3341",
      "tr_cont"       : "N",
      "tr_cont_key"   : "",
      "mac_address"   : ""
  }

  body       = {
      "t3341InBlock"  : {
          "gubun"     : "0",                                  # 0 : 전체
          "gubun1"    : "3",                                  # 3 : 세전계속이익증가율
          "gubun2"    : "1",                                  # 1 : 고정
          "idx"       : 0
      }
  }

  res = requests.post(URL, headers=header, data=json.dumps(body), timeout=1)
  # pprint.pprint(res.json())

  json_data = res.json()
  df = pd.json_normalize(json_data["t3341OutBlock1"])
  time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
  df.to_csv(f'Data/T3341_{time_stamp}.csv')
  ```
  ```py
  if __name__ == "__main__":
      print(df)
  ```
  </details>
  <details open = "">
    <summary>Results</summary>

  ```txt
      rank     hname  salesgrowth  operatingincomegrowt  ordinaryincomegrowth  liabilitytoequity  enterpriseratio      eps       bps    roe  shcode    per    pbr    peg
  0      1      동양파일         4.39                -35.60               6691.58               5.29          1129.14   245.33   6145.71   4.07  228340  12.66   0.51  38.84
  1      2   감성코퍼레이션       139.90               1300.52               5433.07              64.87            13.62   168.35    568.07  37.70  036620  26.46   7.84   1.31
  2      3  선진뷰티사이언스        31.80                 47.70               3772.86             106.80           955.24  1593.39   5276.18  35.91  086710   5.72   1.73   0.52
  3      4      일신석재        84.19                371.91               3032.30             110.34            43.52    30.31    717.60   4.37  007110  42.10   1.78   0.00
  4      5    모베이스전자        17.80                169.62               2912.85             217.62           376.10    92.64   2380.49   4.08  012860  29.90   1.16   0.00
  ..   ...       ...          ...                   ...                   ...                ...              ...      ...       ...    ...     ...    ...    ...    ...
  95    96     큐에스아이       -22.75                -51.57                179.33               6.22          1685.83   711.54   8929.14   8.34  066310  15.26   1.22   5.74
  96    97   신세계 I&C        11.80                  4.35                178.53              31.66          4596.92  5253.56  23484.59  28.68  035510   2.53   0.57   1.05
  97    98        윈텍        31.57                211.76                176.70              26.46          1128.32    95.72   1228.32   8.08  320000  32.12   2.50  64.16
  98    99    한글과컴퓨터         9.40                 -3.23                176.47              21.47          2506.32  2147.60  13715.19  18.09  030520   5.83   0.91   1.60
  99   100    파크시스템스        41.89                 80.00                173.67              32.17          3336.79  3233.76  17183.96  21.40  140860  58.79  11.06   2.57

  [100 rows x 14 columns]
  ```
  </details>


## [Request TR 4 (2024.08.26)](#list)

- Advanced from [Request TR 3 (2024.08.22)](#request-tr-3-20240822)
  - Set `_header` directly in `request_tr()`, no longer receiving it from `t****()`
- Code and Results
  <details>
    <summary>request_tr_4.py (mainly changed parts)</summary>

  ```py
  def request_tr(_results, _real=False, _timeout=1):

      ……

      # 요청에 필요한 정보를 설정
      _url = _results["url"]
      _tr_name = _results["tr_name"]

      # 헤더가 딕셔너리에 포함되어 있지 않으면 기본 헤더를 설정
      if not "_header" in _results:
          _header = {
              "content-type": "application/json; charset=utf-8",  # 콘텐츠 타입
              "authorization": None,  # OAuth 토큰 (추후 추가)
              "tr_cd": _tr_name,  # TR 코드
              "tr_cont": "N",  # 연속 조회 여부 (기본값: N)
              "tr_cont_key": "",  # 연속 조회 키 (필요시 사용)
              "mac_address": ""  # MAC 주소 (필요시 사용)
          }
      else:
          _header = _results["header"]

      # OAuth 토큰을 설정
      _header["authorization"] = f"Bearer {oauth.oauth(_real=_real)}"

      # 바디, 출력 블록 태그, 종목 코드 설정
      _body = _results["body"]
      _out_block_tags = _results["out_block_tags"]
      _shcode = _results["shcode"]

      ……
  ```
  ```py
  if __name__ == "__main__":
      ……
      import tr_stock_accno

      # CSPAQ12300 TR 요청 및 결과 확인
      tr_outputs = request_tr(tr_stock_accno.CSPAQ12300())
      ……

      ……
  ```
  </details>
  <details open="">
    <summary>Results</summary>

  ```txt
  RecCnt,AcntNo,Pwd,BalCreTp,CmsnAppTpCode,D2balBaseQryTp,UprcTpCode
  1,55503048401,0000,,,,
  ```
  ```txt
  RecCnt,BrnNm,AcntNm,MnyOrdAbleAmt,MnyoutAbleAmt,SeOrdAbleAmt,KdqOrdAbleAmt,HtsOrdAbleAmt,MgnRat100pctOrdAbleAmt,BalEvalAmt,PchsAmt,RcvblAmt,PnlRat,InvstOrgAmt,InvstPlAmt,CrdtPldgOrdAmt,Dps,D1Dps,D2Dps,OrdDt,MnyMgn,SubstMgn,SubstAmt,PrdayBuyExecAmt,PrdaySellExecAmt,CrdayBuyExecAmt,CrdaySellExecAmt,EvalPnlSum,DpsastTotamt,Evrprc,RuseAmt,EtclndAmt,PrcAdjstAmt,D1CmsnAmt,D2CmsnAmt,D1EvrTax,D2EvrTax,D1SettPrergAmt,D2SettPrergAmt,PrdayKseMnyMgn,PrdayKseSubstMgn,PrdayKseCrdtMnyMgn,PrdayKseCrdtSubstMgn,CrdayKseMnyMgn,CrdayKseSubstMgn,CrdayKseCrdtMnyMgn,CrdayKseCrdtSubstMgn,PrdayKdqMnyMgn,PrdayKdqSubstMgn,PrdayKdqCrdtMnyMgn,PrdayKdqCrdtSubstMgn,CrdayKdqMnyMgn,CrdayKdqSubstMgn,CrdayKdqCrdtMnyMgn,CrdayKdqCrdtSubstMgn,PrdayFrbrdMnyMgn,PrdayFrbrdSubstMgn,CrdayFrbrdMnyMgn,CrdayFrbrdSubstMgn,PrdayCrbmkMnyMgn,PrdayCrbmkSubstMgn,CrdayCrbmkMnyMgn,CrdayCrbmkSubstMgn,DpspdgQty,BuyAdjstAmtD2,SellAdjstAmtD2,RepayRqrdAmtD1,RepayRqrdAmtD2,LoanAmt
  1,,김프로,100000000,100000000,0,0,0,100000000,0,0,0,0.000000,0,0,0,100000000,100000000,100000000,,0,0,0,0,0,0,0,0,100000000,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
  ```
  ```txt
  (No balance in the account)
  ```
  </details>


## [Request TR 3 (2024.08.22)](#list)

- Advanced from [Request TR 2 (2023.07.25)](#request-tr-2-20230725)
  - Passed the real/mock server flag (`_real`) to `oauth.oauth()`
  - Added support for multiple `t****OutBlock*`
  - Added an optional `_timeout` parameter (int) for `requests.post()`
- Code and Results
  <details>
    <summary>request_tr_3.py (mainly changed parts)</summary>

  ```python
  ……
  import oauth_3 as oauth
  ```
  ```py
  def request_tr(_results, _real=False, _timeout=1):

      ……

      # OAuth 토큰을 헤더에 추가
      _header["authorization"] = f"Bearer {oauth.oauth(_real=_real)}"

      # TR 요청을 POST 방식으로 전송
      _res = requests.post(_url, headers=_header, data=json.dumps(_body), timeout=_timeout)
      ……

      # 결과 블록 태그가 단일 문자열인 경우 리스트로 변환
      if isinstance(_out_block_tag, str):
          _out_block_tag = [_out_block_tag]

      _data_frames = []

      # 각 블록 태그에 대해 데이터프레임 생성
      for _out_block in _out_block_tag:
          _data_frame = pd.json_normalize(_json_data[f"{_tr_name}{_out_block}"])
          _data_frames.append(_data_frame)

      return _data_frames, _tr_name, _shcode
  ```
  ```py
  def save_csv(_data_frames, _tr_name, _shcode=""):

      ……

      # 각 데이터프레임을 CSV 파일로 저장
      for i, _data_frame in enumerate(_data_frames):
          if _shcode:
              _path = f'Data/{_tr_name.upper()}_{_shcode}_{_time_stamp}_{i}.csv'
          else:
              _path = f'Data/{_tr_name.upper()}_{_time_stamp}_{i}.csv'

          ……
  ```
  </details>
  <details open="">
    <summary>Results</summary>

  ```txt
  date,close,sign,change,diff,volume,krx_0008,krx_0018,krx_0009,pgmvol,fsc_listing,fsc_sjrate,fsc_0009,gm_volume,gm_value
  20240822,78300,3,0,0.00,8138752,152259,-937901,-175582,485762,3358830711,56.26,373805,37485,2927
  20240821,78300,5,-600,-0.76,7799774,-200013,24803,-70499,152840,3357971144,56.25,-88399,11227,878
  20240820,78900,2,600,0.77,10213542,-783354,-1060351,6133,918352,3357906703,56.25,10331,5113,405
  20240819,78300,5,-1900,-2.37,14124565,1735237,134441,-995169,-473472,3356978020,56.23,-1112469,6504,509
  20240816,80200,2,3000,3.89,20895904,-7324889,-993805,4628772,1911883,3358563961,56.26,4626870,63672,5048
  20240814,77200,2,1100,1.45,13176220,-2154441,-928285,1357217,697682,3352025208,56.15,1416317,73153,5651
  20240813,76100,2,600,0.79,10696333,-1579019,-568949,1491290,366354,3349911209,56.11,1716690,13720,1042
  20240812,75500,2,800,1.07,9629370,-539380,-431124,-69985,543883,3347828165,56.08,-216025,14656,1108
  ```
  ```txt
  파일 저장을 완료하였습니다. : Data/T1716_005930_20240822_220936_0.csv
  ```
  </details>


## [Request TR 2 (2023.07.25)](#list)

- Advanced from [Request TR (2023.07.21)](#request-tr-20230721)
  - `request_tr()`: Change the parameters' type : *tuple* → *dictionary*
  - `save_csv()`  : Exclude *pandas.DataFrame*'s index values when saving
- Code and Results
  <details>
    <summary>request_tr_2.py (mainly changed parts)</summary>

  ```python
  def request_tr(results):
      """
      ……

      Parameters :
          results (dict)      : t****() 함수의 리턴값인 딕셔너리입니다.

      ……
      """

      _url            = results["url"]
      _header         = results["header"]
      _body           = results["body"]
      _tr_name        = results["tr_name"]
      _out_block_tag  = results["out_block_tag"]
      _shcode         = results["shcode"]

      ……
  ```
  ```py
  def save_csv(data_frame, tr_name, shcode=""):
      ……

      ……
      data_frame.to_csv(_path, index=False)
      ……
  ```
  ```py
  if __name__ == "__main__":

      import pprint
      import t1716_2 as t1716

      tr_output = request_tr(t1716.t1716(shcode="005930", period=365))             # 삼성전자, 1년치 일일 데이터
      pprint.pprint(tr_output)
      save_csv(*tr_output)
  ```
  </details>
  <details open="">
    <summary>Results</summary>

  ```txt
  (         date  close sign  change   diff    volume  krx_0008  krx_0018  krx_0009   pgmvol  fsc_listing fsc_sjrate  fsc_0009  gm_volume  gm_value
  0    20230726  70000    3       0   0.00         0         0         0         0        0   3165243552      53.02         0          0         0
  1    20230725  70000    5    -400  -0.57  13500986     49193    -23280   1844693  -940037   3165243552      53.02   1895393     249469     17471
  2    20230724  70400    2     100   0.14  13360061  -2249447  -2985631    576591  2421837   3164288196      53.01    582022     187872     13236
  3    20230721  70300    5    -700  -0.99  16528926   3655097   1135251  -3232093  -823435   3161284337      52.95  -2740185     690377     48199
  4    20230720  71000    5    -700  -0.98   9732730    980710  -1071133   -296382   190441   3164847957      53.01   1200568     212026     15104
  ..        ...    ...  ...     ...    ...       ...       ...       ...       ...      ...          ...        ...       ...        ...       ...
  244  20220801  61300    5    -100  -0.16  13154816    530487  -1367169    240197   313794   2974186694      49.82    -66871     186169     11311
  245  20220729  61400    5    -500  -0.81  15093120   1235234   1473091    616021 -1623959   2973939771      49.82     77992     690338     42576
  246  20220728  61900    2     100   0.16  10745302   -208569  -1255580     81602   695515   2975485738      49.84   1398272     155172      9639
  247  20220727  61800    2     100   0.16   7320997     47874     15345    620603  -330594   2973391951      49.81    930383      87069      5349
  248  20220726  61700    2     600   0.98   6597211   -549225   -534799    811790   137251   2972792162      49.80    555180      47626      2933

  [249 rows x 15 columns],
  't1716',
  '005930')
  ```
  ```txt
  파일 저장을 완료하였습니다. : Data/T1716_005930_20230726_080802.csv
  ```
  </details>


## [Request TR (2023.07.21)](#list)

- Common functions
  - `request_tr()` : request *\<t\*\*\*\*> tr*
  - `save_csv()`   : save data from pandas dataframe to a `.csv` file
- Code and Results
  <details>
    <summary>Code : request_tr.py</summary>

  ```py
  """
  eBest Open API / request_tr
  2023.07.21

  이 코드는 eBest Open API에서 TR을 호출하여 데이터를 조회하고 CSV 파일로 저장하는 코드입니다.
  """
  ```
  ```py
  import datetime
  import json
  import pytz
  import pandas as pd
  import requests

  import oauth2 as oauth
  ```
  ```python
  def request_tr(url, header, body, tr_name, out_block_tag, shcode):
      """
      eBest Open API에서 TR을 호출하여 데이터를 조회하는 함수입니다.

      Parameters:
          url (str)           : API 호출을 위한 URL입니다.
          header (dict)       : API 호출에 필요한 헤더 정보가 담긴 딕셔너리입니다.
          body (dict)         : API 호출에 필요한 바디 정보가 담긴 딕셔너리입니다.
          tr_name (str)       : 함수 이름입니다.
          out_block_tag (str) : 반환 데이터의 태그입니다.
          shcode (str)        : 종목코드를 지정하는 매개변수입니다.

      Returns:
          pandas.DataFrame    : 조회된 데이터가 담긴 DataFrame 객체를 반환합니다.
          str                 : 함수 이름을 반환합니다.
          str                 : 종목코드를 반환합니다.
      """

      header["authorization"] = f"Bearer {oauth.oauth()}"
      _res = requests.post(url, headers=header, data=json.dumps(body), timeout=1)
      _json_data = _res.json()
      # print(json_data)                                                          # Ok
      # print(f"{TR_NAME}{out_block_tag}")                                        # Ok
      _data_frame = pd.json_normalize(_json_data[f"{tr_name}{out_block_tag}"])

      return _data_frame, tr_name, shcode
  ```
  ```py
  def save_csv(data_frame, tr_name, shcode=""):
      """
      조회된 데이터를 CSV 파일로 저장하는 함수입니다.

      Parameters:
          data_frame (pandas.DataFrame) : 조회된 데이터가 담긴 DataFrame 객체입니다.
          tr_name (str)                 : 저장할 파일의 이름을 지정하는 매개변수입니다.
          shcode (str, optional)        : 종목코드를 지정하는 매개변수입니다. 기본값은 ""(빈 문자열)입니다.

      Returns:
          None
      """

      _seoul_timezone = pytz.timezone('Asia/Seoul')
      _time_stamp = datetime.datetime.now(_seoul_timezone).strftime("%Y%m%d_%H%M%S")
      if len(shcode) > 0:
          _path = f'Data/{tr_name.upper()}_{shcode}_{_time_stamp}.csv'
      else:
          _path = f'Data/{tr_name.upper()}_{_time_stamp}.csv'
      data_frame.to_csv(_path)
      print("파일 저장을 완료하였습니다. :", _path)
  ```
  ```py
  if __name__ == "__main__":

      import t1716

      results = request_tr(*t1716.t1716(shcode="005930", period=365))             # 삼성전자, 1년치 일일 데이터
      print(results[0])
      save_csv(*results)
  ```
  </details>
  <details open="">
    <summary>Results</summary>

  ```txt
          date  close sign  change   diff    volume   krx_0008  krx_0018   krx_0009    pgmvol  fsc_listing fsc_sjrate   fsc_0009  gm_volume  gm_value
  0    20230721  70300    5    -700  -0.99  16528926 -135656797 -47587921  187226850  66422136   3161057429      52.95  189453121  111023539   6948297
  1    20230720  71000    5    -700  -0.98   9732730 -139311894 -47899737  191282378  67245571   3164847957      53.01  193243649  110811513   6933193
  2    20230719  71700    5    -300  -0.42  10851948 -140292604 -47019045  191388319  67055130   3163456948      52.99  191852640  110486152   6909844
  3    20230718  72000    5   -1300  -1.77  11282654 -141004884 -45818326  190916335  65954614   3163380264      52.99  191775956  110112691   6882647
  4    20230717  73300    5    -100  -0.14  10060049 -142362894 -45165996  191707382  66590493   3164885311      53.02  193281003  109698081   6852294
  ..        ...    ...  ...     ...    ...       ...        ...       ...        ...       ...          ...        ...        ...        ...       ...
  243  20220728  61900    2     100   0.16  10745302     238401  -2887326    2630540   -829418   2975485738      49.84    3881430     523771     32276
  244  20220727  61800    2     100   0.16   7320997     446970  -2327261    1853423  -1524933   2973391951      49.81    1787643     436702     26927
  245  20220726  61700    2     600   0.98   6597211     399096  -2012012    1563414  -1194339   2972792162      49.80    1187854     389076     23993
  246  20220725  61100    5    -200  -0.33   9193681     948321  -1614464     614373  -1331590   2972099731      49.79     495423     337887     20852
  247  20220722  61300    5    -500  -0.81  10261310    1022114  -1862181     739607   -342577   2972375415      49.79     771107          0         0

  [248 rows x 15 columns]
  ```
  ```txt
  파일 저장을 완료하였습니다. : Data/T1716_005930_20230722_173359.csv
  ```
  </details>


## [Oauth 3 (2024.08.22)](#list)

- Advanced from [Oauth 2 (2023.07.21)](#oauth-2-20230721)
  - `oauth_3.py`
    - Added a `_real` parameter to distinguish between real and mock servers
    - Modified the `URL` string (due to the company name change)
  - `key.py` : Added `KEY` and `SECRET` for the real server and `USER_ID` for the *t1859* TR
- Code and Results
  <details>
    <summary>Code : key.py (not uploaded)</summary>

  ```py
  KEY = "{your app key}"
  SECRET = "{your secret key}"
  MOCK_KEY = "{your app key}"
  MOCK_SECRET = "{your secret key}"

  USER_ID = "{your ID}"
  ```
  </details>
  <details>
    <summary>Code : oauth_3.py (mainly changed parts)</summary>

  ```py
  # OAuth 토큰을 요청할 기본 URL
  URL = "https://openapi.ls-sec.co.kr:8080/oauth2/token"
  ```
  ```python
  def oauth(_test=False, _real=False):

      ……

      # 실서버 또는 모의서버에 따라 앱 키와 시크릿 키를 설정
      if _real is True:
          _app_key = key.KEY
          _app_secret = key.SECRET
      else:
          _app_key = key.MOCK_KEY
          _app_secret = key.MOCK_SECRET

      ……
  ```
  ```py
  if __name__ == "__main__":
      # 테스트 모드로 OAuth 함수 호출하여 액세스 토큰과 요청/응답 데이터를 출력
      url, res, _ = oauth(_test=True)
      ……
  ```
  </details>
  <details open = "">
    <summary>Results</summary>

  ```txt
  URL      : https://openapi.ls-sec.co.kr:8080/oauth2/token 

  OAuth 응답 내용:
  {'access_token': '********',
  'expires_in': 58023,
  'scope': 'oob',
  'token_type': 'Bearer'}
  ```
  </details>


## [Oauth 2 (2023.07.21)](#list)

- Advanced from [Oauth (2023.07.11)](#oauth-20230711)
  - A function structure has been introduced into the same actual execution content.
- Code and Results
  <details>
    <summary>Code : key.py (not uploaded)</summary>

  - Add comments
  ```python
  """
  eBest Open API / key
  2023.07.11

  이 파일은 eBest Open API를 사용하기 위해 필요한 애플리케이션 키와 비밀 키를 저장하는 파일입니다.
  애플리케이션 키는 API 호출에 필요한 인증을 위해 사용되며, 반드시 비밀로 유지되어야 합니다.
  따라서 이 파일은 외부에 노출되지 않도록 주의해야 합니다.
  """

  MOCK_KEY    = "{your app key}"
  MOCK_SECRET = "{your secret key}"
  ```
  </details>
  <details>
    <summary>Code : oauth2.py</summary>

  ```py
  """
  eBest Open API / 접근토큰 발급 (token)
  2023.07.21

  이 코드는 eBest Open API 서버에 OAuth 토큰을 요청하는 함수를 포함한 코드입니다.
  OAuth 토큰은 API를 호출할 때 인증 정보로 사용되며, API 호출을 위해 반드시 필요합니다.

  사용 전 준비사항:
  1. eBest Open API 개발자 센터에서 앱 키와 시크릿 키를 발급받아야 합니다.
  2. key.py 파일에 발급받은 앱 키와 시크릿 키를 저장해야 합니다. (예: MOCK_KEY, MOCK_SECRET)

  개선사항:
  1. OAuth.py (2023.07.11)의 코드를 oauth()라는 함수로 재작성하였습니다.
  2. test 변수의 값(True/False)에 따라 return값이 달라집니다.
  """
  ```
  ```py
  import pprint
  import requests

  import key
  ```
  ```python
  def oauth(test = False):
      """
      eBest Open API 서버에 OAuth 토큰을 요청하는 함수입니다.

      Parameters:
          test (bool) : 테스트 모드 여부를 설정하는 매개변수입니다. 기본값은 False입니다.

      Returns:
          str         : 성공적으로 OAuth 토큰을 받아온 경우 해당 토큰을 반환합니다.

      Raises:
          requests.exceptions.RequestException : OAuth 요청 중 예외가 발생한 경우 예외를 발생시킵니다.
      """

      # 개발자가 발급받은 앱 키와 시크릿 키를 사용합니다.
      _app_key = key.MOCK_KEY
      _app_secret = key.MOCK_SECRET

      # OAuth 토큰을 요청할 API 경로를 설정합니다.
      _path = "oauth2/token"
      _url_base = "https://openapi.ebestsec.co.kr:8080"
      _url = f"{_url_base}/{_path}"

      # OAuth 요청에 필요한 헤더 정보를 설정합니다.
      _header = {
          "content-type": "application/x-www-form-urlencoded"
      }

      # OAuth 요청에 필요한 파라미터 정보를 설정합니다.
      _param = {
          "grant_type": "client_credentials",
          "appkey": _app_key,
          "appsecretkey": _app_secret,
          "scope": "oob"
      }

      # OAuth 요청을 실행하고 응답을 받아옵니다.
      try:
          _res = requests.post(_url, headers=_header, params=_param, timeout=1)
          _access_token = _res.json()["access_token"]
      except requests.exceptions.RequestException as _e:
          # OAuth 요청 중 예외가 발생한 경우 예외를 발생시킵니다.
          raise _e

      if test:
          return _url, _res, _access_token
      else:
          return _access_token
  ```
  ```py
  if __name__ == "__main__":
      # OAuth 함수를 호출하여 액세스 토큰을 받아옵니다.

      url, res, _ = oauth(test = True)
      print("URL      :", url, "\n")                          # OAuth 토큰 요청을 보낸 URL 출력
      print("OAuth    :")
      pprint.pprint(res.json())                               # OAuth 응답 내용 출력
  ```
  </details>
  <details open = "">
    <summary>Results</summary>

  ```txt
  URL      : https://openapi.ebestsec.co.kr:8080/oauth2/token

  OAuth    :
  {'access_token': '******',
  'expires_in': 50352,
  'scope': 'oob',
  'token_type': 'Bearer'}
  ```
  </details>


## [Oauth (2023.07.11)](#list)

- Oauth; Open Authorization
- References
  - [eBest OPEN API](https://openapi.ls-sec.co.kr) > [API 가이드 > OAuth 인증 > 접근토큰 발급](https://openapi.ls-sec.co.kr/apiservice#G_ffd2def7-a118-40f7-a0ab-cd4c6a538a90#A_33bd887a-6652-4209-88cd-5324bc7c5e36)
  - [eBest OPEN API](https://openapi.ls-sec.co.kr) > [OPEN API > OPEN API 이용안내](https://openapi.ls-sec.co.kr/howto-use) > 03. 접근토큰 발급
- Code and Results
  <details>
    <summary>Code : Key.py (not uploaded)</summary>

  ```python
  MOCK_KEY    = "{your app key}"
  MOCK_SECRET = "{your secret key}"
  ```
  </details>
  <details>
    <summary>Code : Oauth.py</summary>

  ```python
  import pprint
  import requests
  import Key
  ```
  ```python
  APP_KEY     = Key.MOCK_KEY
  APP_SECRET  = Key.MOCK_SECRET

  header      = {
      "content-type"  : "application/x-www-form-urlencoded"
  }
  param       = {
      "grant_type"    : "client_credentials",
      "appkey"        : APP_KEY,
      "appsecretkey"  : APP_SECRET,
      "scope"         : "oob"
  }

  PATH        = "oauth2/token"
  URL_BASE    = "https://openapi.ebestsec.co.kr:8080"
  URL         = f"{URL_BASE}/{PATH}"

  res = requests.post(URL, headers=header, params=param, timeout=1)
  ACCESS_TOKEN = res.json()["access_token"]
  ```
  ```python
  if __name__ == "__main__":
      print("URL          : ", URL, "\n")                     # Ok
      print("OAuth        : ")
      pprint.pprint(res.json())                               # Ok
  ```
  </details>
  <details open = "">
    <summary>Results</summary>

  ```txt
  URL          :  https://openapi.ebestsec.co.kr:8080/oauth2/token

  OAuth        :
  {'access_token': '******',
   'expires_in': 105831,
   'scope': 'oob',
   'token_type': 'Bearer'}
  ```
  </details>
