import numpy as np
import pandas as pd

from datetime import datetime
from sqlalchemy.orm import Session

from src.entity.prediction import Prediction
from src.connector.db_connector import db_connect
from src.service.util import diff_percentage, round


class PredictionRepository:
    connection = None

    def __init__(self):
        self.connection = db_connect()

    def get_time(self, df):
        return f'{df["time_month"]:.0f}.' \
               f'{df["time_day"]:.0f}:' \
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
            x_df_full,

            started_at: datetime
    ) -> Prediction:
        prediction = Prediction()

        prediction.model = model
        prediction.started_at = started_at

        prediction.market = market
        prediction.asset = asset
        prediction.interval = interval

        prediction.time = self.get_time(x_df_full.iloc[-1])

        prediction.price_close = round(x_df.iloc[-2]['close'])
        prediction.price_close_next = round(x_df.iloc[-1]['close'])
        prediction.price_close_next_diff = diff_percentage(
            v1=x_df.iloc[-2]['close'],
            v2=x_df.iloc[-1]['close'],
        )
        prediction.price_close_predicted = round(y_df.iloc[-1]['close'])
        prediction.price_close_predicted_diff = diff_percentage(
            v1=y_df.iloc[-2]['close'],
            v2=y_df.iloc[-1]['close']
        )

        if np.sign(prediction.price_close_next_diff) == np.sign(prediction.price_close_predicted_diff):
            prediction.is_match = True
        else:
            prediction.is_match = False

        with Session(self.connection) as session:
            session.add(prediction)
            session.commit()

        return prediction
