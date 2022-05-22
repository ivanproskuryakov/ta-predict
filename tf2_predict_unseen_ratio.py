import numpy as np

from src.service.predictor_unseen import make_prediction
from src.parameters import market, ASSET, INTERVAL


asset = ASSET
interval = INTERVAL

(x_df_open, y_df_open) = make_prediction(market, ASSET, INTERVAL)

# Measure
# ------------------------------------------------------------------------


tail = y_df_open['open'].tail(2).values

last = tail[0]
prediction = tail[1]
trend = "negative"

if prediction > last:
    trend = "positive"

diff = np.round(last / (prediction * 100), 2)

print(last)
print(prediction)
print(trend)
print(f'{diff}%')
