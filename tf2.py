import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from binance import Client
from service.reader_ta import ReaderTA


# Load data
# ------------------------------------------------------------------------
asset = 'ROSE'
interval = Client.KLINE_INTERVAL_5MINUTE

reader = ReaderTA()
collection_original = reader.read(asset, interval)
collection = collection_original[-4000:]
prepared = []

for i in range(0, len(collection)):
    prepared.append([
        # datetime.utcfromtimestamp(collection[i]['time_open']),
        collection[i]['price_open'],
        # collection[i]['price_high'],
        # collection[i]['price_low'],
        # collection[i]['price_close'],
        # collection[i]['volume'],
        #
        # collection[i]['avg_percentage'],
        # collection[i]['trades'],
        # collection[i]['volume_taker'],
    ])

df = pd.DataFrame(prepared, None, [
    # 'date',
    'open',
    # 'high', 'low', 'close', 'volume',
    # 'avg_percentage', 'trades', 'volume_taker'
])
pd.options.display.precision = 12
np.set_printoptions(precision=12, suppress=True)


target_names = [
    'open',
    # 'high', 'low', 'close', 'volume'
]


# Data preparation and scaling
# ------------------------------------------------------------------------

shift_steps = 5

x_data = df.values[:-shift_steps] # cut tail, array size - 5
y_data = df.values[shift_steps:] # cut head


train_split = 0.9
num_data = len(x_data)
num_train = int(train_split * num_data)
num_signals = x_data.shape[1]

x_train = x_data[0:num_train]
x_test = x_data[num_train:]

y_train = y_data[0:num_train]
y_test = y_data[num_train:]


x_scaler = MinMaxScaler()
x_train_scaled = x_scaler.fit_transform(x_train)
x_test_scaled = x_scaler.transform(x_test)

y_scaler = MinMaxScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)
