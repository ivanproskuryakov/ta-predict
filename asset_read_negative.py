import numpy as np

from yachalk import chalk
from datetime import datetime
from service import reader

negative = reader.negative

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