import numpy as np
import pandas as pd
from decimal import Decimal

from src.parameters import price_height


def round(n: float, decimals=10):
    return np.round(float(n), decimals)


def diff_percentage(v2, v1):
    diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
    diff = np.round(diff, 4)

    return diff


def diff_percentage_sum(df: pd.DataFrame) -> int:
    percentage = 0

    for i in range(1, len(df)):
        close_previous = df.iloc[i - 1]['close']
        close_current = df.iloc[i]['close']
        percentage = percentage + diff_percentage(close_current, close_previous)

    return percentage


def diff_price(price: float):
    diff = price_height / price

    return diff


def get_precision(f: float):
    precision = str(Decimal(f)).index('1')

    if precision == 0:
        return 2

    return precision - 1
