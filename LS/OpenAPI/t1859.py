"""
LS Open API / t1866, t1859 TR 요청 모듈
2024.08.22

이 모듈은 LS Open API를 통해 t1866 및 t1859 TR 데이터를 요청하고 결과를 처리하는 기능을 제공합니다.
t1866은 종목 검색 기능을, t1859는 특정 기준에 따른 종목 리스트를 조회하는 기능을 수행합니다.

함수:
    t1866(_gb="0", _cont=""):
        종목 검색을 위한 t1866 TR 데이터를 요청하기 위한 URL, 헤더, 바디 등을 생성합니다.

    t1859(_query_index="0000"):
        특정 기준에 따른 종목 리스트 조회를 위한 t1859 TR 데이터를 요청하기 위한 URL, 헤더, 바디 등을 생성합니다.

주의사항:
    이 모듈을 사용하기 전에 `request_tr_3` 모듈과 `key` 모듈이 필요합니다.
    `key` 모듈에는 사용자 ID와 인증 정보가 저장되어 있어야 합니다.
    t1866 TR에서 얻은 query_index를 t1859 TR로 직접 전달하지 않습니다.

히스토리:
1   2024.08.22 최초 작성
"""


import key
import request_tr_3 as request_tr


# API 요청을 위한 기본 URL 설정
URL = "https://openapi.ls-sec.co.kr:8080/stock/item-search"


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
