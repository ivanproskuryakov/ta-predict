# import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
# import pandas as pd

import matplotlib.pyplot as plt

import weather

from keras.models import Sequential
from keras.models import Sequential
from keras.layers import Input, Dense, GRU, Embedding
from keras.optimizer_v2.rmsprop import RMSprop
from keras.callbacks import EarlyStopping, ModelCheckpoint, TensorBoard, ReduceLROnPlateau
from keras.backend import square, mean

# weather.maybe_download_and_extract()
#
# cities = weather.cities



# Load Data
# ------------------------------------------------------------
df = weather.load_resampled_data()

df.drop(('Esbjerg', 'Pressure'), axis=1, inplace=True)
df.drop(('Roskilde', 'Pressure'), axis=1, inplace=True)

# print(cities)
# exit()
# print(df.head())

# df['Esbjerg']['Pressure'].plot()
# plt.show()

# df['Roskilde']['Pressure'].plot()
# plt.show()

# print(df.values.shape)
# print(df.head(1))



# Add Data
# ------------------------------------------------------------
df['Various', 'Day'] = df.index.dayofyear
df['Various', 'Hour'] = df.index.hour



# Target Data for Prediction
# ------------------------------------------------------------

target_city = 'Odense'
target_names = ['Temp', 'WindSpeed', 'Pressure']
shift_days = 1
shift_steps = shift_days * 24  # Number of hours.

# df['Odense']['Temp']['2006-05':'2006-07'].plot()
# df['Aarhus']['Temp']['2006-05':'2006-07'].plot()
# df['Roskilde']['Temp']['2006-05':'2006-07'].plot()

df_targets = df[target_city][target_names].shift(-shift_steps)
df[target_city][target_names].head(shift_steps + 5)

# print(df.index.dayofyear)
# print(df.index.hour)
# plt.show()



# NumPy Arrays
# ------------------------------------------------------------

# We now convert the Pandas data-frames to NumPy arrays that can be input to the neural network.
# We also remove the last part of the numpy arrays, because the target-data has `NaN` for
# the shifted period, and we only want to have valid data and we need the same
# array-shapes for the input- and output-data.

# These are the input-signals:
x_data = df.values[0:-shift_steps]

# These are the output-signals (or target-signals):
y_data = df_targets.values[:-shift_steps]

# This is the number of observations (aka. data-points or samples) in the data-set:
num_data = len(x_data)

# This is the fraction of the data-set that will be used for the training-set:
train_split = 0.9

# This is the number of observations in the training-set:
num_train = int(train_split * num_data)

# This is the number of observations in the test-set:
num_test = num_data - num_train

# These are the input-signals for the training- and test-sets
x_train = x_data[0:num_train]
x_test = x_data[num_train:]
len(x_train) + len(x_test)

# These are the output-signals for the training- and test-sets:
y_train = y_data[0:num_train]
y_test = y_data[num_train:]
len(y_train) + len(y_test)

# This is the number of input-signals:
num_x_signals = x_data.shape[1]
# num_x_signals

# This is the number of output-signals:
num_y_signals = y_data.shape[1]



# Scaled Data
# ------------------------------------------------------------

# print("Min:", np.min(x_train))
# print("Max:", np.max(x_train))

# We first create a scaler-object for the input-signals.
x_scaler = MinMaxScaler()

# We then detect the range of values from the training-data and scale the training-data.
x_train_scaled = x_scaler.fit_transform(x_train)

# Apart from a small rounding-error, the data has been scaled to be between 0 and 1.
x_test_scaled = x_scaler.transform(x_test)

# The target-data comes from the same data-set as the input-signals, because it is
# the weather-data for one of the cities that is merely time-shifted. But the target-data
# could be from a different source with different value-ranges, so we create a separate
# scaler-object for the target-data.

y_scaler = MinMaxScaler()
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)




## Data Generator
# ------------------------------------------------------------

# The data-set has now been prepared as 2-dimensional numpy arrays.
# The training-data has almost 300k observations, consisting of 20 input-signals and 3 output-signals.

# These are the array-shapes of the input and output data:
print(x_train_scaled.shape)
print(y_train_scaled.shape)

# Instead of training the Recurrent Neural Network on the complete sequences of almost 300k observations,
# we will use the following function to create a batch of shorter sub-sequences picked at random from the training-data.

def batch_generator(batch_size, sequence_length):
    """
    Generator function for creating random batches of training-data.
    """

    # Infinite loop.
    while True:
        # Allocate a new array for the batch of input-signals.
        x_shape = (batch_size, sequence_length, num_x_signals)
        x_batch = np.zeros(shape=x_shape, dtype=np.float16)

        # Allocate a new array for the batch of output-signals.
        y_shape = (batch_size, sequence_length, num_y_signals)
        y_batch = np.zeros(shape=y_shape, dtype=np.float16)

        # Fill the batch with random sequences of data.
        for i in range(batch_size):
            # Get a random start-index.
            # This points somewhere into the training-data.
            idx = np.random.randint(num_train - sequence_length)

            # Copy the sequences of data starting at this index.
            x_batch[i] = x_train_scaled[idx:idx + sequence_length]
            y_batch[i] = y_train_scaled[idx:idx + sequence_length]

        yield (x_batch, y_batch)


# We will use a large batch-size so as to keep the GPU near 100% work-load.
# You may have to adjust this number depending on your GPU, its RAM and your choice of `sequence_length` below.
batch_size = 256


# We will use a sequence-length of 1344, which means that each random sequence contains observations for 8 weeks.
# One time-step corresponds to one hour, so 24 x 7 time-steps corresponds to a week, and 24 x 7 x 8 corresponds to 8 weeks.
sequence_length = 24 * 7 * 8

# We then create the batch-generator.
generator = batch_generator(batch_size=batch_size, sequence_length=sequence_length)

# We can then test the batch-generator to see if it works.
x_batch, y_batch = next(generator)

# This gives us a random batch of 256 sequences, each sequence having 1344 observations,
# and each observation having 20 input-signals and 3 output-signals.
print(x_batch.shape)
print(y_batch.shape)

# We can plot one of the 20 input-signals as an example.
batch = 0   # First sequence in the batch.
signal = 0  # First signal from the 20 input-signals.
seq = x_batch[batch, :, signal]
plt.plot(seq)

# We can also plot one of the output-signals that we want the model to learn how to predict given all those 20 input signals.
seq = y_batch[batch, :, signal]
plt.plot(seq)

# plt.show()




# Validation Set
# ------------------------------------------------------------

# The neural network trains quickly so we can easily run many training epochs.
# But then there is a risk of overfitting the model to the training-set so it does
# not generalize well to unseen data. We will therefore monitor the model's performance
# on the test-set after each epoch and only save the model's weights if the performance is improved on the test-set.

# The batch-generator randomly selects a batch of short sequences from the training-data and uses
# that during training. But for the validation-data we will instead run through the entire sequence
# from the test-set and measure the prediction accuracy on that entire sequence.

validation_data = (np.expand_dims(x_test_scaled, axis=0),
                   np.expand_dims(y_test_scaled, axis=0))




# Create the Recurrent Neural Network
# ------------------------------------------------------------
# We are now ready to create the Recurrent Neural Network (RNN).
# We will use the Keras API for this because of its simplicity. See Tutorial #03-C for
# a tutorial on Keras and Tutorial #20 for more information on Recurrent Neural Networks.

model = Sequential()
model.add(GRU(units=512,
              return_sequences=True,
              input_shape=(None, num_x_signals,)))
