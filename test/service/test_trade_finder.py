from fixture.ohlc import crate_ohlc_many_bullish, crate_ohlc_many_bearish

from src.service.dataset_builder import DatasetBuilder
from src.service.trade_finder import TradeFinder
from src.service.reporter import Reporter
from sklearn.preprocessing import MinMaxScaler

reporter = Reporter()
trade_finder = TradeFinder()
scaler = MinMaxScaler()


def test_find_bullish():
    assets = [
        'BTC',
    ]

    builder = DatasetBuilder(
        market='USDT',
        assets=assets,
        interval='5m',
    )

    crate_ohlc_many_bullish(asset='BTC', market='USDT', interval='5m', price=10000, quantity=100)

    collection = builder.build_dataset_predict(width=100)
    x_df = collection[0]
    x_df_original = x_df.copy()
    y_df = x_df.drop(columns=['asset', 'time_close'])

    data = []
    data.append((x_df_original, y_df))

    df = reporter.report_build(data=data)

    db_bullish = trade_finder.find_bullish(df, diff=0, rsi=0, trades=0, limit=10)

    assert db_bullish.loc[0]['asset'] == 'BTC'


def test_find_bearish():
    assets = [
        'BTC',
    ]

    builder = DatasetBuilder(
        market='USDT',
        assets=assets,
        interval='5m',
    )

    crate_ohlc_many_bearish(asset='BTC', market='USDT', interval='5m', price=10000, quantity=100)

    collection = builder.build_dataset_predict(width=100)
    x_df = collection[0]
    x_df_original = x_df.copy()
    y_df = x_df.drop(columns=['asset', 'time_close'])

    data = []
    data.append((x_df_original, y_df))

    df = reporter.report_build(data=data)

    df_bearish = trade_finder.find_bearish(df, diff=0, rsi=100, trades=0, limit=10)

    assert df_bearish.loc[0]['asset'] == 'BTC'
