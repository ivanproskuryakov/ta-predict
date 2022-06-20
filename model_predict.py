import sys
import tensorflow as tf

from src.service.predictor_unseen import data_load_parallel_all, make_prediction_ohlc_close

from src.parameters import market, assets
from src.service.reporter import render_console_table

interval = sys.argv[1]

model = tf.keras.models.load_model('model/ta.keras')

print(interval)
print("------------------------------------------------------------------------------------------")

items = data_load_parallel_all(assets=assets, market=market, interval=interval)

report = []

for item in items:
    asset, x_df, last_item = item

    y_df = make_prediction_ohlc_close(x_df, model)

    report.append((asset, last_item, x_df, y_df))

render_console_table(report)
