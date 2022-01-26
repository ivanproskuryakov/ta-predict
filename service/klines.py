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
        collection = []

        for i in range(1, len(klines)):
            c = klines[i]
            p = klines[i - 1]

            time_open = c[0] / 1000
            price_open = self.round(c[1])
            price_close = self.round(c[3])
            trades = p[8]

            # --
            avg_current = self.price_average(c)
            avg_previous = self.price_average(p)
            avg_diff = self.round(avg_current - avg_previous)

            item = {
                'time_open': time_open,
                'price_open': price_open,
                'avg_current': avg_current,
                'avg_percentage': self.round(avg_diff * 100 / avg_current, 2),
                'trades': trades,
            }

            collection.append(item)

        return collection
