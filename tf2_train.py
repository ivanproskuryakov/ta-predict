import tensorflow as tf

from keras.layers import Dense, GRU, LSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from binance import Client
from service.dataset_builder import build_dataset_prepared
from service.generator_window import WindowGenerator
from parameters import SIZE_BATCH, SIZE_SHIFT

# Data load
# ------------------------------------------------------------------------

asset = 'ROSE'
interval = Client.KLINE_INTERVAL_5MINUTE
filepath_model = f'data/ta_{asset}_{interval}.keras'

[df, train_df, val_df, test_df, df_num_signals] = build_dataset_prepared(asset=asset, interval=interval)

# Generator function
# --------------------------------------------------------

shift = SIZE_SHIFT
batch_size = SIZE_BATCH

window = WindowGenerator(
    input_width=30,
    label_width=30,
    shift=shift,
    batch_size=SIZE_BATCH,
    label_columns=['open'],
    train_df=train_df,
    val_df=val_df,
    test_df=test_df,
)

model = tf.keras.models.Sequential([
    GRU(
        units=520,
        return_sequences=True,
        input_shape=(None, df_num_signals,)
    ),
    LSTM(20, return_sequences=True),
    Dense(units=1),
])

callback_early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    mode='min',
    verbose=1
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

callback_checkpoint = ModelCheckpoint(
    filepath=filepath_model,
    monitor='val_loss',
    verbose=1,
    save_weights_only=True,
    save_best_only=True
)

model.fit(
    window.train,
    epochs=20,
    validation_data=window.val,
    callbacks=[
        # callback_early_stopping,
        callback_reduce_lr,
        # callback_checkpoint,
    ]
)

model.save(filepath_model)
