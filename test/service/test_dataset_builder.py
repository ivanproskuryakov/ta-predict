from fixture.ohlc import crate_ohlc_many_bullish

from src.entity.ohlc import Ohlc
from src.service.dataset_builder import DatasetBuilder
from src.connector.db_connector import db_connect


def test_build_dataset_train():
    engine = db_connect()
    Ohlc.metadata.drop_all(bind=engine)
    Ohlc.metadata.create_all(bind=engine)

    assets = [
        'BTC',
        'ETH',
    ]

    builder = DatasetBuilder(
        market='USDT',
        assets=assets,
        interval='5m',
    )

    crate_ohlc_many_bullish(asset='BTC', market='USDT', interval='5m', price=10000, quantity=100)
    crate_ohlc_many_bullish(asset='ETH', market='USDT', interval='5m', price=1000, quantity=100)

    train, validate, test = builder.build_dataset_train()

    assert train['open'].iloc[0] == 0.0

    assert validate['open'].iloc[0] == 0.7070707070707059

    assert test['open'].iloc[0] == 0.9090909090909065

    assert len(train) == 140
    assert len(train.keys()) == 11

    assert len(validate) == 40
    assert len(validate.keys()) == 11

    assert len(test) == 20
    assert len(test.keys()) == 11
