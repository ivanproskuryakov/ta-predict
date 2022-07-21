from fixture.ohlc import crate_ohlc_many

from src.entity.ohlc import Ohlc
from src.service.backtester import BackTester
from src.connector.db_connector import db_connect


def test_backtester_run():
    engine = db_connect()
    Ohlc.metadata.drop_all(bind=engine)
    Ohlc.metadata.create_all(bind=engine)
    backtester = BackTester()

    crate_ohlc_many(asset='BTC', market='USDT', interval='15m', price=10000, quantity=20)

    dfs = backtester.run([], width=10 + 1)

    assert len(dfs[0]) == 11
    assert len(dfs) == 9
