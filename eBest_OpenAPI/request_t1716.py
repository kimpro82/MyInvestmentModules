"""
eBest Open API / 외인기관종목별동향 (t1716) 실행
2023.07.25

History :
    1   2023.07.21  최초 작성
    2   2023.07.25  request_tr()의 리턴값을 병합하여 하나의 CSV 파일로 출력
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
    unique_keys = ["date"]                                                      # to remove duplicated columns

    # print(todts)                                                              # Ok

    for shcode in shcodes:
        merged_df = pd.DataFrame()
        for todt in todts:
            results = request_tr.request_tr(t1716.t1716(shcode=shcode, todt=todt, period=PERIOD))
            merged_df = pd.concat([merged_df, results[0]])
            print(f"{TR_NAME} / {shcode} 종목 / {todt} 데이터를 수신하였습니다.")
            time.sleep(1)
        merged_df.drop_duplicates(subset=unique_keys, keep='first', inplace=True)
        request_tr.save_csv(data_frame=merged_df, tr_name=TR_NAME, shcode=shcode)
