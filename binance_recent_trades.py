import requests
import pandas as pd
import sys

from tabulate import tabulate

# https://binance-docs.github.io/apidocs/spot/en/#order-book

asset = sys.argv[1]

response = requests.get(f'https://www.binance.com/api/v3/depth?symbol={asset}USDT')

data = response.json()

headers = [
    "bid price",
    "bid qty",
    "-",
    "ask price",
    "ask qty",
]

df = pd.DataFrame(data['bids'])
df_bid = pd.DataFrame(data['asks'])

df[4] = df_bid[0]
df[5] = df_bid[1]

print(tabulate(df.values, headers, tablefmt="simple", numalign="right"))
