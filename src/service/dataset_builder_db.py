import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.service.estimator import estimate_ta_fill_na
from src.repository.ohlc_repository import OhlcRepository
from src.connector import db_connector


def build_dataset(market: str, asset: str, interval: str):
    driver = db_connector.db_connect()
    repository = OhlcRepository(driver)

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
