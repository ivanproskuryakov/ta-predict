import tensorflow as tf

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

from src.parameters_usdt import market, assets
from src.parameters_btc import assets_btc
from src.parameters import assets_down

from src.service.reporter import Reporter
from src.service.trade_finder import TradeFinder
from src.service.trader import Trader
from src.service.dataset_builder import DatasetBuilder


class Predictor:
    trader: Trader
    reporter: Reporter
    trade_finder: TradeFinder
    dataset_builder: DatasetBuilder

    interval: str
    model = None

    def __init__(self, interval: str):
        self.interval = interval
        self.trader = Trader()
        self.reporter = Reporter()
        self.trade_finder = TradeFinder()
        self.dataset_builder = DatasetBuilder(
            assets=assets,
            assets_btc=assets_btc,
            assets_down=assets_down,
            interval=self.interval,
            market=market,
        )

        np.set_printoptions(precision=4)
        pd.set_option("display.precision", 4)

    def run(self):
        now = datetime.now()
        start_at = now - timedelta(hours=2)
        data = []

        # --------

        collection = self.dataset_builder.build_dataset_predict(
            start_at=start_at.timestamp(),
        )

        time_db_load = datetime.now() - now

        self.model = tf.keras.models.load_model('model/gru-b-1000-48.keras')

        for item in collection:
            asset, x_df, df_scaled = item

            y_df = self.make_prediction_ohlc_close(df_scaled)

            data.append((
                asset,
                x_df,
                y_df
            ))

        time_prediction = datetime.now() - now

        # --------

        df = self.reporter.report_build(data=data)
        df_best = self.trade_finder.pick_best_options(df, diff=1, diff_sum=0)

        report = self.reporter.report_prettify(df)
        report_best = self.reporter.report_prettify(df_best)

        print(report)
        print(report_best)

        print(f'start: {start_at}')
        print(f'interval: {self.interval}')
        print(f'db_load: {time_db_load}')
        print(f'prediction: {time_prediction}')

    def make_prediction_ohlc_close(self, x_df):
        # Scale
        # ------------------------------------------------------------------------
        scaler = MinMaxScaler()
        scaled = scaler.fit_transform(x_df)

        x_df_scaled = pd.DataFrame(scaled, None, x_df.keys())
        x_df_scaled_expanded = np.expand_dims(x_df_scaled, axis=0)

        # Predict
        # ------------------------------------------------------------------------
        y = self.model.predict(x_df_scaled_expanded, verbose=0)

        df = pd.DataFrame(0, index=np.arange(len(y[0])), columns=x_df.keys())

        df['close'] = y[0]

        y_inverse = scaler.inverse_transform(df)

        y_df = pd.DataFrame(y_inverse, None, x_df.keys())

        return y_df
