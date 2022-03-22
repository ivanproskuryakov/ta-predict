from service import reader
from binance import Client
from yachalk import chalk
from datetime import datetime
import numpy as np

interval = Client.KLINE_INTERVAL_5MINUTE
asset = 'ETH'

reader = reader.Reader()
collection = reader.read(asset, interval)

magnitude_positive = 0
magnitude_negative = 0
percentage_positive = 0
percentage_negative = 0
negative = 0
median = len(collection) / 2

for sequence in collection:
    is_positive = sequence[0]
    time = datetime.utcfromtimestamp(sequence[1][0]['time_open'])
    sum = 0
    percentage = []

    for item in sequence[1]:
        sum = sum + item['avg_percentage']
        percentage.append(item['avg_percentage'])

    if is_positive:
        magnitude_positive = magnitude_positive + (len(sequence[1]))
        percentage_positive = percentage_positive + sum
        print(
            time,
            percentage,
            chalk.green(f'{np.round(sum, 2):.2f}'),
        )
    else:
        magnitude_negative = magnitude_negative + (len(sequence[1]))
        percentage_negative = percentage_negative + sum
        print(
            time,
            percentage,
            chalk.red(f'{np.round(sum, 2):.2f}'),
        )

print(
    magnitude_positive,
    magnitude_positive / median,
    percentage_positive,
    percentage_positive / median,
)
print(
    magnitude_negative,
    magnitude_negative / median,
    percentage_negative,
    percentage_negative / median,
)
