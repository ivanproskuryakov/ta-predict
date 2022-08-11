import sys

from src.service.subscriber import Subscriber

from src.parameters import assets, market

interval = sys.argv[1]  # 5m, 15m, 30m ...
model_path = sys.argv[2]  # /Users/ivan/code/ta/model/gru-g-50-5000-223-5m-BTC.keras

subscriber = Subscriber(
    assets=assets,
    market=market,
    interval=interval,
    model_path=model_path,
    width=1000
)

subscriber.subscribe()
