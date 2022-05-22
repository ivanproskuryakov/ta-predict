from src.repository.ohlc_repository import OhlcRepository
from src.connector.db_connector import db_connect
from src.entity.ohlc import Ohlc

connection = db_connect()
ohlcRepository = OhlcRepository(connection)

list = []
for i in range(10):
    ohlc = Ohlc()

    ohlc.exchange = 'binance'
    ohlc.interval = '3m'
    ohlc.market = 'USDT'
    ohlc.asset = 'BTC'

    ohlc.time_open = 1652961600
    ohlc.time_close = 1652961700

    ohlc.price_open = 1000.1
    ohlc.price_low = 1000.2
    ohlc.price_high = 1000.3
    ohlc.price_close = 1000.4

    ohlc.avg_current = 0
    ohlc.avg_percentage = 0

    ohlc.trades = 0
    ohlc.volume = 0
    ohlc.volume_taker = 0
    ohlc.volume_maker = 0

    ohlc.quote_asset_volume = 0

    list.append(ohlc)

ohlcRepository.create_many(list=list)
