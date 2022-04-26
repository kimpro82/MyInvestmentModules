import mojito
import pprint
import Key

# print(mojito.__version__)                                         # test : ok

key = Key.key
secret = Key.secret

broker = mojito.KoreaInvestment(api_key=key, api_secret=secret)
resp = broker.fetch_price("005930")
pprint.pprint(resp)                                                 # success