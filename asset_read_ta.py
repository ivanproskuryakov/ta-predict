import sys
import pandas as pd
import vendor.indicators as qtpylib

from binance import Client
from service.reader_ta import ReaderTA
from datetime import datetime
import talib.abstract as ta

# ----
asset = sys.argv[1]
interval = Client.KLINE_INTERVAL_5MINUTE
# ----

reader = ReaderTA()
collection = reader.read(asset, interval)
prepared = []

for i in range(0, len(collection)):
    prepared.append([
        datetime.utcfromtimestamp(collection[i]['time_open']),
        collection[i]['price_open'],
        collection[i]['price_high'],
        collection[i]['price_low'],
        collection[i]['price_close'],
        collection[i]['volume'],
    ])

df = pd.DataFrame(prepared, None, ['date', 'open', 'high', 'low', 'close', 'volume'])


adx = ta.ADX(df, timeperiod=14)
macd = ta.MACD(df)
rsi = ta.RSI(df, timeperiod=14)
bollinger = qtpylib.bollinger_bands(qtpylib.typical_price(df), window=20, stds=2)

print(adx)
print(macd)
print(rsi)