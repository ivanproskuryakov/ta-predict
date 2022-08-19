import sys
import matplotlib.pyplot as plt

from src.parameters import market
from src.service.dataset_builder import DatasetBuilder
from src.service.predictor import Predictor

# Variables
# ------------------------------------------------------------------------

interval = sys.argv[1]  # 5m, 15m, 30m ...
model_path = sys.argv[2]  # /Users/ivan/code/ta/model/gru-g-50-5000-223-5m-BTC.keras

assets = [
    'BTC',
    'ETH',
    'BNB',
    'ADA',
]
tail = 50
width = 500

# Services
# ------------------------------------------------------------------------

predictor = Predictor(
    assets=assets,
    market=market,
    interval=interval,
    model_path='model/gru-g-50-1000-11-1m-BTCUSDT.keras',
    width=width
)
dataset_builder = DatasetBuilder(
    assets,
    interval,
    market,
)

# Data load
# Predicting close price on the next time interval
# ------------------------------------------------------------------------

collection = dataset_builder.build_dataset_predict(width=width)

for x_df in collection:
    asset = x_df.iloc[-1]['asset']
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
        label=f'predict {interval} {asset}',
        marker='.'
    )

    plt.legend()

plt.show()
