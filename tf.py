import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from binance import Client

from keras.models import Sequential
from keras.optimizer_v2.rmsprop import RMSprop
from keras.layers import Dense, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from keras.backend import square, mean

from service.dataset_builder import build_dataset

# Load data
# ------------------------------------------------------------------------

pd.options.display.precision = 12
np.set_printoptions(precision=12, suppress=True)

asset = 'ROSE'
interval = Client.KLINE_INTERVAL_5MINUTE
df = build_dataset(asset=asset, interval=interval)

target_names = [
    'open',
]

# Data preparation
# ------------------------------------------------------------------------

shift_steps = 5

x_data = df.values[:-shift_steps]  # cut tail, array size - 5
# y_data = df.shift(-shift_steps).values[:-shift_steps]
y_data = df.values[shift_steps:]  # cut head

print('---------------------------------')
print('HEAD')
print('df')
print(df.head(10))
print('x')
print(x_data[:10])
print('y')
print(y_data[:10])

print('TAIL')
print('df')
print(df.tail(10))
print('x')
print(x_data[-shift_steps:])
print('y')
print(y_data[-shift_steps:])

# print(len(df))
# print(len(x_data))
# print(len(y_data))
# exit()


train_split = 0.9
num_data = len(x_data)
num_train = int(train_split * num_data)
num_signals = x_data.shape[1]

x_train = x_data[0:num_train]
x_test = x_data[num_train:]

y_train = y_data[0:num_train]
y_test = y_data[num_train:]

# Data Scaling
# ------------------------------------------------------------------------

x_scaler = MinMaxScaler()
x_train_scaled = x_scaler.fit_transform(x_train)
x_test_scaled = x_scaler.transform(x_test)

y_scaler = MinMaxScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)


# Data Generator
# ------------------------------------------------------------------------

def batch_generator(batch_size, sequence_length):
    """
    Generator function for creating random batches of training-data.
    """

    # Infinite loop.
    while True:
        # Allocate a new array for the batch of input-signals.
        x_shape = (batch_size, sequence_length, num_signals)
        x_batch = np.zeros(shape=x_shape, dtype=np.float16)

        # Allocate a new array for the batch of output-signals.
        y_shape = (batch_size, sequence_length, num_signals)
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
sequence_length = int(24 * 60 / 5)  # 1 day
generator = batch_generator(batch_size=batch_size, sequence_length=sequence_length)

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
    GRU(units=50,
        return_sequences=True,
        input_shape=(None, num_signals,)
        )
)
model.add(Dense(num_signals, activation='sigmoid'))


# Loss Function
# ------------------------------------------------------------------------

def loss_mse_warmup(y_true, y_pred):
    warmup_steps = 50
    """
    Calculate the Mean Squared Error between y_true and y_pred,
    but ignore the beginning "warmup" part of the sequences.

    y_true is the desired output.
    y_pred is the model's output.
    """

    # The shape of both input tensors are:
    # [batch_size, sequence_length, num_signals].

    # Ignore the "warmup" parts of the sequences
    # by taking slices of the tensors.
    y_true_slice = y_true[:, warmup_steps:, :]
    y_pred_slice = y_pred[:, warmup_steps:, :]

    # These sliced tensors both have this shape:
    # [batch_size, sequence_length - warmup_steps, num_signals]

    # Calculate the Mean Squared Error and use it as loss.
    mse = mean(square(y_true_slice - y_pred_slice))

    return mse


# Compile Model
# ------------------------------------------------------------------------

optimizer = RMSprop(learning_rate=0.001)
model.compile(loss=loss_mse_warmup, optimizer=optimizer)
model.summary()

# Callback Functions
# ------------------------------------------------------------------------

callback_checkpoint = ModelCheckpoint(
    filepath='data/checkpoint_ta.keras',
    monitor='val_loss',
    verbose=1,
    save_weights_only=True,
    save_best_only=True
)
callback_early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    verbose=1
)
callback_tensorboard = TensorBoard(
    log_dir='data',
    histogram_freq=0,
    write_graph=False
)
callback_reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,
    min_lr=1e-4,
    patience=0,
    verbose=1
)

callbacks = [
    callback_early_stopping,
    callback_checkpoint,
    callback_tensorboard,
    callback_reduce_lr
]

# Train the Recurrent Neural Network
# ------------------------------------------------------------------------

model.fit(
    x=generator,
    epochs=10,
    steps_per_epoch=50,
    validation_data=validation_data,
    callbacks=callbacks
)

# Performance on Test-Set
# ------------------------------------------------------------------------

result = model.evaluate(
    x=np.expand_dims(x_test_scaled, axis=0),
    y=np.expand_dims(y_test_scaled, axis=0)
)

print("loss (test-set):", result)


# Generate Predictions
# ------------------------------------------------------------------------

def plot_comparison(start_idx, length, train=True):
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

        # Plot labels etc.
        plt.ylabel(target_names[signal])
        plt.legend()
        plt.show()


plot_comparison(start_idx=0, length=50000, train=True)
