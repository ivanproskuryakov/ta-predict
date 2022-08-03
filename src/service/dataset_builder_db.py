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

    def build_dataset_all(
            self,
            market: str,
            assets: list[str],
            assets_down: list[str],
            assets_btc: list[str],
            interval: str
    ) -> [
        pd.DataFrame,
        pd.DataFrame
    ]:
        train = []
        validate = []

        for asset in assets:
            df_train, df_validate = self.build_dataset_asset(
                asset=asset,
                assets_down=assets_down,
                assets_btc=assets_btc,
                market=market,
                interval=interval
            )

            train.append(df_train)
            validate.append(df_validate)

        train = pd.concat(train)
        validate = pd.concat(validate)

        return train, validate

    def build_dataset_asset(
            self,
            market: str,
            asset: str,
            assets_down: list[str],
            assets_btc: list[str],
            interval: str
    ) -> [
        pd.DataFrame,
        pd.DataFrame
    ]:
        df = self.repository.get_full_df(
            exchange=self.exchange,
            market=market,
            asset=asset,
            interval=interval
        )
        # df_down = self.repository.find_down_df(
        #     exchange=self.exchange,
        #     assets_down=assets_down,
        #     interval=interval
        # )
        # df_btc = self.repository.find_btc_df(
        #     exchange=self.exchange,
        #     assets_btc=assets_btc,
        #     interval=interval
        # )
        #
        # min_len = self.repository.get_df_len_min()

        # if len(df_ohlc) != min_len or len(df_down) != min_len or len(df_btc) != min_len:
        #     raise Exception("Data frame lengths are not equal")
        #
        # df = pd.concat([df_ohlc, df_down, df_btc], axis=1)

        # df_ta_na = df[::-1].reset_index(drop=True)

        df = estimate_ta_fill_na(df)

        # Data Scaling
        # ------------------------------------------------------------------------

        scaled = self.scaler.fit_transform(df)

        df = pd.DataFrame(scaled, None, df.keys())

        # Data split
        # --------------------------------------------------------
        n = len(df)
        n_split = n * 0.8
        df_train = df[0:int(n_split)]
        dv_validate = df[int(n_split):]

        return df_train, dv_validate
