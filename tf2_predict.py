import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from service.dataset_builder import build_dataset
from parameters import market, SIZE_BATCH, ASSET, INTERVAL

# Data
# ------------------------------------------------------------------------

asset = ASSET
interval = INTERVAL
batch_size = SIZE_BATCH + 1
# filepath_model = f'data/ta_{market}_{asset}_{interval}.keras'
filepath_model = f'trained/ta_USDT_BTC_1m.keras'

df = build_dataset(
    market=market,
    asset=asset,
    interval=interval
)

df_tail = df[-batch_size:]
x = np.expand_dims(df_tail, axis=0)

# Model
# ------

model = tf.keras.models.load_model(filepath_model)
y = model.predict(x)

price_open = y[0][:, 0]

# Plotting
# ----------------------------------------------------------------------------------

plt.plot(price_open[5:], label='true')

plt.ylabel('open')
plt.legend()
plt.show()
