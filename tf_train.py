import numpy as np
import pandas as pd
import tensorflow as tf

from sklearn.preprocessing import MinMaxScaler

from keras.models import Sequential
from keras.layers import Dense, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau

from src.service.generator import batch_generator
from src.service.dataset_builder_db import build_dataset_multi_step

# Load data
# ------------------------------------------------------------------------

pd.options.display.precision = 30
np.set_printoptions(precision=30, suppress=True)

# Data load & train
# ------------------------------------------------------------------------

interval = '15m'
asset = 'BTC'
market = 'USDT'

df = build_dataset_multi_step(
    market=market,
    asset=asset,
    interval=interval
)

# exit()

df_num_signals = df.shape[1]

# Data preparation
# ------------------------------------------------------------------------

shift_steps = 3

x_data = df.values[:-shift_steps]  # cut tail, array size - 5
y_data = df.values[shift_steps:]  # cut head

num_data = len(x_data)
num_train = int(0.9 * num_data)

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


batch_size = 500
sequence_length = 50

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
        units=100,
        return_sequences=True,
        input_shape=(None, df_num_signals,)
    ),
    Dense(df_num_signals, activation='sigmoid'),
])

model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)
#
# model.compile(
#     loss=loss_mse_warmup,
#     optimizer=RMSprop(learning_rate=0.001)
# )

callback_checkpoint = ModelCheckpoint(
    filepath='data/checkpoint.keras',
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

# Training
# ------------------------------------------------------------------------

model.fit(
    x=generator,
    epochs=20,
    steps_per_epoch=20,
    validation_data=validation_data,
    callbacks=callbacks
)

model.save('data/tf.keras')

# Performance test
# ------------------------------------------------------------------------

result = model.evaluate(
    x=np.expand_dims(x_test_scaled, axis=0),
    y=np.expand_dims(y_test_scaled, axis=0)
)

print("loss (test-set):", result)
