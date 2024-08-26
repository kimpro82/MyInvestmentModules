"""
LS Open API / [주식] 계좌 TR 요청 모듈
2024.08.26

이 모듈은 LS 증권의 Open API를 사용하여 특정 TR (Transaction Request) 요청을 처리하는 기능을 제공합니다. 
주로 주식 계좌와 관련된 정보 조회를 위한 CSPAQ12300 및 t0424 TR 요청을 포함합니다.

히스토리:
1   2024.08.26 최초 작성
"""


import sys
import request_tr_4 as request_tr


# API 요청을 위한 기본 URL 설정
URL = "https://openapi.ls-sec.co.kr:8080/stock/accno"

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
