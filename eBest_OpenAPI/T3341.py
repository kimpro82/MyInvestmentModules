"""
eBest Open API / Financial Rank (t3341)
2023.07.14
"""

# import pprint
import datetime
import json
import pandas as pd
import requests

import OAuth


URL_BASE    = "https://openapi.ebestsec.co.kr:8080"
PATH        = "stock/investinfo"
URL         = f"{URL_BASE}/{PATH}"

header      = {
    "content-type"  : "application/json; charset=UTF-8",
    "authorization" : f"Bearer {OAuth.ACCESS_TOKEN}",
    "tr_cd"         : "t3341",
    "tr_cont"       : "N",
    "tr_cont_key"   : "",
    "mac_address"   : ""
}

body       = {
    "t3341InBlock": {
        "gubun"     : "0",                                  # 0 : 전체
        "gubun1"    : "3",                                  # 3 : 세전계속이익증가율
        "gubun2"    : "1",                                  # 1 : 고정
        "idx"       : 0
  }
}

res = requests.post(URL, headers=header, data=json.dumps(body), timeout=1)
# pprint.pprint(res.json())

json_data = res.json()
df = pd.json_normalize(json_data["t3341OutBlock1"])
time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
df.to_csv(f'Data/T3341_{time_stamp}.csv')

if __name__ == "__main__":
    print(df)
