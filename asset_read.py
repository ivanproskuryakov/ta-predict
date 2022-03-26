import numpy as np

from service import reader
from binance import Client
from yachalk import chalk
from datetime import datetime
from parameters import NEGATIVE_PEAK

asset = 'ROSE'
interval = Client.KLINE_INTERVAL_5MINUTE

reader = reader.Reader()
collection = reader.read(
    asset,
    interval
)

positive = {
    "peak": 5,
    "percentage": 0,
    "percentage_max": 0,
    "magnitude": 0,
    "magnitude_max": 0,
    "sequence": 0,
    "sequence_max": 0,
}
negative = {
    "peak": 6,
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

trades = []
trade = None

for sequence in collection:
    seq_len = len(sequence[1])
    percentage_sum = 0
    percentage = []

    if seq_len:
        is_positive = sequence[0]
        time = datetime.utcfromtimestamp(sequence[1][0]['time_open'])

        # -----------------------------------

        for item in sequence[1]:
            percentage_sum = percentage_sum + item['avg_percentage']
            percentage.append(item['avg_percentage'])

            if is_positive:
                if positive["percentage_max"] < item['avg_percentage']:
                    positive["percentage_max"] = item['avg_percentage']
                if positive["magnitude_max"] < seq_len:
                    positive["magnitude_max"] = seq_len
            else:
                if negative["percentage_max"] > item['avg_percentage']:
                    negative["percentage_max"] = item['avg_percentage']
                if negative["magnitude_max"] < seq_len:
                    negative["magnitude_max"] = seq_len

        # -----------------------------------

        if is_positive:
            positive["magnitude"] = positive["magnitude"] + seq_len
            positive["percentage"] = positive["percentage"] + percentage_sum
            last_hour_plus = last_hour_plus + percentage_sum

            print(
                time,
                percentage,
                chalk.green(f'{np.round(percentage_sum, 2):.2f}'),
            )

            if trade:
                trade["percentage"] = trade["percentage"] + percentage_sum

                if trade["percentage"] >= trade["percentage_sell"]:
                    print(chalk.green(
                        '\t\t\t\t -------------------- SELL --------------------- \t',
                        f'{trade["percentage"]:.2f}',
                        f'{trade["percentage_sell"]:.2f}',
                        f'{trade["price_open"]:.10f}',
                        f'{item["price_open"]:.10f}',
                    ))
                    trade = None

        else:
            negative["magnitude"] = negative["magnitude"] + seq_len
            negative["percentage"] = negative["percentage"] + percentage_sum
            last_hour_minus = last_hour_minus + percentage_sum

            print(
                time,
                percentage,
                chalk.red(f'{np.round(percentage_sum, 2):.2f}')
            )

            if seq_len >= NEGATIVE_PEAK:
                trades.append([percentage_sum, item["price_open"]])
                trade = {
                    "percentage": percentage_sum,
                    "percentage_sell": abs(percentage_sum * 1),
                    "price_open": item['price_open'],
                }

                print(chalk.red(
                    '\t\t\t\t -------------------- BUY --------------------- \t',
                    f'{percentage_sum:.2}',
                    f'{item["price_open"]:.10f}',
                ))

        # -----------------------------------

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
print('\n')
print('Tades')
print('-----------------')
print(len(trades))
print(len(trades) / 180)
