# url https://www.tensorflow.org/tutorials/structured_data/time_series

import tensorflow as tf
import matplotlib.pyplot as plt

from base import train_df, val_df, test_df
from window_generator import WindowGenerator

window = WindowGenerator(
    input_width=24,
    label_width=24,
    shift=3,
    label_columns=['T (degC)'],
    train_df=train_df,
    val_df=val_df,
    test_df=test_df,
)

model = tf.keras.models.Sequential([
    # Shape [batch, time, features] => [batch, time, lstm_units]
    tf.keras.layers.LSTM(32, return_sequences=True),
    # Shape => [batch, time, features]
    tf.keras.layers.Dense(units=1)
])

print('Input shape:', window.example[0].shape)
print('Output shape:', model(window.example[0]).shape)

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=2,
    mode='min'
)
model.compile(
    loss=tf.losses.MeanSquaredError(),
    optimizer=tf.optimizers.Adam(),
    metrics=[tf.metrics.MeanAbsoluteError()]
)
history = model.fit(
    window.train,
    epochs=20,
    validation_data=window.val,
    callbacks=[early_stopping]
)

window.plot(model)

plt.show()
