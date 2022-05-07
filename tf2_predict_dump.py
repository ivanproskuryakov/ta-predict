from service.klines import KLines
import json
from binance import Client

interval = Client.KLINE_INTERVAL_1MINUTE
start_at = '1 hours ago UTC'
market = 'USDT'
asset = 'BTC'

klines = KLines()

sequence = klines.build_klines(
    market,
    asset,
    interval,
    start_at
)

text = json.dumps(sequence)

file = open(f'test/{market}_{asset}_{interval}.json', 'w')
file.write(text)
file.close()
