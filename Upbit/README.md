# My `Upbit Open API` Application Modules

### \<Reference>
- [Documentation] 업비트 개발자 센터 ☞ https://docs.upbit.com/
- [Github] sharebook-kr/pyupbit ☞ https://github.com/sharebook-kr/pyupbit
- [Wikidocs] 암호화폐 자동매매를 위한 파이썬과 CCXT ☞ https://wikidocs.net/book/8616

### \<List>
- [Init. (2022.04.27)](#init-20220427)


## [Init. (2022.04.27)](#list)

- Practices to get balance, ticker, candle data(minute) and orderbook by *Upbit Open API*
- Use the original API code, not `pyupbit`

  <details>
      <summary>Codes : key_sample.py</summary>

  ```python
  import os
  ```
  ```python
  ACCESS_KEY = '{ACCESS_KEY}'
  SECRET_KEY = '{SECRET_KEY}}'

  os.environ['UPBIT_ACCESS_KEY'] = ACCESS_KEY
  os.environ['UPBIT_SECRET_KEY'] = SECRET_KEY
  ```

  But I'm not entirely convinced that this is the correct way to use `os.environ`.
  </details>

  <details>
      <summary>Codes : test_balance.py</summary>

  ```python
  import os
  import uuid
  import pprint
  import jwt
  import requests

  import key                                                  # Don't remove it
  ```
  ```python
  ACCESS_KEY = os.environ['UPBIT_ACCESS_KEY']
  SECRET_KEY = os.environ['UPBIT_SECRET_KEY']
  SERVER_URL = "https://api.upbit.com"

  payload = {
      'access_key': ACCESS_KEY,
      'nonce': str(uuid.uuid4()),
  }

  jwt_token = jwt.encode(payload, SECRET_KEY)
  authorization_token = f'Bearer {jwt_token}'
  headers = {
    'Authorization': authorization_token,
  }
  ```
  ```python
  # Test
  if __name__ == "__main__" :
      # print(authorization_token[:10])                       # Ok

      res = requests.get(SERVER_URL + '/v1/accounts', "", headers=headers, timeout=1)
      pprint.pprint(res.json())
  ```

  ### Output
  ```
  [{'avg_buy_price': '0',
    'avg_buy_price_modified': True,
    'balance': '49323.31567256',
    'currency': 'KRW',
    'locked': '0',
    'unit_currency': 'KRW'},
    ……
  ```
  </details>
  <details>
    <summary>Codes : test_ticker.py</summary>

  ```python
  import pprint
  import requests
  ```
  ```python
  URL = "https://api.upbit.com/v1/ticker"
  params = {
      "markets": ["KRW-BTC"],
  }
  headers = {
      "accept": "application/json",
  }
  response = requests.get(URL, params=params, headers=headers, timeout=1)
  ```
  ```python
  # Test
  if __name__ == "__main__" :
      pprint.pprint(response.json())
  ```

  ### Output
  ```
  [{'acc_trade_price': 53770743984.69168,
    'acc_trade_price_24h': 69094458373.3278,
    'acc_trade_volume': 1378.10136839,
    'acc_trade_volume_24h': 1771.01848943,
    'change': 'RISE',
    ……
  ```
  </details>
  <details>
      <summary>Codes : test_orderbook.py</summary>

  ```python
  import pprint
  import requests
  ```
  ```python
  URL = "https://api.upbit.com/v1/orderbook"
  params = {
      "markets": ["KRW-BTC"],
  }
  headers = {
      "accept": "application/json",
  }
  response = requests.get(URL, params=params, headers=headers, timeout=1)
  ```
  ```python
  # Test
  if __name__ == "__main__" :
      pprint.pprint(response.json())
  ```

  ### Output
  ```
  [{'market': 'KRW-BTC',
    'orderbook_units': [{'ask_price': 39106000.0,
                        'ask_size': 0.05116399,
                        'bid_price': 39079000.0,
                        'bid_size': 0.06953873},
                        ……
    'timestamp': 1682865310319,
    'total_ask_size': 2.5738719399999996,
    'total_bid_size': 5.978590620000001}]
  ```
  </details>
  <details>
      <summary>Codes : test_candle_minute.py</summary>

  ```python
  import pprint
  import requests
  ```
  ```python
  UNIT = "1"
  URL = "https://api.upbit.com/v1/candles/minutes/" + UNIT
  params = {
      "market": "KRW-BTC",
      "to" : "",
      "count" : "10",                                         # max = 200
  }
  headers = {
      "accept": "application/json",
  }
  response = requests.get(URL, params=params, headers=headers, timeout=1)
  ```
  ```python
  # Test
  if __name__ == "__main__" :
      pprint.pprint(response.json())
  ```

  ### Output
  ```
  [{'candle_acc_trade_price': 12754252.90366,
    'candle_acc_trade_volume': 0.32614408,
    'candle_date_time_kst': '2023-04-30T23:33:00',
    'candle_date_time_utc': '2023-04-30T14:33:00',
    'high_price': 39107000.0,
    'low_price': 39090000.0,
    'market': 'KRW-BTC',
    'opening_price': 39090000.0,
    'timestamp': 1682865216635,
    'trade_price': 39107000.0,
    'unit': 1},
  ……
  ```
  </details>
