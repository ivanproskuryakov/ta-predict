import pandas as pd

from datetime import datetime
from tabulate import tabulate

from src.service.util import diff_percentage, paint_diff


def render_console_table(report):
    data = []
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

    for item in report:
        asset, last_item, x_df, y_df = item

        y_tail = y_df.tail(2)
        x_tail = x_df.tail(2)

        x1 = x_tail.iloc[0]
        x2 = x_tail.iloc[1]
        y1 = y_tail.iloc[0]
        y2 = y_tail.iloc[1]

        # print(x2)
        # print(asset)
        # print('-------')
        # print(x_tail)
        # print(x_df)
        # print(y_tail)
        # print(y_df)

        date = datetime.fromtimestamp(last_item["time_open"])

        diff = diff_percentage(v2=y2['close'], v1=y1['close'])

        volume_market = x2["volume"] * x1["open"]

        data.append([
            asset,
            paint_diff(diff),
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

    df = pd.DataFrame(data, None, headers)

    df.sort_values(by=['trades', 'diff'], inplace=True, ascending=True)

    df = df.reset_index(drop=True)

    print(tabulate(df.values, headers, tablefmt="simple", numalign="right"))
