import sys
import tensorflow as tf
import numpy as np
import pandas as pd
from datetime import datetime

from src.parameters_usdt import market, assets
from src.parameters_btc import assets_btc
from src.parameters import assets_down

from src.service.reporter import Reporter
from src.service.trade_finder import TradeFinder
from src.service.trader import Trader
from src.service.dataset_builder_db import DatasetBuilderDB
from src.service.predictor_unseen import make_prediction_ohlc_close

# --------

np.set_printoptions(precision=4)
pd.set_option("display.precision", 4)

interval = sys.argv[1]
start_at = datetime.utcnow()
start_at_diff = int(start_at.timestamp() - 100 * 5 * 60)

# print(start_at_diff)
# exit()

trader = Trader()
reporter = Reporter()
trade_finder = TradeFinder()
dataset_builder = DatasetBuilderDB(
    assets=assets,
    assets_btc=assets_btc,
    assets_down=assets_down,
    interval=interval,
    market=market,
    start_at=start_at_diff,
)


data = []

# --------

model = tf.keras.models.load_model('model/gru-b.keras')

collection = dataset_builder.build_dataset_all()

time_download = datetime.utcnow() - start_at

for item in collection:
    asset, x_df, last_item = item

    y_df = make_prediction_ohlc_close(x_df, model)

    data.append((asset, last_item, x_df, y_df))

time_prediction = datetime.utcnow() - start_at

# --------

df = reporter.report_build(data=data)
df_best = trade_finder.pick_best_options(df, diff=1, diff_sum=0)

report = reporter.report_prettify(df)
report_best = reporter.report_prettify(df_best)

# trader.trade_buy_many(
#     df=df_best,
#     limit=10,
#     interval=interval,
#     buy_time=start_at,
# )

print(report)
print(report_best)

print(f'start: {start_at}')
print(f'interval: {interval}')
print(f'download: {time_download}')
print(f'prediction: {time_prediction}')
