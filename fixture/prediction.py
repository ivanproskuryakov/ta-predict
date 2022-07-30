import json
import pandas as pd


def load_predictions() -> list:
    assets = [
        'BTC',
        'ETH',
        'IOTA',
        'ONT',
        'TUSD',
        'XLM',
    ]
    data = []

    for asset in assets:
        file = open(f'fixture/prediction/prediction_{asset}_x_df.json', 'r')
        x_df = pd.DataFrame.from_dict(json.loads(file.read()))
        file = open(f'fixture/prediction/prediction_{asset}_y_df.json', 'r')
        y_df = pd.DataFrame.from_dict(json.loads(file.read()))
        # file = open(f'fixture/prediction/prediction_{asset}_last_item.json', 'r')
        # last_item = json.loads(file.read())

        data.append((asset, x_df, y_df))

    return data
