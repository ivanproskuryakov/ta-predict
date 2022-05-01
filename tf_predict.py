import numpy as np
import pandas as pd
import tensorflow as tf

import matplotlib.pyplot as plt

from keras.optimizer_v2.rmsprop import RMSprop
from sklearn.preprocessing import MinMaxScaler
from binance import Client

from service.dataset_builder import build_dataset
from service.loss import loss_mse_warmup

# Load
# ------------------------------------------------------------------------
pd.options.display.precision = 30
np.set_printoptions(precision=30, suppress=True)

asset = 'ETH'
interval = Client.KLINE_INTERVAL_5MINUTE
df = build_dataset(asset=asset, interval=interval)

# Preparation
# ------------------------------------------------------------------------

shift_steps = 5

x_data = df.values[:-shift_steps]  # cut tail, array size - 5
y_data = df.values[shift_steps:]  # cut head

num_data = len(x_data)
num_train = int(0.9 * num_data)

x_train = x_data[0:num_train]
x_test = x_data[num_train:]

y_train = y_data[0:num_train]
y_test = y_data[num_train:]

# Scaling
# ------------------------------------------------------------------------

x_scaler = MinMaxScaler()
x_train_scaled = x_scaler.fit_transform(x_train)
x_test_scaled = x_scaler.transform(x_test)

y_scaler = MinMaxScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)

# Model
# ------------------------------------------------------------------------

model = tf.keras.models.load_model('data/tf.keras', custom_objects={
    "loss_mse_warmup": loss_mse_warmup,
    "optimizer": RMSprop(learning_rate=0.001)
})

# Predicting
# ------------------------------------------------------------------------

# x = x_train_scaled[0:100]
# y_true = y_train[0:100]

x = x_test_scaled[-50:]
y_true = y_test[-50:]

x = np.expand_dims(x, axis=0)

y_pred = model.predict(x)
y_pred_rescaled = y_scaler.inverse_transform(y_pred[0])

signal_pred = y_pred_rescaled[:, 0]
signal_true = y_true[:, 0]

# Rendering
# ----------------------------------------------------------------------------------

plt.figure(figsize=(15, 5))

plt.plot(signal_true, label='true')
plt.plot(signal_pred, label='pred')

plt.ylabel('open')
plt.legend()
plt.show()
