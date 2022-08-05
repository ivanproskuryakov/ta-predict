import numpy as np
import pandas as pd
from decimal import Decimal


class Utility:
    def round(self, n: float, decimals=10):
        return np.round(float(n), decimals)

    def diff_percentage(self, v2, v1):
        diff = ((v2 - v1) / ((v2 + v1) / 2)) * 100
        diff = np.round(diff, 4)

        return diff

    def diff_percentage_sum(self, df: pd.DataFrame) -> int:
        percentage = 0

        for i in range(1, len(df)):
            close_previous = df.iloc[i - 1]['close']
            close_current = df.iloc[i]['close']
            percentage = percentage + self.diff_percentage(close_current, close_previous)

        return percentage

    def get_precision(self, f: float):
        precision = str(Decimal(f)).index('1')

        if precision == 0:
            return 2

        return precision - 1
