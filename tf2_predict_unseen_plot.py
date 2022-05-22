import matplotlib.pyplot as plt

from src.service.predictor_unseen import make_prediction
from src.parameters import market, ASSET, INTERVAL

asset = ASSET
interval = INTERVAL

(x_df_open, y_df_open) = make_prediction(market, ASSET, INTERVAL)

# Plot
# ------------------------------------------------------------------------
tail = 20

plt.figure(figsize=(16, 8))

plt.plot(x_df_open['open'].tail(tail - 1).values, label='real', marker='.')
plt.plot(y_df_open['open'].tail(tail).values, label='predict', marker='.')

plt.ylabel('open')
plt.xlabel('time')
plt.legend()
plt.show()
