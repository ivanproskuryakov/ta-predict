import numpy as np

from sqlalchemy.orm import Session

from src.entity.prediction import Prediction
from src.connector.db_connector import db_connect


class PredictionRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def find(
            self,
            exchange: str,
            market: str,
            asset: str,
            interval: str,
            time_open: int,
    ):

        with Session(self.connection) as session:
            collection = session.query(Prediction) \
                .filter(Prediction.exchange == exchange) \
                .filter(Prediction.market == market) \
                .filter(Prediction.interval == interval) \
                .filter(Prediction.asset == asset) \
                .filter(Prediction.time_open == time_open) \
                .all()

        return collection

    def create(
            self,
            exchange: str,
            market: str,
            asset: str,
            interval: str,
            data
    ):
        prediction = Prediction()

        prediction.time_open = np.round(data['time_open'], 0)

        prediction.exchange = exchange
        prediction.interval = interval
        prediction.market = market
        prediction.asset = asset

        prediction.price_prediction = 0
        # prediction.price_real
        # prediction.price_error

        prediction.percentage_prediction = 0
        # prediction.percentage_real = 0
        # prediction.percentage_error = 0

        with Session(self.connection) as session:
            session.add(prediction)
            session.commit()

    def update(self, prediction: Prediction, data: Prediction):
        with Session(self.connection) as session:
            prediction.asset = data.asset
