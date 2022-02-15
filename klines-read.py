from datetime import datetime
from yachalk import chalk
from parameters import assets
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

for p in assets:
    line += f'{p} \t'

print(line)

threshold = 2

for i in range(len(collections[0])):
    time = collections[0][i]['time_open']
    line = f'\n ' \
           f'{datetime.utcfromtimestamp(time).strftime("%Y-%m-%d")} \t'

    for p in range(len(assets)):
        value = float(collections[p][i]['avg_percentage'])
        text = f'{value:.1f}'

        if value > threshold:
            text = chalk.green(f'{value:.1f}')
        if value < -threshold:
            text = chalk.red(f'{value:.1f}')

        line += f'{text} \t'

    print(line)
