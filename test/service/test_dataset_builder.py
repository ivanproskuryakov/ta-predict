from fixture.ohlc import crate_ohlc_many

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

    crate_ohlc_many(asset='BTC', market='USDT', interval='5m', price=10000, quantity=100)
    crate_ohlc_many(asset='ETH', market='USDT', interval='5m', price=1000, quantity=100)

    train, validate = builder.build_dataset_train()

    assert train['open'].iloc[0] == 0.0
    assert train['open'].iloc[1] == 0.000000
    assert train['open'].iloc[2] == 0.00515463917525949

    assert validate['open'].iloc[0] == 0.9072164948453576
    assert validate['open'].iloc[1] == 0.9175257731958766
    assert validate['open'].iloc[2] == 0.9278350515463814

    assert len(train) == 180
    assert len(train.keys()) == 223

    assert len(validate) == 20
    assert len(validate.keys()) == 223
