import tensorflow as tf

from keras.layers import Dense, GRU
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder import DatasetBuilder
from src.service.window_generator import WindowGenerator
from src.parameters_usdt import market
from src.parameters_usdt_train import assets

# Variables
# ------------------------------------------------------------------------
filepath_model = f'data/gru-100-b.keras'
filepath_checkpoint = f'data/gru-100-b.checkpoint'

interval = '5m'
width = 100
start_at = -1

# Data load & train
# ------------------------------------------------------------------------
dataset_builder = DatasetBuilder(
    market=market,
    assets=assets,
    interval=interval,
)

train_df, validate_df = dataset_builder.build_dataset_train()

df_num_signals = train_df.shape[1]

print(f'training: {interval} {assets} {df_num_signals}')

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
    factor=0.5,
    min_lr=0,
    patience=10,
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
        units=600,
        return_sequences=True,
        input_shape=(None, df_num_signals)
    ),
    Dense(units=1, activation='linear', input_dim=df_num_signals),
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
    batch_size=200,
    label_columns=[
        # 'open',
        # 'high',
        # 'low',
        'close',
    ],
    train_df=train_df,
    val_df=validate_df,
)

# latest = tf.train.latest_checkpoint('data')
# model.load_weights(latest)

model.fit(
    window.train,
    epochs=50,
    validation_data=window.val,
    callbacks=[
        callback_early_stopping,
        callback_reduce_lr,
        callback_checkpoint,
    ]
)

model.save(filepath_model)