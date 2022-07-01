import pandas as pd

from datetime import datetime
from src.repository.ohlc_repository import OhlcRepository
from src.service.util import diff_percentage
from src.service.util import round


def crate_ohlc_many(asset: str, market: str, interval: str, quantity: int) -> pd.DataFrame:
    ohlc_repository = OhlcRepository()

    collection = []
    time_open = 1650011400
    time_close = 1650011400

    for i in range(quantity):
        price_open = round(10000, 10)
        price_high = round(10000, 10)
        price_low = round(10000, 10)
        price_close = round(10000, 10)

        volume = round(10000, 0)
        quote_asset_volume = round(10000, 0)
        trades = round(10000, 0)
        volume_maker = round(10000, 0)
        volume_taker = round(10000, 0)

        date = datetime.utcfromtimestamp(time_open)

        item = {
            'price_open': price_open,
            'price_high': price_high,
            'price_low': price_low,
            'price_close': price_close,
            'price_diff': diff_percentage(price_close, price_open),

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
