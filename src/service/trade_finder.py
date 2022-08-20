import pandas as pd


class TradeFinder:
    def find_bullish(self, df: pd.DataFrame, diff: float, rsi: float, trades: int, limit: int) -> pd.DataFrame:
        df = df.query(f'diff > {diff} and rsi > {rsi} and trades > {trades}')

        df = df.sort_values(by=['diff'], ascending=False)
        df = df.reset_index(drop=True)
        df = df[0:limit]

        return df

    def find_bearish(self, df: pd.DataFrame, diff: float, rsi: float, trades: int, limit: int) -> pd.DataFrame:
        df = df.query(f'diff < {diff} and rsi < {rsi} and trades > {trades}')

        df = df.sort_values(by=['diff'], ascending=True)
        df = df.reset_index(drop=True)
        df = df[0:limit]

        return df
