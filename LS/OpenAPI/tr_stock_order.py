"""
LS Open API / [주식] 주문 TR 요청 모듈
2024.08.28

히스토리:
1   2024.08.28 최초 작성
"""


import sys
import request_tr_4 as request_tr


# API 요청을 위한 기본 URL 설정
URL = "https://openapi.ls-sec.co.kr:8080/stock/order"

def CSPAT00601(_body):
    """

    """

    # TR 요청을 위한 URL 설정
    _url = URL

    # 함수 이름으로 TR 이름 설정
    _tr_name = sys._getframe().f_code.co_name

    # 출력 블록 태그 (결과 데이터를 참조하기 위한 키) 설정
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

    """

    # TR 요청을 위한 URL 설정
    _url = URL

    # 함수 이름으로 TR 이름 설정
    _tr_name = sys._getframe().f_code.co_name

    # 출력 블록 태그 (결과 데이터를 참조하기 위한 키) 설정
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

    cspat00601_body = {
        "CSPAT00601InBlock1": {
            "IsuNo": "A005930",             # 종목번호 (모의투자: A+종목코드)
            "OrdQty": 1,                    # 주문수량
            "OrdPrc": 60000.0,              # 주문가
            "BnsTpCode": "2",               # 매매구분 (1:매도, 2:매수)
            "OrdprcPtnCode": "00",          # 호가유형코드 (00:지정가, 03:시장가 등)
            "MgntrnCode": "000",            # 신용거래코드 (000:보통)
            "LoanDt": "",                   # 대출일
            "OrdCndiTpCode": "0",           # 주문조건구분 (0:없음, 1:IOC, 2:FOK)
        }
    }
    cspat00601_params = CSPAT00601(cspat00601_body)
    pprint.pprint(cspat00601_params)
    results1 = request_tr.request_tr(cspat00601_params, _real=False, _timeout=3)
    pprint.pprint(results1[0])
    OrdNo = results1[0][1]["OrdNo"].values[0]
    print(OrdNo)

    cspat00701_body = {
        "CSPAT00701InBlock1": {
            "OrgOrdNo": OrdNo,              # 원주문번호
            "IsuNo": "A005930",             # 종목번호 (모의투자: A+종목코드)
            "OrdQty": 1,                    # 주문수량
            "OrdprcPtnCode": "00",          # 호가유형코드 (00:지정가, 03:시장가 등)
            "OrdCndiTpCode": "0",           # 주문조건구분 (0:없음, 1:IOC, 2:FOK)
            "OrdPrc": 61000.0,              # 주문가
        }
    }
    cspat00701_params = CSPAT00701(cspat00701_body)
    pprint.pprint(cspat00701_params)
    results2 = request_tr.request_tr(cspat00701_params, _real=False, _timeout=3)
    pprint.pprint(results2)

    # 결과를 CSV 파일로 저장
    # request_tr.save_csv(_data_frames=results1[0], _tr_name=results1[1])
