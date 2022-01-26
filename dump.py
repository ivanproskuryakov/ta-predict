from binance import Client
from service import klines
from datetime import datetime
from yachalk import chalk

k = klines.KLines()
pairs = [
    "BNB",
    "ETH",
    "ADA",
    "SOL",
    "XRP",
    "DOT",
    "ATOM",
    "HBAR",
    "IOTA",
    "AVAX",

    "COTI",
    "NEAR",
    "BAT",
    "WAVES",
    "MINA",
    "EGLD",
    "XTZ",
    "ALGO",
    "LUNA",
    "KSM",
    "MATIC",
    "ONE",
    "ROSE",
]
interval = Client.KLINE_INTERVAL_1DAY
start_at = '30 days ago UTC'
market = 'BTC'

collections = []

for p in pairs:
    collection = k.build_klines(
        p + market,
        interval,
        start_at
    )
    collections.append(collection)

line = f' -- date -- \t'

for p in pairs:
    line += f'{p} \t'

print(line)

for c in collections[0]:
    line = f'\n ' \
           f'{datetime.utcfromtimestamp(c).strftime("%Y-%m-%d")} \t'

    for i in range(len(pairs)):
        value = float(collections[i][c][0])
        text = f'{value:.1f}'

        if value > 1:
            text = chalk.green(f'{value:.1f}')
        if value < -1:
            text = chalk.red(f'{value:.1f}')

        line += f'{text} \t'

    print(line)
