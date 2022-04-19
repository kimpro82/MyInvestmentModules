# My `KIS Developers` Application Modules

Codes with `KIS Developers` from **Korea Investment & Securities Co., Ltd.**

**\<Reference>**  
- KIS 트레이딩 오픈API 개발자 센터 ☞ https://apiportal.koreainvestment.com/
- 파이썬으로 배우는 오픈API 트레이딩 초급 예제 ☞ https://wikidocs.net/book/7559
- 파이썬으로 배우는 한국투자증권 Websocket 사용 예제 ☞ https://wikidocs.net/book/7847
- KIS Developers (Github) ☞ https://github.com/koreainvestment/open-trading-api

## \<List>
- [Oauth (2022.04.19)](#oauth-20220419)


## [Oauth (2022.04.19)](#list)

  Oauth : Open Authorization

### 01) 보안인증키 발급
  https://wikidocs.net/159336

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
  https://wikidocs.net/159337

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