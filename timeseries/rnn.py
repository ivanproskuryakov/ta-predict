# url https://www.tensorflow.org/tutorials/structured_data/time_series

import tensorflow as tf
import matplotlib.pyplot as plt

from base import compile_and_fit, wide_window

# 6. Recurrent neural network
# ------------------------------------------------------------------
# A Recurrent Neural Network (RNN) is a type of neural network well-suited to time series data.
# RNNs process a time series step-by-step, maintaining an internal state from time-step to time-step.

# With return_sequences=True, the model can be trained on 24 hours of data at a time.
lstm_model = tf.keras.models.Sequential([
    # Shape [batch, time, features] => [batch, time, lstm_units]
    tf.keras.layers.LSTM(32, return_sequences=True),
    # Shape => [batch, time, features]
    tf.keras.layers.Dense(units=1)
])


print('Input shape:', wide_window.example[0].shape)
print('Output shape:', lstm_model(wide_window.example[0]).shape)


history = compile_and_fit(lstm_model, wide_window)

wide_window.plot(lstm_model)

plt.show()
