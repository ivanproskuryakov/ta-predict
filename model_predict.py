import sys
import tensorflow as tf
import numpy as np
import pandas as pd
from datetime import datetime

from src.parameters_usdt import market, assets
from src.service.reporter import Reporter
from src.service.trade_finder import TradeFinder
from src.service.predictor_unseen import data_load_parallel_all, make_prediction_ohlc_close

# --------

np.set_printoptions(precision=4)
pd.set_option("display.precision", 4)

reporter = Reporter()
trade_finder = TradeFinder()

interval = sys.argv[1]
start_at = datetime.now()
data = []

# --------

model = tf.keras.models.load_model('model/ta.keras')

collection = data_load_parallel_all(
    assets=assets,
    market=market,
    interval=interval
)

time_download = datetime.now() - start_at

for item in collection:
    asset, x_df, last_item = item

    y_df = make_prediction_ohlc_close(x_df, model)

    data.append((asset, last_item, x_df, y_df))

time_prediction = datetime.now() - start_at

# --------

df = reporter.report_build(data=data)
report = reporter.report_prettify(df)
best = trade_finder.pick_best_option(df)

print(report)
print(f'start: {start_at}')
print(f'interval: {interval}')
print(f'download: {time_download}')
print(f'prediction: {time_prediction}')
