import numpy as np


def diff_percentage(v2, v1):
    diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100 / 2
    diff = np.round(diff, 4)

    return diff
