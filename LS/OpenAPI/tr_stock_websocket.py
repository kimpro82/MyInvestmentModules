"""
LS Open API / [주식] 실시간 시세 TR 요청 모듈
2024.09.04

히스토리:
1   2024.09.04 최초 작성
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
    import pprint

    cs0_params = SC0(_real=False)
    pprint.pprint(cs0_params)
    results0 = request_tr.request_tr(cs0_params, _real=False, _timeout=3)
    pprint.pprint(results0)

    cs1_params = SC1(_real=False)
    pprint.pprint(cs1_params)
    results1 = request_tr.request_tr(cs1_params, _real=False, _timeout=3)
    pprint.pprint(results1)

    cs2_params = SC2(_real=False)
    pprint.pprint(cs2_params)
    results2 = request_tr.request_tr(cs2_params, _real=False, _timeout=3)
    pprint.pprint(results2)

    cs3_params = SC3(_real=False)
    pprint.pprint(cs3_params)
    results3 = request_tr.request_tr(cs3_params, _real=False, _timeout=3)
    pprint.pprint(results3)

    cs4_params = SC4(_real=False)
    pprint.pprint(cs4_params)
    results4 = request_tr.request_tr(cs4_params, _real=False, _timeout=3)
    pprint.pprint(results4)

    # 결과를 CSV 파일로 저장
    request_tr.save_csv(_data_frames=results0, _tr_name="SC0")
    request_tr.save_csv(_data_frames=results1, _tr_name="SC1")
    request_tr.save_csv(_data_frames=results2, _tr_name="SC2")
    request_tr.save_csv(_data_frames=results3, _tr_name="SC3")
    request_tr.save_csv(_data_frames=results4, _tr_name="SC4")
