from service import klines
from parameters import assets, market, intervals
import json

k = klines.KLines()

start_at = '30 day ago UTC'

for interval in intervals:
    for asset in assets:
        sequence = k.build_klines(
            asset + market,
            interval,
            start_at
        )

        print(f'{asset} {interval}')

        text = json.dumps(sequence)

        file = open(f'out_klines/{asset}_{interval}.json', 'w')
        file.write(text)
        file.close()
