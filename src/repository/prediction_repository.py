from datetime import datetime

from src.entity.ohlc import Ohlc
from src.entity.prediction import Prediction
from src.connector.db_connector import db_connect


class PredictionRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def create(self,
               ohlc: Ohlc,
               ohlc_next: Ohlc,
               model: str,
               started_at: datetime
               ) -> Prediction:
        prediction = Prediction()

        prediction.model = model
        prediction.started_at = started_at

        prediction.market = ohlc.market
        prediction.asset = ohlc.asset
        prediction.interval = ohlc.interval

        prediction.time_open = ohlc.time_open
        prediction.time_close = ohlc.time_close

        prediction.price_close = ohlc.price_close
        prediction.price_close_next = ohlc_next.price_close
        prediction.price_close_next_predicted = ohlc_next.price_close

        return prediction
