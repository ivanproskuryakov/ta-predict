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

y_df = pd.DataFrame(np.zeros((len(x), len(x.columns))), columns=x.columns)
y_df['open'] = y[0]

# Plot
# ------------------------------------------------------------------------

plt.figure(figsize=(16, 8))

plt.plot(x['open'].values, label='real', marker='.')
plt.plot(y_df['open'].values, label='real', marker='.')

plt.ylabel(market)
plt.xlabel('time')
plt.legend()
plt.show()
