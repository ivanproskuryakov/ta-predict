from binance import Client
from service import klines
from datetime import datetime

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
        line += f'{collections[i][c][0]:.1f} \t'

    print(line)
