# [My `eBest OPEN API` Application Modules](../README.md#my-ebest-open-api-application-modules)

Codes with `OPEN API` from *eBest Investment & Securities Co., Ltd.*


### \<Reference>
- eBest OPEN API Portal https://openapi.ebestsec.co.kr/ 

### \<List>
- [재무순위종합(t3341, 2023.07.14)](#재무순위종합t3341-20230714)
- [Oauth (2023.07.11)](#oauth-20230711)


## [재무순위종합(t3341) (2023.07.14)](#list)

- [eBest OPEN API](https://openapi.ebestsec.co.kr) > [API 가이드 > 주식 > [주식] 투자정보](https://openapi.ebestsec.co.kr/apiservice#G_73142d9f-1983-48d2-8543-89b75535d34c#A_3dbce945-a73c-475c-9758-88d9922ab94e) > 재무순위종합


  <details>
    <summary>Codes : T3341.py</summary>

  ```py
  # import pprint
  import datetime
  import json
  import pandas as pd
  import requests

  import OAuth
  ```
  ```py

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
  ```
  ```py
  if __name__ == "__main__":
      print(df)
  ```
  </details>
  <details open = "">
    <summary>Output</summary>

  ```txt
      rank     hname  salesgrowth  operatingincomegrowt  ordinaryincomegrowth  liabilitytoequity  enterpriseratio      eps       bps    roe  shcode    per    pbr    peg
  0      1      동양파일         4.39                -35.60               6691.58               5.29          1129.14   245.33   6145.71   4.07  228340  12.66   0.51  38.84
  1      2   감성코퍼레이션       139.90               1300.52               5433.07              64.87            13.62   168.35    568.07  37.70  036620  26.46   7.84   1.31
  2      3  선진뷰티사이언스        31.80                 47.70               3772.86             106.80           955.24  1593.39   5276.18  35.91  086710   5.72   1.73   0.52
  3      4      일신석재        84.19                371.91               3032.30             110.34            43.52    30.31    717.60   4.37  007110  42.10   1.78   0.00
  4      5    모베이스전자        17.80                169.62               2912.85             217.62           376.10    92.64   2380.49   4.08  012860  29.90   1.16   0.00
  ..   ...       ...          ...                   ...                   ...                ...              ...      ...       ...    ...     ...    ...    ...    ...
  95    96     큐에스아이       -22.75                -51.57                179.33               6.22          1685.83   711.54   8929.14   8.34  066310  15.26   1.22   5.74
  96    97   신세계 I&C        11.80                  4.35                178.53              31.66          4596.92  5253.56  23484.59  28.68  035510   2.53   0.57   1.05
  97    98        윈텍        31.57                211.76                176.70              26.46          1128.32    95.72   1228.32   8.08  320000  32.12   2.50  64.16
  98    99    한글과컴퓨터         9.40                 -3.23                176.47              21.47          2506.32  2147.60  13715.19  18.09  030520   5.83   0.91   1.60
  99   100    파크시스템스        41.89                 80.00                173.67              32.17          3336.79  3233.76  17183.96  21.40  140860  58.79  11.06   2.57

  [100 rows x 14 columns]
  ```
  </details>


## [Oauth (2023.07.11)](#list)

- Oauth; Open Authorization
- [eBest OPEN API](https://openapi.ebestsec.co.kr) > [API 가이드 > OAuth 인증 > 접근토큰 발급](https://openapi.ebestsec.co.kr/apiservice#G_ffd2def7-a118-40f7-a0ab-cd4c6a538a90#A_33bd887a-6652-4209-88cd-5324bc7c5e36)
- [eBest OPEN API](https://openapi.ebestsec.co.kr) > [OPEN API > OPEN API 이용안내](https://openapi.ebestsec.co.kr/howto-use) > 03. 접근토큰 발급

  <details>
    <summary>Codes : Key.py (not uploaded)</summary>

    ```python
    MOCK_KEY    = "{your app key}"
    MOCK_SECRET = "{your secret key}"
    ```
  </details>
  <details>
    <summary>Codes : Oauth.py</summary>

  ```python
  import pprint
  import requests
  import Key
  ```
  ```python
  APP_KEY     = Key.MOCK_KEY
  APP_SECRET  = Key.MOCK_SECRET

  header      = {
      "content-type"  : "application/x-www-form-urlencoded"
  }
  param       = {
      "grant_type"    : "client_credentials",
      "appkey"        : APP_KEY,
      "appsecretkey"  : APP_SECRET,
      "scope"         : "oob"
  }

  PATH        = "oauth2/token"
  URL_BASE    = "https://openapi.ebestsec.co.kr:8080"
  URL         = f"{URL_BASE}/{PATH}"

  res = requests.post(URL, headers=header, params=param, timeout=1)
  ACCESS_TOKEN = res.json()["access_token"]
  ```
  ```python
  if __name__ == "__main__":
      print("URL          : ", URL, "\n")                     # Ok
      print("OAuth        : ")
      pprint.pprint(res.json())                               # Ok
  ```
  </details>
  <details open = "">
    <summary>Output</summary>

  ```txt
  URL          :  https://openapi.ebestsec.co.kr:8080/oauth2/token

  OAuth        :
  {'access_token': '******',
   'expires_in': 105831,
   'scope': 'oob',
   'token_type': 'Bearer'}
  ```
  </details>