import numpy as np
import talib as ta
import json

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
for p in pairs:
    with open('out_klines/' + p + '.json') as f:
        data = f.read()
        collection = json.loads(data)
        f.close()

    prices = []

    for item in collection:
        prices.append(item['price_close'])

    a = np.array(prices) * 10000

    out = ta.MACD(a, fastperiod=12, slowperiod=26, signalperiod=9)
    print(p)
    print('--------')
    print(out[0])