from fixture.ohlc import crate_ohlc_many

from src.entity.ohlc import Ohlc
from src.service.dataset_builder_db import DatasetBuilderDB
from src.connector.db_connector import db_connect


def test_build_dataset_all():
    engine = db_connect()
    Ohlc.metadata.drop_all(bind=engine)
    Ohlc.metadata.create_all(bind=engine)

    builder = DatasetBuilderDB()

    assets = [
        'BTC',
        'ETH',
    ]
    assets_down = [
        'BTCUP',
        'BTCDOWN',
        'ETHUP',
        'BNBUP',
    ]
    assets_btc = [
        'BNB',
        'ADA',
    ]
    crate_ohlc_many(asset='BTC', market='USDT', interval='5m', price=10000, tail_quantity=10)
    crate_ohlc_many(asset='ETH', market='USDT', interval='5m', price=1000, tail_quantity=10)

    # USDT market
    crate_ohlc_many(asset='BTCUP', market='USDT', interval='5m', price=10000, tail_quantity=10)
    crate_ohlc_many(asset='BTCDOWN', market='USDT', interval='5m', price=10000, tail_quantity=10)
    crate_ohlc_many(asset='ETHUP', market='USDT', interval='5m', price=10000, tail_quantity=10)
    crate_ohlc_many(asset='BNBUP', market='USDT', interval='5m', price=10000, tail_quantity=10)

    # BTC market
    crate_ohlc_many(asset='BNB', market='BTC', interval='5m', price=0.011, tail_quantity=10)
    crate_ohlc_many(asset='ADA', market='BTC', interval='5m', price=0.00002, tail_quantity=10)

    train, validate = builder.build_dataset_all(
        market='USDT',
        assets=assets,
        assets_down=assets_down,
        assets_btc=assets_btc,
        interval='5m',
    )

    assert train['open'].iloc[0] == 0.0
    assert train['open'].iloc[1] == 0.3333333333334849
    assert train['open'].iloc[2] == 0.6666666666669698
    # assert train['open'].iloc[3] == 10000.0
    # assert train['open'].iloc[5] == 10002.0

    assert validate['open'].iloc[0] == 1
    assert validate['open'].iloc[1] == 1

    assert len(train) == 6
    assert len(train.keys()) == 86
    assert len(validate) == 2
    assert len(validate.keys()) == 86
