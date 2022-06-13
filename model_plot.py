import matplotlib.pyplot as plt
import tensorflow as tf

from src.service.predictor_unseen import make_prediction
from src.service.dataset_builder_realtime import build_dataset
from src.parameters import market, ASSET, INTERVAL

asset = ASSET
interval = '15m'
tail = 50
shift_steps = 20

# Predict
# ------------------------------------------------------------------------

model = tf.keras.models.load_model(f'data/ta_{shift_steps}.keras')
x_df_open, last_item = build_dataset(market, ASSET, INTERVAL)

x_df_open = x_df_open.tail(50)
y_df_open = make_prediction(x_df_open, model)

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
    y_df_open['open'].values,
    color='green',
    label=f'predict {interval}',
    marker='.'
)

plt.legend()
plt.show()
