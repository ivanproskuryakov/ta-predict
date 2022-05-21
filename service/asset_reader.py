import json
import pandas as pd


def read_asset_file(path: str):
    with open(path) as f:
        data = f.read()
        collection = json.loads(data)
        f.close()

    prepared = []

    for i in range(0, len(collection)):
        prepared.append([
            # datetime.utcfromtimestamp(collection[i]['time_open']),
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
        ])

    df = pd.DataFrame(prepared, None, [
        # 'date',
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
    ])

    return df
