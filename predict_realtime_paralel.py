import time
import ray

from datetime import datetime
from binance import Client

from src.service.predictor_unseen import data_prepare
from src.parameters import market, assets

interval = Client.KLINE_INTERVAL_30MINUTE
start_time = time.time()

print(interval)
print(datetime.now().strftime('%Y %m %d %H:%M:%S'))
print("------------------------------------------------------------------------------------------")

fns = []

for asset in assets:
    fns.append(data_prepare.remote(market, asset, interval))

data = ray.get(fns)

print(len(data))

print(datetime.now().strftime('%Y %m %d %H:%M:%S'))
print("------------------------------------------------------------------------------------------")
