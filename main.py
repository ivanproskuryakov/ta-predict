import sys

from src.service.subscriber import Subscriber


def main():
    interval = sys.argv[1]

    subscriber = Subscriber(interval=interval)

    subscriber.run()


if __name__ == "__main__":
    main()
