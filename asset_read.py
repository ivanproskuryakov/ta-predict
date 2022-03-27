import numpy as np

from service import reader
from binance import Client
from yachalk import chalk
from datetime import datetime

asset = 'ROSE'
interval = Client.KLINE_INTERVAL_1MINUTE

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
    totals = {
        "trades": 0,
        "percentage": 0,
    }
    percentage = []

    if seq_len:
        is_positive = sequence[0]
        time = datetime.utcfromtimestamp(sequence[1][0]['time_open'])

        # -----------------------------------

        for item in sequence[1]:
            totals["percentage"] = totals["percentage"] + item['avg_percentage']
            totals["trades"] = totals["trades"] + item['trades']
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

        if trade:
            trade["percentage"] = trade["percentage"] + totals["percentage"]
            print(f'\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t{trade["percentage"]:.2f}')

            if trade["percentage"] > 0:
                print(chalk.green(
                    '\t\t\t\t -------------------- SELL --------------------- \t',
                    f'{trade["percentage"]:.2f}',
                    f'{trade["percentage_sell"]:.2f}',
                    f'{trade["price_open"]:.10f}',
                    f'{item["price_open"]:.10f}',
                ))
                trade = None

        # -----------------------------------

        if is_positive:
            positive["magnitude"] = positive["magnitude"] + seq_len
            positive["percentage"] = positive["percentage"] + totals["percentage"]
            last_hour_plus = last_hour_plus + totals["percentage"]

            print(
                time,
                percentage,
                chalk.green(f'{np.round(totals["percentage"], 2):.2f}'),
                f'{totals["trades"]:.0f}',
            )

        else:
            negative["magnitude"] = negative["magnitude"] + seq_len
            negative["percentage"] = negative["percentage"] + totals["percentage"]
            last_hour_minus = last_hour_minus + totals["percentage"]

            print(
                time,
                percentage,
                chalk.red(f'{np.round(totals["percentage"], 2):.2f}'),
                f'{totals["trades"]:.0f}',
            )

            if not trade and seq_len > 5 and totals["trades"] > 600:
                trades.append([totals["percentage"], item["price_open"]])
                trade = {
                    "percentage": totals["percentage"],
                    "percentage_sell": abs(totals["percentage"]),
                    "price_open": item['price_open'],
                }

                print(chalk.red(
                    '\t\t\t\t -------------------- BUY --------------------- \t',
                    f'{totals["percentage"]:.2}',
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
# print(len(trades) / 180)
