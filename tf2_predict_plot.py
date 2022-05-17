import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from service.dataset_builder import build_dataset_prepared, build_dataset
from service.util import split_window
from parameters import market, SIZE_BATCH, SIZE_SHIFT, ASSET, INTERVAL, SIZE_INPUT_LABEL

# Data
# ------------------------------------------------------------------------

asset = ASSET
interval = INTERVAL
shift = SIZE_SHIFT
batch_size = SIZE_BATCH
input_width = SIZE_INPUT_LABEL
label_width = SIZE_INPUT_LABEL
filepath_model = f'data/ta_{market}_{asset}_{interval}.keras'

[df, train_df, val_df, test_df, df_num_signals] = build_dataset_prepared(
    market=market,
    asset=asset,
    interval=interval
)
# df = build_dataset(
#     market=market,
#     asset=asset,
#     interval=interval
# )

x = train_df
y = np.expand_dims(df, axis=0)

# Model
# ------

model = tf.keras.models.load_model(filepath_model)
model.predict(y)

# plot vars
# ------

max_subplots = 1

total_window_size = input_width + shift
input_indices = np.arange(0, input_width)
label_indices = np.arange(shift, total_window_size)

# plot data
# --------

data = np.array(x, dtype=np.float32)

ds = tf.keras.utils.timeseries_dataset_from_array(
    data=data,
    targets=None,
    sequence_length=total_window_size,
    sequence_stride=1,
    # shuffle=True,
    batch_size=batch_size,
)

ds = ds.map(lambda x: split_window(x, total_window_size, label_width, input_width))

inputs, labels = next(iter(ds))

# render
# -------

plt.figure(figsize=(12, 8))

for n in range(max_subplots):
    predictions = model(inputs)

    plt.subplot(max_subplots, 1, n + 1)
    plt.ylabel(f'open [normed]')
    plt.plot(
        input_indices,
        inputs[n, :, 0],
        label='Inputs',
        marker='.',
        zorder=-10
    )
    plt.scatter(
        label_indices,
        labels[n, :, 0],
        edgecolors='k',
        label='Labels',
        c='#2ca02c',
        s=64
    )
    plt.scatter(
        label_indices,
        predictions[n, :, 0],
        marker='X',
        edgecolors='k',
        label='Predictions',
        c='#ff7f0e',
        s=64
    )

    if n == 0:
        plt.legend()

plt.xlabel('time')

plt.show()
