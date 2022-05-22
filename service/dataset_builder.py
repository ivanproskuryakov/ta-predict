import pandas as pd

from deprecated import deprecated
from sklearn.preprocessing import MinMaxScaler

from service.asset_reader import read_asset_file
from service.estimator import estimate_ta_fill_na


@deprecated
def scale_data(df):
    scaler = MinMaxScaler()

    scaled = scaler.fit_transform(df)
    df_scaled = pd.DataFrame(scaled, None, df.keys())

    return df_scaled


def build_dataset_seen(market: str, asset: str, interval: str):
    path = f'out_klines/{market}/{asset}_{interval}.json'

    df_ohlc = read_asset_file(path)

    df = estimate_ta_fill_na(df_ohlc)

    return df


def build_dataset_unseen(market: str, asset: str, interval: str):
    path = f'test/{market}_{asset}_{interval}.json'

    df_ohlc = read_asset_file(path)

    df = estimate_ta_fill_na(df_ohlc)

    return df


def build_dataset(market: str, asset: str, interval: str):
    df = build_dataset_seen(market, asset, interval)
    df_num_signals = df.shape[1]

    # Data split
    # --------------------------------------------------------
    n = len(df)
    train_df = df[0:int(n * 0.7)]
    val_df = df[int(n * 0.7):int(n * 0.9)]
    test_df = df[int(n * 0.9):]

    # Sets preparation
    # --------------------------------------------------------

    # train_mean = train_df.mean()
    # train_std = train_df.std()
    #
    # train_df = (train_df - train_mean) / train_std
    # val_df = (val_df - train_mean) / train_std
    # test_df = (test_df - train_mean) / train_std

    return [
        df,
        train_df,
        val_df,
        test_df,
        df_num_signals
    ]
