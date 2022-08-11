import pandas as pd

from datetime import datetime
from src.repository.ohlc_repository import OhlcRepository
from src.service.util import Utility


def crate_ohlc_many(asset: str, market: str, interval: str, price: float, quantity: int) -> pd.DataFrame:
    ohlc_repository = OhlcRepository()
    utility = Utility()

    collection = []
    time_open = 1650011400
    time_close = 1650011400

    for i in range(quantity):
        price_open = price + i
        price_high = price + i
        price_low = price + i
        price_close = price + i

        volume = 1 + i
        quote_asset_volume = 1
        trades = 1
        volume_maker = 1
        volume_taker = 1

        time_open = time_open + 5 * 60 * i
        time_close = time_close + 5 * 60 * i

        date = datetime.utcfromtimestamp(time_open)

        item = {
            'price_open': price_open,
            'price_high': price_high,
            'price_low': price_low,
            'price_close': price_close,
            'price_diff': utility.diff_percentage(price_close, price_open),

            'time_open': time_open,
            'time_close': time_close,

            'time_month': date.month,
            'time_hour': date.hour,
            'time_day': date.day,
            'time_minute': date.minute,

            'trades': trades,
            'volume': volume,
            'volume_taker': volume_taker,
            'volume_maker': volume_maker,

            'quote_asset_volume': quote_asset_volume,
        }

        collection.append(item)

    df = ohlc_repository.create_many(
        exchange='binance',
        market=market,
        asset=asset,
        interval=interval,
        collection=collection,
    )

    return df
