from src.repository.ohlc_repository import OhlcRepository
from src.connector.db_connector import db_connect

connection = db_connect()
ohlcRepository = OhlcRepository(connection)

ohlcRepository.add(
    'binance',
    'USDT',
    'BTC',
    '5m',

    1652961600,
    1652961700,

    1000.1,
    1000.2,
    1000.3,
    1000.4,

    0,
    0,
    0,
    0,
    0,
    0,
    0,
)
