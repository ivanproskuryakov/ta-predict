import numpy as np
import time
from yachalk import chalk

from src.service.predictor_unseen import make_prediction
from src.parameters import market, ASSET, INTERVAL

asset = ASSET
interval = INTERVAL
starttime = time.time()

time_sec = 15

while True:
    print('\n\n\n')
    print("tick ....")

    time.sleep(time_sec - ((time.time() - starttime) % time_sec))

    x_df_open, y_df_open = make_prediction(market, ASSET, INTERVAL)

    # Measure
    # ------------------------------------------------------------------------

    last_real = x_df_open['open'].tail(1).values[0]
    tail = y_df_open['open'].tail(2).values

    last = tail[0]
    prediction = tail[1]

    diff = 100 * (prediction - last) / ((prediction + last) / 2)

    print(ASSET)
    print(f'real: {last_real}')
    print(f'prediction: {last} -> {prediction}')

    if diff > 0.05:
        print(chalk.green(f'diff: {diff}%'))
    elif diff < 0.05:
        print(chalk.red(f'diff: {diff}%'))
    else:
        print(f'diff: {diff}%')
