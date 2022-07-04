import matplotlib.pyplot as plt
import tensorflow as tf

from src.service.predictor_unseen import make_prediction_ohlc_close
from src.service.dataset_builder_api import DatasetBuilderAPI
from src.parameters import market
from src.parameters_btc import assets_btc
from src.parameters import assets_down

tail = 100
assets = [
    'BTC'
]
interval = '15m'
dataset_builder = DatasetBuilderAPI(
    assets,
    assets_btc,
    assets_down,
    interval,
    market,
)

# Predict
# ------------------------------------------------------------------------

model = tf.keras.models.load_model(f'model/ta.keras')
x, last_item = dataset_builder.build_dataset_all()

y = make_prediction_ohlc_close(x, model)

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

a = plt.subplot(2, 1, 1)
a.plot(
    x['open'].tail(tail).values,
    color='blue',
    label='real',
    marker='.'
)

b = plt.subplot(2, 1, 2)
plt.plot(
    y['close'].tail(tail).values,
    color='green',
    label=f'predict {interval}',
    marker='.'
)

plt.legend()
plt.show()
