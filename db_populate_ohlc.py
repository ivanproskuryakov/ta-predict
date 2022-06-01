from src.repository.ohlc_repository import OhlcRepository
from src.connector.db_connector import db_connect
from src.service.klines import KLines
from src.parameters_train import assets

start_at = '8 year ago UTC'
exchange = 'binance'
market = 'USDT'

connection = db_connect()
repository = OhlcRepository(connection)
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
