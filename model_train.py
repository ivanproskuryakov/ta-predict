import tensorflow as tf
import numpy as np

from keras.layers import Dense, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder_db import build_dataset_multi_step
from src.service.generator import batch_generator
from src.parameters import market

# Variables
# ------------------------------------------------------------------------
sequence_length = 100
shift_steps = 4
interval = '15m'
asset = 'BTC'

filepath_model = f'data/ta_{market}_{shift_steps}.keras'
filepath_checkpoint = f'data/ta_{market}_{shift_steps}.checkpoint'

print(f'training interval: {interval} {asset}')

# Data load & train
# ------------------------------------------------------------------------

df = build_dataset_multi_step(
    market=market,
    asset=asset,
    interval=interval
)

df_num_signals = df.shape[1]

# Model definition
# ------------------------------------------------------------------------

callback_early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    mode='min',
    verbose=1
)

callback_reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    min_lr=0.00001,
    patience=5,
    verbose=1,
)

callback_checkpoint = ModelCheckpoint(
    filepath=filepath_checkpoint,
    monitor='val_loss',
    verbose=1,
    save_weights_only=True,
    save_best_only=True
)
model = tf.keras.models.Sequential([
    GRU(
        units=500,
        return_sequences=True,
        input_shape=(None, df_num_signals)
    ),
    # LSTM(df_num_signals, return_sequences=False),
    # Dense(units=df_num_signals, activation='linear', input_dim=df_num_signals),
    # Dense(units=df_num_signals, activation='relu', input_dim=df_num_signals),
    Dense(units=1),
])

model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)

# Generator function
# --------------------------------------------------------
x_data = df.values[0:-shift_steps]
y_data = df.shift(-shift_steps).values[:-shift_steps]

num_data = len(x_data)

num_train = int(0.9 * num_data)

x_train = x_data[0:num_train]
x_validate = x_data[num_train:]

y_train = y_data[0:num_train]
y_validate = y_data[num_train:]

generator = batch_generator(x_data=x_data, y_data=y_data, batch_size=100, sequence_length=50)

# Generator function
# --------------------------------------------------------

model.fit(
    x=generator,
    epochs=20,
    steps_per_epoch=100,
    validation_data=(
        np.expand_dims(x_validate, axis=0),
        np.expand_dims(y_validate, axis=0)
    ),
    callbacks=[
        # callback_early_stopping,
        callback_reduce_lr,
        callback_checkpoint,
    ]
)

model.save(filepath_model)
