import pandas as pd

class TradeFinder:

    def pick_best_options(self, df: pd.DataFrame, diff: float) -> pd.DataFrame:
        df = df.query(f'diff > {diff}')

        df = df.sort_values(by=['trades'], ascending=False)

        df = df.reset_index(drop=True)

        return df
