import numpy as np

from yachalk import chalk
from datetime import datetime
from service import reader

asset = 'ADA'
interval = '1m'

reader = reader.Reader()
split = reader.read(asset, interval)
negative = split[0]

print('Negative')
print('-------------------------------------------------------------------------------------------------')
for sequence in negative:
    time_open = sequence[0]['time_open']
    time = datetime.utcfromtimestamp(time_open)

    sum = 0
    percentage = []
    for item in sequence:
        sum = sum + item['avg_percentage']
        percentage.append(item['avg_percentage'])

    print(
        time,
        percentage,
        chalk.red(f'{np.round(sum, 2):.1f}'),
    )

print(len(negative))