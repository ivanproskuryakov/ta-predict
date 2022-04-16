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
collection = reader.read(asset, interval)
prepared = []

for i in range(0, len(collection)):
    prepared.append([
        # datetime.utcfromtimestamp(collection[i]['time_open']),
        collection[i]['price_open'],
        collection[i]['price_high'],
        collection[i]['price_low'],
        collection[i]['price_close'],
        collection[i]['volume'],

        collection[i]['avg_percentage'],
        collection[i]['trades'],
        collection[i]['volume_taker'],
    ])

df = pd.DataFrame(prepared, None, [
    # 'date',
    'open', 'high', 'low', 'close', 'volume',
    'avg_percentage', 'trades', 'volume_taker'
])
pd.options.display.precision = 12


# ------------------------------------------------------------------------

shift_steps = int(24 * 60 / 5)
# shift_steps = 10

# Create a new data-frame with the time-shifted data.
df_targets = df.shift(-shift_steps)

# These are the input-signals:
x_data = df.values[0:-shift_steps]

# These are the output-signals (or target-signals):
y_data = df_targets.values[:-shift_steps]

num_data = len(x_data)
train_split = 0.9
num_train = int(train_split * num_data)
num_test = num_data - num_train

x_train = x_data[0:num_train]
x_test = x_data[num_train:]

num_x_signals = x_data.shape[1]
num_y_signals = y_data.shape[1]

print('-----------------------------')
print('num train', num_train)
print('num test', num_test)
print('num all', len(x_train) + len(x_test))

print(num_x_signals)
print(num_y_signals)

# ------------------------------------------------------------------------

print("Min:", np.min(x_train))
print("Max:", np.max(x_train))

x_scaler = MinMaxScaler()
x_train_scaled = x_scaler.fit_transform(x_train)
x_test_scaled = x_scaler.transform(x_test)

# print("Min scaled train:", np.min(x_train_scaled))
# print("Max scaled train:", np.max(x_train_scaled))
#
# print("Min text train:", np.min(x_test_scaled))
# print("Max text train:", np.max(x_test_scaled))


# y_scaler = MinMaxScaler()
# y_train_scaled = y_scaler.fit_transform(y_train)
# y_test_scaled = y_scaler.transform(y_test)