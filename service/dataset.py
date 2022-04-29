from service.reader_ta import read
from service.scaler import scale_data
from service.estimator import estimate_ta


def build_dataset(asset, interval):
    df_raw = read(asset, interval)
    df_ta = estimate_ta(df_raw)
    df_nan = df_ta.fillna(0)
    df = scale_data(df_nan)

    df_num_signals = df.shape[1]

    # Data split
    # --------------------------------------------------------
    n = len(df)
    train_df = df[0:int(n * 0.7)]
    val_df = df[int(n * 0.7):int(n * 0.9)]
    test_df = df[int(n * 0.9):]

    # Normalize the data
    # --------------------------------------------------------

    train_mean = train_df.mean()
    train_std = train_df.std()

    train_df = (train_df - train_mean) / train_std
    val_df = (val_df - train_mean) / train_std
    test_df = (test_df - train_mean) / train_std

    return [
        train_df,
        val_df,
        test_df,
        train_df.shape[1]
    ]
