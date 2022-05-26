import time
import tensorflow as tf
from yachalk import chalk
from datetime import datetime

from src.service.predictor_unseen import make_prediction
from src.parameters import market, assets, INTERVAL
from src.service.util import diff_percentage

interval = INTERVAL
start_time = time.time()

time_sec = 20

filepath_model = f'model/ta_{market}_BTC_{interval}.keras'
model = tf.keras.models.load_model(filepath_model)

while True:
    time.sleep(time_sec - ((time.time() - start_time) % time_sec))

    print('\n\n')
    print(datetime.now().strftime('%Y %m %d %H:%M:%S'))
    print("------------------------------------------------------------------------------------------")

    for asset in assets:
        x_df_open, y_df_open = make_prediction(market, asset, INTERVAL, model)

        # Measure
        # ------------------------------------------------------------------------

        last_real = x_df_open['open'].tail(1).values[0]
        tail = y_df_open['open'].tail(2).values

        last = tail[0]
        prediction = tail[1]

        diff = diff_percentage(prediction=prediction, last=last)

        print(f'asset: {asset}')
        print(f'real: {last_real} prediction: {last} -> {prediction}')

        if diff > 0.05:
            print(chalk.green(f'diff: {diff}%'))
        elif diff < -0.05:
            print(chalk.red(f'diff: {diff}%'))
        else:
            print(f'diff: {diff}%')
