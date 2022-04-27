import numpy as np
import sys

from yachalk import chalk
from datetime import datetime
from binance import Client

from service.reader import Reader
from service.estimator import trades_diff_total

# ----
asset = sys.argv[1]
interval = Client.KLINE_INTERVAL_5MINUTE
# ----

reader = Reader()
collection = reader.read(asset, interval)

positive = {
    "peak": 5,
    "percentage": 0,
    "percentage_max": 0,
    "sequence": 0,
    "sequence_max": 0,
}
negative = {
    "peak": 6,
    "percentage": 0,
    "percentage_max": 0,
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
        "volume": 0,
        "volume_taker": 0,
        "volume_maker": 0,
        "volume_taken": 0,
    }
    percentage = []

    if seq_len:
        is_positive = sequence[0]
        time = datetime.utcfromtimestamp(sequence[1][0]['time_open'])

        # -----------------------------------

        for item in sequence[1]:
            totals["trades"] = totals["trades"] + item['trades']
            totals["percentage"] = totals["percentage"] + item['avg_percentage']
            totals["volume"] = totals["volume"] + item['volume']
            totals["volume_taker"] = totals["volume_taker"] + item['volume_taker']
            totals["volume_maker"] = totals["volume_maker"] + item['volume_maker']
            totals["volume_taken"] = reader.volume_taken(totals)
            percentage.append(item['avg_percentage'])

        # -----------------------------------

        if is_positive:
            if positive["percentage_max"] < item['avg_percentage']:
                positive["percentage_max"] = item['avg_percentage']
            if positive["sequence_max"] < seq_len:
                positive["sequence_max"] = seq_len
        else:
            if negative["percentage_max"] > item['avg_percentage']:
                negative["percentage_max"] = item['avg_percentage']
            if negative["sequence_max"] < seq_len:
                negative["sequence_max"] = seq_len

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
                trades.append({
                    "buy": trade["price_open"],
                    "sell": item["price_open"],
                    "start": trade["time_open"],
                    "end": item["time_open"],
                })
                trade = None

        # -----------------------------------

        if is_positive:
            positive["sequence"] = positive["sequence"] + seq_len
            positive["percentage"] = positive["percentage"] + totals["percentage"]
            last_hour_plus = last_hour_plus + totals["percentage"]

            print(
                time,
                f'{totals["volume_taken"]:.0f}%',
                percentage,
                chalk.green(f'{np.round(totals["percentage"], 2):.2f}'),
                f'{totals["trades"]:.0f}',
                f'V{totals["volume"]:.0f} = T{totals["volume_taker"]:.0f} + M{totals["volume_maker"]:.0f}',
            )

        else:
            negative["sequence"] = negative["sequence"] + seq_len
            negative["percentage"] = negative["percentage"] + totals["percentage"]
            last_hour_minus = last_hour_minus + totals["percentage"]

            print(
                time,
                f'{totals["volume_taken"]:.0f}%',
                percentage,
                chalk.red(f'{np.round(totals["percentage"], 2):.2f}'),
                f'{totals["trades"]:.0f}',
                f'V{totals["volume"]:.0f} = T{totals["volume_taker"]:.0f} + M{totals["volume_maker"]:.0f}',
            )

            if not trade and totals["volume_taken"] < 15 and totals["trades"] > 100:
                trade = {
                    "percentage": totals["percentage"],
                    "percentage_sell": 0,
                    "price_open": item['price_open'],
                    "time_open": item['time_open'],
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
print(len(trades), f'{trades_diff_total(trades):.20f}')
