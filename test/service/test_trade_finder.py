from fixture.ohlc import crate_ohlc_many

from src.service.dataset_builder import DatasetBuilder
from src.service.trade_finder import TradeFinder
from src.service.reporter import Reporter
from sklearn.preprocessing import MinMaxScaler

reporter = Reporter()
trade_finder = TradeFinder()
scaler = MinMaxScaler()


def test_pick_best_options():
    assets = [
        'BTC',
    ]

    builder = DatasetBuilder(
        market='USDT',
        assets=assets,
        interval='5m',
    )

    crate_ohlc_many(asset='BTC', market='USDT', interval='5m', price=10000, quantity=100)

    collection = builder.build_dataset_predict()
    x_df = collection[0]
    x_df_original = x_df.copy()
    y_df = x_df.drop(columns=['asset', 'time_close'])

    data = []
    data.append((x_df_original, y_df))

    df = reporter.report_build(data=data)

    db_best = trade_finder.pick_best_options(df, diff=0, rsi=0, trades=0)

    best = db_best.loc[0]

    assert best['asset'] == 'BTC'
