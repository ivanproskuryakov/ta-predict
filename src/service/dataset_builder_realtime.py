import pandas as pd

from src.service.estimator import estimate_ta_fill_na
from src.service.klines import KLines
from src.service.util import diff_percentage


def build_dataset(
        market: str, asset: str, interval: str, start_at: str,
        df_down: pd.DataFrame,
        df_btc: pd.DataFrame
):
    klines = KLines()
    prepared = []

    collection = klines.build_klines(
        market,
        asset,
        interval,
        start_at,
        # end_at
    )

    # file = open('data/ohlc.json', 'w')
    # file.write(json.dumps(collection))
    #
    # file = open('data/ohlc.json', 'r')
    # collection = json.loads(file.read())

    for item in collection:
        diff = diff_percentage(item['price_close'], item['price_open'])

        prepared.append([
            item['price_open'],
            item['price_high'],
            item['price_low'],
            item['price_close'],

            item['time_month'],
            item['time_day'],
            item['time_hour'],
            item['time_minute'],

            item['trades'],
            item['volume'],
            item['volume_taker'],
            item['volume_maker'],
            item['quote_asset_volume'],

            diff,
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

        'trades',
        'volume',
        'volume_taker',
        'volume_maker',
        'quote_asset_volume',

        'price_diff',
    ])

    df = pd.concat([df_ohlc, df_down, df_btc], axis=1)
    df = estimate_ta_fill_na(df)

    return df, item


def build_dataset_down(market: str, asset: str, interval: str, start_at: str):
    klines = KLines()
    prepared = []

    collection = klines.build_klines(
        market,
        asset,
        interval,
        start_at
    )

    for item in collection:
        prepared.append([
            item['price_open'],
            item['price_high'],
            item['price_low'],
            item['price_close'],

            item['trades'],
            item['volume'],
            item['volume_taker'],
            item['volume_maker'],
        ])

    df = pd.DataFrame(prepared, None, [
        f'open_{asset}',
        f'high_{asset}',
        f'low_{asset}',
        f'close_{asset}',

        f'trades_{asset}',
        f'volume_{asset}',
        f'volume_taker_{asset}',
        f'volume_maker_{asset}',
    ])

    return df


def build_dataset_btc(market: str, asset: str, interval: str, start_at: str):
    klines = KLines()
    prepared = []

    collection = klines.build_klines(
        market,
        asset,
        interval,
        start_at
    )

    for item in collection:
        prepared.append([
            item['price_open'],
            item['price_close'],

            item['trades'],
        ])

    df = pd.DataFrame(prepared, None, [
        f'open_{asset}',
        f'close_{asset}',

        f'trades_{asset}',
    ])

    return df
