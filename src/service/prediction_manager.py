from binance import Client

from src.repository.prediction_repository import PredictionRepository
from src.service.klines import KLines
from src.parameters import exchange, assets, market


class PredictionManager:
    connection = None
    klines = None

    def __init__(self):
        self.repository = PredictionRepository()
        self.klines = KLines()

    def fetch_populate(self):
        interval = Client.KLINE_INTERVAL_1MINUTE
        start_at = '1 minute ago UTC'

        for asset in assets:
            collection = self.klines.build_klines(
                market,
                asset,
                interval,
                start_at
            )

            total = len(collection)
            data = collection[total - 1]

            self.find_or_create(asset, interval, data)

    def find_or_create(self, asset: str, interval: str, data):
        prediction = self.repository.find(
            exchange=exchange,
            market=market,
            asset=asset,
            interval=interval,
            time_open=data['time_open']
        )

        if not prediction:
            self.repository.create(
                exchange=exchange,
                market=market,
                asset=asset,
                interval=interval,
                data=data
            )
