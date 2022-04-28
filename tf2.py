import matplotlib.pyplot as plt

import tensorflow as tf
from keras.layers import Dense, GRU, LSTM
from keras.callbacks import ReduceLROnPlateau, EarlyStopping


from binance import Client
from service.window_generator import WindowGenerator
from service.reader_ta import read
from service.scaler import scale_data
from service.estimator import estimate_ta

# Data load
# ------------------------------------------------------------------------
asset = 'ROSE'
# interval = Client.KLINE_INTERVAL_1MINUTE
# interval = Client.KLINE_INTERVAL_3MINUTE
# interval = Client.KLINE_INTERVAL_5MINUTE
interval = Client.KLINE_INTERVAL_30MINUTE

df_raw = read(asset, interval)
df_ta = estimate_ta(df_raw)
df_nan = df_ta.fillna(0)
df = scale_data(df_nan)

df_num_signals = df.shape[1]

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
    input_width=50,
    label_width=50,
    shift=1,
    batch_size=64,
    label_columns=['open'],
    train_df=train_df,
    val_df=val_df,
    test_df=test_df,
)

model = tf.keras.models.Sequential([
    GRU(
        units=50,
        return_sequences=True,
        input_shape=(None, df_num_signals,)
    ),
    # LSTM(50, return_sequences=True),
    Dense(units=1),
])

callback_early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    # mode='min',
    # verbose=1
)
callback_reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.1,
    min_lr=0.001,
    patience=1,
    verbose=1
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
    callbacks=[
        callback_early_stopping,
        callback_reduce_lr,
    ]
)

window.plot(model, 'open', 4)

plt.show()
