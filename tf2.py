import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd

from binance import Client

from service.window_generator import WindowGenerator
from service.reader_ta import ReaderTA

# Data load
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
    'open',
    'high',
    'low',
    'close',

    'volume',
    'avg_percentage',
    'trades',
    'volume_taker'
])

print(len(df))

# Data split
# --------------------------------------------------------
n = len(df)
train_df = df[0:int(n * 0.7)]
val_df = df[int(n * 0.7):int(n * 0.9)]
test_df = df[int(n * 0.9):]

# Normalize the data
# --------------------------------------------------------

train_mean = train_df.mean()
train_std = train_df.std()

train_df = (train_df - train_mean) / train_std
val_df = (val_df - train_mean) / train_std
test_df = (test_df - train_mean) / train_std

# Generator function
# --------------------------------------------------------

window = WindowGenerator(
    input_width=30,
    label_width=30,
    shift=1,
    batch_size=256,
    label_columns=['open'],
    train_df=train_df,
    val_df=val_df,
    test_df=test_df,
)

model = tf.keras.models.Sequential([
    # Shape [batch, time, features] => [batch, time, lstm_units]
    tf.keras.layers.LSTM(32, return_sequences=True),
    # Shape => [batch, time, features]
    tf.keras.layers.Dense(units=1)
])

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=2,
    mode='min'
)
model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)
history = model.fit(
    window.train,
    epochs=20,
    validation_data=window.val,
    callbacks=[early_stopping]
)

window.plot(model, 'open', 5)

plt.show()
