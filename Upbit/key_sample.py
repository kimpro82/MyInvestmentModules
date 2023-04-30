"""
key.py

2023.04.27

It contains ACCESS_KEY and SECRET_KEY for using Upbit API.
Keep this file in secret.
"""

import os

ACCESS_KEY = '{ACCESS_KEY}'
SECRET_KEY = '{SECRET_KEY}}'

os.environ['UPBIT_ACCESS_KEY'] = ACCESS_KEY
os.environ['UPBIT_SECRET_KEY'] = SECRET_KEY
