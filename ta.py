import numpy as np
import talib as ta
import pandas as pd

from parameters import assets

for asset in assets:
    df = pd.read_json('out_klines/' + asset + '.json')

    price_float = [float(x) for x in df.price_close]
    percentage_float = [float(x) for x in df.avg_percentage]

    price = np.array(price_float)
    percentage = np.array(percentage_float)

    MACD = ta.MACD(price, fastperiod=12, slowperiod=26, signalperiod=9)
    DEMA = ta.stream_DEMA(price)

    print(asset)
    print('--')
    print(percentage)
    print('--')
    print(price)
    print('--')
    print(ta.stream_BBANDS(price, timeperiod=90))
    print('--')
    print(DEMA)
    print('--')
    print(MACD[0])
    print('------------------------')

    # # print('------------------------')
    # # print(out[0])
    # # print(out[1])
    # print(out[2])