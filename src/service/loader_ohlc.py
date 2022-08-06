import concurrent.futures

from binance import enums
from datetime import datetime, timedelta

from src.service.klines import KLines
from src.repository.ohlc_repository import OhlcRepository
from src.entity.ohlc import Ohlc
from src.connector.db_connector import db_connect


class LoaderOHLC:
    repository: OhlcRepository
    exchange: str = 'binance'

    def __init__(self, ):
        self.repository = OhlcRepository(start_at=-1)

    def flush(self):
        engine = db_connect()

        Ohlc.metadata.drop_all(bind=engine)
        Ohlc.metadata.create_all(bind=engine)

    def load(self,
             assets: [str],
             market: str,
             end_at: datetime,
             interval: str,
             width: int
             ) -> [str]:
        multiplier = int(interval[:-1])
        frames = width * multiplier
        futures = []
        assets_real = []

        print('width', width)
        print('frames', frames)
        print('multiplier', multiplier)
        print('end_at', end_at)

        start_at = end_at - timedelta(minutes=frames)

        # ---------------

        repository = OhlcRepository(-1)
        klines = KLines()

        exchange = 'binance'
        groups = [
            {
                "market": market,
                "assets": assets,
                "type": enums.HistoricalKlinesType.SPOT
            },
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
            for group in groups:
                for asset in group["assets"]:
                    futures.append(
                        executor.submit(
                            klines.build_klines,
                            group["market"],
                            asset,
                            group["type"],
                            interval,
                            start_at.timestamp(),
                            end_at.timestamp(),
                        )
                    )
                for i in range(len(assets)):
                    asset = assets[i]
                    collection = futures[i].result()

                    if len(collection) > 0:
                        print(f'processing: {asset} {group["market"]} {interval}')
                        print(asset, len(collection))

                        assets_real.append(asset)
                        repository.create_many(
                            exchange,
                            group["market"],
                            asset,
                            interval,
                            collection
                        )

        return assets_real
