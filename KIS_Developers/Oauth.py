import requests
import json
import Key


## 03. 서비스 연결 (Oauth)

## 01) 보안인증키 발급

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


## 02) 해쉬키(Hashkey) 발급

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

datas = {
    "CANO": '00000000',
    "ACNT_PRDT_CD": "01",
    "OVRS_EXCG_CD": "SHAA",
    "PDNO": "00001",
    "ORD_QTY": "500",
    "OVRS_ORD_UNPR": "52.65",
    "ORD_SVR_DVSN_CD": "0"
}

# print(hashkey(datas))                                             ## Success