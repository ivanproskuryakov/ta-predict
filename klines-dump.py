from binance import Client
from service import klines
from parameters import assets
import json

k = klines.KLines()

interval = Client.KLINE_INTERVAL_1HOUR
start_at = '30 days ago UTC'
market = 'BTC'

for p in assets:
    sequence = k.build_klines(
        p + market,
        interval,
        start_at
    )

    print(f'{p}')

    text = json.dumps(sequence)

    file = open('out_klines/' + p + '.json', 'w')
    file.write(text)
    file.close()
