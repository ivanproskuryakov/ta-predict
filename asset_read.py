from service import reader
from binance import Client
from yachalk import chalk
from datetime import datetime
import numpy as np

interval = Client.KLINE_INTERVAL_5MINUTE
asset = 'ADA'

reader = reader.Reader()
collection = reader.read(asset, interval)

magnitude_positive = 0
magnitude_negative = 0
percentage_positive = 0
percentage_negative = 0
negative = 0
median = len(collection) / 2

last_hour = 0
last_hour_plus = 0
last_hour_minus = 0

def is_last_hour(last_hour, hour):
    h = hour

    if hour == 0:
        h = 24

    diff = abs(last_hour - h)

    return diff == 4


for sequence in collection:
    if len(sequence[1]):
        is_positive = sequence[0]
        sum = 0
        percentage = []
        time = datetime.utcfromtimestamp(sequence[1][0]['time_open'])

        for item in sequence[1]:
            sum = sum + item['avg_percentage']
            percentage.append(item['avg_percentage'])

        if is_positive:
            magnitude_positive = magnitude_positive + (len(sequence[1]))
            percentage_positive = percentage_positive + sum
            last_hour_plus = last_hour_plus + sum
            print(
                time,
                percentage,
                chalk.green(f'{np.round(sum, 2):.2f}'),
            )
        else:
            magnitude_negative = magnitude_negative + (len(sequence[1]))
            percentage_negative = percentage_negative + sum
            last_hour_minus = last_hour_minus + sum
            print(
                time,
                percentage,
                chalk.red(f'{np.round(sum, 2):.2f}'),
            )


        if is_last_hour(last_hour, time.hour):
            print(f'{last_hour_plus:.2f} {last_hour_minus:.2f}')
            print(f'{last_hour_plus - (abs(last_hour_minus)):.2f}')
            print('')
            print('')
            last_hour = time.hour
            last_hour_plus = 0
            last_hour_minus = 0

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
