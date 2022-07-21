import pandas as pd

from src.service.predictor import Predictor
from src.service.dataset_builder_db import DatasetBuilderDB
from src.repository.ohlc_repository import OhlcRepository
from src.repository.prediction_repository import PredictionRepository


class BackTester:
    prediction_repository: PredictionRepository
    ohlc_repository: OhlcRepository
    builder: DatasetBuilderDB
    predictor: Predictor

    models: list
    width: int
    interval: str
    market: str

    def __init__(self, models: list, interval: str, market: str):
        self.prediction_repository = PredictionRepository()
        self.ohlc_repository = OhlcRepository()
        self.builder = DatasetBuilderDB()
        self.predictor = Predictor(interval=interval)

        self.models = models
        self.interval = interval
        self.market = market

    def load_model(self, name: str):
        self.predictor.load_model(name=f'model/{name}')

    def datasets_predict(self, df: pd.DataFrame, width: int, scaler):
        x_df = df[0: width]
        y_df = self.predictor.make_prediction_ohlc_close(x_df=x_df, scaler=scaler)

        return y_df

    def datasets_build(self, asset: str, width: int) -> [pd.DataFrame]:
        width_plus = width + 1
        df, scaler = self.builder.build_dataset_predict(
            asset=asset,
            market=self.market,
            interval=self.interval,
        )

        total = len(df)
        total_adjusted = total - width_plus

        dfs = []

        for i in range(0, total_adjusted):
            j = i + width_plus
            crop = df[i:j]

            dfs.append(crop)

        return dfs, scaler
