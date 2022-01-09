from binance import Client
from collections import OrderedDict

import numpy as np

class KLines:
    def round(self, n: float, decimals=10):
        return np.round(float(n), decimals)

    def price_average(self, k: float):
        avg = (float(k[1]) + float(k[2]) + float(k[3]) + float(k[4])) / 4

        return self.round(avg)

    def build_klines(self, symbol: str, interval: str, start_str: str):
        client = Client()
        klines = client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_str
        )
        collection = OrderedDict()

        diff_total = 0
        percentage_total = 0

        for i in range(1, len(klines)):
            c = klines[i]
            p = klines[i - 1]

            # --

            time_open = c[0] / 1000
            price_open = self.round(c[1])
            price_close = self.round(c[3])
            price_diff = self.round(price_close - price_open)
            price_diff_percentage = self.round(price_diff * 100 / price_close)
            # trades = p[8]

            # --

            avg_current = self.price_average(c)
            avg_previous = self.price_average(p)
            avg_diff = self.round(avg_current - avg_previous)
            avg_percentage = self.round(avg_diff * 100 / avg_current)

            diff_total += avg_diff
            percentage_total += avg_percentage

            collection[time_open] = [
                # price_diff,
                avg_percentage,
                # avg_diff,
                # avg_percentage,
            ]

        return collection