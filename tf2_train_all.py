import tensorflow as tf

from keras.layers import Dense, GRU, LSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder_db import build_dataset
from src.service.generator_window import WindowGenerator
from src.parameters import market, assets, intervals

# Variables
# ------------------------------------------------------------------------

df_num_signals = 40

filepath_model = f'data/ta_{market}.keras'
filepath_checkpoint = f'data/ta_{market}.checkpoint'

# Model definition
# ------------------------------------------------------------------------


callback_reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    min_lr=0.00001,
    # min_lr=0,
    patience=2,
    verbose=1,

    # mode='auto',
    # min_delta=0.0001,
    # cooldown=0,
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
        units=200,
        return_sequences=True,
        input_shape=(None, df_num_signals)
    ),
    Dense(units=df_num_signals, activation='relu', input_dim=df_num_signals),
    Dense(units=1),
])

model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)

# Data load & train
# ------------------------------------------------------------------------

for interval in intervals:
    for asset in assets:
        print(f'training interval: {interval} {asset}')

        train_df, val_df, df_num_signals = build_dataset(
            market=market,
            asset=asset,
            interval=interval
        )

        # Generator function
        # --------------------------------------------------------

        window = WindowGenerator(
            input_width=100,
            label_width=100,
            shift=1,
            batch_size=500,
            label_columns=['open'],
            train_df=train_df,
            val_df=val_df,
        )

        model.fit(
            window.train,
            epochs=5,
            validation_data=window.val,
            callbacks=[
                # callback_early_stopping,
                callback_reduce_lr,
                # callback_checkpoint,
            ]
        )

model.save(filepath_model)
