import pandas as pd

from sklearn.preprocessing import MinMaxScaler

from src.service.estimator import estimate_ta_fill_na
from src.repository.ohlc_repository import OhlcRepository


class DatasetBuilder:
    repository: OhlcRepository
    exchange: str = 'binance'

    assets: [str]
    interval: str
    market: str

    def __init__(self,
                 assets: [str],
                 interval: str,
                 market: str,
                 ):
        self.assets = assets
        self.interval = interval
        self.market = market

        self.repository = OhlcRepository()

    def build_dataset_train(self) -> [pd.DataFrame, pd.DataFrame]:
        train = []
        validate = []

        for asset in self.assets:
            df = self.repository.get_full_df(
                asset=asset,
                market=self.market,
                interval=self.interval,
                exchange=self.exchange,
            )

            df_ta_na = estimate_ta_fill_na(df)

            # Data Scaling
            # ------------------------------------------------------------------------
            scaler = MinMaxScaler()  # todo: improve scaling part
            scaled = scaler.fit_transform(df_ta_na)

            df = pd.DataFrame(scaled, None, df_ta_na.keys())

            # Data split
            # --------------------------------------------------------
            n = len(df)
            df_train = df[0:int(n * 0.9)]
            dv_validate = df[int(n * 0.9):]

            train.append(df_train)
            validate.append(dv_validate)

        train = pd.concat(train)
        validate = pd.concat(validate)

        return train, validate

    def build_dataset_predict(self, width: int):
        collection = []

        for asset in self.assets:
            df = self.repository.get_df_predict(
                asset=asset,
                exchange=self.exchange,
                market=self.market,
                interval=self.interval,
            )
            if len(df) >= width:
                df = estimate_ta_fill_na(df)

                collection.append(df)

        return collection
