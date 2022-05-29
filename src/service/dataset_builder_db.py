from src.service.estimator import estimate_ta_fill_na
from src.repository.ohlc_repository import OhlcRepository
from src.connector import db_connector
import pandas as pd

from sklearn.preprocessing import MinMaxScaler


def df_from_data(data: []):
    df = pd.DataFrame(data, None, [
        'open',
        'high',
        'low',
        'close',

        'time_month',
        'time_day',
        'time_hour',
        'time_minute',

        'avg_percentage',
        'avg_current',

        'trades',
        'volume',
        'volume_taker',
        'volume_maker',

        'quote_asset_volume',
        # 'epoch',
    ])

    return df


def build_dataset(market: str, asset: str, interval: str):
    driver = db_connector.db_connect()
    repository = OhlcRepository(driver)

    data = repository.find_all_with_df(
        exchange='binance',
        market=market,
        asset=asset,
        interval=interval
    )
    df_ohlc = df_from_data(data)

    df = estimate_ta_fill_na(df_ohlc)

    df_num_signals = df.shape[1]

    # Data Scaling
    # ------------------------------------------------------------------------

    # scaler = MinMaxScaler()
    # data_scaled = scaler.fit_transform(df)
    # df = df_from_data(data_scaled)

    print(df)
    exit()

    # Data split
    # --------------------------------------------------------
    n = len(df)
    train_df = df[0:int(n * 0.9)]
    val_df = df[int(n * 0.9):]

    # # Sets preparation
    # # --------------------------------------------------------
    #
    # train_mean = train_df.mean()
    # train_std = train_df.std()
    #
    # train_df = (train_df - train_mean) / train_std
    # val_df = (val_df - train_mean) / train_std

    return train_df, val_df, df_num_signals
