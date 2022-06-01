import time
import tensorflow as tf

from datetime import datetime
from binance import Client
from src.service.predictor_unseen import data_load_all, make_prediction
from src.service.util import diff_percentage, paint_diff
from src.parameters import market, assets

interval = Client.KLINE_INTERVAL_30MINUTE
start_time = time.time()

model = tf.keras.models.load_model('model/ta_USDT_5m.keras')

print(interval)
print(datetime.now().strftime('%Y %m %d %H:%M:%S'))
print("------------------------------------------------------------------------------------------")

data = data_load_all(assets=assets, market=market, interval=interval)

for x_df in data:
    x_df_open, y_df_open = make_prediction(x_df, model)

    # Measure
    # ------------------------------------------------------------------------

    last_real = x_df_open['open'].tail(1).values[0]
    tail = y_df_open['open'].tail(2).values

    last = tail[0]
    prediction = tail[1]

    diff = diff_percentage(v2=prediction, v1=last)

    print(f''
          f'{paint_diff(diff)} \t |'
          f'{last_real:.4f} \t | '
          f'{last:.6f} -> {prediction:.6f} \t | '
          f'')

    if diff > 1 or diff < -1:
        print(x_df_open.tail(1))

print(datetime.now().strftime('%Y %m %d %H:%M:%S'))
print("------------------------------------------------------------------------------------------")
