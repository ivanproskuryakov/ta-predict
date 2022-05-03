import matplotlib.pyplot as plt

import tensorflow as tf

from service.generator_window import WindowGenerator
from service.dataset_builder import build_dataset_prepared
from parameters import SIZE_BATCH, SIZE_SHIFT, ASSET, INTERVAL, SIZE_INPUT_LABEL

# Data load
# ------------------------------------------------------------------------

asset = ASSET
interval = INTERVAL
shift = SIZE_SHIFT
batch_size = SIZE_BATCH
width = SIZE_INPUT_LABEL

filepath_model = f'data/ta_{asset}_{interval}.keras'

[df, train_df, val_df, test_df, df_num_signals] = build_dataset_prepared(asset=asset, interval=interval)

# Generator function
# --------------------------------------------------------


window = WindowGenerator(
    input_width=30,
    label_width=30,
    shift=shift,
    batch_size=batch_size,
    label_columns=['open'],
    train_df=train_df,
    val_df=val_df,
    test_df=test_df,
)

model = tf.keras.models.load_model(filepath_model)

window.plot(model, 'open', 4)

plt.show()
