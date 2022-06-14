import numpy as np
import datetime
from binance import Client
from datetime import datetime

from src.parameters import API_KEY, API_SECRET
from src.service.util import diff_percentage


class KLines:
    def round(self, n: float, decimals=10):
        return np.round(float(n), decimals)

    def price_average(self, k: float):
        avg = (float(k[1]) + float(k[2]) + float(k[3]) + float(k[4])) / 4

        return self.round(avg)

    def build_klines(self, market: str, asset: str, interval: str, start_str: str):
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
            start_str=start_str
        )
        collection = []

        for current in klines:
            time_open = current[0] / 1000
            price_open = self.round(current[1], 10)
            price_high = self.round(current[2], 10)
            price_low = self.round(current[3], 10)
            price_close = self.round(current[4], 10)
            volume = self.round(float(current[5]), 1)
            time_close = current[6] / 1000

            quote_asset_volume = self.round(float(current[7]), 0)
            trades = self.round(float(current[8]), 0)
            volume_maker = self.round(float(current[9]), 0)
            volume_taker = self.round(volume - volume_maker, 1)

            avg_current = self.price_average(current)
            date = datetime.utcfromtimestamp(time_open)

            item = {
                'price_open': price_open,
                'price_high': price_high,
                'price_low': price_low,
                'price_close': price_close,

                'time_open': time_open,
                'time_close': time_close,

                'time_month': date.month,
                'time_hour': date.hour,
                'time_day': date.day,
                'time_minute': date.minute,

                'avg_current': avg_current,
                'avg_percentage': diff_percentage(price_close, price_open),

                'trades': trades,
                'volume': volume,
                'volume_taker': volume_taker,
                'volume_maker': volume_maker,

                'quote_asset_volume': quote_asset_volume,
            }

            collection.append(item)

        return collection
