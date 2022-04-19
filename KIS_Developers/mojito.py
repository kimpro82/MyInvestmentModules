import mojito
import pprint
import Key

key = Key.key
secret = Key.secret

broker = mojito.KoreaInvestment(api_key=key, api_secret=secret)
resp = broker.fetch_price("J", "005930")
pprint.pprint(resp)