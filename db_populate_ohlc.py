from src.repository.ohlc_repository import OhlcRepository
from src.connector.db_connector import db_connect
from src.service.klines import KLines
from src.parameters import intervals, assets

start_at = '8 year ago UTC'
exchange = 'binance'
market = 'USDT'

connection = db_connect()
repository = OhlcRepository(connection)
klines = KLines()

for asset in assets:
    for interval in intervals:
        print(f'processing: {interval}')
        collection = klines.build_klines(
            market,
            asset,
            interval,
            start_at
        )

        repository.create_many(exchange, market, asset, interval, collection)
