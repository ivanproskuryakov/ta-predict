import tensorflow as tf
import numpy as np
import pandas as pd

from keras.layers import Dense, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder_db import build_dataset
from src.service.generator import batch_generator_random
from src.parameters import market

pd.set_option("display.precision", 6)
np.set_printoptions(precision=6)

# Variables
# ------------------------------------------------------------------------
sequence_length = 50
shift_steps = 1
interval = '15m'
asset = 'BTC'

filepath_model = f'data/ta_{shift_steps}.keras'
filepath_checkpoint = f'data/ta_{shift_steps}.checkpoint'

print(f'training interval: {interval} {asset} {shift_steps}')

# Data load
# ------------------------------------------------------------------------

df = build_dataset(
    market=market,
    asset=asset,
    interval=interval
)

df_num_signals = df.shape[1]

x = df.shift(-shift_steps).iloc[:-shift_steps]
y = df.iloc[:-shift_steps]

# # print(df['open'].head(10))
# # print(df['open'].tail(10))
# print('x')
# # print(x.head(10))
# print(x.tail(10))
# # print(x[-10:, 0])
# print('y')
# # print(y.head(10))
# print(y.tail(10))
# # print(y[-10:, 0])
# print(len(x))
# print(len(y))
# exit()

num_train = int(0.9 * len(x))

x_train = x[0:num_train]
x_validate = x[num_train:]

y_train = y[0:num_train]
y_validate = y[num_train:]

# Generator function
# --------------------------------------------------------

generator = batch_generator_random(
    x_data=x_train,
    y_data=y_train,
    batch_size=100,
    sequence_length=sequence_length
)

# Model
# ------------------------------------------------------------------------

callback_early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=10,
    mode='min',
    verbose=1
)
callback_reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.3,
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
    Dense(units=df_num_signals, activation='sigmoid'),
])

model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)

model.fit(
    x=generator,
    epochs=10,
    steps_per_epoch=100,
    validation_data=(
        np.expand_dims(x_validate, axis=0),
        np.expand_dims(y_validate, axis=0)
    ),
    callbacks=[
        callback_early_stopping,
        callback_reduce_lr,
        callback_checkpoint,
    ]
)

model.save(filepath_model)
