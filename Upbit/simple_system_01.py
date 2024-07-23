"""
Upbit Auto Trader Version 0.1 / Author : kimpro82

This program interacts with Upbit's REST API to:
- Fetch market data in real-time using WebSockets
- Place buy orders if the top-traded asset's balance is below 49% of the account's evaluation
- Place sell orders for non-top-traded assets or if the top-traded asset's balance exceeds 51%
- Display account balances and recent orders on the console, refreshing every second
"""

import asyncio
import aiohttp
import websockets
import json
import time
import sys
from datetime import datetime
from key import UPBIT_ACCESS_KEY, UPBIT_SECRET_KEY
import jwt  # PyJWT
import uuid

BASE_URL = "https://api.upbit.com/v1"

# JWT 토큰 생성 함수
def generate_jwt_token():
    payload = {
        'access_key': UPBIT_ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
    }
    token = jwt.encode(payload, UPBIT_SECRET_KEY, algorithm='HS256')
    return f"Bearer {token}"

# 비동기 시세 조회 함수 (WebSocket 이용)
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
            print(data)  # 시세 정보 출력 (디버깅 목적)

# 비동기 매수 함수
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

# 비동기 매도 함수
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

# 비동기 잔고 조회 함수
async def fetch_balances(session):
    url = f"{BASE_URL}/accounts"
    headers = {
        "Authorization": generate_jwt_token()
    }
    async with session.get(url, headers=headers) as response:
        return await response.json()

# 비동기 체결 조회 함수
async def fetch_orders(session):
    url = f"{BASE_URL}/orders"
    headers = {
        "Authorization": generate_jwt_token()
    }
    async with session.get(url, headers=headers) as response:
        return await response.json()

# 비동기 거래대금 1위 종목 조회 함수
async def fetch_top_traded_ticker(session):
    url = f"{BASE_URL}/ticker?markets=KRW-BTC,KRW-ETH,KRW-XRP"
    async with session.get(url) as response:
        data = await response.json()
        return max(data, key=lambda x: x['acc_trade_price_24h'])

# 매수/매도 조건 함수
async def trade_logic(session):
    balances = await fetch_balances(session)
    top_ticker = await fetch_top_traded_ticker(session)
    total_balance_krw = sum(float(balance['balance']) * float(balance['avg_buy_price']) if balance['currency'] != 'KRW' else float(balance['balance']) for balance in balances)
    top_ticker_balance = next((balance for balance in balances if balance['currency'] == top_ticker['market'].split('-')[1]), None)
    
    if top_ticker_balance:
        top_ticker_balance_value = float(top_ticker_balance['balance']) * float(top_ticker['trade_price'])
        top_ticker_ratio = top_ticker_balance_value / total_balance_krw
    else:
        top_ticker_balance_value = 0
        top_ticker_ratio = 0

    # 매수 조건: 거래대금 1위 종목 잔고가 계좌 평가금액의 49% 미만이라면 50%에서 모자라는 만큼 매수
    if top_ticker_ratio < 0.49:
        buy_amount_krw = total_balance_krw * 0.50 - top_ticker_balance_value
        buy_price = float(top_ticker['trade_price'])
        buy_volume = buy_amount_krw / buy_price
        await buy_order(session, top_ticker['market'], buy_price, buy_volume)

    # 매도 조건: 거래대금 1위 종목이 아닌 종목의 잔고나, 1위 종목의 계좌 내 평가금액이 51%를 초과할 경우 50%로부터의 초과분만큼 매도
    for balance in balances:
        if balance['currency'] == 'KRW':
            continue
        ticker = f"KRW-{balance['currency']}"
        if ticker != top_ticker['market']:
            await sell_order(session, ticker, float(balance['avg_buy_price']), float(balance['balance']))
        elif top_ticker_ratio > 0.51:
            sell_amount_krw = top_ticker_balance_value - total_balance_krw * 0.50
            sell_volume = sell_amount_krw / float(top_ticker['trade_price'])
            await sell_order(session, top_ticker['market'], float(top_ticker['trade_price']), sell_volume)

# 콘솔 출력 함수
async def print_console():
    start_time = datetime.now()
    while True:
        current_time = datetime.now()
        elapsed_time = current_time - start_time

        # 전체 초를 구하고, 이를 DD-HH-MM-SS 형식으로 변환
        total_seconds = int(elapsed_time.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        elapsed_time_formatted = f"{days:02d}-{hours:02d}-{minutes:02d}-{seconds:02d}"

        # current_time을 초 단위로 변환하고, 소수점 둘째 자리까지 반올림
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

        output = [
            f"Upbit Auto Trader Version 0.1 / Author : kimpro82\n\n",
            f"프로그램 실행 시작 시간 : {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"실행 후  경과 시간      : {elapsed_time_formatted}\n",
            f"현재화면 출력 시간      : {current_time_str}\n",
        ]

        async with aiohttp.ClientSession() as session:
            balances = await fetch_balances(session)
            orders = await fetch_orders(session)
        
        # 잔고 및 원화 환산 금액 출력
        output.append("\n[잔고 데이터]\n")
        
        for balance in balances:
            if isinstance(balance, dict) and 'currency' in balance and 'balance' in balance:
                currency = f"{balance['currency']:<6}"  # 여섯 칸으로 통일
                amount = f"{float(balance['balance']):14,.2f}"  # 14자리, 세 자리마다 쉼표, 소수점 두 자리
                
                # avg_buy_price와 unit_currency를 이용해 원화 환산 금액 계산
                avg_buy_price = float(balance.get('avg_buy_price', 0))
                unit_currency = balance['unit_currency']
                won_value = float(balance['balance']) * avg_buy_price
                won_value_formatted = f"{won_value:14,.2f}"  # 14자리, 세 자리마다 쉼표, 소수점 두 자리

                if currency == "KRW   ":
                    output.append(f"{currency} : {amount} ({unit_currency} {amount})\n")
                else:
                    output.append(f"{currency} : {amount} ({unit_currency} {won_value_formatted})\n")
            else:
                output.append(f"Unexpected data format in balance: {balance}\n")

        output.append("\n[가장 최근 거래내역 5건]\n")
        if isinstance(orders, list):
            recent_orders = orders[:5]
            for order in recent_orders:
                if isinstance(order, dict) and 'market' in order and 'side' in order and 'price' in order and 'volume' in order:
                    output.append(f"{order['market']} - {order['side']} - {order['price']} - {order['volume']}\n")
                else:
                    output.append(f"Unexpected data format in order: {order}\n")
        else:
            output.append(f"Unexpected data format in orders: {orders}\n")

        sys.stdout.write("\033c")  # Clear the console
        sys.stdout.write(''.join(output))
        sys.stdout.flush()

        await asyncio.sleep(1)

async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            fetch_market_data(),
            print_console(),
            trade_logic(session)
        )

if __name__ == "__main__":
    asyncio.run(main())
