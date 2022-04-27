# My `KIS Developers` Application Modules

Codes with `KIS Developers` from *Korea Investment & Securities Co., Ltd.*


**\<Reference>**  
- KIS 트레이딩 오픈API 개발자 센터 ☞ https://apiportal.koreainvestment.com/
- 파이썬으로 배우는 오픈API 트레이딩 초급 예제 ☞ https://wikidocs.net/book/7559
- 파이썬으로 배우는 한국투자증권 Websocket 사용 예제 ☞ https://wikidocs.net/book/7847
- KIS Developers (Github) ☞ https://github.com/koreainvestment/open-trading-api


## \<List>
- [Inquire Price (2022.04.26)]()
- [Oauth (2022.04.19)](#oauth-20220419)


## [Inquire Price (2022.04.26)](#list)

- Call a specific stock's current price and daily price-related data  
※ Need to improve not to call the API access token more than one times

### 01) 주식현재가 시세
&nbsp;&nbsp; - https://wikidocs.net/159339

#### InquirePrice.py
```python
import requests

import Key                                                          ## save keys seperately
import Oauth                                                        ## call Oauth.ACCESS_TOKEN

APP_KEY = Key.key
APP_SECRET = Key.secret
ACCESS_TOKEN = Oauth.ACCESS_TOKEN
```
```python
URL_BASE = "https://openapivts.koreainvestment.com:29443"           ## 모의투자
PATH = "uapi/domestic-stock/v1/quotations/inquire-price"
URL = f"{URL_BASE}/{PATH}"
# print(URL)
# https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-price

headers = {"Content-Type":"application/json", 
           "authorization": f"Bearer {ACCESS_TOKEN}",
           "appKey":APP_KEY,
           "appSecret":APP_SECRET,
           "tr_id":"FHKST01010100"}

params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":"005930"                                       # 005930; 삼성전자
}

res = requests.get(URL, headers=headers, params=params)
# print(res.json())                                                 # success; call all data
print(res.json()['output']['stck_prpr'])                          # success
```
```
66100
```

### 02) 주식현재가 일자별
&nbsp;&nbsp; - https://wikidocs.net/159340

#### InquirePrice.py
```python
PATH = "uapi/domestic-stock/v1/quotations/inquire-daily-price"
URL = f"{URL_BASE}/{PATH}"
# print(URL)
# https://openapivts.koreainvestment.com:29443/uapi/domestic-stock/v1/quotations/inquire-daily-price

# headers = {"Content-Type":"application/json",
#             "authorization":f"Bearer {ACCESS_TOKEN}",
#             "appKey":APP_KEY,
#             "appSecret":APP_SECRET,
#             "tr_id":"FHKST01010100"}

headers["tr_id"] = "FHKST01010400"                                  # change only 'tr_id' among the parameters in 'headers'

params = {
    "fid_cond_mrkt_div_code":"J",
    "fid_input_iscd":"005930",
    "fid_org_adj_prc":"1",
    "fid_period_div_code":"D"
}

res = requests.get(URL, headers=headers, params=params)
# print(res.json())                                                 # success; call all data
for i in range(0, 10) :
    print(res.json()['output'][i]['stck_bsop_date'], res.json()['output'][i]['stck_clpr'], res.json()['output'][i]['prdy_ctrt'], res.json()['output'][i]['acml_vol'])
```
```
20220426 66100 -0.30 12946923
20220425 66300 -1.04 11016474
20220422 67000 -1.03 11791478
20220421 67700 0.45 12847448
20220420 67400 0.15 16693293
20220419 67300 0.90 12959434
20220418 66700 0.15 10119203
20220415 66600 -1.33 13176415
20220414 67500 -1.75 16409494
20220413 68700 2.54 17378619
```


## [Oauth (2022.04.19)](#list)

Oauth; Open Authorization

### 01) 보안인증키 발급
&nbsp;&nbsp; - https://wikidocs.net/159336

#### Key.py (not uploaded)
```python
key = ""
secret = ""

key2 = ""
secret2 = ""
```

#### Oauth.py
```python
import requests
import json
import Key
```
```python
APP_KEY = Key.key
APP_SECRET = Key.secret
URL_BASE = "https://openapivts.koreainvestment.com:29443"           ## 모의투자

headers = {"content-type" : "application/json"}
body = {
    "grant_type" : "client_credentials",
    "appkey" : APP_KEY, 
    "appsecret" : APP_SECRET,
}

PATH = "oauth2/tokenP"

URL = f"{URL_BASE}/{PATH}"
# print(URL)                                                        ## https://openapivts.koreainvestment.com:29443/oauth2/token

res = requests.post(URL, headers=headers, data=json.dumps(body))
# print(res.text)                                                   ## {"access_token":"ACCESS_TOKEN","token_type":"Bearer","expires_in":86400}

ACCESS_TOKEN = res.json()["access_token"]
# print(ACCESS_TOKEN)                                               ## Success
```

#### 02) 해쉬키(Hashkey) 발급
&nbsp;&nbsp; - https://wikidocs.net/159337

#### Oauth.py
```python
def hashkey(datas) :

    PATH = "uapi/hashkey"
    URL = f"{URL_BASE}/{PATH}"

    headers = {
        'content-Type' : 'application/json',
        'appKey' : APP_KEY,
        'appSecret' : APP_SECRET,
    }

    res = requests.post(URL, headers=headers, data=json.dumps(datas))
    hashkey = res.json()["HASH"]

    return hashkey
```
```python
datas = {
    "CANO": '00000000',
    "ACNT_PRDT_CD": "01",
    "OVRS_EXCG_CD": "SHAA",
    "PDNO": "00001",
    "ORD_QTY": "500",
    "OVRS_ORD_UNPR": "52.65",
    "ORD_SVR_DVSN_CD": "0"
}

print(hashkey(datas))                                               ## Success
```