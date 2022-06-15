import tensorflow as tf

from keras.layers import Dense, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder_db import build_dataset_window_many
from src.service.generator_window import WindowGenerator
from src.parameters import market

# Variables
# ------------------------------------------------------------------------
width = 100

filepath_model = f'data/ta.keras'
filepath_checkpoint = f'data/ta.checkpoint'

interval = '5m'
assets = [
    'BTC',
    "ETH",
    "BNB",
    "NEO",
    "LTC",
    "ADA",
    "XRP",
    "EOS",
]

print(f'training interval: {interval} {assets}')

# Data load & train
# ------------------------------------------------------------------------

train_df, validate_df = build_dataset_window_many(
    market=market,
    assets=assets,
    interval=interval
)

df_num_signals = train_df.shape[1]

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
    factor=0.2,
    min_lr=0,
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
    # Dense(units=df_num_signals, activation='linear'-, input_dim=df_num_signals),
    # Dense(units=df_num_signals, activation='relu', input_dim=df_num_signals),
    Dense(units=10),
])

model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)

# Generator function
# --------------------------------------------------------

window = WindowGenerator(
    input_width=width,
    label_width=width,
    shift=1,
    batch_size=500,
    label_columns=[
        'open',
        'high',
        'low',
        'close',

        'trades',
        'volume',
        'volume_taker',
        'volume_maker',
        'quote_asset_volume',

        'diff',
    ],
    train_df=train_df,
    val_df=validate_df,
)

model.fit(
    window.train,
    epochs=500,
    validation_data=window.val,
    callbacks=[
        callback_early_stopping,
        callback_reduce_lr,
        callback_checkpoint,
    ]
)

model.save(filepath_model)
