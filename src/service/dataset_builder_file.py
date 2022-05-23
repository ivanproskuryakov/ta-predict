import json
import pandas as pd

from src.service.estimator import estimate_ta_fill_na


def build_dataset(market: str, asset: str, interval: str):
    path = f'unseen/{market}_{asset}_{interval}.json'

    with open(path) as f:
        data = f.read()
        collection = json.loads(data)
        f.close()

    prepared = []

    for i in range(0, len(collection)):
        prepared.append([
            collection[i]['price_open'],
            collection[i]['price_high'],
            collection[i]['price_low'],
            collection[i]['price_close'],

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

    return df
