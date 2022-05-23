import json
import sys

from datetime import datetime
from yachalk import chalk

from src.parameters import assets as assets_available

assets = assets_available[0:23]
interval = sys.argv[1]
collections = []

for asset in assets:
    with open(f'out_klines/{asset}_{interval}.json') as f:
        data = f.read()
        collection = json.loads(data)
        f.close()
        collections.append(collection)

threshold = 0
total = len(collections[0])

line = f' -- date -- \t'

for i in range(len(assets)):
    line += f'{assets[i]} \t'

print(line)

for i in range(total):
    time = collections[0][i]['time_open']
    line = f'\n ' \
           f'{datetime.utcfromtimestamp(time).strftime("%Y-%m-%d")} \t'

    for a in range(len(assets)):
        item = collections[a][i]

        percentage = float(item['avg_percentage'])
        change = f'{percentage:.1f}'

        if percentage > threshold:
            change = chalk.green(f'{percentage:.1f}')
        if percentage < -threshold:
            change = chalk.red(f'{percentage:.1f}')

        line += f'{change} \t'

    print(line)