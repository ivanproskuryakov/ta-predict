import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler
from binance import Client

from keras.models import Sequential
from keras.optimizer_v2.rmsprop import RMSprop
from keras.layers import Dense, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau

from service.dataset_builder import build_dataset
from service.generator_batch import batch_generator
from service.loss import loss_mse_warmup

# Load data
# ------------------------------------------------------------------------

pd.options.display.precision = 30
np.set_printoptions(precision=30, suppress=True)

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
y_data = df.values[shift_steps:]  # cut head

num_data = len(x_data)
num_train = int(0.9 * num_data)
df_num_signals = x_data.shape[1]

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

print('------')
print(y_train_scaled)
print('------')
print(y_train_scaled[0])

# exit()

# Data Generator
# ------------------------------------------------------------------------


batch_size = 256
sequence_length = int(24 * 60 / 5)  # 1 day

generator = batch_generator(
    x_data=x_train_scaled,
    y_data=y_train_scaled,
    batch_size=batch_size,
    sequence_length=sequence_length,
)

# Validation Set
# ------------------------------------------------------------------------

validation_data = (
    np.expand_dims(x_test_scaled, axis=0),
    np.expand_dims(y_test_scaled, axis=0)
)

# Model
# ------------------------------------------------------------------------
model = Sequential([
    GRU(
        units=50,
        return_sequences=True,
        input_shape=(None, df_num_signals,)
    ),
    Dense(df_num_signals, activation='sigmoid'),
])

model.compile(
    loss=loss_mse_warmup,
    optimizer=RMSprop(learning_rate=0.001)
)

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
    epochs=2,
    steps_per_epoch=2,
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
