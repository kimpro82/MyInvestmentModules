import requests

import Key                                                          ## save keys seperately
import Oauth                                                        ## call Oauth.ACCESS_TOKEN


## 04. 현재가 조회 

## 01) 주식현재가 시세

APP_KEY = Key.key
APP_SECRET = Key.secret
ACCESS_TOKEN = Oauth.ACCESS_TOKEN

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
print(res.json()['output']['stck_prpr'])                            # success


## 02) 주식현재가 일자별

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