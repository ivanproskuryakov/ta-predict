import numpy as np


def batch_generator_random(
        x_data,
        y_data,
        x_num_signals,
        y_num_signals,
        batch_size,
        sequence_length,
):
    num_train = len(x_data)

    while True:
        # Allocate a new array for the batch of input-signals.
        x_shape = (batch_size, sequence_length, x_num_signals)
        x_batch = np.zeros(shape=x_shape, dtype=np.float32)

        # Allocate a new array for the batch of output-signals.
        y_shape = (batch_size, sequence_length, y_num_signals)
        y_batch = np.zeros(shape=y_shape, dtype=np.float32)

        # Fill the batch with random sequences of data.
        for i in range(batch_size):
            # Get a random start-index.
            # This points somewhere into the training-data.
            idx = np.random.randint(num_train - sequence_length)

            # Copy the sequences of data starting at this index.
            x_batch[i] = x_data[idx:idx + sequence_length]
            y_batch[i] = y_data[idx:idx + sequence_length]

        yield (x_batch, y_batch)
