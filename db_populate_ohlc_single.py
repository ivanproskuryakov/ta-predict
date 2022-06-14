from src.repository.ohlc_repository import OhlcRepository
from src.service.klines import KLines

start_at = '8 year ago UTC'
exchange = 'binance'
market = 'USDT'

repository = OhlcRepository()
klines = KLines()

interval = '15m'
asset = 'BTC'

print(f'processing: {asset} {interval}')

collection = klines.build_klines(
    market,
    asset,
    interval,
    start_at
)

repository.create_many(exchange, market, asset, interval, collection)