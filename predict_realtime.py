import time
import tensorflow as tf
from yachalk import chalk
from datetime import datetime
from binance import Client

from src.service.predictor_unseen import make_prediction
from src.parameters import market, assets
from src.service.util import diff_percentage

interval = Client.KLINE_INTERVAL_15MINUTE
start_time = time.time()
time_sec = 60 * 5

model = tf.keras.models.load_model('model/ta_USDT_BTC_1m.keras')

while True:
    time.sleep(time_sec - ((time.time() - start_time) % time_sec))

    print('\n\n')
    print(interval)
    print(datetime.now().strftime('%Y %m %d %H:%M:%S'))
    print("------------------------------------------------------------------------------------------")

    for asset in assets:
        x_df_open, y_df_open, last_item = make_prediction(market, asset, interval, model)

        date = datetime.utcfromtimestamp(last_item["time_open"])

        # Measure
        # ------------------------------------------------------------------------

        last_real = x_df_open['open'].tail(1).values[0]
        tail = y_df_open['open'].tail(2).values

        last = tail[0]
        prediction = tail[1]

        diff = diff_percentage(prediction=prediction, last=last)

        print(f'{asset} {last_real:.4f} | f{last:.4f} -> {prediction:.4f} | {date.strftime("%Y %m %d %H:%M:%S")}')

        if diff > 0.05:
            print(chalk.green(f'diff: {diff}%'))
        elif diff < -0.05:
            print(chalk.red(f'diff: {diff}%'))
        else:
            print(f'diff: {diff}%')
