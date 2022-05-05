from service.klines import KLines
import json


def dump_many(market: str, assets: [], intervals: [], start_at: str):
    klines = KLines()

    for interval in intervals:
        for asset in assets:
            print(f'starting: {market} {asset} {interval}')

            sequence = klines.build_klines(
                market,
                asset,
                interval,
                start_at
            )

            print(f'dumping: {market} {asset} {interval}')

            text = json.dumps(sequence)

            file = open(f'out_klines/{market}/{asset}_{interval}.json', 'w')
            file.write(text)
            file.close()
