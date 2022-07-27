import webbrowser
import tensorflow as tf

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, timedelta

from src.parameters_usdt_top import market, assets
from src.service.reporter import Reporter
from src.service.trade_finder import TradeFinder
from src.service.trader import Trader
from src.service.dataset_builder import DatasetBuilder


class Predictor:
    trader: Trader
    reporter: Reporter
    trade_finder: TradeFinder
    dataset_builder: DatasetBuilder
    scaler = MinMaxScaler()

    interval: str
    model = None
    model_path: str = 'model/gru-b-1000-48.keras'
    width: int = 1000

    def __init__(self, interval: str):
        self.interval = interval
        self.trader = Trader()
        self.reporter = Reporter()
        self.trade_finder = TradeFinder()
        self.scaler = MinMaxScaler()
        self.dataset_builder = DatasetBuilder(
            assets=assets,
            assets_btc=[],
            assets_down=[],
            interval=self.interval,
            market=market,
        )

        np.set_printoptions(precision=4)
        pd.set_option("display.precision", 4)

    def predict(self):
        now = datetime.now()
        start_at = datetime.utcnow() - timedelta(minutes=(self.width + 100) * 5)
        data = []

        collection = self.dataset_builder.build_dataset_predict(
            start_at=start_at.timestamp(),
            end_at=now.timestamp(),
        )

        time_db_load = datetime.now() - now

        self.model = tf.keras.models.load_model(self.model_path)

        for item in collection:
            asset, x_df = item

            if len(x_df) > self.width:
                x_df_expanded = np.expand_dims(
                    self.scaler.fit_transform(x_df),
                    axis=0
                )

                y = self.model.predict(x_df_expanded, verbose=0)

                df = pd.DataFrame(0, index=np.arange(len(y[0])), columns=x_df.keys())

                df['close'] = y[0]

                y_inverse = self.scaler.inverse_transform(df)

                y_df = pd.DataFrame(y_inverse, None, x_df.keys())

                data.append((
                    asset,
                    x_df,
                    y_df
                ))

        time_prediction = datetime.now() - now
        total = len(data)

        # --------

        if total:
            df = self.reporter.report_build(data=data)
            df_best = self.trade_finder.pick_best_options(df, diff=1, diff_sum=0)
            df_worst = self.trade_finder.pick_worst_options(df, diff=-10)

            report = self.reporter.report_prettify(df)
            report_best = self.reporter.report_prettify(df_best)
            report_worst = self.reporter.report_prettify(df_worst)

            print(report)
            print(report_best)
            print(report_worst)

            if len(df_best):
                webbrowser.open(df_best.iloc[-1]['url'], new=2)

        else:
            print('--- no data ---')

        print(f'started: {now}')
        print(f'total: {total}')
        print(f'interval: {self.interval}')
        print(f'db_load: {time_db_load}')
        print(f'prediction: {time_prediction}')

    def make_prediction_ohlc_close(self, x_df):
        x_df_expanded = np.expand_dims(x_df, axis=0)

        y = self.model.predict(x_df_expanded, verbose=0)

        df = pd.DataFrame(0, index=np.arange(len(y[0])), columns=x_df.keys())

        df['close'] = y[0]

        y_inverse = self.scaler.inverse_transform(df)

        y_df = pd.DataFrame(y_inverse, None, x_df.keys())

        return y_df
