import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import pandas as pd

from service.dataset_builder import build_dataset_prepared
from parameters import market, SIZE_BATCH, SIZE_SHIFT, ASSET, INTERVAL, SIZE_INPUT_LABEL

# Data
# ------------------------------------------------------------------------

tail = 20

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
x = test_df
x_expanded = np.expand_dims(x, axis=0)

# Model
# ------

model = tf.keras.models.load_model(filepath_model)
y = model.predict(x_expanded)

# Slice
# ------------------------------------------------------------------------

y_df = pd.DataFrame(np.zeros((len(x), 1)), columns=['open'])
y_df['open'] = y[0][:, 0]

x_df = pd.DataFrame(np.zeros((len(x), 1)), columns=['open'])
x_df['open'] = x['open'].values

y_df.loc[-1] = 0
y_df = y_df.sort_index().reset_index(drop=True)

val = x_df.loc[len(x)-1]
print(val)
x_df = x_df.append(val, ignore_index=True)


# Plot
# ------------------------------------------------------------------------

plt.figure(figsize=(16, 8))

plt.plot(x_df['open'].tail(tail).values, label='real', marker='.')
plt.plot(y_df['open'].tail(tail).values, label='real', marker='.')

plt.ylabel(market)
plt.xlabel('time')
plt.legend()
plt.show()
