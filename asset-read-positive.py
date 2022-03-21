from yachalk import chalk
import numpy as np
from datetime import datetime
from service import assetReader

positive = assetReader.positive

print('Positive')
print('-------------------------------------------------------------------------------------------------')
for sequence in positive:
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
        chalk.green(f'{np.round(sum, 2):.1f}'),
    )

print(len(positive))
