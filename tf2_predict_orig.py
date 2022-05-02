import matplotlib.pyplot as plt

import tensorflow as tf

from binance import Client
from service.generator_window import WindowGenerator
from service.dataset_builder import build_dataset_prepared

# Data load
# ------------------------------------------------------------------------
asset = 'SOL'
interval = Client.KLINE_INTERVAL_1HOUR
filepath_model = f'data/ta_{asset}.keras'

[df, train_df, val_df, test_df, df_num_signals] = build_dataset_prepared(asset=asset, interval=interval)

# Generator function
# --------------------------------------------------------

window = WindowGenerator(
    input_width=30,
    label_width=30,
    shift=8,
    batch_size=10,
    label_columns=['open'],
    train_df=train_df,
    val_df=val_df,
    test_df=test_df,
)

model = tf.keras.models.load_model(filepath_model, custom_objects={
    # "loss": tf.losses.MeanSquaredError(),
    # "optimizer": tf.optimizers.Adam(),
    # "metrics": [tf.metrics.MeanAbsoluteError()]
})

window.plot(model, 'open', 4)

plt.show()
