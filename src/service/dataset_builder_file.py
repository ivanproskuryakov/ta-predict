import json
import pandas as pd
from datetime import datetime

from src.service.estimator import estimate_ta_fill_na


def build_dataset(market: str, asset: str, interval: str):
    path = f'unseen/{market}_{asset}_{interval}.json'

    with open(path) as f:
        data = f.read()
        collection = json.loads(data)
        f.close()

    prepared = []

    for i in range(0, len(collection)):
        time_open = collection[i]['time_open'] / 1000
        date = datetime.utcfromtimestamp(time_open)

        prepared.append([
            collection[i]['price_open'],
            collection[i]['price_high'],
            collection[i]['price_low'],
            collection[i]['price_close'],

            date.month,
            date.day,
            date.hour,
            date.minute,

            collection[i]['avg_percentage'],
            collection[i]['avg_current'],

            collection[i]['trades'],
            collection[i]['volume'],
            collection[i]['volume_taker'],
            collection[i]['volume_maker'],

            collection[i]['quote_asset_volume'],
            # datetime.utcfromtimestamp(collection[i]['time_open']),
        ])

    df_ohlc = pd.DataFrame(prepared, None, [
        'open',
        'high',
        'low',
        'close',

        'time_month',
        'time_day',
        'time_hour',
        'time_minute',

        'avg_percentage',
        'avg_current',

        'trades',
        'volume',
        'volume_taker',
        'volume_maker',

        'quote_asset_volume',
        # 'epoch',
    ])

    df = estimate_ta_fill_na(df_ohlc)

    # Sets preparation
    # --------------------------------------------------------

    # train_mean = df.mean()
    # train_std = df.std()
    #
    # df = (df - train_mean) / train_std

    return df
