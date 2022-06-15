import pandas as pd
import json
from datetime import datetime

from src.service.estimator import estimate_ta_fill_na
from src.service.klines import KLines
from src.service.util import diff_percentage


def build_dataset(market: str, asset: str, interval: str):
    klines = KLines()
    start_at = '1 week ago UTC'
    prepared = []

    # collection = klines.build_klines(
    #     market,
    #     asset,
    #     interval,
    #     start_at
    # )
    #
    # file = open('data/ohlc.json', 'w')
    # file.write(json.dumps(collection))

    file = open('data/ohlc.json', 'r')
    collection = json.loads(file.read())

    for item in collection:
        time_open = item['time_open'] / 1000
        date = datetime.utcfromtimestamp(time_open)
        diff = diff_percentage(item['price_close'], item['price_open'])

        prepared.append([
            item['price_open'],
            item['price_high'],
            item['price_low'],
            item['price_close'],

            # date.month,
            # date.day,
            # date.hour,
            # date.minute,

            # item['avg_percentage'],
            # item['avg_current'],

            item['trades'],
            item['volume'],
            item['volume_taker'],
            item['volume_maker'],
            item['quote_asset_volume'],

            diff,

            # datetime.utcfromtimestamp(item['time_open']),
        ])

    df_ohlc = pd.DataFrame(prepared, None, [
        'open',
        'high',
        'low',
        'close',

        # 'time_month',
        # 'time_day',
        # 'time_hour',
        # 'time_minute',

        # 'avg_percentage',
        # 'avg_current',

        'trades',
        'volume',
        'volume_taker',
        'volume_maker',
        'quote_asset_volume',

        'price_diff',
        # 'epoch',
    ])

    df = estimate_ta_fill_na(df_ohlc)

    return df, item
