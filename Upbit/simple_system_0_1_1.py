"""
Upbit Auto Trader Version 0.1.1 / Author : kimpro82
2024.07.25

[설명]
이 모듈은 Upbit의 REST API 및 WebSocket을 사용하여 자동으로 암호화폐 매매를 수행하는 프로그램입니다.
- 실시간 시세 데이터를 WebSocket을 통해 조회
- 계좌 잔고 및 최근 거래내역을 콘솔에 출력
- (테스트용) 매수 및 매도 로직을 정의하여 거래를 자동으로 실행

[히스토리]
- 0.1   2024.07.23 Init.
- 0.1.1 2024.07.25 Refactoring : 함수 분할 및 계층화

[함수 계층 구조]
main
│
├── generate_jwt_token
│
├── fetch_market_data
├── fetch_top_traded_ticker
├── fetch_balances
├── fetch_orders
│
├── buy_order
├── sell_order
├── trade_logic
│   ├── calculate_top_ticker_balance
│   ├── perform_buy_logic
│   └── perform_sell_logic
│
└── print_console
    ├── format_elapsed_time
    ├── generate_console_output
    ├── generate_balances_output
    └── generate_orders_output
"""

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
    """
    Upbit API를 호출하기 위한 JWT 토큰을 생성합니다.
    
    Returns:
        str: 인증을 위한 JWT 토큰 문자열 (Bearer 타입)
    """
    payload = {
        'access_key': UPBIT_ACCESS_KEY,
        'nonce': str(uuid.uuid4()),
    }
    token = jwt.encode(payload, UPBIT_SECRET_KEY, algorithm='HS256')
    return f"Bearer {token}"

async def fetch_market_data():
    """
    WebSocket을 통해 실시간으로 시세 데이터를 받아옵니다.
    
    주의: 현재 시세 데이터는 디버깅 목적으로만 출력됩니다.
    """
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri) as websocket:
        subscribe_message = [{
            "ticket": "test",
            "type": "ticker",
            "codes": ["KRW-BTC", "KRW-ETH", "KRW-XRP"],
            "isOnlyRealtime": True
        }]
        await websocket.send(json.dumps(subscribe_message))

async def fetch_top_traded_ticker(session):
    """
    거래대금 1위 종목을 조회합니다.
    
    Args:
        session (aiohttp.ClientSession): 비동기 HTTP 요청을 위한 세션
    
    Returns:
        dict: 거래대금 1위 종목의 시세 정보를 담고 있는 JSON 응답
    """
    url = f"{BASE_URL}/ticker?markets=KRW-BTC,KRW-ETH,KRW-XRP"
    async with session.get(url) as response:
        data = await response.json()
        return max(data, key=lambda x: x['acc_trade_price_24h'])

async def fetch_balances(session):
    """
    현재 계좌의 잔고 정보를 조회합니다.
    
    Args:
        session (aiohttp.ClientSession): 비동기 HTTP 요청을 위한 세션
    
    Returns:
        list: 계좌의 잔고 정보를 담고 있는 JSON 응답
    """
    url = f"{BASE_URL}/accounts"
    headers = {
        "Authorization": generate_jwt_token()
    }
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def fetch_orders(session):
    """
    현재 계좌의 최근 거래내역을 조회합니다.
    
    Args:
        session (aiohttp.ClientSession): 비동기 HTTP 요청을 위한 세션
    
    Returns:
        list: 최근 거래내역을 담고 있는 JSON 응답
    """
    url = f"{BASE_URL}/orders"
    headers = {
        "Authorization": generate_jwt_token()
    }
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def buy_order(session, market, price, volume):
    """
    지정된 시장에 매수 주문을 수행합니다.
    
    Args:
        session (aiohttp.ClientSession): 비동기 HTTP 요청을 위한 세션
        market (str): 매수할 시장 코드
        price (float): 주문 가격
        volume (float): 주문 수량
    
    Returns:
        dict: 매수 주문의 결과를 담고 있는 JSON 응답
    """
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
    """
    지정된 시장에 매도 주문을 수행합니다.
    
    Args:
        session (aiohttp.ClientSession): 비동기 HTTP 요청을 위한 세션
        market (str): 매도할 시장 코드
        price (float): 주문 가격
        volume (float): 주문 수량
    
    Returns:
        dict: 매도 주문의 결과를 담고 있는 JSON 응답
    """
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

