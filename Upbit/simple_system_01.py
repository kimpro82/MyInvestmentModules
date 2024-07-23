"""
Upbit Auto Trader Version 0.1 / Author : kimpro82

이 프로그램은 Upbit의 REST API를 사용하여 다음 작업을 수행합니다:
- WebSocket을 이용하여 실시간 시세 데이터 조회
- 거래대금 1위 종목의 잔고가 계좌 평가 금액의 49% 미만일 경우, 50%에 미달하는 만큼 매수
- 거래대금 1위 종목이 아닌 종목의 잔고나 1위 종목의 평가 금액이 51%를 초과할 경우, 50%로부터 초과분만큼 매도
- 계좌 잔고 및 최근 거래내역을 콘솔에 출력하며, 매초 새로 고침
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
        while True:
            response = await websocket.recv()
            data = json.loads(response)
            print(data)  # 시세 정보 출력 (디버깅 목적)

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

async def trade_logic(session):
    """
    매수 및 매도 로직을 수행합니다.
    - 거래대금 1위 종목의 잔고 비율이 49% 미만일 경우 매수
    - 거래대금 1위 종목이 아닌 종목의 잔고나 1위 종목의 잔고 비율이 51%를 초과할 경우 매도
    
    Args:
        session (aiohttp.ClientSession): 비동기 HTTP 요청을 위한 세션
    """
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

async def print_console():
    """
    콘솔에 계좌 잔고와 최근 거래내역을 출력합니다.
    - 프로그램의 실행 시간과 경과 시간을 포맷하여 출력
    - 계좌의 잔고와 각 자산의 원화 환산 금액 출력
    - 최근 5건의 거래내역을 출력
    
    이 함수는 매초 갱신됩니다.
    """
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
        
        elapsed_time_formatted = f"{days:02d} {hours:02d}:{minutes:02d}:{seconds:02d}"

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
    """
    비동기적으로 주요 기능을 실행합니다.
    - WebSocket을 통해 시세 데이터를 조회
    - 콘솔에 계좌 잔고 및 최근 거래내역을 출력
    - 매수 및 매도 로직을 수행
    """
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(
            fetch_market_data(),
            print_console(),
            trade_logic(session)
        )

if __name__ == "__main__":
    asyncio.run(main())
