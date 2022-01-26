import numpy
import talib
from talib import MA_Type

close = numpy.random.random(100)
upper, middle, lower = talib.BBANDS(close, matype=MA_Type.T3)
# output = talib.SMA(close)

output = talib.MOM(close, timeperiod=5)

# print(upper)
# print('--------')
# print(middle)
# print('--------')
# print(lower)
print(output)
