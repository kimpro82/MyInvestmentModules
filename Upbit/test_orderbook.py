"""
test_orderbook.py

2023.04.27
"""

import pprint
import requests

URL = "https://api.upbit.com/v1/orderbook"
params = {
    "markets": ["KRW-BTC"],
}
headers = {
    "accept": "application/json",
}
response = requests.get(URL, params=params, headers=headers, timeout=1)

# Test
if __name__ == "__main__" :
    pprint.pprint(response.json())
