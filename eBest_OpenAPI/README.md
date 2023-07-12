# My `eBest OPEN API` Application Modules

Codes with `OPEN API` from *eBest Investment & Securities Co., Ltd.*


### \<Reference>
- eBest OPEN API Portal https://openapi.ebestsec.co.kr/ 

### \<List>
- [Oauth (2023.07.11)](#oauth-20230711)


## [Oauth (2023.07.11)](#list)

- Oauth; Open Authorization

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