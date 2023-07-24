"""
eBest Open API / request_tr
2023.07.21

이 코드는 eBest Open API에서 TR을 호출하여 데이터를 조회하고 CSV 파일로 저장하는 코드입니다.
"""


import datetime
import json
import pytz
import pandas as pd
import requests

import oauth2 as oauth


def request_tr(url, header, body, tr_name, out_block_tag, shcode):
    """
    eBest Open API에서 TR을 호출하여 데이터를 조회하는 함수입니다.

    Parameters:
        url (str)           : API 호출을 위한 URL입니다.
        header (dict)       : API 호출에 필요한 헤더 정보가 담긴 딕셔너리입니다.
        body (dict)         : API 호출에 필요한 바디 정보가 담긴 딕셔너리입니다.
        tr_name (str)       : 함수 이름입니다.
        out_block_tag (str) : 반환 데이터의 태그입니다.
        shcode (str)        : 종목코드를 지정하는 매개변수입니다.

    Returns:
        pandas.DataFrame    : 조회된 데이터가 담긴 DataFrame 객체를 반환합니다.
        str                 : 함수 이름을 반환합니다.
        str                 : 종목코드를 반환합니다.
    """

    header["authorization"] = f"Bearer {oauth.oauth()}"
    _res = requests.post(url, headers=header, data=json.dumps(body), timeout=1)
    _json_data = _res.json()
    # print(json_data)                                                          # Ok
    # print(f"{TR_NAME}{out_block_tag}")                                        # Ok
    _data_frame = pd.json_normalize(_json_data[f"{tr_name}{out_block_tag}"])

    return _data_frame, tr_name, shcode


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
    data_frame.to_csv(_path)
    print("파일 저장을 완료하였습니다. :", _path)


if __name__ == "__main__":

    import t1716

    results = request_tr(*t1716.t1716(shcode="005930", period=365))             # 삼성전자, 1년치 일일 데이터
    print(results[0])
    save_csv(*results)
