import pandas as pd
from yachalk import chalk

from tabulate import tabulate

from src.service.util import diff_percentage, diff_percentage_sum


class Reporter():
    def build_time(self, unscaled_last):
        time = f"{unscaled_last['time_month']:.0f} " \
               f"{unscaled_last['time_day']:.0f} " \
               f"{unscaled_last['time_hour']:.0f} " \
               f"{unscaled_last['time_minute']:.0f} "

        return time

    def report_prettify(self, df):
        df['diff'] = df['diff'].apply(lambda x: chalk.green(x) if x > 0.1 else x)

        table = tabulate(
            tabular_data=df.values,
            headers=df.keys(),
            tablefmt="simple",
            numalign="right"
        )

        return table

    def report_build(self, data) -> pd.DataFrame:
        report = []
        headers = [
            "asset",
            "diff",
            "diff_sum",
            "close_price_modified",
            "close_price",
            "trades",
            "volume",

            "date",
            "h",
            "m",
            "url",
        ]

        for item in data:
            asset, x_df, x_df_unscaled, y_df = item

            x_tail = x_df.tail(30)
            x_last = x_tail.iloc[-1]

            unscaled_last = x_df_unscaled.iloc[-1]
            unscaled_last_time = self.build_time(unscaled_last)

            y1 = y_df.iloc[-2]
            y2 = y_df.iloc[-1]

            diff = diff_percentage(v2=y2['close'], v1=y1['close'])
            diff_sum = diff_percentage_sum(x_tail)

            report.append([
                asset,
                diff,
                diff_sum,
                x_last['close'],
                unscaled_last["close"],
                x_last["trades"],
                x_last["volume"],

                unscaled_last_time,
                f'{x_last["time_hour"]:.0f}',
                f'{x_last["time_minute"]:.0f}',
                f'https://www.binance.com/en/trade/{asset}_USDT',
            ])

        df = pd.DataFrame(report, None, headers)

        df.sort_values(by=['diff'], inplace=True, ascending=True)

        df = df.reset_index(drop=True)

        return df
