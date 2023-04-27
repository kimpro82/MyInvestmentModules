"""
test_balance.py

2023.04.27
"""

import os
import uuid
import pprint
import jwt
import requests

import key                                                  # Don't remove it

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

# Test
if __name__ == "__main__" :
    # print(authorization_token[:10])                       # Ok

    res = requests.get(SERVER_URL + '/v1/accounts', "", headers=headers, timeout=1)
    pprint.pprint(res.json())
