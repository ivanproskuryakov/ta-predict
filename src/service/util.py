import numpy as np

from keras.backend import square, mean
from yachalk import chalk


def diff_percentage(v2, v1):
    diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
    diff = np.round(diff, 4)

    return diff


def paint_diff(diff: float):
    color = f'{diff:.4f}'

    if diff > 0:
        color = chalk.green(f'{diff:.4f}%')
    # if diff < -1:
    #     color = chalk.red(f'{diff:.4f}%')

    return color


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
