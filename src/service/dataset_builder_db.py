import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.service.estimator import estimate_ta_fill_na
from src.repository.ohlc_repository import OhlcRepository


def build_dataset_window(market: str, asset: str, interval: str):
    repository = OhlcRepository()

    df_ohlc = repository.find_all_with_df(
        exchange='binance',
        market=market,
        asset=asset,
        interval=interval
    )

    df_ta_na = estimate_ta_fill_na(df_ohlc)
    df_num_signals = df_ta_na.shape[1]

    # Data Scaling
    # ------------------------------------------------------------------------

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df_ta_na)

    df = pd.DataFrame(scaled, None, df_ta_na.keys())

    # Data split
    # --------------------------------------------------------
    n = len(df)
    train_df = df[0:int(n * 0.9)]
    val_df = df[int(n * 0.9):]

    return train_df, val_df, df_num_signals


def build_dataset_random(market: str, asset: str, interval: str):
    repository = OhlcRepository()

    df_ohlc = repository.find_all_with_df(
        exchange='binance',
        market=market,
        asset=asset,
        interval=interval
    )

    df = df_ohlc.fillna(0)

    # df_ta_na = estimate_ta_fill_na(df_na)

    # Data Scaling
    # ------------------------------------------------------------------------

    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(df)

    return pd.DataFrame(scaled, None, df.keys())