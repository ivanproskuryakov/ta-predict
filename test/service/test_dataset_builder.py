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
        'ETH',
        'LTC',
    ]

    crate_ohlc_many(asset='BTC', market='USDT', interval='5m', quantity=10)
    crate_ohlc_many(asset='ETH', market='USDT', interval='5m', quantity=10)

    # USDT market
    crate_ohlc_many(asset='BTCUP', market='USDT', interval='5m', quantity=10)
    crate_ohlc_many(asset='BTCDOWN', market='USDT', interval='5m', quantity=10)
    crate_ohlc_many(asset='ETHUP', market='USDT', interval='5m', quantity=10)
    crate_ohlc_many(asset='BNBUP', market='USDT', interval='5m', quantity=10)

    # BTC market
    crate_ohlc_many(asset='ETH', market='BTC', interval='5m', quantity=10)
    crate_ohlc_many(asset='LTC', market='BTC', interval='5m', quantity=10)

    train, validate = builder.build_dataset_all(
        market='USDT',
        assets=assets,
        assets_down=assets_down,
        assets_btc=assets_btc,
        interval='5m',
    )

    assert train['open'].iloc[0] == 0.0
    assert train['open'].iloc[1] == 0.11111111111108585
    assert train['open'].iloc[2] == 0.2222222222221717

    assert validate['open'].iloc[0] == 1
    assert validate['open'].iloc[1] == 1

    assert len(train) == 18
    assert len(train.keys()) == 86
    assert len(validate) == 2
    assert len(validate.keys()) == 86
