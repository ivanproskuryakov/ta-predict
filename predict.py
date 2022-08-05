import sys

from src.service.subscriber import Subscriber
from src.parameters_usdt_top import assets, market

interval = sys.argv[1]  # 5m, 15m, 30m ...

subscriber = Subscriber(
    assets=assets,
    market=market,
    interval=interval,
    model_path='/Users/ivan/code/ta/model/gru-g-50-5000-223-5m-BTC.keras',
    width=1000
)

subscriber.subscribe()
