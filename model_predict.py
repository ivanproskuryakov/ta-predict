import tensorflow as tf
import numpy as np
import pandas as pd

from datetime import datetime, timedelta

from src.parameters_usdt import market, assets
from src.parameters_btc import assets_btc
from src.parameters import assets_down

from src.service.reporter import Reporter
from src.service.trade_finder import TradeFinder
from src.service.trader import Trader
from src.service.dataset_builder import DatasetBuilder
from src.service.predictor_unseen import make_prediction_ohlc_close

# --------

np.set_printoptions(precision=4)
pd.set_option("display.precision", 4)

interval = '1m'

end_at = now = datetime.now()
start_at = end_at - timedelta(hours=2)

trader = Trader()
reporter = Reporter()
trade_finder = TradeFinder()
dataset_builder = DatasetBuilder(
    assets=assets,
    assets_btc=assets_btc,
    assets_down=assets_down,
    interval=interval,
    market=market,
)

data = []

# --------

collection = dataset_builder.build_dataset_predict(
    start_at=start_at.timestamp(),
    end_at=end_at.timestamp(),
)

time_db_load = datetime.now() - now

model = tf.keras.models.load_model('model/gru-b-100-48.keras')

for item in collection:
    asset, x_df, df_scaled = item

    y_df = make_prediction_ohlc_close(df_scaled, model)

    data.append((
        asset,
        x_df,
        y_df
    ))

time_prediction = datetime.now() - now

# --------

df = reporter.report_build(data=data)
df_best = trade_finder.pick_best_options(df, diff=1, diff_sum=0)

report = reporter.report_prettify(df)
report_best = reporter.report_prettify(df_best)

print(report)
print(report_best)

print(f'start: {start_at}')
print(f'interval: {interval}')
print(f'db_load: {time_db_load}')
print(f'prediction: {time_prediction}')
