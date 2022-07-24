import pandas as pd

from datetime import datetime
from sklearn.preprocessing import MinMaxScaler

from src.service.predictor import Predictor
from src.service.dataset_builder_db import DatasetBuilderDB
from src.repository.ohlc_repository import OhlcRepository
from src.repository.prediction_repository import PredictionRepository

from src.service.util import diff_percentage


class BackTester:
    prediction_repository: PredictionRepository
    ohlc_repository: OhlcRepository
    builder: DatasetBuilderDB
    predictor: Predictor

    width: int
    interval: str
    market: str

    scaler: MinMaxScaler

    def __init__(self, interval: str, market: str):
        self.prediction_repository = PredictionRepository()
        self.ohlc_repository = OhlcRepository()
        self.builder = DatasetBuilderDB()
        self.predictor = Predictor(interval=interval)

        self.interval = interval
        self.market = market

        self.scaler = MinMaxScaler()

    def load_model(self, name: str):
        self.predictor.load_model(name=f'model/{name}')

    def datasets_predict(self, df: pd.DataFrame, width: int, scaler):
        x_df = df[0: width]
        y_df = self.predictor.make_prediction_ohlc_close(x_df=x_df, scaler=scaler)

        return y_df

    def run(self, asset: str, model: str, width: int):
        x_dfs = self.datasets_build(asset=asset, width=width)

        self.load_model(name=model)
        started_at = datetime.now()

        for x_df in x_dfs:
            rescaled = self.scaler.inverse_transform(x_df)
            x_df_rescaled = pd.DataFrame(rescaled, None, x_df.keys())

            y_df = self.datasets_predict(df=x_df, width=width, scaler=self.scaler)

            x_diff = diff_percentage(v2=x_df_rescaled.iloc[-1]['close'], v1=x_df_rescaled.iloc[-2]['close'])
            y_diff = diff_percentage(v2=y_df.iloc[-1]['close'], v1=y_df.iloc[-2]['close'])

            self.prediction_repository.create(
                market=self.market,
                asset=asset,
                interval=self.interval,
                model=model,

                x_df=x_df_rescaled,
                y_df=y_df,
                started_at=started_at,
            )

            print(x_diff, y_diff)

    def datasets_build(self, asset: str, width: int) -> [pd.DataFrame]:
        width_plus = width + 1
        df = self.builder.build_dataset_predict(
            asset=asset,
            market=self.market,
            interval=self.interval,
            scaler=self.scaler
        )

        total = len(df)
        total_adjusted = total - width_plus

        dfs = []

        for i in range(0, total_adjusted):
            j = i + width_plus
            crop = df[i:j]

            dfs.append(crop)

        return dfs
