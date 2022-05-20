import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from service.dataset_builder import build_dataset_prepared
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
x = train_df
y = np.expand_dims(df, axis=0)

# Model
# ------
tail = 30
model = tf.keras.models.load_model(filepath_model)

y_pred = model.predict(y)

plt.figure(figsize=(12, 8))

plt.plot(x['open'].values[-tail:], label='true', marker='.')
plt.plot(y_pred[0][-tail:], label='pred', marker='X')

plt.ylabel('open')
plt.legend()
plt.show()
