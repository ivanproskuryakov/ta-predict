from datetime import datetime
from yachalk import chalk
from parameters import assets
import numpy as np
import json


start_at = '20 days ago UTC'
collections = []

for a in assets:
    with open('out_klines/' + a + '.json') as f:
        data = f.read()
        collection = json.loads(data)
        f.close()
        collections.append(collection)

threshold = 1
total = len(collections[0])

line = f' -- date -- \t'

for i in range(len(assets)):
    price_start = np.round(collections[i][0]['price_open'], 10)
    price_end = np.round(collections[i][total - 1]['price_open'], 10)
    line += f'{assets[i]} \t'
    # line += f'{assets[i]} {price_start:.9f}{price_end:9f} \t'

print(line)


for i in range(total):
    time = collections[0][i]['time_open']
    line = f'\n ' \
           f'{datetime.utcfromtimestamp(time).strftime("%Y-%m-%d")} \t'

    for a in range(len(assets)):
        item = collections[a][i]

        percentage = float(item['avg_percentage'])
        volume = float(item['volume'])
        volume_taker = int(item['volume_taker'])
        volume_maker = int(item['volume_maker'])
        trades = int(item['trades'])
        change = f'{percentage:.1f}'

        if percentage > threshold:
            change = chalk.green(f'{percentage:.1f}')
        if percentage < -threshold:
            change = chalk.red(f'{percentage:.1f}')

        line += f'{change} \t'
        # line += f'{change} {volume}+{volume_taker}-{volume_maker},{trades} \t'

    print(line)