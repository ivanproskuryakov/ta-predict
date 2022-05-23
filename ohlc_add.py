from src.repository.ohlc_repository import OhlcRepository
from src.connector.db_connector import db_connect
from src.service.klines import KLines
from binance import Client

start_at = '5 year ago UTC'
exchange = 'binance'
market = 'USDT'
asset = 'BTC'
interval = Client.KLINE_INTERVAL_1MINUTE

connection = db_connect()
ohlcRepository = OhlcRepository(connection)
klines = KLines()

collection = klines.build_klines(
    market,
    asset,
    interval,
    start_at
)

ohlcRepository.create_many(exchange, market, asset, interval, collection)
