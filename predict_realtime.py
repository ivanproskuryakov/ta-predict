import time
import tensorflow as tf
from yachalk import chalk
from datetime import datetime
from binance import Client

from src.service.predictor_unseen import make_prediction
from src.parameters import market, assets
from src.service.util import diff_percentage

interval = Client.KLINE_INTERVAL_30MINUTE
start_time = time.time()
time_sec = 60 * 15

model = tf.keras.models.load_model('model/ta_USDT_5m.keras')


def paint_diff(diff: float):
    color = f'{diff:.4f}%'

    if diff > 1:
        color = chalk.green(f'{diff:.4f}%')
    if diff < -1:
        color = chalk.red(f'{diff:.4f}%')

    return color


while True:
    print('\n\n')
    print(interval)
    print(datetime.now().strftime('%Y %m %d %H:%M:%S'))
    print("------------------------------------------------------------------------------------------")

    for asset in assets:
        x_df_open, y_df_open, last_item = make_prediction(market, asset, interval, model)

        date = datetime.fromtimestamp(last_item["time_open"])

        # Measure
        # ------------------------------------------------------------------------

        last_real = x_df_open['open'].tail(1).values[0]
        tail = y_df_open['open'].tail(2).values

        last = tail[0]
        prediction = tail[1]

        diff = diff_percentage(v2=prediction, v1=last)

        print(f''
              f'{asset}\t'
              f'{paint_diff(diff)} \t |'
              f'{last_real:.4f} \t | '
              f'{last:.6f} -> {prediction:.6f} \t | '
              f'{date.strftime("%Y %m %d %H:%M:%S")}'
              f'')

        if diff > 1 or diff < -1:
            print(last_item)

    time.sleep(time_sec - ((time.time() - start_time) % time_sec))
