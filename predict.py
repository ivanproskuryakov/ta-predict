import sys

from src.service.subscriber import Subscriber

interval = sys.argv[1]  # 5m, 15m, 30m ...

subscriber = Subscriber(
    interval=interval,
    model_path='model/gru-b-1000-48.keras',
    width=1000
)

subscriber.subscribe()
