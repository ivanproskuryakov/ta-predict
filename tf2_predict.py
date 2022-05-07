import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from service.dataset_builder import build_dataset
from parameters import market, ASSET, INTERVAL

# Data
# ------------------------------------------------------------------------


asset = ASSET
interval = INTERVAL
filepath_model = f'trained/ta_USDT_BTC_1m.keras'

df = build_dataset(
    market=market,
    asset=asset,
    interval=interval,
    test=True
)

df_tail = df[-1:]
x = np.expand_dims(df, axis=0)

# Model
# ----------------------------------------------------------------------------------


model = tf.keras.models.load_model(filepath_model)
y = model.predict(x)

price_open = y[0][:, 0]

# print(df['open'])
# print(price_open)
# exit()



plt.figure(figsize=(15, 5))

plt.plot(df['open'], label='true')
plt.plot(price_open, label='pred')

plt.ylabel('open')
plt.legend()
plt.show()
