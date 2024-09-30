"""
LS Open API / [주식] 주문 TR 요청 모듈
2024.09.30

설명:
이 모듈은 LS Open API를 통해 주식 주문, 정정 주문, 취소 주문을 비동기 방식으로 처리하는 기능을 제공합니다.
각 API 요청은 재사용 가능한 `send_api_request()` 함수를 통해 발송됩니다.

구성:
1. 비동기 주문 발송 함수: send_order_async
2. 비동기 정정 주문 함수: correct_order_async
3. 비동기 취소 주문 함수: cancel_order_async
4. API 요청 발송 함수: send_api_request
5. 메인 실행 함수: main

사용 예:
비동기 함수는 메인 실행 함수(main)에서 순차적으로 호출되어 주문, 정정, 취소 요청을 진행합니다.

히스토리:
1   2024.09.06 최초 작성
2   2024.09.30 비동기식으로 재구현
"""


import asyncio
import pprint
import aiohttp
import oauth_3 as oauth

# API 요청을 위한 기본 URL 설정
URL      = "https://openapi.ls-sec.co.kr:9443/stock/websocket"
MOCK_URL = "https://openapi.ls-sec.co.kr:29443/stock/websocket"
ORDER_URL = "https://openapi.ls-sec.co.kr:8080/stock/order"


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
