import sys

from src.service.subscriber import Subscriber

interval = sys.argv[1]

subscriber = Subscriber(interval=interval)

subscriber.run()
