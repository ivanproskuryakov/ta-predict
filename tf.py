import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

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


# Sets preparation
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

y_train = y_data[0:num_train]
y_test = y_data[num_train:]

num_x_signals = x_data.shape[1]
num_y_signals = y_data.shape[1]


# Scaling
# ------------------------------------------------------------------------

print('num train', num_train)
print('num test', num_test)
print('num all', len(x_train) + len(x_test))

print('signals', num_x_signals, num_y_signals)

x_scaler = MinMaxScaler()
x_train_scaled = x_scaler.fit_transform(x_train)
x_test_scaled = x_scaler.transform(x_test)

y_scaler = MinMaxScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)

print("X Min:", np.min(x_train))
print("X Max:", np.max(x_train))

print("X Min scaled train:", np.min(x_train_scaled))
print("X Max scaled train:", np.max(x_train_scaled))

print("X Min text train:", np.min(x_test_scaled))
print("X Max text train:", np.max(x_test_scaled))

print("Y Min:", np.min(y_train))
print("Y Max:", np.max(y_train))

print("Y Min scaled train:", np.min(y_train_scaled))
print("Y Max scaled train:", np.max(y_train_scaled))

print("Y Min text train:", np.min(y_train_scaled))
print("Y Max text train:", np.max(y_train_scaled))


# Data Generator
# ------------------------------------------------------------------------

print('X shape trained', x_train_scaled.shape)
print('Y shape trained', y_train_scaled.shape)


def batch_generator(batch_size, sequence_length):
    """
    Generator function for creating random batches of training-data.
    """

    # Infinite loop.
    while True:
        # Allocate a new array for the batch of input-signals.
        x_shape = (batch_size, sequence_length, num_x_signals)
        x_batch = np.zeros(shape=x_shape, dtype=np.float16)

        # Allocate a new array for the batch of output-signals.
        y_shape = (batch_size, sequence_length, num_y_signals)
        y_batch = np.zeros(shape=y_shape, dtype=np.float16)

        # Fill the batch with random sequences of data.
        for i in range(batch_size):
            # Get a random start-index.
            # This points somewhere into the training-data.
            idx = np.random.randint(num_train - sequence_length)

            # Copy the sequences of data starting at this index.
            x_batch[i] = x_train_scaled[idx:idx + sequence_length]
            y_batch[i] = y_train_scaled[idx:idx + sequence_length]

        yield (x_batch, y_batch)



batch_size = 256
sequence_length = int(24 * 60 / 5) # 1 day

generator = batch_generator(batch_size=batch_size, sequence_length=sequence_length)

x_batch, y_batch = next(generator)

# print(sequence_length)
# print(len(x_batch))
# print(len(y_batch))
# print(x_batch)

# print(x_batch.shape)
# print(y_batch.shape)


batch = 0   # First sequence in the batch.
signal = 0  # First signal from the 20 input-signals.

seq = x_batch[batch, :, signal]
plt.plot(seq)
seq = y_batch[batch, :, signal]
plt.plot(seq)

plt.show()


# Validation Set
# ------------------------------------------------------------------------

validation_data = (np.expand_dims(x_test_scaled, axis=0), np.expand_dims(y_test_scaled, axis=0))