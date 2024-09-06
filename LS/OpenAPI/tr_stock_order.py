"""
LS Open API / [주식] 주문 TR 요청 모듈
2024.09.06

설명:
이 모듈은 LS 증권 Open API를 통해 주식 주문, 정정, 취소 요청을 처리하는 기능을 제공합니다.
주요 TR 코드인 CSPAT00601(주문), CSPAT00701(정정), CSPAT00801(취소)에 대한 요청 데이터를 
생성하고 API 서버에 요청하는 구조로 이루어져 있습니다. 각 함수는 주문 데이터를 인자로 받아 
해당 TR에 맞는 형식으로 API 호출에 필요한 정보를 구성하며, 호출 결과는 CSV 파일로 저장될 수 있습니다.

구성:
1. CSPAT00601: 주식 매수 주문 요청을 위한 함수
2. CSPAT00701: 주식 주문 정정 요청을 위한 함수
3. CSPAT00801: 주식 주문 취소 요청을 위한 함수
4. 메인 실행부: 주식 주문 → 주문 정정 → 주문 취소 순서로 API 호출 흐름을 실행

사용 예:
해당 모듈은 `request_tr` 모듈을 통해 TR 요청을 수행하며, 실제 환경과 모의 투자 환경을 구분하여
TR 요청을 수행할 수 있습니다. 본 예시에서는 모의 투자를 가정하여 API 요청 흐름을 보여줍니다.

히스토리:
1   2024.09.06 최초 작성
"""


import sys
import request_tr_4 as request_tr


# API 요청을 위한 기본 URL 설정
URL = "https://openapi.ls-sec.co.kr:8080/stock/order"


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
