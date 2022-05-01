import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

from binance import Client
from service.dataset_builder import build_dataset_prepared

# Data
# ------------------------------------------------------------------------

asset = 'SOL'
interval = Client.KLINE_INTERVAL_1HOUR
filepath_model = f'data/ta_{asset}_{interval}.keras'

[df, train_df, val_df, test_df, df_num_signals] = build_dataset_prepared(asset=asset, interval=interval)

x = np.expand_dims(test_df, axis=0)

# Model
# ------

model = tf.keras.models.load_model(filepath_model)
model.predict(x)

# plot vars
# ------


input_width = 30
label_width = 30
shift = 8
batch_size = 3
train_df = train_df
max_subplots = 3



total_window_size = input_width + shift
input_indices = np.arange(0, input_width)
label_indices = np.arange(shift, total_window_size)

# print(input_indices)
# print(label_indices)
# exit()


# plot data
# --------

def split_window(features):
    label_start = total_window_size - label_width

    input_slice = slice(0, input_width)
    labels_slice = slice(label_start, None)

    inputs = features[:, input_slice, :]
    labels = features[:, labels_slice, :]

    inputs.set_shape([None, input_width, None])
    labels.set_shape([None, label_width, None])

    return inputs, labels


data = np.array(train_df, dtype=np.float32)

ds = tf.keras.utils.timeseries_dataset_from_array(
    data=data,
    targets=None,
    sequence_length=total_window_size,
    sequence_stride=1,
    shuffle=True,
    batch_size=batch_size,
)

ds = ds.map(split_window)

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
