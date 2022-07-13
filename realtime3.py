import json
import websocket

from src.parameters import assets_down, market
from src.parameters_usdt import assets, market
from src.parameters_btc import assets_btc, market_btc

from src.repository.ohlc_repository import OhlcRepository
from src.service.klines_short import build_klines

# https://github.com/binance-us/binance-official-api-docs/blob/master/web-socket-streams.md#klinecandlestick-streams


repository = OhlcRepository(-1)

interval = '3m'
socket = 'wss://stream.binance.com:9443/ws'
symbols = [f'{x}{market}@kline_{interval}'.lower() for x in assets]
# symbols_btc = [f'{x}{market_btc}@kline_{interval}'.lower() for x in assets_btc]
# symbols_down = [f'{x}{market}@kline_{interval}'.lower() for x in assets_down]

symbols_total = len(symbols)

print(symbols, symbols_total)
# print(symbols, symbols_btc, symbols_down, symbols_total)

collection = []


def on_open(ws):
    print("opened")
    subscribe_message = {
        "method": "SUBSCRIBE",
        "params": symbols,
        "id": 1
    }

    ws.send(json.dumps(subscribe_message))


def on_message(ws, message):
    m = json.loads(message)

    if 'k' in m:
        k = m['k']
        symbol = m['s']
        is_closed = k['x']
        asset = symbol.replace(market, '')

        if is_closed:
            item = build_klines(k=k)

            collection.append(item)

        if len(collection) == symbols_total:
            repository.create_many(
                exchange='binance',
                market=market,
                interval=interval,
                asset=asset,
                collection=collection
            )
            print('timeframe added ...')
            collection.clear()


def on_error(ws, message):
    print("on_error")
    print(json.loads(message))


def on_close(ws):
    print("on_close")


ws = websocket.WebSocketApp(
    url=socket,
    on_open=on_open,
    on_message=on_message,
    on_close=on_close,
    on_error=on_error
)

ws.run_forever()
