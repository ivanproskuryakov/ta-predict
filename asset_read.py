from service import reader
from binance import Client
from yachalk import chalk
from datetime import datetime
import numpy as np

asset = 'ROSE'
interval = Client.KLINE_INTERVAL_5MINUTE

reader = reader.Reader()
collection = reader.read(
    asset,
    interval
)

positive = {
    "percentage": 0,
    "percentage_max": 0,
    "magnitude": 0,
    "magnitude_max": 0,
    "sequence": 0,
    "sequence_max": 0,
}
negative = {
    "percentage": 0,
    "percentage_max": 0,
    "magnitude": 0,
    "magnitude_max": 0,
    "sequence": 0,
    "sequence_max": 0,
}

median = len(collection) / 2
last_hour = 0
last_hour_plus = 0
last_hour_minus = 0

for sequence in collection:
    sequence_len = len(sequence[1])
    sum = 0
    percentage = []

    if sequence_len:
        is_positive = sequence[0]
        time = datetime.utcfromtimestamp(sequence[1][0]['time_open'])

        for item in sequence[1]:
            sum = sum + item['avg_percentage']
            percentage.append(item['avg_percentage'])

            if is_positive:
                if positive["percentage_max"] < item['avg_percentage']:
                    positive["percentage_max"] = item['avg_percentage']
                if positive["magnitude_max"] < sequence_len:
                    positive["magnitude_max"] = sequence_len
            else:
                if negative["percentage_max"] > item['avg_percentage']:
                    negative["percentage_max"] = item['avg_percentage']
                if negative["magnitude_max"] < sequence_len:
                    negative["magnitude_max"] = sequence_len

        if is_positive:
            positive["magnitude"] = positive["magnitude"] + sequence_len
            positive["percentage"] = positive["percentage"] + sum
            last_hour_plus = last_hour_plus + sum

            print(
                time,
                percentage,
                chalk.green(f'{np.round(sum, 2):.2f}'),
            )
        else:
            negative["magnitude"] = negative["magnitude"] + sequence_len
            negative["percentage"] = negative["percentage"] + sum
            last_hour_minus = last_hour_minus + sum

            print(
                time,
                percentage,
                chalk.red(f'{np.round(sum, 2):.2f}'),
            )

        if reader.is_last_hour(last_hour, time.hour):
            print(f'{last_hour_plus:.2f} {last_hour_minus:.2f}')
            print(f'{last_hour_plus - (abs(last_hour_minus)):.2f}')
            print('')
            print('')
            last_hour = time.hour
            last_hour_plus = 0
            last_hour_minus = 0

print('\n')
print(asset, interval)
print('\n')
print('Positive')
print('-----------------')
print(positive)
print('\n')
print('Negative')
print('-----------------')
print(negative)
