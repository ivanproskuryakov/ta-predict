import tensorflow as tf

from keras.layers import Dense, GRU, LSTM, Dropout
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder_db import DatasetBuilderDB
from src.service.generator_window import WindowGenerator
from src.parameters import market, assets, assets_down
from src.parameters_btc import assets_btc

assets = [
    # 'BTC',
    # 'ETH',
    # "BNB",
    # "XRP",
    "ADA",
    # 'TRX',
]

dataset_builder_db = DatasetBuilderDB()

# Variables
# ------------------------------------------------------------------------
width = 50
units = 1000
interval = '3m'

# Data load & train
# ------------------------------------------------------------------------
train_df, validate_df = dataset_builder_db.build_dataset_all(
    market=market,
    assets=assets,
    assets_down=assets_down,
    assets_btc=assets_btc,
    interval=interval
)

# print(train_df)

df_num_signals = train_df.shape[1]
data_dir = 'data'
assets_names = '-'.join(assets)
name = f'gru-d-{width}-{units}-{df_num_signals}-{interval}-{assets_names}'

filepath_model = f'{data_dir}/{name}.keras'
filepath_checkpoint = f'{data_dir}/{name}.checkpoint'

print(f'training: {interval} {assets} {df_num_signals} {name}')

# Model definition
# ------------------------------------------------------------------------

callback_early_stopping = EarlyStopping(
    monitor='val_loss',
    # monitor='mean_absolute_error',
    patience=50,
    mode='min',
    verbose=1
)
callback_reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.5,
    min_delta=1e-8,
    min_lr=0,
    patience=2,
    verbose=1,
)
callback_checkpoint = ModelCheckpoint(
    filepath=filepath_checkpoint,
    monitor='val_loss',
    verbose=1,
    save_freq="epoch",
    period=1,
    save_weights_only=True,
    save_best_only=False
)

model = tf.keras.models.Sequential([
    GRU(
        units=units,
        return_sequences=True,
        input_shape=(None, df_num_signals)
    ),
    # Dropout(0.3),
    # GRU(
    #     units=500,
    #     return_sequences=True,
    #     input_shape=(None, df_num_signals)
    # ),
    # Dropout(0.3),
    # LSTM(
    #     units=width,
    #     return_sequences=True,
    #     input_shape=(None, df_num_signals)
    # ),
    Dense(units=1, activation='linear', input_dim=df_num_signals),
    # Dense(units=1, activation='relu', input_dim=df_num_signals),
])

model.compile(
    # loss=tf.losses.MeanSquaredError(),
    loss=tf.losses.MeanAbsoluteError(),
    optimizer=tf.optimizers.Adam(),
    # optimizer=tf.optimizers.Adam(lr=0.0001),
    metrics=[
        tf.metrics.MeanAbsoluteError(),
        tf.metrics.MeanAbsolutePercentageError(),
        # tf.metrics.Accuracy()
    ]
)

# Generator function
# --------------------------------------------------------

window = WindowGenerator(
    input_width=width,
    label_width=width,
    shift=1,
    batch_size=500,
    label_columns=[
        # 'open',
        # 'high',
        # 'low',
        'close',
    ],
    train_df=train_df,
    val_df=validate_df,
)

# latest = tf.train.latest_checkpoint(data_dir)
# model.load_weights(latest)

model.fit(
    window.train,
    epochs=100,
    validation_data=window.val,
    callbacks=[
        callback_early_stopping,
        callback_reduce_lr,
        callback_checkpoint,
    ]
)

model.save(filepath_model)
