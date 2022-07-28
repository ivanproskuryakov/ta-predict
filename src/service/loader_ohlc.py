import pandas as pd

from binance import enums
from datetime import datetime, timedelta

from src.service.klines import KLines
from src.repository.ohlc_repository import OhlcRepository
from src.entity.ohlc import Ohlc
from src.connector.db_connector import db_connect


class LoaderOHLC:
    repository: OhlcRepository
    exchange: str = 'binance'

    assets: [str]
    market: str

    def __init__(self,
                 assets: [str],
                 market: str,
                 ):
        self.assets = assets
        self.market = market

        self.repository = OhlcRepository(start_at=-1)

    def flush(self):
        engine = db_connect()

        Ohlc.metadata.drop_all(bind=engine)
        Ohlc.metadata.create_all(bind=engine)

    def load(self, end_at: datetime, interval: str, width: int) -> [pd.DataFrame, pd.DataFrame]:
        multiplier = int(interval[:-1])

        frames = width * multiplier

        print(width)
        print(frames)
        print(multiplier)
        print(end_at)

        start_at = end_at - timedelta(minutes=frames)

        # ---------------

        repository = OhlcRepository(-1)
        klines = KLines()

        exchange = 'binance'
        groups = [
            {
                "market": self.market,
                "assets": self.assets,
                "type": enums.HistoricalKlinesType.SPOT
            },
        ]

        for group in groups:
            for asset in group["assets"]:
                print(f'processing: {asset} {group["market"]} {interval}')

                collection = klines.build_klines(
                    market=group["market"],
                    asset=asset,
                    klines_type=group["type"],
                    interval=interval,
                    start_at=start_at.timestamp(),
                    end_at=end_at.timestamp(),
                )

                print(asset)
                print(len(collection))

                repository.create_many(
                    exchange,
                    group["market"],
                    asset,
                    interval,
                    collection
                )
