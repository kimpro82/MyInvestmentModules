import asyncio
import json
import sys
import uuid
from datetime import datetime
import aiohttp
import websockets
from key import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY
import jwt  # PyJWT

BASE_URL = "https://api.upbit.com/v1"

def generate_jwt_token():
    payload = {
        'access_key': UPBIT_ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
    }
    token = jwt.encode(payload, UPBIT_SECRET_KEY, algorithm='HS256')
    return f"Bearer {token}"

async def fetch_market_data():
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri) as websocket:
        subscribe_message = [{
            "ticket": "test",
            "type": "ticker",
            "codes": ["KRW-BTC", "KRW-ETH", "KRW-XRP"],
            "isOnlyRealtime": True
        }]
        await websocket.send(json.dumps(subscribe_message))
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(data)

async def buy_order(session, market, price, volume):
    url = f"{BASE_URL}/orders"
    headers = {
        "Authorization": generate_jwt_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "market": market,
        "side": "bid",
        "price": str(price),
        "volume": str(volume),
        "ord_type": "limit"
    }
    async with session.post(url, headers=headers, json=payload) as response:
        return await response.json()

async def sell_order(session, market, price, volume):
    url = f"{BASE_URL}/orders"
    headers = {
        "Authorization": generate_jwt_token(),
        "Content-Type": "application/json"
    }
    payload = {
        "market": market,
        "side": "ask",
        "price": str(price),
        "volume": str(volume),
        "ord_type": "limit"
    }
    async with session.post(url, headers=headers, json=payload) as response:
        return await response.json()

async def fetch_balances(session):
    url = f"{BASE_URL}/accounts"
    headers = {
        "Authorization": generate_jwt_token()
    }
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def fetch_orders(session):
    url = f"{BASE_URL}/orders"
    headers = {
        "Authorization": generate_jwt_token()
    }
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def fetch_top_traded_ticker(session):
    url = f"{BASE_URL}/ticker?markets=KRW-BTC,KRW-ETH,KRW-XRP"
    async with session.get(url) as response:
        data = await response.json()
        return max(data, key=lambda x: x['acc_trade_price_24h'])

async def calculate_top_ticker_balance(balances, top_ticker):
    total_balance_krw = sum(
        float(balance['balance']) * float(balance['avg_buy_price']) if balance['currency'] != 'KRW' else float(balance['balance'])
        for balance in balances
    )
    top_ticker_balance = next(
        (balance for balance in balances if balance['currency'] == top_ticker['market'].split('-')[1]), 
        None
    )
    if top_ticker_balance:
        top_ticker_balance_value = float(top_ticker_balance['balance']) * float(top_ticker['trade_price'])
        top_ticker_ratio = top_ticker_balance_value / total_balance_krw
    else:
        top_ticker_balance_value = 0
        top_ticker_ratio = 0

    return total_balance_krw, top_ticker_balance_value, top_ticker_ratio

async def perform_buy_logic(session, top_ticker, total_balance_krw, top_ticker_balance_value, top_ticker_ratio):
    if top_ticker_ratio < 0.49:
        buy_amount_krw = total_balance_krw * 0.50 - top_ticker_balance_value
        buy_price = float(top_ticker['trade_price'])
        buy_volume = buy_amount_krw / buy_price
        await buy_order(session, top_ticker['market'], buy_price, buy_volume)

async def perform_sell_logic(session, balances, top_ticker, total_balance_krw, top_ticker_ratio):
    for balance in balances:
        if balance['currency'] == 'KRW':
            continue
        ticker = f"KRW-{balance['currency']}"
        if ticker != top_ticker['market']:
            await sell_order(session, ticker, float(balance['avg_buy_price']), float(balance['balance']))
        elif top_ticker_ratio > 0.51:
            sell_amount_krw = (top_ticker_ratio - 0.50) * total_balance_krw
            sell_volume = sell_amount_krw / float(top_ticker['trade_price'])
            await sell_order(session, top_ticker['market'], float(top_ticker['trade_price']), sell_volume)

async def trade_logic(session):
    balances = await fetch_balances(session)
    top_ticker = await fetch_top_traded_ticker(session)
    total_balance_krw, top_ticker_balance_value, top_ticker_ratio = await calculate_top_ticker_balance(balances, top_ticker)
    await perform_buy_logic(session, top_ticker, total_balance_krw, top_ticker_balance_value, top_ticker_ratio)
    await perform_sell_logic(session, balances, top_ticker, total_balance_krw, top_ticker_ratio)

async def print_console():
    start_time = datetime.now()
    while True:
        current_time = datetime.now()
        elapsed_time = current_time - start_time
        elapsed_time_formatted = format_elapsed_time(elapsed_time)
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

        output = generate_console_output(start_time, elapsed_time_formatted, current_time_str)

        async with aiohttp.ClientSession() as session:
            balances = await fetch_balances(session)
            orders = await fetch_orders(session)

        output.append(generate_balances_output(balances))
        output.append(generate_orders_output(orders))

        sys.stdout.write("\033c")  # Clear the console
        sys.stdout.write(''.join(output))
        sys.stdout.flush()

        await asyncio.sleep(1)

def format_elapsed_time(elapsed_time):
    total_seconds = int(elapsed_time.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{days:02d} {hours:02d}:{minutes:02d}:{seconds:02d}"

def generate_console_output(start_time, elapsed_time_formatted, current_time_str):
    return [
        "Upbit Auto Trader Version 0.1 / Author : kimpro82\n\n",
        f"프로그램 실행 시작 시간 : {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n",
        f"실행 후  경과 시간      : {elapsed_time_formatted}\n",
        f"현재화면 출력 시간      : {current_time_str}\n",
    ]

def generate_balances_output(balances):
    output = ["\n[잔고 데이터]\n"]
    for balance in balances:
        if isinstance(balance, dict) and 'currency' in balance and 'balance' in balance:
            currency = f"{balance['currency']:<6}"
            amount = f"{float(balance['balance']):14,.2f}"
            avg_buy_price = float(balance.get('avg_buy_price', 0))
            unit_currency = balance['unit_currency']
            won_value = float(balance['balance']) * avg_buy_price
            won_value_formatted = f"{won_value:14,.2f}"

            if currency == "KRW   ":
                output.append(f"{currency} : {amount} ({unit_currency} {amount})\n")
            else:
                output.append(f"{currency} : {amount} ({unit_currency} {won_value_formatted})\n")
        else:
            output.append(f"Unexpected data format in balance: {balance}\n")
    return ''.join(output)

def generate_orders_output(orders):
    output = ["\n[가장 최근 거래내역 5건]\n"]
    if isinstance(orders, list):
        recent_orders = orders[:5]
        for order in recent_orders:
            if isinstance(order, dict) and 'market' in order and 'side' in order and 'price' in order and 'volume' in order:
                output.append(f"{order['market']} - {order['side']} - {order['price']} - {order['volume']}\n")
            else:
                output.append(f"Unexpected data format in order: {order}\n")
    else:
        output.append(f"Unexpected data format in orders: {orders}\n")
    return ''.join(output)

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            fetch_market_data(),
            print_console(),
            trade_logic(session)
        )

if __name__ == "__main__":
    asyncio.run(main())