async def trade_logic(session):
    """
    매수 및 매도 로직을 수행합니다.
    - 거래대금 1위 종목의 잔고 비율이 49% 미만일 경우 매수
    - 거래대금 1위 종목이 아닌 종목의 잔고나 1위 종목의 잔고 비율이 51%를 초과할 경우 매도
    
    Args:
        session (aiohttp.ClientSession): 비동기 HTTP 요청을 위한 세션
    """

    async def calculate_top_ticker_balance(balances, top_ticker):
        """
        거래대금 1위 종목의 잔고 비율을 계산합니다.
        
        Args:
            balances (list): 계좌 잔고 정보
            top_ticker (dict): 거래대금 1위 종목의 시세 정보
        
        Returns:
            tuple: 총 원화 잔고, 거래대금 1위 종목의 잔고 가치, 거래대금 1위 종목의 잔고 비율
        """
        total_balance_krw = sum(
            float(balance['balance']) * float(balance['avg_buy_price']) if balance['currency'] != 'KRW' else float(balance['balance'])
            for balance in balances
        )
        top_ticker_balance = next(
            (balance for balance in balances if balance['currency'] == top_ticker['market'].split('-')[1]), None
        )
        if top_ticker_balance:
            top_ticker_balance_value = float(top_ticker_balance['balance']) * float(top_ticker['trade_price'])
            top_ticker_ratio = top_ticker_balance_value / total_balance_krw
        else:
            top_ticker_balance_value = 0
            top_ticker_ratio = 0

        return total_balance_krw, top_ticker_balance_value, top_ticker_ratio

    async def perform_buy_logic(top_ticker, total_balance_krw, top_ticker_balance_value, top_ticker_ratio):
        """
        매수 로직을 수행합니다.
        
        Args:
            top_ticker (dict): 거래대금 1위 종목의 시세 정보
            total_balance_krw (float): 총 원화 잔고
            top_ticker_balance_value (float): 거래대금 1위 종목의 잔고 가치
            top_ticker_ratio (float): 거래대금 1위 종목의 잔고 비율
        """
        if top_ticker_ratio < 0.49:
            buy_amount_krw = total_balance_krw * 0.50 - top_ticker_balance_value
            buy_price = float(top_ticker['trade_price'])
            buy_volume = buy_amount_krw / buy_price
            await buy_order(session, top_ticker['market'], buy_price, buy_volume)

    async def perform_sell_logic(balances, top_ticker, total_balance_krw, top_ticker_ratio):
        """
        매도 로직을 수행합니다.
        
        Args:
            balances (list): 계좌 잔고 정보
            top_ticker (dict): 거래대금 1위 종목의 시세 정보
            total_balance_krw (float): 총 원화 잔고
            top_ticker_ratio (float): 거래대금 1위 종목의 잔고 비율
        """
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

    balances = await fetch_balances(session)
    top_ticker = await fetch_top_traded_ticker(session)
    total_balance_krw, top_ticker_balance_value, top_ticker_ratio = await calculate_top_ticker_balance(balances, top_ticker)
    await perform_buy_logic(top_ticker, total_balance_krw, top_ticker_balance_value, top_ticker_ratio)
    await perform_sell_logic(balances, top_ticker, total_balance_krw, top_ticker_ratio)

async def print_console():
    """
    콘솔에 잔고 및 거래내역을 실시간으로 출력합니다.
    - 프로그램 실행 시간 및 경과 시간
    - 현재 계좌 잔고
    - 가장 최근 거래내역 5건
    
    주의: 이 함수는 무한 루프를 통해 주기적으로 콘솔을 업데이트합니다.
    """
    start_time = datetime.now()

    def format_elapsed_time(elapsed_time):
        """
        경과 시간을 포맷팅합니다.
        
        Args:
            elapsed_time (datetime.timedelta): 경과 시간
        
        Returns:
            str: 포맷팅된 경과 시간 문자열
        """
        total_seconds = int(elapsed_time.total_seconds())
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{days:02d} {hours:02d}:{minutes:02d}:{seconds:02d}"

    def generate_console_output(start_time, elapsed_time_formatted, current_time_str):
        """
        콘솔에 출력할 기본 정보를 생성합니다.
        
        Args:
            start_time (datetime): 프로그램 시작 시간
            elapsed_time_formatted (str): 포맷팅된 경과 시간 문자열
            current_time_str (str): 현재 시간 문자열
        
        Returns:
            list: 콘솔에 출력할 정보 리스트
        """
        return [
            "Upbit Auto Trader Version 0.1.1 / Author : kimpro82\n\n",
            f"프로그램 실행 시작 시간 : {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"실행 후  경과 시간      : {elapsed_time_formatted}\n",
            f"현재화면 출력 시간      : {current_time_str}\n",
        ]

    def generate_balances_output(balances):
        """
        잔고 정보를 포맷팅하여 출력합니다.
        
        Args:
            balances (list): 계좌 잔고 정보
        
        Returns:
            str: 포맷팅된 잔고 정보 문자열
        """
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
        """
        최근 거래내역을 포맷팅하여 출력합니다.
        
        Args:
            orders (list): 최근 거래내역
        
        Returns:
            str: 포맷팅된 거래내역 문자열
        """
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

        sys.stdout.write("\033c")  # 콘솔 화면 지우기
        sys.stdout.write(''.join(output))
        sys.stdout.flush()

        await asyncio.sleep(1)  # 1초마다 업데이트

async def main():
    """
    비동기적으로 프로그램의 주요 작업을 실행합니다.
    - 실시간 시세 데이터 조회
    - 매매 로직 수행
    - 콘솔 출력
    """
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(fetch_market_data()),
            asyncio.create_task(trade_logic(session)),
            asyncio.create_task(print_console())
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
