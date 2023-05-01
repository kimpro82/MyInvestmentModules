"""
test_candle_minute.py

2023.04.27
"""

import pprint
import requests

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

# Test
if __name__ == "__main__" :
    pprint.pprint(response.json())
