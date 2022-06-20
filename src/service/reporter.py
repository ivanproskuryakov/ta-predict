from datetime import datetime
from tabulate import tabulate
from src.service.util import diff_percentage, paint_diff


def render_console_table(report):
    table = []
    headers = [
        "asset",
        "diff %",
        "last real",
        "p1",
        "p2",
        "trades",
        "date",
        "url",
    ]

    for item in report:
        asset, last_item, x_df, y_df = item

        date = datetime.fromtimestamp(last_item["time_open"])

        # Measure
        last_real = x_df['close'].tail(1).values[0]

        tail = y_df['close'].tail(2).values

        # print(tail)

        last = tail[0]
        prediction = tail[1]

        diff = diff_percentage(v2=prediction, v1=last)

        if diff > 0.6:
            table.append([
                asset,
                paint_diff(diff),
                last_real,
                f'{tail[0]:.4f}',
                f'{tail[1]:.4f}',
                last_item["trades"],
                date.strftime("%Y %m %d %H:%M:%S"),
                f'https://www.binance.com/en/trade/{asset}_USDT',
            ])

    print(tabulate(table, headers, tablefmt="simple", numalign="right"))
