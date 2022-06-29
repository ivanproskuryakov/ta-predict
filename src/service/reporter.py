import pandas as pd
from yachalk import chalk

from datetime import datetime
from tabulate import tabulate

from src.service.util import diff_percentage


class Reporter():
    def report_prettify(self, df):
        df['diff'] = df['diff'].apply(lambda x: chalk.green(x) if x > 0.1 else x)
        # df['diff'] = df['diff'].apply(lambda x: chalk.red(x) if x < 0.1 else x)

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
            "trades",
            "volume",
            "volume_market",

            "x1o",
            "x2c",
            "y1c",
            "y2c",
            "date",
            "h",
            "m",
            "url",
        ]

        for item in data:
            asset, last_item, x_df, y_df = item

            y_tail = y_df.tail(2)
            x_tail = x_df.tail(2)

            x1 = x_tail.iloc[0]
            x2 = x_tail.iloc[1]
            y1 = y_tail.iloc[0]
            y2 = y_tail.iloc[1]

            date = datetime.fromtimestamp(last_item["time_open"])

            diff = diff_percentage(v2=y2['close'], v1=y1['close'])

            volume_market = x2["volume"] * x1["open"]

            report.append([
                asset,
                diff,
                x2["trades"],
                x2["volume"],
                volume_market,

                f'{x1["open"]:.4f}',
                f'{x2["close"]:.4f}',
                f'{y1["close"]:.4f}',
                f'{y2["close"]:.4f}',

                date.strftime("%Y %m %d %H:%M:%S"),
                f'{x2["time_hour"]:.0f}',
                f'{x2["time_minute"]:.0f}',
                f'https://www.binance.com/en/trade/{asset}_USDT',
            ])

        df = pd.DataFrame(report, None, headers)

        df.sort_values(by=['trades', 'diff'], inplace=True, ascending=True)

        df = df.reset_index(drop=True)

        return df
