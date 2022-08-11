from binance import enums
from datetime import datetime, timedelta

from src.repository.ohlc_repository import OhlcRepository
from src.service.klines import KLines

# Variables
# ------------------------------------------------------------------------

end_at = datetime.utcnow()
start_at = end_at - timedelta(days=365 * 10)

exchange = 'binance'
interval = '5m'
groups = [
    {
        "market": 'USDT',
        "assets": [
            'BTC',
            # 'ETH',
        ],
        "type": enums.HistoricalKlinesType.SPOT
    },
]

# Population of data
# ------------------------------------------------------------------------

repository = OhlcRepository()
klines = KLines()

for group in groups:
    for asset in group["assets"]:
        print(f'processing: {asset} {group["market"]} {interval}')

        collection = klines.build_klines(
            group["market"],
            asset,
            group["type"],
            interval,
            start_at.timestamp(),
            end_at.timestamp(),
        )

        print(len(collection))

        repository.create_many(
            exchange,
            group["market"],
            asset,
            interval,
            collection
        )
