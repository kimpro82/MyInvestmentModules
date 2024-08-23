"""
eBest Open API / OAuth
2023.07.11
"""


import pprint
import requests
import Key

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


if __name__ == "__main__":
    print("URL          : ", URL, "\n")                     # Ok
    print("OAuth        : ")
    pprint.pprint(res.json())                               # Ok
