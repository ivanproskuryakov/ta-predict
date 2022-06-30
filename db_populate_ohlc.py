from datetime import datetime, timedelta

from src.repository.ohlc_repository import OhlcRepository
from src.service.klines import KLines
from src.parameters import assets_down
from src.parameters_btc import assets_btc

# end_at = datetime.utcnow()
# start_at = end_at - timedelta(365 * 8)  # 8 years

repository = OhlcRepository()
klines = KLines()

start_at = '1650000000'
end_at = '1656110684'

exchange = 'binance'
interval = '5m'
groups = [
    {
        "market": 'USDT',
        "assets": [
            'BTC',
            "BNB",
            "NEO",
            "LTC",
            "ADA",
            "XRP",
            "EOS",
        ]
    },
    {
        "market": 'USDT',
        "assets": assets_down
    },
    {
        "market": 'BTC',
        "assets": assets_btc
    }
]

for group in groups:
    for asset in group["assets"]:
        print(f'processing: {asset} {group["market"]} {interval}')

        collection = klines.build_klines(
            group["market"],
            asset,
            interval,
            start_at,
            end_at,
        )

        print(len(collection))

        repository.create_many(
            exchange,
            group["market"],
            asset,
            interval,
            collection
        )
