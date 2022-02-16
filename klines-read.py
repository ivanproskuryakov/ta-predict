from datetime import datetime
from yachalk import chalk
from parameters import assets
import numpy as np
import json


start_at = '20 days ago UTC'
market = 'BTC'
collections = []

for p in assets:
    with open('out_klines/' + p + '.json') as f:
        data = f.read()
        collection = json.loads(data)
        f.close()
        collections.append(collection)

line = f' -- date -- \t'

for a in assets:
    line += f'{a} \t'

print(line)

threshold = 0
total = len(collections[0])

for i in range(total):
    time = collections[0][i]['time_open']
    line = f'\n ' \
           f'{datetime.utcfromtimestamp(time).strftime("%Y-%m-%d")} \t'

    for a in range(len(assets)):
        item = collections[a][i]

        percentage = float(item['avg_percentage'])
        volume = float(item['volume'])
        volume_buy = float(item['volume_buy'])
        volume_sell = float(item['volume_sell'])
        trades = float(item['trades'])
        change = f'{percentage:.1f}'

        if percentage > threshold:
            change = chalk.green(f'{percentage:.1f}')
        if percentage < -threshold:
            change = chalk.red(f'{percentage:.1f}')

        line += f'{change} {volume}|{volume_buy}|{volume_sell}|{trades} \t'

    print(line)

price_start = np.round(collections[0][0]['price_open'], 10)
price_end = np.round(collections[0][total-1]['price_open'], 10)

print(f'{price_start:.10f}')
print(f'{price_end:.10f}')
