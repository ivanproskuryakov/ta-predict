from keras.backend import square, mean


def split_window(features, total_window_size, label_width, input_width):
    label_start = total_window_size - label_width

    input_slice = slice(0, input_width)
    labels_slice = slice(label_start, None)

    inputs = features[:, input_slice, :]
    labels = features[:, labels_slice, :]

    inputs.set_shape([None, input_width, None])
    labels.set_shape([None, label_width, None])

    return inputs, labels

def loss_mse_warmup(y_true, y_pred):
    warmup_steps = 50
    """
    Calculate the Mean Squared Error between y_true and y_pred,
    but ignore the beginning "warmup" part of the sequences.

    y_true is the desired output.
    y_pred is the model's output.
    """

    # The shape of both input tensors are:
    # [batch_size, sequence_length, num_signals].

    # Ignore the "warmup" parts of the sequences
    # by taking slices of the tensors.
    y_true_slice = y_true[:, warmup_steps:, :]
    y_pred_slice = y_pred[:, warmup_steps:, :]

    # These sliced tensors both have this shape:
    # [batch_size, sequence_length - warmup_steps, num_signals]

    # Calculate the Mean Squared Error and use it as loss.
    mse = mean(square(y_true_slice - y_pred_slice))

    return mse
