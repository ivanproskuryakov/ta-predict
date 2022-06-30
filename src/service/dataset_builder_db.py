import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from src.service.estimator import estimate_ta_fill_na
from src.repository.ohlc_repository import OhlcRepository


class DatasetBuilderDB:
    repository: OhlcRepository
    scaler: MinMaxScaler
    exchange: str = 'binance'

    def __init__(self):
        self.scaler = MinMaxScaler()
        self.repository = OhlcRepository()

    def build_dataset_all(self, market: str, assets: list[str], interval: str) -> [
        pd.DataFrame,
        pd.DataFrame
    ]:
        train = []
        validate = []

        for asset in assets:
            df_train, df_validate = self.build_dataset_asset(
                asset=asset,
                market=market,
                interval=interval
            )

            train.append(df_train)
            validate.append(df_validate)

        train = pd.concat(train)
        validate = pd.concat(validate)

        return train, validate

    def build_dataset_asset(self, market: str, asset: str, interval: str) -> [
        pd.DataFrame,
        pd.DataFrame
    ]:
        df_ohlc = self.repository.get_df_full_desc(
            exchange=self.exchange,
            market=market,
            asset=asset,
            interval=interval
        )
        df_down = self.repository.find_down_df(
            exchange=self.exchange,
            interval=interval
        )
        df_btc = self.repository.get_df_btc_desc(
            exchange=self.exchange,
            asset=asset,
            interval=interval
        )
        min_len = self.repository.get_df_len_min()

        df = pd.concat([df_ohlc, df_down, df_btc], axis=1)

        df_min = df[0:min_len]

        df_ta_na = estimate_ta_fill_na(df_min)

        # Data Scaling
        # ------------------------------------------------------------------------

        scaled = self.scaler.fit_transform(df_ta_na)

        df = pd.DataFrame(scaled, None, df_ta_na.keys())

        # Data split
        # --------------------------------------------------------
        n = len(df)
        df_train = df[0:int(n * 0.9)]
        dv_validate = df[int(n * 0.9):]

        return df_train, dv_validate
