import sys

from src.service.subscriber import Subscriber

interval = sys.argv[1]  # 5m, 15m, 30m ...

subscriber = Subscriber(
    interval=interval,
    model_path='/Users/ivan/code/ta/model/gru-g-50-5000-223-5m-BTC.keras',
    width=500
)

subscriber.subscribe()
