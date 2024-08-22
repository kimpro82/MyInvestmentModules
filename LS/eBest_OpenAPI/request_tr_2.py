"""
eBest Open API / request_tr
2023.07.25

이 코드는 eBest Open API에서 TR을 호출하여 데이터를 조회하고 CSV 파일로 저장하는 코드입니다.

History :
    1   2023.07.21  최초 작성
    2   2023.07.25  request_tr(): t****()의 리턴값을 딕셔너리 타입으로 받도록 변경
                    save_csv()  : 저장시 pandas.DataFrame의 index 값 제외
"""


import datetime
import json
import pytz
import pandas as pd
import requests

import oauth2 as oauth


def request_tr(results):
    """
    eBest Open API에서 TR을 호출하여 데이터를 조회하는 함수입니다.

    Parameters :
        results (dict)      : t****() 함수의 리턴값인 딕셔너리입니다.

    Returns:
        pandas.DataFrame    : 조회된 데이터가 담긴 DataFrame 객체를 반환합니다.
        str                 : 함수 이름을 반환합니다.
        str                 : 종목코드를 반환합니다.
    """

    _url            = results["url"]
    _header         = results["header"]
    _body           = results["body"]
    _tr_name        = results["tr_name"]
    _out_block_tag  = results["out_block_tag"]
    _shcode         = results["shcode"]

    _header["authorization"] = f"Bearer {oauth.oauth()}"
    _res = requests.post(_url, headers=_header, data=json.dumps(_body), timeout=1)
    _json_data = _res.json()
    # print(_json_data)                                                         # Ok
    # print(f"{_tr_name}{_out_block_tag}")                                      # Ok
    _data_frame = pd.json_normalize(_json_data[f"{_tr_name}{_out_block_tag}"])

    return _data_frame, _tr_name, _shcode


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
    data_frame.to_csv(_path, index=False)
    print("파일 저장을 완료하였습니다. :", _path)


if __name__ == "__main__":

    import pprint
    import t1716_2 as t1716

    tr_output = request_tr(t1716.t1716(shcode="005930", period=365))             # 삼성전자, 1년치 일일 데이터
    pprint.pprint(tr_output)
    save_csv(*tr_output)
