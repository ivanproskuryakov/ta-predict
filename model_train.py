import tensorflow as tf

from keras.layers import Dense, GRU, LSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder_db import build_dataset
from src.service.generator_window import WindowGenerator
from src.parameters import market

# Variables
# ------------------------------------------------------------------------
df_num_signals = 45
width = 200

filepath_model = f'data/ta_{market}_shift3.keras'
filepath_checkpoint = f'data/ta_{market}_shift3.checkpoint'

interval = '15m'
asset = 'BTC'

print(f'training interval: {interval} {asset}')

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
    Dense(units=df_num_signals),
])

model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)

# Data load & train
# ------------------------------------------------------------------------

train_df, val_df, df_num_signals = build_dataset(
    market=market,
    asset=asset,
    interval=interval
)

# Generator function
# --------------------------------------------------------

window = WindowGenerator(
    input_width=width,
    label_width=width,
    shift=3,
    batch_size=500,
    label_columns=['open'],
    train_df=train_df,
    val_df=val_df,
)

model.fit(
    window.train,
    epochs=500,
    validation_data=window.val,
    callbacks=[
        # callback_early_stopping,
        callback_reduce_lr,
        callback_checkpoint,
    ]
)

model.save(filepath_model)
