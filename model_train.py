import tensorflow as tf

from keras.layers import Dense, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder import DatasetBuilder
from src.service.window_generator import WindowGenerator

# Variables
# ------------------------------------------------------------------------
assets = [
    'BTCUSDT',
    # 'BTCUSDC',
    # 'BTCBUSD',
    # 'BTCDAI',
]
market = 'USDT'
width = 50
units = 1000
interval = '1m'

# Data load & train
# ------------------------------------------------------------------------
dataset_builder = DatasetBuilder(
    assets=assets,
    market=market,
    interval=interval
)

train_df, validate_df = dataset_builder.build_dataset_train()

df_num_signals = train_df.shape[1]
data_dir = 'data'
assets_names = '-'.join(assets)
name = f'gru-g-{width}-{units}-{df_num_signals}-{interval}-{assets_names}'

filepath_model = f'{data_dir}/{name}.keras'
filepath_checkpoint = f'{data_dir}/{name}.checkpoint'

print(f'training: {interval} {assets} {df_num_signals} {name}')

# Model definition
# ------------------------------------------------------------------------

callback_early_stopping = EarlyStopping(
    monitor='val_loss',
    # monitor='mean_absolute_error',
    patience=10,
    mode='min',
    verbose=1
)
callback_reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    # min_delta=1e-4,
    # min_delta=1e-18,
    min_lr=0,
    patience=3,
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
    # Dense(units=1, activation='softmax', input_dim=df_num_signals),
    Dense(units=1, activation='linear', input_dim=df_num_signals),
    # Dense(units=1, activation='tanh', input_dim=df_num_signals),
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
    batch_size=100,
    label_columns=[
        # 'open',
        # 'high',
        # 'low',
        'close',
    ],
    train_df=train_df,
    val_df=validate_df,
)

latest = tf.train.latest_checkpoint(data_dir)
model.load_weights(latest)

model.fit(
    window.train,
    epochs=1,
    validation_data=window.val,
    callbacks=[
        callback_early_stopping,
        callback_reduce_lr,
        callback_checkpoint,
    ]
)

model.save(filepath_model)
