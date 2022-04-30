import tensorflow as tf

from binance import Client
from service.window_generator import WindowGenerator
from service.dataset_builder import build_dataset

# Data load
# ------------------------------------------------------------------------

asset = 'SOL'
interval = Client.KLINE_INTERVAL_1HOUR
filepath_model = f'data/ta_{asset}_{interval}.keras'

[train_df, val_df, test_df, df_num_signals] = build_dataset(asset=asset, interval=interval)

df = val_df[-30:]

# print(df)
# print(len(df))
# exit()

# Generator function
# --------------------------------------------------------

window = WindowGenerator(
    input_width=30,
    label_width=30,
    shift=8,
    batch_size=3,
    label_columns=['open'],
    train_df=train_df,
    val_df=val_df,
    test_df=test_df,
)
model = tf.keras.models.load_model(filepath_model)


print(model.summary())
# model.predict(val_df)

# plt.show()
