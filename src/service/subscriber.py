import json
import websocket
from datetime import datetime

from src.repository.ohlc_repository import OhlcRepository
from src.parameters_usdt import assets, market
from src.service.klines_short import build_klines
from src.service.predictor import Predictor
from src.service.loader_ohlc import LoaderOHLC


class Subscriber:
    total: int = 0
    symbols_total: int = 0
    width: int
    interval: str
    model_path: str
    symbols: [str]
    socket: str = 'wss://stream.binance.com:9443/ws'

    repository: OhlcRepository
    predictor: Predictor
    loaderOHLC: LoaderOHLC

    def __init__(self, interval: str, model_path: str, width: int):
        self.width = width
        self.interval = interval
        self.model_path = model_path
        self.repository = OhlcRepository(-1)

    def subscribe(self):
        self.loaderOHLC = LoaderOHLC()
        self.loaderOHLC.flush()

        assets_real = self.loaderOHLC.load(
            assets=assets,
            market=market,
            end_at=datetime.utcnow(),
            interval=self.interval,
            width=self.width
        )

        self.symbols = [f'{x}{market}@kline_{self.interval}'.lower() for x in assets_real]
        self.symbols_total: int = len(self.symbols)

        self.predictor = Predictor(
            assets=assets_real,
            market=market,
            interval=self.interval,
            width=self.width,
            model_path=self.model_path
        )

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

                self.repository.create_many(
                    exchange='binance',
                    market=market,
                    interval=self.interval,
                    asset=asset,
                    collection=[item]
                )

                self.total = self.total + 1

                print(f'{asset} - {self.interval}')

                if self.total == self.symbols_total:
                    self.total = 0
                    self.predictor.predict()

    def on_error(self, ws, message):
        print("on_error")
        print(json.loads(message))

    def on_close(self, ws):
        print("on_close")
