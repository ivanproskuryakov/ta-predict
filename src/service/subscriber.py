import json
import websocket

from src.repository.ohlc_repository import OhlcRepository
from src.parameters_usdt import assets, market
from src.service.klines_short import build_klines


class Subscriber:
    interval: str
    socket: str = 'wss://stream.binance.com:9443/ws'
    repository: OhlcRepository
    collection = []

    def __init__(self, interval: str):
        self.interval = interval
        self.symbols = [f'{x}{market}@kline_{interval}'.lower() for x in assets]
        self.symbols_total: int = len(self.symbols)
        self.repository = OhlcRepository(-1)

        print(self.symbols, self.symbols_total)

    def run(self):
        ws = websocket.WebSocketApp(
            url=self.socket,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error
        )

        ws.run_forever()

    def on_open(self, ws):
        print("opened")
        subscribe_message = {
            "method": "SUBSCRIBE",
            "params": self.symbols,
            "id": 1
        }

        ws.send(json.dumps(subscribe_message))

    def on_message(self, ws, message):
        m = json.loads(message)

        if 'k' in m:
            k = m['k']
            symbol = m['s']
            is_closed = k['x']
            asset = symbol.replace(market, '')

            if is_closed:
                item = build_klines(k=k)

                self.collection.append(item)

            if len(self.collection) == self.symbols_total:
                self.repository.create_many(
                    exchange='binance',
                    market=market,
                    interval=self.interval,
                    asset=asset,
                    collection=self.collection
                )

                print('timeframe added ...', len(self.collection))
                self.collection.clear()

    def on_error(self, ws, message):
        print("on_error")
        print(json.loads(message))

    def on_close(self, ws):
        print("on_close")
