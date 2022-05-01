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

model = tf.keras.models.load_model(filepath_model)
model.predict(x)

# plot
# ------


# ---
input_width = 30
label_width = 30
shift = 8
batch_size = 3
label_columns = ['open']
train_df = train_df
val_df = val_df
test_df = test_df
plot_col = 'open'
max_subplots = 3

input_slice = slice(0, input_width)

total_window_size = input_width + shift
label_start = total_window_size - label_width
labels_slice = slice(label_start, None)
column_indices = {name: i for i, name in enumerate(train_df.columns)}
input_indices = np.arange(total_window_size)[input_slice]
label_indices = np.arange(total_window_size)[labels_slice]
label_col_index = 0

# example
# --------


def split_window(features):
    inputs = features[:, input_slice, :]
    labels = features[:, labels_slice, :]

    if label_columns is not None:
        labels = tf.stack(
            [labels[:, :, column_indices[name]] for name in label_columns],
            axis=-1)


    # manually. This way the `tf.data.Datasets` are easier to inspect.
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

# print(inputs, labels)
# exit()
# ---




plt.figure(figsize=(12, 8))
plot_col_index = column_indices[plot_col]
max_n = min(max_subplots, len(inputs))

for n in range(max_n):
    plt.subplot(max_n, 1, n + 1)
    plt.ylabel(f'{plot_col} [normed]')
    plt.plot(
        input_indices,
        inputs[n, :, plot_col_index],
        label='Inputs',
        marker='.',
        zorder=-10
    )

    plt.scatter(
        label_indices,
        labels[n, :, label_col_index],
        edgecolors='k',
        label='Labels',
        c='#2ca02c',
        s=64
    )

    if model is not None:
        predictions = model(inputs)
        plt.scatter(
            label_indices,
            predictions[n, :, label_col_index],
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
