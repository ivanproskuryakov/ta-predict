import webbrowser
import tensorflow as tf

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from datetime import datetime

from src.service.reporter import Reporter
from src.service.trade_finder import TradeFinder
from src.service.dataset_builder import DatasetBuilder


class Predictor:
    interval: str
    model_path: str
    width: int

    model = None
    collection = None

    reporter: Reporter
    trade_finder: TradeFinder
    dataset_builder: DatasetBuilder
    scaler = MinMaxScaler()

    def __init__(self, interval: str, width: int, model_path: str, assets: [str], market: str, ):
        self.model_path = model_path
        self.width = width
        self.interval = interval
        self.reporter = Reporter()
        self.trade_finder = TradeFinder()
        self.scaler = MinMaxScaler()
        self.dataset_builder = DatasetBuilder(
            assets=assets,
            interval=self.interval,
            market=market,
        )

        np.set_printoptions(precision=4)
        pd.set_option("display.precision", 4)

    def load_model(self):
        self.model = tf.keras.models.load_model(self.model_path, compile=False)

    def predict(self, tail_crop: int = 0):
        now = datetime.now()
        data = []

        collection = self.dataset_builder.build_dataset_predict(width=self.width)

        time_db_load = datetime.now() - now

        self.load_model()

        for x_df in collection:
            x_df = x_df[:-tail_crop]

            x_df_original = x_df.copy()
            x_df = x_df.drop(columns=['asset', 'time_close'])

            x_df_expanded = np.expand_dims(
                self.scaler.fit_transform(x_df),
                axis=0
            )

            print('predicting', x_df_original.iloc[-1]['asset'])

            y = self.model.predict(x_df_expanded, verbose=0)

            df = pd.DataFrame(0, index=np.arange(len(y[0])), columns=x_df.keys())

            df['close'] = y[0]

            y_inverse = self.scaler.inverse_transform(df)

            y_df = pd.DataFrame(y_inverse, None, x_df.keys())

            data.append((
                x_df_original,
                y_df
            ))

        time_prediction = datetime.now() - now
        total = len(data)

        # --------

        if total:
            df = self.reporter.report_build(data=data)
            df_best = self.trade_finder.pick_best_options(df, diff=2, rsi=60, trades=50)
            df_worst = self.trade_finder.pick_worst_options(df, diff=-3, rsi=-40)

            report = self.reporter.report_prettify(df)
            report_best = self.reporter.report_prettify(df_best)
            report_worst = self.reporter.report_prettify(df_worst)

            print('all')
            print(report)
            print('best')
            print(report_best)
            print('worst')
            print(report_worst)

            webbrowser.open(df.iloc[-1]['url'], new=2)

        else:
            print('--- no data ---')

        print(f'started: {now}')
        print(f'total: {total}')
        print(f'interval: {self.interval}')
        print(f'db_load: {time_db_load}')
        print(f'prediction: {time_prediction}')

    def make_prediction_ohlc_close(self, x_df):
        x_df = x_df.drop(columns=['asset', 'time_close'])

        x_df_fitted = self.scaler.fit_transform(x_df)

        x_df_expanded = np.expand_dims(x_df_fitted, axis=0)

        y = self.model.predict(x_df_expanded, verbose=0)

        df = pd.DataFrame(0, index=np.arange(len(y[0])), columns=x_df.keys())

        df['close'] = y[0]

        y_inverse = self.scaler.inverse_transform(df)

        y_df = pd.DataFrame(y_inverse, None, x_df.keys())

        return y_df
