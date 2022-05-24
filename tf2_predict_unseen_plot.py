import matplotlib.pyplot as plt

from src.service.predictor_unseen import make_prediction
from src.parameters import market, ASSET, INTERVAL

asset = ASSET
interval = INTERVAL
tail = 20

x_df_open, y_df_open = make_prediction(market, ASSET, INTERVAL)

# Plot align
# ------------------------------------------------------------------------

x_df_open.loc[len(x_df_open)] = x_df_open.loc[len(x_df_open) - 1]

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
