import numpy as np


def round(n: float, decimals=10):
    return np.round(float(n), decimals)


def diff_percentage(v2, v1):
    diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
    diff = np.round(diff, 4)

    return diff
