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

    df = estimate_ta_fill_na(df_ohlc)
    df_num_signals = df.shape[1]

    # Data split
    # --------------------------------------------------------
    n = len(df)
    train_df = df[0:int(n * 0.9)]
    val_df = df[int(n * 0.9):]
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
