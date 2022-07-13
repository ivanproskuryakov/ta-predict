import datetime
from datetime import datetime

from src.service.util import diff_percentage, round


def build_klines(k: {}):
    time_open = k['t'] / 1000
    price_open = round(k['o'], 10)
    price_high = round(k['c'], 10)
    price_low = round(k['h'], 10)
    price_close = round(k['l'], 10)
    volume = round(float(k['v']), 1)
    time_close = k['T'] / 1000

    quote_asset_volume = round(float(k['q']), 0)
    trades = round(float(k['n']), 0)

    volume_taker = round(float(k['V']), 1) # Taker buy base asset volume
    volume_maker = round(volume - volume_taker, 0)

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

    return item
