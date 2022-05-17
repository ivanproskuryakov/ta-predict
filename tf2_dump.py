from service.klines import KLines
import json

from parameters import intervals

# 1440 - 1 minutes
# 480 - 3 minutes
# 288 - 5 minutes
# 96 - 15 minutes
# 48 - 30 minutes
# 24 - 1 hour
# 6 - 4 hour
# 2 - 12 hour
# 1 - 1 day

for interval in intervals:
    start_at = '24 hours ago UTC'
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
