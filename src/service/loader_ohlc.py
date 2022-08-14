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
        self.repository = OhlcRepository()

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
        time = interval[-1:]
        width_multiplied = width * multiplier
        futures = []
        assets_real = []

        print('width', width)
        print('width_multiplied', width_multiplied)
        print('multiplier', multiplier)
        print('end_at', end_at)

        start_at = end_at - timedelta(minutes=width_multiplied)

        if time == 'h':
            start_at = end_at - timedelta(hours=width_multiplied)
        if time == 'd':
            start_at = end_at - timedelta(days=width_multiplied)

        # ---------------

        klines = KLines()

        exchange = 'binance'
        groups = [
            {
                "market": market,
                "assets": assets,
                "type": enums.HistoricalKlinesType.SPOT
            },
        ]

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
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

                    print(f'processing: {asset} {group["market"]} {interval}', len(collection))

                    if len(collection) > 0:
                        assets_real.append(asset)
                        self.repository.create_many(
                            exchange,
                            group["market"],
                            asset,
                            interval,
                            collection
                        )

        return assets_real
