import tensorflow as tf

from keras.layers import Dense, GRU, LSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

from service.dataset_builder import build_dataset
from service.generator_window import WindowGenerator

from parameters import market, ASSET, intervals

# Var
# ------------------------------------------------------------------------

SIZE_SHIFT = 1
SIZE_BATCH = 50
SIZE_INPUT_LABEL = 30

# Data load
# ------------------------------------------------------------------------

for interval in intervals:
    asset = ASSET
    shift = SIZE_SHIFT
    batch_size = SIZE_BATCH
    width = SIZE_INPUT_LABEL
    filepath_model = f'data/ta_{market}_{asset}_{interval}.keras'

    [df, train_df, val_df, test_df, df_num_signals] = build_dataset(
        market=market, asset=asset,
        interval=interval
    )

    # Generator function
    # --------------------------------------------------------

    window = WindowGenerator(
        input_width=SIZE_INPUT_LABEL,
        label_width=SIZE_INPUT_LABEL,
        shift=shift,
        batch_size=SIZE_BATCH,
        label_columns=['open'],
        train_df=train_df,
        val_df=val_df,
        test_df=test_df,
    )

    model = tf.keras.models.Sequential([
        GRU(
            units=100,
            return_sequences=True,
            input_shape=(None, df_num_signals,)
        ),
        LSTM(100, return_sequences=True),
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
        epochs=100,
        validation_data=window.val,
        callbacks=[
            # callback_early_stopping,
            callback_reduce_lr,
            # callback_checkpoint,
        ]
    )

    model.save(filepath_model)
