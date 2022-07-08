import pandas as pd
from yachalk import chalk

from datetime import datetime
from tabulate import tabulate

from src.service.util import diff_percentage, diff_percentage_sum


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
            "diff_sum",
            "close_price_modified",
            "close_price",
            "trades",
            "volume",
            # "volume_market",

            # "x1o",
            # "x2c",
            # "y1c",
            # "y2c",

            "date",
            "h",
            "m",
            "url",
        ]

        for item in data:
            asset, last_item, x_df, y_df = item

            x_tail = x_df.tail(10)
            x_last = x_tail.iloc[-1]

            y1 = y_df.iloc[-2]
            y2 = y_df.iloc[-1]

            date = datetime.fromtimestamp(last_item["time_open"])

            diff = diff_percentage(v2=y2['close'], v1=y1['close'])
            diff_sum = diff_percentage_sum(x_tail)

            # print(x_tail)
            # print(x_last)
            # print(diff_sum)
            # exit()

            report.append([
                asset,
                diff,
                diff_sum,
                x_last['close'],
                last_item["price_close"],
                x_last["trades"],
                x_last["volume"],
                # volume_market,

                # f'{x1["open"]:.4f}',
                # f'{x2["close"]:.4f}',
                # f'{y1["close"]:.4f}',
                # f'{y2["close"]:.4f}',

                date.strftime("%Y %m %d %H:%M:%S"),
                f'{x_last["time_hour"]:.0f}',
                f'{x_last["time_minute"]:.0f}',
                f'https://www.binance.com/en/trade/{asset}_USDT',
            ])

        df = pd.DataFrame(report, None, headers)

        df.sort_values(by=['diff_sum'], inplace=True, ascending=False)

        df = df.reset_index(drop=True)

        return df
