"""
LS Open API / [주식] 실시간 시세 TR 요청 모듈
2024.09.06

히스토리:
1   2024.09.06 최초 작성
"""


import sys
import oauth_3 as oauth
import request_tr_4 as request_tr


# API 요청을 위한 기본 URL 설정
URL = "https://openapi.ls-sec.co.kr:9443/stock/websocket"
MOCK_URL = "https://openapi.ls-sec.co.kr:29443/stock/websocket"


def SC0(_body="", _real=False):
    """

    """

    _tr_name = sys._getframe().f_code.co_name

    # TR 요청을 위한 URL 설정
    if not _real:
        _url = URL
    else:
        _url = MOCK_URL

    _header = {
        "token": f"Bearer {oauth.oauth(_real=_real)}",
        "tr_type": "1",
    }

    if _body == "":
        _body = {
            "tr_cd": _tr_name,
            "tr_key": "",
        }

    # TR 요청에 필요한 정보를 딕셔너리로 반환
    return {
        'url': _url,              # 요청 URL
        'header': _header,        # 요청 header
        'body': _body,            # 요청 바디
        'tr_name': _tr_name,      # TR 코드 이름
        'out_block_tags': ["header", "body"],  # 출력 블록 태그
        'shcode': None,           # 종목 코드 (필요시 사용)
    }


def SC1(_body="", _real=False):
    """

    """

    _tr_name = sys._getframe().f_code.co_name

    # TR 요청을 위한 URL 설정
    if not _real:
        _url = URL
    else:
        _url = MOCK_URL

    _header = {
        "token": f"Bearer {oauth.oauth(_real=_real)}",
        "tr_type": "1",
    }

    if _body == "":
        _body = {
            "tr_cd": _tr_name,
            "tr_key": "",
        }

    # TR 요청에 필요한 정보를 딕셔너리로 반환
    return {
        'url': _url,              # 요청 URL
        'header': _header,        # 요청 header
        'body': _body,            # 요청 바디
        'tr_name': _tr_name,      # TR 코드 이름
        'out_block_tags': ["header", "body"],  # 출력 블록 태그
        'shcode': None,           # 종목 코드 (필요시 사용)
    }


def SC2(_body="", _real=False):
    """

    """

    _tr_name = sys._getframe().f_code.co_name

    # TR 요청을 위한 URL 설정
    if not _real:
        _url = URL
    else:
        _url = MOCK_URL

    _header = {
        "token": f"Bearer {oauth.oauth(_real=_real)}",
        "tr_type": "1",
    }

    if _body == "":
        _body = {
            "tr_cd": _tr_name,
            "tr_key": "",
        }

    # TR 요청에 필요한 정보를 딕셔너리로 반환
    return {
        'url': _url,              # 요청 URL
        'header': _header,        # 요청 header
        'body': _body,            # 요청 바디
        'tr_name': _tr_name,      # TR 코드 이름
        'out_block_tags': ["header", "body"],  # 출력 블록 태그
        'shcode': None,           # 종목 코드 (필요시 사용)
    }


def SC3(_body="", _real=False):
    """

    """

    _tr_name = sys._getframe().f_code.co_name

    # TR 요청을 위한 URL 설정
    if not _real:
        _url = URL
    else:
        _url = MOCK_URL

    _header = {
        "token": f"Bearer {oauth.oauth(_real=_real)}",
        "tr_type": "1",
    }

    if _body == "":
        _body = {
            "tr_cd": _tr_name,
            "tr_key": "",
        }

    # TR 요청에 필요한 정보를 딕셔너리로 반환
    return {
        'url': _url,              # 요청 URL
        'header': _header,        # 요청 header
        'body': _body,            # 요청 바디
        'tr_name': _tr_name,      # TR 코드 이름
        'out_block_tags': ["header", "body"],  # 출력 블록 태그
        'shcode': None,           # 종목 코드 (필요시 사용)
    }


def SC4(_body="", _real=False):
    """

    """

    _tr_name = sys._getframe().f_code.co_name

    # TR 요청을 위한 URL 설정
    if not _real:
        _url = URL
    else:
        _url = MOCK_URL

    _header = {
        "token": f"Bearer {oauth.oauth(_real=_real)}",
        "tr_type": "1",
    }

    if _body == "":
        _body = {
            "tr_cd": _tr_name,
            "tr_key": "",
        }

    # TR 요청에 필요한 정보를 딕셔너리로 반환
    return {
        'url': _url,              # 요청 URL
        'header': _header,        # 요청 header
        'body': _body,            # 요청 바디
        'tr_name': _tr_name,      # TR 코드 이름
        'out_block_tags': ["header", "body"],  # 출력 블록 태그
        'shcode': None,           # 종목 코드 (필요시 사용)
    }


if __name__ == "__main__":
    import asyncio
    import pprint
    import tr_stock_order

    # 실제 환경 여부 설정 (False: 모의투자)
    IS_REAL = False

    # 주식 종목번호 설정 (삼성전자: A005930)
    if IS_REAL:
        IsuNo = "005930"
    else:
        IsuNo = "A005930"

    # 호가유형코드 및 주문가 설정
    OrdprcPtnCode = "00"                    # 지정가
    OrdPrc1 = 60000.0                       # 최초 주문가
    OrdPrc2 = 65000.0                       # 정정 주문가
    OrdQty = 1                              # 주문 수량

    def sync_request_tr(params, _real, _timeout):
        return request_tr.request_tr(params, _real=_real, _timeout=_timeout)

    async def send_order():
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

        # 동기 함수를 비동기로 실행
        cspat00601_params = tr_stock_order.CSPAT00601(cspat00601_body)
        loop = asyncio.get_running_loop()

        results0 = await loop.run_in_executor(None, sync_request_tr, cspat00601_params, IS_REAL, 3)
        pprint.pprint(results0)

        cs0_params = SC0(_real=False)
        results0r = await loop.run_in_executor(None, sync_request_tr, cs0_params, IS_REAL, 3)
        pprint.pprint(results0r)

    async def main():
        await asyncio.gather(
            send_order(),
        )

    # cs1_params = SC1(_real=False)
    # pprint.pprint(cs1_params)
    # results1 = request_tr.request_tr(cs1_params, _real=IS_REAL, _timeout=3)
    # pprint.pprint(results1)

    # cs2_params = SC2(_real=False)
    # pprint.pprint(cs2_params)
    # results2 = request_tr.request_tr(cs2_params, _real=IS_REAL, _timeout=3)
    # pprint.pprint(results2)

    # cs3_params = SC3(_real=False)
    # pprint.pprint(cs3_params)
    # results3 = request_tr.request_tr(cs3_params, _real=IS_REAL, _timeout=3)
    # pprint.pprint(results3)

    # cs4_params = SC4(_real=False)
    # pprint.pprint(cs4_params)
    # results4 = request_tr.request_tr(cs4_params, _real=IS_REAL, _timeout=3)
    # pprint.pprint(results4)

    # 결과를 CSV 파일로 저장
    # request_tr.save_csv(_data_frames=results0r, _tr_name="SC0")
    # request_tr.save_csv(_data_frames=results1r, _tr_name="SC1")
    # request_tr.save_csv(_data_frames=results2r, _tr_name="SC2")
    # request_tr.save_csv(_data_frames=results3r, _tr_name="SC3")
    # request_tr.save_csv(_data_frames=results4r, _tr_name="SC4")
