"""
LS Open API / t0424 TR 요청 모듈
2024.08.26

이 모듈은 LS 증권의 Open API를 사용하여 특정 TR (Transaction Request) 요청을 처리하는 기능을 제공합니다. 
특히, t0424 TR 코드를 사용하여 주식 정보를 조회합니다.

히스토리:
1   2024.08.26 최초 작성
"""

import request_tr_3 as request_tr

# API 요청을 위한 기본 URL 설정
URL = "https://openapi.ls-sec.co.kr:8080/stock/accno"

def t0424(_cts_expcode=""):
    """
    t0424 TR 요청을 위한 함수.

    이 함수는 t0424 TR에 필요한 요청 URL, 헤더, 바디 및 출력 블록 태그를 설정하고 반환합니다.
    
    Args:
        _cts_expcode (str, optional): 연속 조회를 위한 종목 코드. 기본값은 빈 문자열입니다.

    Returns:
        dict: t0424 TR 요청에 필요한 정보가 담긴 딕셔너리.
    """

    # TR 요청을 위한 URL 설정
    _url = URL
    _tr_cd = "t0424"  # TR 코드 설정

    # 요청에 필요한 헤더 설정
    _header = {
        "content-type": "application/json; charset=utf-8",  # 콘텐츠 타입
        "authorization": None,  # 인증 토큰 (실제 요청 시 추가 필요)
        "tr_cd": _tr_cd,  # TR 코드
        "tr_cont": "N",  # 연속 조회 여부 (기본값: N)
        "tr_cont_key": "",  # 연속 조회 키 (필요시 사용)
        "mac_address": ""  # MAC 주소 (필요시 사용)
    }

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

    # 출력 블록 태그 (결과 데이터를 참조하기 위한 키)
    _out_block_tag = ["OutBlock", "OutBlock1"]

    # TR 요청에 필요한 정보를 딕셔너리로 반환
    return {
        'url': _url,              # 요청 URL
        'header': _header,        # 요청 헤더
        'body': _body,            # 요청 바디
        'tr_name': _tr_cd,        # TR 코드 이름
        'out_block_tag': _out_block_tag,  # 출력 블록 태그
        'shcode': None,           # 종목 코드 (필요시 사용)
    }

if __name__ == "__main__":
    import pprint

    # t0424 TR 요청을 위한 파라미터 설정
    t0424_params = t0424(_cts_expcode="")

    # TR 요청 및 결과 출력
    results = request_tr.request_tr(t0424_params, _real=False, _timeout=3)
    
    # 첫 번째 결과 블록의 첫 번째 데이터와 두 번째 데이터를 출력
    pprint.pprint(results[0][0])
    pprint.pprint(results[0][1])
    
    # 결과를 CSV 파일로 저장
    request_tr.save_csv(_data_frames=results[0], _tr_name="t0424")
