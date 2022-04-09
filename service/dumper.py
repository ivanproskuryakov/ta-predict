from service.klines import KLines
from parameters import market
import json


class AssetDumper:
    def dumpMany(self, assets: [], intervals: [], start_at: str):
        klines = KLines()

        for interval in intervals:
            for asset in assets:
                sequence = klines.build_klines(
                    asset + market,
                    interval,
                    start_at
                )

                print(f'{asset} {interval}')

                text = json.dumps(sequence)

                file = open(f'out_klines/{asset}_{interval}.json', 'w')
                file.write(text)
                file.close()
