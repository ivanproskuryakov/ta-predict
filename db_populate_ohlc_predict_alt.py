import sys

import concurrent.futures

from binance import enums
from datetime import datetime, timedelta

from src.repository.ohlc_repository import OhlcRepository
from src.service.klines import KLines

from src.parameters_usdt import assets, market

interval = float(sys.argv[1])

end_at = datetime.utcfromtimestamp(interval)
start_at = end_at - timedelta(hours=55)

repository = OhlcRepository(-1)
klines = KLines()

exchange = 'binance'
interval = '3m'
groups = [
    {
        "market": market,
        "assets": assets,
        "type": enums.HistoricalKlinesType.SPOT
    },
]

futures = []

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    for group in groups:
        for asset in group["assets"]:
            print(f'api read: {asset} {group["market"]} {interval}')

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
            print(f'db insert: {asset} {group["market"]} {interval}')

            collection = futures[i].result()
            asset = assets[i]

            repository.create_many(
                exchange,
                group["market"],
                asset,
                interval,
                collection
            )
