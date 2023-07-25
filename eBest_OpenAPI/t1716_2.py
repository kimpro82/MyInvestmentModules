"""
eBest Open API / 외인기관종목별동향 (t1716)
2023.07.25

이 코드는 eBest Open API에서 t1716 TR을 호출하기 위한 코드입니다.
t1716 TR은 주식 시장의 기관 및 외인 순매매 정보를 조회하는 TR입니다.

History :
    1 2023.07.21 최초 작성
    2 2023.07.25 t1716()의 리턴값을 딕셔너리 타입으로 변경
"""


from datetime import datetime, timedelta
import pytz


def t1716(shcode = "005930", todt = "", period = 366):
    """
    eBest Open API에서 t1716 TR을 호출하기 위한 URL, 헤더 및 바디 정보를 반환하는 함수입니다.

    Parameters  :
        shcode (str, optional)  : 종목코드를 지정하는 매개변수입니다. 기본값은 "005930"(삼성전자)로 설정됩니다.
        todt (str, optional)    : 조회를 종료할 날짜를 지정하는 매개변수입니다. 기본값은 오늘 날짜로 설정됩니다.
        period (int, optional)  : 조회 기간을 지정하는 매개변수입니다. 기본값은 365일(1년)입니다.

    Returns     :
        dict                    : 함수 호출 시 반환되는 값들을 딕셔너리로 묶어 반환합니다.
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
    _todt_datetime  = datetime.strptime(_todt, '%Y%m%d').astimezone(_seoul_timezone)
    _fromdt         = (_todt_datetime - timedelta(period)).strftime("%Y%m%d")

    _body           = {
        "t1716InBlock": {
            "shcode"    : shcode,                           # 종목코드
            "gubun"     : "0",                              # 0:일간순매수 1:기간내누적순매수
            "fromdt"    : _fromdt,                          # 시작일자 : YYYYMMDD (default : 종료일자로부터 1년 전)
            "todt"      : _todt,                            # 종료일자 : YYYYMMDD
            "prapp"     : 100,                              # 프로그램매매 감산 적용율 - %단위
            "prgubun"   : "1",                              # PR적용구분(0:적용안함1:적용)
            "orggubun"  : "1",                              # 기관적용(0:미적용 1:적용)
            "frggubun"  : "1"                               # 외인적용(0:미적용 1:적용)
        }
    }

    _out_block_tag  = "OutBlock"

    return {
        'url'           : _url,
        'header'        : _header,
        'body'          : _body,
        'tr_name'       : t1716.__name__,
        'out_block_tag' : _out_block_tag,
        'shcode'        : shcode
    }


if __name__ == "__main__":

    import pprint

    results = t1716()                                       # 함수 호출 결과를 딕셔너리로 받음
    pprint.pprint(results)
