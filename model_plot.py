import matplotlib.pyplot as plt

from src.parameters import market
from src.service.dataset_builder import DatasetBuilder
from src.service.predictor import Predictor

tail = 50
width = 500
assets = [
    'BTC'
]
interval = '1m'

predictor = Predictor(
    assets=assets,
    market=market,
    interval=interval,
    model_path='/home/ivan/code/ta/data/gru-g-50-1000-11-1m-BTCUSDT.keras',
    width=width
)
dataset_builder = DatasetBuilder(
    assets,
    interval,
    market,
)

# Loading data
# Predicting close price on the next time interval
# ------------------------------------------------------------------------

collection = dataset_builder.build_dataset_predict(width=width)
x_df = collection[0]
x_df_shifted = x_df[:-1]

predictor.load_model()
y_df = predictor.make_prediction_ohlc_close(x_df=x_df_shifted)

# Plotting
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
    x_df['open'].tail(tail).values,
    color='blue',
    label='real',
    marker='.'
)

b = plt.subplot(2, 1, 2)
plt.plot(
    y_df['close'].tail(tail).values,
    color='green',
    label=f'predict {interval}',
    marker='.'
)

plt.legend()
plt.show()
