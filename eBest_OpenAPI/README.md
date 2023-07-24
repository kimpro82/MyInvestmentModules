# [My `eBest OPEN API` Application Modules](../README.md#my-ebest-open-api-application-modules)

Codes with `OPEN API` from *eBest Investment & Securities Co., Ltd.*


### \<Reference>
- eBest OPEN API Portal https://openapi.ebestsec.co.kr/ 

### \<List>
- [Request TR (2023.07.21)](#request-tr-20230721)
- [외인기관종목별동향(t1716, 2023.07.21)](#외인기관종목별동향t1716-20230721)
- [Oauth 2 (2023.07.21)](#oauth-2-20230721)
- [재무순위종합(t3341, 2023.07.14)](#재무순위종합t3341-20230714)
- [Oauth (2023.07.11)](#oauth-20230711)


## [Request TR (2023.07.21)](#list)

- Common functions
  - `request_tr()` : request *\<t\*\*\*\*> tr*
  - `save_csv()`   : save data from pandas dataframe to a `.csv` file

  <details>
    <summary>Codes : request_tr.py</summary>

  ```py
  """
  eBest Open API / request_tr
  2023.07.21

  이 코드는 eBest Open API에서 TR을 호출하여 데이터를 조회하고 CSV 파일로 저장하는 코드입니다.
  """
  ```
  ```py
  import datetime
  import json
  import pytz
  import pandas as pd
  import requests

  import oauth2 as oauth
  ```
  ```python
  def request_tr(url, header, body, tr_name, out_block_tag, shcode):
      """
      eBest Open API에서 TR을 호출하여 데이터를 조회하는 함수입니다.

      Parameters:
          url (str)           : API 호출을 위한 URL입니다.
          header (dict)       : API 호출에 필요한 헤더 정보가 담긴 딕셔너리입니다.
          body (dict)         : API 호출에 필요한 바디 정보가 담긴 딕셔너리입니다.
          tr_name (str)       : 함수 이름입니다.
          out_block_tag (str) : 반환 데이터의 태그입니다.
          shcode (str)        : 종목코드를 지정하는 매개변수입니다.

      Returns:
          pandas.DataFrame    : 조회된 데이터가 담긴 DataFrame 객체를 반환합니다.
          str                 : 함수 이름을 반환합니다.
          str                 : 종목코드를 반환합니다.
      """

      header["authorization"] = f"Bearer {oauth.oauth()}"
      _res = requests.post(url, headers=header, data=json.dumps(body), timeout=1)
      _json_data = _res.json()
      # print(json_data)                                                          # Ok
      # print(f"{TR_NAME}{out_block_tag}")                                        # Ok
      _data_frame = pd.json_normalize(_json_data[f"{tr_name}{out_block_tag}"])

      return _data_frame, tr_name, shcode
  ```
  ```py
  def save_csv(data_frame, tr_name, shcode=""):
      """
      조회된 데이터를 CSV 파일로 저장하는 함수입니다.

      Parameters:
          data_frame (pandas.DataFrame) : 조회된 데이터가 담긴 DataFrame 객체입니다.
          tr_name (str)                 : 저장할 파일의 이름을 지정하는 매개변수입니다.
          shcode (str, optional)        : 종목코드를 지정하는 매개변수입니다. 기본값은 ""(빈 문자열)입니다.

      Returns:
          None
      """

      _seoul_timezone = pytz.timezone('Asia/Seoul')
      _time_stamp = datetime.datetime.now(_seoul_timezone).strftime("%Y%m%d_%H%M%S")
      if len(shcode) > 0:
          _path = f'Data/{tr_name.upper()}_{shcode}_{_time_stamp}.csv'
      else:
          _path = f'Data/{tr_name.upper()}_{_time_stamp}.csv'
      data_frame.to_csv(_path)
      print("파일 저장을 완료하였습니다. :", _path)
  ```
  ```py
  if __name__ == "__main__":

      import t1716

      results = request_tr(*t1716.t1716(shcode="005930", period=365))             # 삼성전자, 1년치 일일 데이터
      print(results[0])
      save_csv(*results)
  ```
  </details>
  <details open="">
    <summary>Output</summary>

  ```txt
          date  close sign  change   diff    volume   krx_0008  krx_0018   krx_0009    pgmvol  fsc_listing fsc_sjrate   fsc_0009  gm_volume  gm_value
  0    20230721  70300    5    -700  -0.99  16528926 -135656797 -47587921  187226850  66422136   3161057429      52.95  189453121  111023539   6948297
  1    20230720  71000    5    -700  -0.98   9732730 -139311894 -47899737  191282378  67245571   3164847957      53.01  193243649  110811513   6933193
  2    20230719  71700    5    -300  -0.42  10851948 -140292604 -47019045  191388319  67055130   3163456948      52.99  191852640  110486152   6909844
  3    20230718  72000    5   -1300  -1.77  11282654 -141004884 -45818326  190916335  65954614   3163380264      52.99  191775956  110112691   6882647
  4    20230717  73300    5    -100  -0.14  10060049 -142362894 -45165996  191707382  66590493   3164885311      53.02  193281003  109698081   6852294
  ..        ...    ...  ...     ...    ...       ...        ...       ...        ...       ...          ...        ...        ...        ...       ...
  243  20220728  61900    2     100   0.16  10745302     238401  -2887326    2630540   -829418   2975485738      49.84    3881430     523771     32276
  244  20220727  61800    2     100   0.16   7320997     446970  -2327261    1853423  -1524933   2973391951      49.81    1787643     436702     26927
  245  20220726  61700    2     600   0.98   6597211     399096  -2012012    1563414  -1194339   2972792162      49.80    1187854     389076     23993
  246  20220725  61100    5    -200  -0.33   9193681     948321  -1614464     614373  -1331590   2972099731      49.79     495423     337887     20852
  247  20220722  61300    5    -500  -0.81  10261310    1022114  -1862181     739607   -342577   2972375415      49.79     771107          0         0

  [248 rows x 15 columns]
  ```
  ```txt
  파일 저장을 완료하였습니다. : Data/T1716_005930_20230722_173359.csv
  ```
  </details>


## [외인기관종목별동향(t1716, 2023.07.21)](#list)

- [eBest OPEN API](https://openapi.ebestsec.co.kr) > [API 가이드 > 주식 > [주식] 외인/기관](https://openapi.ebestsec.co.kr/apiservice?group_id=73142d9f-1983-48d2-8543-89b75535d34c&api_id=90378c39-f93e-4f95-9670-f76e5c924cc6) > 외인기관종목별동향 (t1716)
- Only save parameters, that will be called by `request_tr()` in [Request TR (2023.07.21)](#request-tr-20230721)

  <details>
    <summary>Codes : t1716.py</summary>

  ```py
  """
  eBest Open API / 외인기관종목별동향 (t1716)
  2023.07.21

  이 코드는 eBest Open API에서 t1716 TR을 호출하기 위한 예시 코드입니다.
  t1716 TR은 주식 시장의 기관 및 외인 순매매 정보를 조회하는 TR입니다.
  """
  ```
  ```py
  from datetime import datetime, timedelta
  import pytz
  ```
  ```python
  def t1716(shcode = "005930", todt = "", period = 365) :
      """
      eBest Open API에서 t1716 TR을 호출하기 위한 URL, 헤더 및 바디 정보를 반환하는 함수입니다.

      Parameters:
          shcode (str, optional)  : 종목코드를 지정하는 매개변수입니다. 기본값은 "005930"(삼성전자)로 설정됩니다.
          todt (str, optional)    : 조회를 종료할 날짜를 지정하는 매개변수입니다. 기본값은 오늘 날짜로 설정됩니다.
          period (int, optional)  : 조회 기간을 지정하는 매개변수입니다. 기본값은 365일(1년)입니다.

      Returns:
          tuple                   : url, 헤더, 바디 정보, 함수 이름, 반환 데이터 태그, 종목코드를 포함하는 튜플을 반환합니다.
      """

      _url_base   = "https://openapi.ebestsec.co.kr:8080"
      _path       = "stock/frgr-itt"
      _url        = f"{_url_base}/{_path}"

      _header     = {
          "content-type"  : "application/json; charset=UTF-8",
          "authorization" : None,                             # fill in RunTR()
          "tr_cd"         : "t1716",
          "tr_cont"       : "N",
          "tr_cont_key"   : "",
          "mac_address"   : ""
      }

      # 시작일자와 종료일자를 YYYYMMDD 형식으로 생성하기
      _seoul_timezone = pytz.timezone('Asia/Seoul')
      _seoul_dt       = datetime.now(_seoul_timezone)
      _todt           = _seoul_dt.strftime('%Y%m%d') if todt == "" else todt
      _todt_datetime = datetime.strptime(_todt, '%Y%m%d').astimezone(_seoul_timezone)
      _fromdt = (_todt_datetime - timedelta(period)).strftime("%Y%m%d")

      _body           = {
          "t1716InBlock" : {
              "shcode"    : shcode,                           # 종목코드
              "gubun"     : "1",                              # 0:일간순매수 1:기간내누적순매수
              "fromdt"    : _fromdt,                          # 시작일자 : YYYYMMDD (default : 종료일자로부터 1년 전)
              "todt"      : _todt,                            # 종료일자 : YYYYMMDD
              "prapp"     : 0,                                # 프로그램매매 감산 적용율 - %단위
              "prgubun"   : "0",                              # PR적용구분(0:적용안함1:적용)
              "orggubun"  : "1",                              # 기관적용(0:미적용 1:적용)
              "frggubun"  : "1"                               # 외인적용(0:미적용 1:적용)
          }
      }

      _out_block_tag = "OutBlock"

      return _url, _header, _body, t1716.__name__, _out_block_tag, shcode
  ```
  ```py
  if __name__ == "__main__":

      import pprint

      url, header, body, tr_name, out_block_tag, shcode_ = t1716()

      print("URL              :")
      pprint.pprint(url)
      print("\nheader           :")
      pprint.pprint(header)
      print("\nbody             :")
      pprint.pprint(body)
      print("\ntr name          :")
      pprint.pprint(tr_name)
      print("\nOutBlockTag      :")
      pprint.pprint(out_block_tag)
      print("\nshcode           :")
      pprint.pprint(shcode_)
  ```
  </details>
  <details open="">
    <summary>Output</summary>

  ```txt
  URL              :
  'https://openapi.ebestsec.co.kr:8080/stock/frgr-itt'

  header           :
  {'authorization': None,
  'content-type': 'application/json; charset=UTF-8',
  'mac_address': '',
  'tr_cd': 't1716',
  'tr_cont': 'N',
  'tr_cont_key': ''}

  body             :
  {'t1716InBlock': {'frggubun': '1',
                    'fromdt': '20220722',
                    'gubun': '1',
                    'orggubun': '1',
                    'prapp': 0,
                    'prgubun': '0',
                    'shcode': '005930',
                    'todt': '20230722'}}

  tr name          :
  't1716'

  OutBlockTag      :
  'OutBlock'

  shcode           :
  '005930'
  ```
  </details>


## [Oauth 2 (2023.07.21)](#list)

- Advanced from [Oauth (2023.07.11)](#oauth-20230711)

  <details>
    <summary>Codes : key.py (not uploaded)</summary>

  - Add comments
  ```python
  """
  eBest Open API / key
  2023.07.11

  이 파일은 eBest Open API를 사용하기 위해 필요한 애플리케이션 키와 비밀 키를 저장하는 파일입니다.
  애플리케이션 키는 API 호출에 필요한 인증을 위해 사용되며, 반드시 비밀로 유지되어야 합니다.
  따라서 이 파일은 외부에 노출되지 않도록 주의해야 합니다.
  """

  MOCK_KEY    = "{your app key}"
  MOCK_SECRET = "{your secret key}"
  ```
  </details>
  <details>
    <summary>Codes : oauth2.py</summary>

  ```py
  """
  eBest Open API / 접근토큰 발급 (token)
  2023.07.21

  이 코드는 eBest Open API 서버에 OAuth 토큰을 요청하는 함수를 포함한 코드입니다.
  OAuth 토큰은 API를 호출할 때 인증 정보로 사용되며, API 호출을 위해 반드시 필요합니다.

  사용 전 준비사항:
  1. eBest Open API 개발자 센터에서 앱 키와 시크릿 키를 발급받아야 합니다.
  2. key.py 파일에 발급받은 앱 키와 시크릿 키를 저장해야 합니다. (예: MOCK_KEY, MOCK_SECRET)

  개선사항:
  1. OAuth.py (2023.07.11)의 코드를 oauth()라는 함수로 재작성하였습니다.
  2. test 변수의 값(True/False)에 따라 return값이 달라집니다.
  """
  ```
  ```py
  import pprint
  import requests

  import key
  ```
  ```python
  def oauth(test = False):
      """
      eBest Open API 서버에 OAuth 토큰을 요청하는 함수입니다.

      Parameters:
          test (bool) : 테스트 모드 여부를 설정하는 매개변수입니다. 기본값은 False입니다.

      Returns:
          str         : 성공적으로 OAuth 토큰을 받아온 경우 해당 토큰을 반환합니다.

      Raises:
          requests.exceptions.RequestException : OAuth 요청 중 예외가 발생한 경우 예외를 발생시킵니다.
      """

      # 개발자가 발급받은 앱 키와 시크릿 키를 사용합니다.
      _app_key = key.MOCK_KEY
      _app_secret = key.MOCK_SECRET

      # OAuth 토큰을 요청할 API 경로를 설정합니다.
      _path = "oauth2/token"
      _url_base = "https://openapi.ebestsec.co.kr:8080"
      _url = f"{_url_base}/{_path}"

      # OAuth 요청에 필요한 헤더 정보를 설정합니다.
      _header = {
          "content-type": "application/x-www-form-urlencoded"
      }

      # OAuth 요청에 필요한 파라미터 정보를 설정합니다.
      _param = {
          "grant_type": "client_credentials",
          "appkey": _app_key,
          "appsecretkey": _app_secret,
          "scope": "oob"
      }

      # OAuth 요청을 실행하고 응답을 받아옵니다.
      try:
          _res = requests.post(_url, headers=_header, params=_param, timeout=1)
          _access_token = _res.json()["access_token"]
      except requests.exceptions.RequestException as _e:
          # OAuth 요청 중 예외가 발생한 경우 예외를 발생시킵니다.
          raise _e

      if test:
          return _url, _res, _access_token
      else:
          return _access_token
  ```
  ```py
  if __name__ == "__main__":
      # OAuth 함수를 호출하여 액세스 토큰을 받아옵니다.

      url, res, _ = oauth(test = True)
      print("URL      :", url, "\n")                          # OAuth 토큰 요청을 보낸 URL 출력
      print("OAuth    :")
      pprint.pprint(res.json())                               # OAuth 응답 내용 출력
  ```
  </details>
  <details open = "">
    <summary>Output</summary>

  ```txt
  URL      : https://openapi.ebestsec.co.kr:8080/oauth2/token

  OAuth    :
  {'access_token': '******',
  'expires_in': 50352,
  'scope': 'oob',
  'token_type': 'Bearer'}
  ```
  </details>


## [재무순위종합(t3341) (2023.07.14)](#list)

- [eBest OPEN API](https://openapi.ebestsec.co.kr) > [API 가이드 > 주식 > [주식] 투자정보](https://openapi.ebestsec.co.kr/apiservice#G_73142d9f-1983-48d2-8543-89b75535d34c#A_580d2770-a7a9-49e3-9ec1-49ed8bc734a2) > 재무순위종합


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
      "t3341InBlock"  : {
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
- References
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