import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from binance import Client
from service.generator_window import WindowGenerator
from service.dataset_builder import build_dataset_prepared

# Data
# ------------------------------------------------------------------------

asset = 'SOL'
interval = Client.KLINE_INTERVAL_1HOUR
filepath_model = f'data/ta_{asset}_{interval}.keras'

[df, train_df, val_df, test_df, df_num_signals] = build_dataset_prepared(asset=asset, interval=interval)

x = np.expand_dims(test_df, axis=0)


window = WindowGenerator(
    input_width=30,
    label_width=30,
    shift=8,
    batch_size=3,
    label_columns=['open'],
    train_df=train_df,
    val_df=val_df,
    test_df=test_df,
)

model = tf.keras.models.load_model(filepath_model)
model.predict(x)

window.plot(model, 'open', 1)

plt.show()