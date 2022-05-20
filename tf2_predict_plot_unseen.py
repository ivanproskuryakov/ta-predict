import numpy as np
import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

from service.dataset_builder import build_dataset_unseen
from parameters import market, ASSET, INTERVAL

# Data
# ------------------------------------------------------------------------

tail = 30
asset = ASSET
interval = INTERVAL
filepath_model = f'data/ta_{market}_{asset}_{interval}.keras'

df = build_dataset_unseen(
    market=market,
    asset=asset,
    interval=interval,
)


scaler = MinMaxScaler()
scaled = scaler.fit_transform(df)

df_scaled = pd.DataFrame(scaled, None, df.keys())


# # print(df_scaled)
# # print(df_scaled_inverse)


model = tf.keras.models.load_model(filepath_model)

y = np.expand_dims(df_scaled, axis=0)
y_pred = model.predict(y)

dummy = pd.DataFrame(np.zeros((len(df), len(df.columns))), columns=df.columns)
dummy['open'] = y_pred[0][:,0]

df_scaled_inverse = scaler.inverse_transform(dummy)

dummy['open'] = df_scaled_inverse[:,0]

print(df['open'])
print(dummy['open'])
# print(df_scaled_inverse[:,0])

# exit()



# x.append(pd.Series(), ignore_index=True)
#



plt.figure(figsize=(12, 8))

plt.plot(df['open'], label='true', marker='.')
plt.plot(dummy['open'], label='true', marker='.')

plt.ylabel('open')
plt.legend()
plt.show()
