import sys

from src.service.subscriber import Subscriber

interval = sys.argv[1] # 5m, 15m, 30m ...

subscriber = Subscriber(interval=interval)

subscriber.listen()
