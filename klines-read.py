import numpy as np
import talib
import json
from talib import MA_Type

p = 'BNB'

with open('out_klines/' + p + '.json') as f:
    data = f.read()
    collection = json.loads(data)
    f.close()

prices = []

for item in collection:
    prices.append(item['price_close'])
    # print(item['price_open'])

a = np.array(prices)

print(a)
print(prices)

# close = numpy.random.random(100)
#
# output = talib.SMA(a)
#
#
# print(close)
# print(prices)
# print(output)
# output = talib.MOM(a, timeperiod=5)

# print(a)
# print(output)
