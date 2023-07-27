"""
eBest Open API / 외인기관종목별동향 (t1716) 실행
2023.07.25

이 코드는 eBest Open API에서 t1716 TR을 호출하여 주어진 종목 코드와 조회 기간에 따른 외인과 기관의 순매매 정보를 조회하고,
이를 하나의 DataFrame으로 병합한 뒤 하나의 CSV 파일로 저장하는 작업을 수행합니다.

Parameters  :
    TR_NAME (str)       : TR을 호출하는 함수의 이름으로 사용될 문자열입니다.
    shcodes (list)      : 조회할 종목 코드들이 담긴 리스트입니다.
    todts (list)        : 조회를 종료할 날짜들이 담긴 리스트입니다.
    YEARS (int)         : 조회 기간의 연도 수를 나타내는 정수입니다.
    PERIOD (int)        : 조회 기간을 나타내는 정수로, 최대 366일까지 조회가 가능합니다.
    unique_keys (list)  : 중복된 열을 제거하기 위해 사용될 DataFrame의 열 이름들이 담긴 리스트입니다.

Returns     :
    None
"""


import time
import t1716_2 as t1716
import request_tr_2 as request_tr
import pandas as pd


if __name__ == "__main__":

    TR_NAME = "t1716"
    shcodes = ["122630", "252670", "233740", "251340"]
    todts   = []
    YEARS   = 10
    for i in range(0, YEARS):
        todts.append(str(2022 - i) + "1231")
    PERIOD  = 366
        # It seems to have a maximum value of 366 (why not 365? considering leap years)
    unique_keys = ["shcode", "date"]                                            # to remove duplicated columns

    # print(todts)                                                              # Ok

    merged_df = pd.DataFrame()
    for shcode in shcodes:
        merged_df_2 = pd.DataFrame()
        for todt in todts:
            results = request_tr.request_tr(t1716.t1716(shcode=shcode, todt=todt, period=PERIOD))
            merged_df_2 = pd.concat([merged_df_2, results[0]])
            print(f"{TR_NAME} / {shcode} 종목 / {todt} 데이터를 수신하였습니다.")
            time.sleep(1)
        merged_df_2["shcode"] = shcode
        merged_df = pd.concat([merged_df, merged_df_2])
    merged_df.drop_duplicates(subset=unique_keys, keep='first', inplace=True)
    request_tr.save_csv(data_frame=merged_df, tr_name=TR_NAME)
