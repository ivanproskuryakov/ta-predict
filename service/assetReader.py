from yachalk import chalk
import numpy as np
from datetime import datetime
import json

asset = 'ADA'
interval = '5m'

with open(f'out_klines/{asset}_{interval}.json') as f:
    data = f.read()
    collection = json.loads(data)
    f.close()

threshold = 0.1
total = len(collection)

print(f'{asset} {interval} {total}')
print(f'--------------------------')

overall = ''
negative = []
positive = []
total = len(collection)


def append(collection: [], item: float):
    if len(collection) == 0:
        collection.append([])

    l = len(collection) - 1
    collection[l].append(item)


for i in range(1, total):
    time = collection[i]['time_open']
    item = collection[i]
    item_previous = collection[i - 1]

    percentage = float(item['avg_percentage'])
    percentage_previous = float(item_previous['avg_percentage'])
    # volume = float(item['volume'])
    # volume_taker = int(item['volume_taker'])
    # volume_maker = int(item['volume_maker'])
    # trades = int(item['trades'])
    change = f'{percentage:.1f}'

    if percentage > threshold:
        if percentage_previous < 0:
            positive.append([])
        change = chalk.green(f'{percentage:.1f}')
        append(positive, item)

    if percentage < threshold:
        if percentage_previous > 0:
            negative.append([])
        change = chalk.red(f'{percentage:.1f}')
        append(negative, item)

    overall += f'{change} '