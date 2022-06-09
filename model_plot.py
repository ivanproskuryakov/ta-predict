import matplotlib.pyplot as plt
import tensorflow as tf

from src.service.predictor_unseen import make_prediction
from src.service.dataset_builder_realtime import build_dataset
from src.parameters import market, ASSET, INTERVAL

asset = ASSET
interval = INTERVAL
tail = 100
asset,
# Predict
# ------------------------------------------------------------------------

model = tf.keras.models.load_model('data/tf.keras')
x_df_open, last_item = build_dataset(market, ASSET, INTERVAL)

y_df_open = make_prediction(x_df_open, model)

# Plot align
# ------------------------------------------------------------------------

# x_df_open.loc[len(x_df_open)] = x_df_open.loc[len(x_df_open) - 1]
# x_df_open.loc[len(x_df_open)] = x_df_open.loc[len(x_df_open) - 1]
# x_df_open.loc[len(x_df_open)] = x_df_open.loc[len(x_df_open) - 1]

# Plot
# ------------------------------------------------------------------------

plt.figure(figsize=(16, 8))

plt.xlim(left=0)
plt.xlim(right=tail)

plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['axes.edgecolor'] = 'white'
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 1
plt.rcParams['grid.color'] = "#cccccc"
plt.grid(True)

a = plt.subplot(2, 1, 1)
a.plot(
    x_df_open['open'].tail(tail).values,
    color='blue',
    label='real',
    marker='.'
)

b = plt.subplot(2, 1, 2)
b.plot(
    y_df_open['open'].tail(tail).values,
    color='green',
    label=f'predict {interval}',
    marker='.'
)

plt.legend()
plt.show()
