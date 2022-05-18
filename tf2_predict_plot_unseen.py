import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from service.dataset_builder import build_dataset_unseen
from service.util import split_window
from parameters import market, ASSET, INTERVAL

# Data
# ------------------------------------------------------------------------

asset = ASSET
interval = INTERVAL
batch_size = 50
filepath_model = f'data/ta_{market}_{asset}_{interval}.keras'

df = build_dataset_unseen(
    market=market,
    asset=asset,
    interval=interval,
)
x = df
y = np.expand_dims(df, axis=0)

model = tf.keras.models.load_model(filepath_model)
model.predict(y)

# plot vars
# ------

total_window_size = 30 + 1
input_indices = np.arange(0, 30)
label_indices = np.arange(1, total_window_size)

# plot data
# --------

data = np.array(x, dtype=np.float32)

ds = tf.keras.utils.timeseries_dataset_from_array(
    data=data,
    targets=None,
    sequence_length=total_window_size,
    sequence_stride=1,
    batch_size=batch_size,
)

ds = ds.map(lambda x: split_window(x, total_window_size, 30, 30))

inputs, labels = next(iter(ds))

predictions = model(inputs)

# render
# -------

for n in range(len(predictions)):
    plt.figure(figsize=(12, 8))
    plt.subplot(1, 1, 1)
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

    plt.legend()
    plt.xlabel('time')

plt.show()
