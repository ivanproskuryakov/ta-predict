import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.service.estimator import estimate_ta_fill_na
from src.repository.ohlc_repository import OhlcRepository


class DatasetBuilder:
    repository: OhlcRepository
    scaler: MinMaxScaler
    exchange: str = 'binance'

    assets: [str]
    assets_down: [str]
    assets_btc: [str]
    interval: str
    market: str

    def __init__(self,
                 assets: [str],
                 assets_down: [str],
                 assets_btc: [str],
                 interval: str,
                 market: str,
                 ):
        self.assets = assets
        self.assets_down = assets_down
        self.assets_btc = assets_btc
        self.interval = interval
        self.market = market

        self.scaler = MinMaxScaler()
        self.repository = OhlcRepository(start_at=-1)

    def build_dataset_train(self) -> [pd.DataFrame, pd.DataFrame]:
        train = []
        validate = []

        for asset in self.assets:
            df_train, df_validate = self.build_dataset_asset(asset=asset)

            train.append(df_train)
            validate.append(df_validate)

        train = pd.concat(train)
        validate = pd.concat(validate)

        return train, validate

    def build_dataset_predict(self, start_at: float, end_at: float ):
        collection = []

        for asset in self.assets:
            df, df_scaled = self.repository.get_full_df(
                asset=asset,
                exchange=self.exchange,
                market=self.market,
                interval=self.interval,
                start_at=start_at,
                end_at=end_at,
            )

            df = df[::-1].reset_index(drop=True)

            df_scaled = df_scaled[::-1].reset_index(drop=True)
            df_scaled = estimate_ta_fill_na(df_scaled)
            scaled = self.scaler.fit_transform(df_scaled)
            df_scaled = pd.DataFrame(scaled, None, df_scaled.keys())

            collection.append((asset, df, df_scaled))

        return collection

    def build_dataset_asset(self, asset: str) -> [pd.DataFrame, pd.DataFrame]:
        df_ohlc = self.repository.get_full_df(
            asset=asset,
            market=self.market,
            interval=self.interval,
            exchange=self.exchange,
        )
        df_down = self.repository.find_down_df(
            assets_down=self.assets_down,
            interval=self.interval,
            exchange=self.exchange,
        )
        df_btc = self.repository.find_btc_df(
            assets_btc=self.assets_btc,
            interval=self.interval,
            exchange=self.exchange,
        )

        min_len = self.repository.get_df_len_min()

        if len(df_ohlc) != min_len or len(df_down) != min_len or len(df_btc) != min_len:
            raise Exception("Data frame lengths are not equal")

        df = pd.concat([df_ohlc, df_down, df_btc], axis=1)

        df_asc = df[::-1].reset_index(drop=True)

        df_ta_na = estimate_ta_fill_na(df_asc)

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
