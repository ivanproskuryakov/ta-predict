import matplotlib.pyplot as plt
import tensorflow as tf

from src.service.predictor_unseen import make_prediction
from src.service.dataset_builder_realtime import build_dataset
from src.parameters import market, tail

asset = 'BTC'
interval = '15m'

# Predict
# ------------------------------------------------------------------------

model = tf.keras.models.load_model(f'data/ta_USDT.keras')
x, last_item = build_dataset(market, asset, interval)

x = x.tail(200)

y = make_prediction(x, model)

# Plot
# ------------------------------------------------------------------------

plt.figure(figsize=(16, 8))

plt.xlim(left=0)
plt.xlim(right=200)

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
    y['open'].tail(tail).values,
    color='green',
    label=f'predict {interval}',
    marker='.'
)

plt.legend()
plt.show()
