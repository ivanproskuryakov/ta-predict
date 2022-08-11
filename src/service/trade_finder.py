import pandas as pd


class TradeFinder:
    def pick_best_options(self, df: pd.DataFrame, diff: float, rsi: float, trades: int) -> pd.DataFrame:
        df = df.query(f'diff > {diff} and rsi > {rsi} and trades > {trades}')

        df = df.sort_values(by=['diff_sum'], ascending=False)

        df = df.reset_index(drop=True)

        return df

    def pick_worst_options(self, df: pd.DataFrame, diff: float, rsi: float) -> pd.DataFrame:
        df = df.query(f'diff < {diff} and rsi < {rsi} and trades > 50')

        df = df.sort_values(by=['diff'], ascending=False)

        df = df.reset_index(drop=True)

        return df
