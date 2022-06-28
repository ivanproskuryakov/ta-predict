import sys
import tensorflow as tf
import numpy as np
import pandas as pd

from src.parameters_usdt import market, assets
from src.service.reporter import render_console_table
from src.service.predictor_unseen import data_load_parallel_all, make_prediction_ohlc_close

np.set_printoptions(precision=4)
pd.set_option("display.precision", 4)

interval = sys.argv[1]

model = tf.keras.models.load_model('model/gru.keras')

print(interval)
print("------------------------------------------------------------------------------------------")

collection = data_load_parallel_all(assets=assets, market=market, interval=interval)

report = []

for data in collection:
    asset, x_df, last_item = data

    y_df = make_prediction_ohlc_close(x_df, model)

    report.append((asset, last_item, x_df, y_df))

render_console_table(report)
