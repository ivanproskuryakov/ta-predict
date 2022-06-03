from src.repository.ohlc_repository import OhlcRepository
from src.service.klines import KLines
from src.parameters import assets

start_at = '8 year ago UTC'
exchange = 'binance'
market = 'USDT'

repository = OhlcRepository()
klines = KLines()

interval = '3m'

for asset in assets:
    print(f'processing: {asset} {interval}')
    collection = klines.build_klines(
        market,
        asset,
        interval,
        start_at
    )

    repository.create_many(exchange, market, asset, interval, collection)
