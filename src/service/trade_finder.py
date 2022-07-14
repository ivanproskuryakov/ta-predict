import pandas as pd


class TradeFinder:

    def pick_best_options(self, df: pd.DataFrame, diff: float, diff_sum: float) -> pd.DataFrame:
        df = df.query(f'diff > {diff} and diff_sum < {diff_sum} and trades > 100')

        df = df.sort_values(by=['diff'], ascending=True)

        df = df.reset_index(drop=True)

        return df

    def pick_worst_options(self, df: pd.DataFrame, diff: float) -> pd.DataFrame:
        df = df.query(f'diff < {diff} and trades > 100')

        df = df.sort_values(by=['diff'], ascending=False)

        df = df.reset_index(drop=True)

        return df
