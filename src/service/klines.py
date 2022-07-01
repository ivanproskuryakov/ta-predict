import datetime
from binance import Client
from datetime import datetime

from src.parameters import API_KEY, API_SECRET
from src.service.util import diff_percentage, round


class KLines:
    def price_average(self, k: float):
        avg = (float(k[1]) + float(k[2]) + float(k[3]) + float(k[4])) / 4

        return round(avg)

    def build_klines(self, market: str, asset: str, interval: str, start_at: str, end_at: str):
        client = Client(
            api_key=API_KEY,
            api_secret=API_SECRET,
        )
        symbol = asset + market
        # Taker - an order that trades immediately before going on the order book
        # Maker - an order that goes on the order book partially or fully

        # 0 Open time,

        # 1 Open,
        # 2 High,
        # 3 Low,
        # 4 Close,
        # 5 Volume,

        # 6 Close time,

        # 7 Quote asset volume,
        # 8 Number of trades,
        # 9 Taker buy base asset volume,
        # 10 Taker buy quote asset volume,

        # 11 Ignore

        klines = client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_at,
            end_str=end_at,
        )
        collection = []

        for current in klines:
            time_open = current[0] / 1000
            price_open = round(current[1], 10)
            price_high = round(current[2], 10)
            price_low = round(current[3], 10)
            price_close = round(current[4], 10)
            volume = round(float(current[5]), 1)
            time_close = current[6] / 1000

            quote_asset_volume = round(float(current[7]), 0)
            trades = round(float(current[8]), 0)
            volume_maker = round(float(current[9]), 0)
            volume_taker = round(volume - volume_maker, 1)

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

        return collection
