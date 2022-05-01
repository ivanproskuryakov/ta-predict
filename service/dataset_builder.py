from service.asset_reader import read_asset_file
from service.normalizer import scale_data
from service.estimator import estimate_ta


def build_dataset(asset, interval):
    df_ohlc = read_asset_file(asset, interval)
    df_ta = estimate_ta(df_ohlc)
    df_nan = df_ta.fillna(0)
    df = scale_data(df_nan)

    return df

def build_dataset_prepared(asset, interval):
    df = build_dataset(asset, interval)
    df_num_signals = df.shape[1]

    # Data split
    # --------------------------------------------------------
    n = len(df)
    train_df = df[0:int(n * 0.7)]
    val_df = df[int(n * 0.7):int(n * 0.9)]
    test_df = df[int(n * 0.9):]

    # Sets preparation
    # --------------------------------------------------------

    train_mean = train_df.mean()
    train_std = train_df.std()

    train_df = (train_df - train_mean) / train_std
    val_df = (val_df - train_mean) / train_std
    test_df = (test_df - train_mean) / train_std

    return [
        df,
        train_df,
        val_df,
        test_df,
        df_num_signals
    ]