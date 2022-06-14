import matplotlib.pyplot as plt
import tensorflow as tf
import pandas as pd
import numpy as np

from sklearn.preprocessing import MinMaxScaler
from src.service.dataset_builder_realtime import build_dataset
from src.parameters import market

asset = 'BTC'
interval = '15m'
tail = 50
shift_steps = 1

# Predict
# ------------------------------------------------------------------------

model = tf.keras.models.load_model(f'data/ta_{shift_steps}.keras')
x, last_item = build_dataset(market, asset, interval)

# x = x[0:-3]

for i in range(10):
    print('......')
    scaler = MinMaxScaler()
    scaled = scaler.fit_transform(x)

    x_df_scaled = pd.DataFrame(scaled, None, x.keys())
    x_df_scaled_expanded = np.expand_dims(x_df_scaled, axis=0)

    y = model.predict(x_df_scaled_expanded, verbose=0)
    y_inverse = scaler.inverse_transform(y[0])

    y = pd.DataFrame(y_inverse, None, columns=x.columns)

    x.loc[len(x)] = y.loc[len(y) - 1]

# Plot
# ------------------------------------------------------------------------

plt.figure(figsize=(16, 8))

plt.xlim(left=0)
plt.xlim(right=100)

plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "#cccccc"
plt.grid(True)
plt.grid(which='minor', alpha=0.2)
plt.grid(which='major', alpha=0.5)

#
# a = plt.subplot(2, 1, 1)
# a.plot(
#     x_df_open['open'].tail(tail).values,
#     color='blue',
#     label='real',
#     marker='.'
# )

# b = plt.subplot(2, 1, 2)
plt.plot(
    y['open'].tail(50).values,
    color='green',
    label=f'predict {interval}',
    marker='.'
)

plt.legend()
plt.show()
