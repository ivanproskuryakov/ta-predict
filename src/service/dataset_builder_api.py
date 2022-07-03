import pandas as pd
import concurrent.futures

from src.service.estimator import estimate_ta_fill_na
from src.service.klines import KLines
from src.service.util import diff_percentage


def build_dataset_full(
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
    )

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


def build_dataset_down(market: str, asset: str, interval: str, start_at: str) -> pd.DataFrame:
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


def build_dataset_btc(market: str, asset: str, interval: str, start_at: str) -> pd.DataFrame:
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


def data_load_down(assets_down: list[str], market: str, interval: str, start_at: str):
    res = []
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for asset in assets_down:
            futures.append(
                executor.submit(
                    build_dataset_down,
                    market, asset, interval, start_at,
                )
            )

        for i in range(len(assets_down)):
            data = futures[i].result()
            res.append(data)

    df_final = pd.concat(res, axis=1)

    return df_final


def data_load_btc(assets_btc: list[str], market: str, interval: str, start_at: str):
    res = []
    futures = []

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for asset in assets_btc:
            futures.append(
                executor.submit(
                    build_dataset_btc,
                    market, asset, interval, start_at,
                )
            )

        for i in range(len(assets_btc)):
            data = futures[i].result()
            res.append(data)

    df_final = pd.concat(res, axis=1)

    return df_final


def build_dataset_all(
        assets: list[str],
        assets_down: list[str],
        assets_btc: list[str],
        market: str,
        interval: str
) -> list:
    res = []
    futures = []
    start_at = '1 week ago UTC'

    df_down = data_load_down(assets_down, market=market, interval=interval, start_at=start_at)
    df_btc = data_load_btc(assets_btc, market=market, interval=interval, start_at=start_at)

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for asset in assets:
            futures.append(
                executor.submit(
                    build_dataset_full,
                    market, asset, interval, start_at, df_down, df_btc
                )
            )

        for i in range(len(assets)):
            data, last_item = futures[i].result()
            res.append((assets[i], data, last_item))

    return res

# file = open('data/ohlc.json', 'w')
# file.write(json.dumps(collection))
#
# file = open('data/ohlc.json', 'r')
# collection = json.loads(file.read())
