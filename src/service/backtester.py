from src.service.dataset_builder_db import DatasetBuilderDB
from src.repository.ohlc_repository import OhlcRepository
from src.repository.prediction_repository import PredictionRepository


class BackTester:
    prediction_repository: PredictionRepository
    ohlc_repository: OhlcRepository
    builder: DatasetBuilderDB

    def __init__(self):
        self.prediction_repository = PredictionRepository()
        self.ohlc_repository = OhlcRepository()
        self.builder = DatasetBuilderDB()

    def run(self, models: list, width: int):
        df = self.builder.build_dataset_predict(
            market='USDT',
            asset='BTC',
            interval='15m',
        )

        total = len(df)
        total_adjusted = total - width

        dfs = []

        for i in range(0, total_adjusted):
            j = i + width
            crop = df[i:j]
            dfs.append(crop)

        return dfs
