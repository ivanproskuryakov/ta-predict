import tensorflow as tf

from keras.layers import Dense, GRU, LSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from src.service.dataset_builder_db import build_dataset
from src.service.generator_window import WindowGenerator
from src.parameters import market, assets, intervals

# Variables
# ------------------------------------------------------------------------

df_num_signals = 36
shift = 1
batch_size = 1000
width = 30

filepath_model = f'data/ta_{market}.keras'

# Model definition
# ------------------------------------------------------------------------


callback_early_stopping = EarlyStopping(
    monitor='val_loss',
    patience=5,
    mode='min',
    verbose=1
)
callback_reduce_lr = ReduceLROnPlateau(
    monitor='val_loss',
    factor=0.2,
    min_lr=0.0001,
    patience=2,
    verbose=1
)

callback_checkpoint = ModelCheckpoint(
    filepath=filepath_model,
    monitor='val_loss',
    verbose=1,
    save_weights_only=True,
    save_best_only=True
)
model = tf.keras.models.Sequential([
    GRU(
        units=100,
        return_sequences=True,
        input_shape=(None, df_num_signals)
    ),
    # LSTM(300, return_sequences=True),
    # Dense(df_num_signals, activation='sigmoid'),
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
            input_width=width,
            label_width=width,
            shift=shift,
            batch_size=500,
            label_columns=['open'],
            train_df=train_df,
            val_df=val_df,
        )

        model.fit(
            window.train,
            epochs=2,
            validation_data=window.val,
            callbacks=[
                # callback_early_stopping,
                callback_reduce_lr,
                # callback_checkpoint,
            ]
        )

model.save(filepath_model)
