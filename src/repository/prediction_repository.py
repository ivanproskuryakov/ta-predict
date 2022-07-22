import pandas as pd

from datetime import datetime
from sqlalchemy.orm import Session

from src.entity.prediction import Prediction
from src.connector.db_connector import db_connect
from src.service.util import diff_percentage


class PredictionRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def get_time(self, df):
        return f'{df["time_month"]:.0f}.' \
               f'{df["time_day"]:.0f}.' \
               f'{df["time_hour"]:.0f}.' \
               f'{df["time_minute"]:.0f}'

    def create(
            self,
            market: str,
            asset: str,
            interval: str,
            model: str,

            x_df,
            y_df,

            started_at: datetime
    ) -> Prediction:
        x_df1 = x_df.iloc[-1]

        prediction = Prediction()

        prediction.model = model
        prediction.started_at = started_at

        prediction.market = market
        prediction.asset = asset
        prediction.interval = interval

        prediction.time = self.get_time(x_df1)

        prediction.price_close = x_df.iloc[-2]['close']
        prediction.price_close_next = x_df.iloc[-1]['close']
        prediction.price_close_next_diff = diff_percentage(
            v2=x_df.iloc[-1]['close'],
            v1=x_df.iloc[-2]['close']
        )
        prediction.price_close_predicted = x_df.iloc[-1]['close']
        prediction.price_close_predicted_diff = diff_percentage(
            v2=y_df.iloc[-1]['close'],
            v1=y_df.iloc[-2]['close']
        )

        if prediction.price_close_next_diff > 0 and prediction.price_close_predicted_diff > 0:
            prediction.is_match = True
        if prediction.price_close_next_diff < 0 and prediction.price_close_predicted_diff < 0:
            prediction.is_match = True

        if prediction.price_close_next_diff > 0 and prediction.price_close_predicted_diff < 0:
            prediction.is_match = False
        if prediction.price_close_next_diff < 0 and prediction.price_close_predicted_diff > 0:
            prediction.is_match = False

        with Session(self.connection) as session:
            session.add(prediction)
            session.commit()

        return prediction
