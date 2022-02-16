from binance import Client
import numpy as np


class KLines:
    def round(self, n: float, decimals=10):
        return np.round(float(n), decimals)

    def price_average(self, k: float):
        avg = (float(k[1]) + float(k[2]) + float(k[3]) + float(k[4])) / 4

        return self.round(avg)

    def build_klines(self, symbol: str, interval: str, start_str: str):
        client = Client()

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

        for i in range(1, len(klines)):
            c = klines[i]
            p = klines[i - 1]

            time_open = c[0] / 1000
            price_open = self.round(c[1], 10)
            price_close = self.round(c[3], 10)

            # --
            avg_current = self.price_average(c)
            avg_previous = self.price_average(p)
            avg_diff = self.round(avg_current - avg_previous)

            volume = self.round(float(p[5]), 1)
            volume_buy = self.round(volume - float(p[9]), 1)
            volume_sell = self.round(volume - volume_buy, 1)
            trades = self.round(float(p[8]), 0)

            item = {
                'time_open': time_open,
                'price_open': price_open,
                'price_close': price_close,
                'avg_current': avg_current,
                'avg_percentage': self.round(avg_diff * 100 / avg_current, 2),
                'volume': volume,
                'volume_buy': volume_buy,
                'volume_sell': volume_sell,
                'trades': trades,
            }

            collection.append(item)

        return collection
