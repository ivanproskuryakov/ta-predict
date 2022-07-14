import sys

from binance import enums
from datetime import datetime, timedelta

from src.repository.ohlc_repository import OhlcRepository
from src.service.klines import KLines

from src.parameters_usdt import assets, market

# ---------------

interval = float(sys.argv[1])
last_time = float(sys.argv[2])

end_at = datetime.utcfromtimestamp(interval)
start_at = end_at - timedelta(minutes=1000)

if interval == '3m':
    start_at = end_at - timedelta(minutes=1000 * 3)

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
