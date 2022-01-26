from binance import Client
from service import klines
import json

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

for p in pairs:
    sequence = k.build_klines(
        p + market,
        interval,
        start_at
    )

    text = json.dumps(sequence)

    file = open('out_klines/' + p + '.json', 'w')
    file.write(text)
    file.close()

    # print(sequence)
