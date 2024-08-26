"""
LS Open API / request_tr 4
2024.08.26

이 코드는 LS Open API에서 TR을 호출하여 데이터를 조회하고 CSV 파일로 저장하는 코드입니다.

History:
    1   2023.07.21  최초 작성
    2   2023.07.25  request_tr(): t****()의 리턴값을 딕셔너리 타입으로 받도록 변경
                    save_csv(): 저장 시 pandas.DataFrame의 index 값 제외
    3   2024.08.22  실서버/모의서버 여부(_real)를 oauth.oauth()에 전달
                    복수 t****OutBlock* 대응: request_tr(), save_csv()
                    _timeout(int, optional)을 requests.post()에 전달
    4   2024.08.26  request_tr()에서 header 데이터 생성하도록 변경
"""

import datetime
import json
import pytz
import pandas as pd
import requests

import oauth_3 as oauth


def request_tr(_results, _real=False, _timeout=1):
    """
    LS Open API에서 TR을 호출하여 데이터를 조회하는 함수입니다.

    Parameters:
        _results(dict)  : t****() 함수의 리턴값인 딕셔너리입니다.
        _real(bool)     : 실서버(True)/모의서버(False) 여부를 지정하는 매개변수입니다.
        _timeout(int)   : requests.post()에 전달할 매개변수입니다.

    Returns:
        list            : 조회된 데이터를 담고 있는 pandas DataFrame 객체의 리스트.
        str             : TR 이름을 나타내는 문자열.
        str             : 종목 코드를 나타내는 문자열.
    """

    # 요청에 필요한 정보를 설정
    _url = _results["url"]
    _tr_name = _results["tr_name"]
    
    # 헤더가 딕셔너리에 포함되어 있지 않으면 기본 헤더를 설정
    if not "_header" in _results:
        _header = {
            "content-type": "application/json; charset=utf-8",  # 콘텐츠 타입
            "authorization": None,  # OAuth 토큰 (추후 추가)
            "tr_cd": _tr_name,  # TR 코드
            "tr_cont": "N",  # 연속 조회 여부 (기본값: N)
            "tr_cont_key": "",  # 연속 조회 키 (필요시 사용)
            "mac_address": ""  # MAC 주소 (필요시 사용)
        }
    else:
        _header = _results["header"]

    # OAuth 토큰을 설정
    _header["authorization"] = f"Bearer {oauth.oauth(_real=_real)}"

    # 바디, 출력 블록 태그, 종목 코드 설정
    _body = _results["body"]
    _out_block_tags = _results["out_block_tags"]
    _shcode = _results["shcode"]

    # TR 요청을 POST 방식으로 전송
    _res = requests.post(_url, headers=_header, data=json.dumps(_body), timeout=_timeout)
    _json_data = _res.json()

    _data_frames = []

    # 각 출력 블록 태그에 대해 데이터프레임 생성
    for _out_block_tag in _out_block_tags:
        _data_frame = pd.json_normalize(_json_data[_out_block_tag])
        _data_frames.append(_data_frame)

    # 조회된 데이터프레임 리스트, TR 이름, 종목 코드를 반환
    return _data_frames, _tr_name, _shcode


def save_csv(_data_frames, _tr_name, _shcode=""):
    """
    조회된 데이터를 CSV 파일로 저장하는 함수입니다.

    Parameters:
        _data_frames(list)      : 조회된 데이터가 담긴 DataFrame 객체들의 리스트입니다.
        _tr_name(str)           : 저장할 파일의 이름을 지정하는 매개변수입니다.
        _shcode(str, optional)  : 종목 코드를 지정하는 매개변수입니다. 기본값은 빈 문자열("")입니다.

    Returns:
        None
    """

    # 현재 시간을 서울 시간대 기준으로 가져와서 타임스탬프 생성
    _seoul_timezone = pytz.timezone('Asia/Seoul')
    _time_stamp = datetime.datetime.now(_seoul_timezone).strftime("%Y%m%d_%H%M%S")

    # 각 데이터프레임을 CSV 파일로 저장
    for i, _data_frame in enumerate(_data_frames):
        if _shcode:
            _path = f'Data/{_tr_name.upper()}_{_shcode}_{_time_stamp}_{i}.csv'
        else:
            _path = f'Data/{_tr_name.upper()}_{_time_stamp}_{i}.csv'

        _data_frame.to_csv(_path, index=False)  # 인덱스 제외하고 저장
        print("파일 저장을 완료하였습니다. :", _path)


if __name__ == "__main__":
    import pprint
    import tr_stock_accno

    # CSPAQ12300 TR 요청 및 결과 확인
    tr_outputs = request_tr(tr_stock_accno.CSPAQ12300())
    pprint.pprint(tr_outputs)

    # 조회된 데이터를 CSV 파일로 저장
    save_csv(*tr_outputs)