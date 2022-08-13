import sys

from src.service.listener import Listener

from src.parameters import market, assets

interval = sys.argv[1]  # 5m, 15m, 30m ...
model_path = sys.argv[2]  # /Users/ivan/code/ta/model/gru-g-50-5000-223-5m-BTC.keras

listener = Listener(
    assets=assets,
    market=market,
    interval=interval,
    model_path=model_path,
    width=500
)

listener.start()
