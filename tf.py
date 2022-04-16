import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from binance import Client
from service.reader_ta import ReaderTA
from keras.models import Sequential
from keras.optimizer_v2.rmsprop import RMSprop
from keras.layers import Input, Dense, GRU, Embedding
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from keras.backend import square, mean

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

target_names = ['open', 'high', 'low', 'close', 'volume']
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

validation_data = (
    np.expand_dims(x_test_scaled, axis=0),
    np.expand_dims(y_test_scaled, axis=0)
)


# Create the Recurrent Neural Network
# ------------------------------------------------------------------------
model = Sequential()
model.add(
    GRU(units=512,
      return_sequences=True,
      input_shape=(None, num_x_signals,)
    )
)
model.add(Dense(num_y_signals, activation='sigmoid'))


# Loss Function
# ------------------------------------------------------------------------

warmup_steps = 50

def loss_mse_warmup(y_true, y_pred):
    """
    Calculate the Mean Squared Error between y_true and y_pred,
    but ignore the beginning "warmup" part of the sequences.

    y_true is the desired output.
    y_pred is the model's output.
    """

    # The shape of both input tensors are:
    # [batch_size, sequence_length, num_y_signals].

    # Ignore the "warmup" parts of the sequences
    # by taking slices of the tensors.
    y_true_slice = y_true[:, warmup_steps:, :]
    y_pred_slice = y_pred[:, warmup_steps:, :]

    # These sliced tensors both have this shape:
    # [batch_size, sequence_length - warmup_steps, num_y_signals]

    # Calculat the Mean Squared Error and use it as loss.
    mse = mean(square(y_true_slice - y_pred_slice))

    return mse


# Compile Model
# ------------------------------------------------------------------------

optimizer = RMSprop(lr=1e-3)
model.compile(loss=loss_mse_warmup, optimizer=optimizer)
model.summary()


# Callback Functions
# ------------------------------------------------------------------------

path_checkpoint = 'data/checkpoint_ta.keras'
callback_checkpoint = ModelCheckpoint(filepath=path_checkpoint,
                                      monitor='val_loss',
                                      verbose=1,
                                      save_weights_only=True,
                                      save_best_only=True)

callback_early_stopping = EarlyStopping(monitor='val_loss',
                                        patience=5, verbose=1)

callback_tensorboard = TensorBoard(log_dir='data',
                                   histogram_freq=0,
                                   write_graph=False)

callback_reduce_lr = ReduceLROnPlateau(monitor='val_loss',
                                       factor=0.1,
                                       min_lr=1e-4,
                                       patience=0,
                                       verbose=1)

callbacks = [callback_early_stopping,
             callback_checkpoint,
             callback_tensorboard,
             callback_reduce_lr]


# Train the Recurrent Neural Network
# ------------------------------------------------------------------------
model.fit(x=generator,
          epochs=2,
          steps_per_epoch=10,
          validation_data=validation_data,
          callbacks=callbacks)


# Load Checkpoint
# ------------------------------------------------------------------------
try:
    model.load_weights(path_checkpoint)
except Exception as error:
    print("Error trying to load checkpoint.")
    print(error)


# Performance on Test-Set
# ------------------------------------------------------------------------

result = model.evaluate(x=np.expand_dims(x_test_scaled, axis=0),
                        y=np.expand_dims(y_test_scaled, axis=0))

print("loss (test-set):", result)

# If you have several metrics you can use this instead.
if False:
    for res, metric in zip(result, model.metrics_names):
        print("{0}: {1:.3e}".format(metric, res))


# Generate Predictions
# ------------------------------------------------------------------------

def plot_comparison(start_idx, length=100, train=True):
    """
    Plot the predicted and true output-signals.

    :param start_idx: Start-index for the time-series.
    :param length: Sequence-length to process and plot.
    :param train: Boolean whether to use training- or test-set.
    """

    if train:
        # Use training-data.
        x = x_train_scaled
        y_true = y_train
    else:
        # Use test-data.
        x = x_test_scaled
        y_true = y_test

    # End-index for the sequences.
    end_idx = start_idx + length

    # Select the sequences from the given start-index and
    # of the given length.
    x = x[start_idx:end_idx]
    y_true = y_true[start_idx:end_idx]

    # Input-signals for the model.
    x = np.expand_dims(x, axis=0)

    # Use the model to predict the output-signals.
    y_pred = model.predict(x)

    # The output of the model is between 0 and 1.
    # Do an inverse map to get it back to the scale
    # of the original data-set.
    y_pred_rescaled = y_scaler.inverse_transform(y_pred[0])

    # For each output-signal.
    for signal in range(len(target_names)):
        # Get the output-signal predicted by the model.
        signal_pred = y_pred_rescaled[:, signal]

        # Get the true output-signal from the data-set.
        signal_true = y_true[:, signal]

        # Make the plotting-canvas bigger.
        plt.figure(figsize=(15, 5))

        # Plot and compare the two signals.
        plt.plot(signal_true, label='true')
        plt.plot(signal_pred, label='pred')

        # Plot grey box for warmup-period.
        p = plt.axvspan(0, warmup_steps, facecolor='black', alpha=0.15)

        # Plot labels etc.
        plt.ylabel(target_names[signal])
        plt.legend()
        plt.show()


plot_comparison(start_idx=100000, length=1000, train=True)