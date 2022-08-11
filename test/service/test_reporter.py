from fixture.ohlc import crate_ohlc_many

from src.service.dataset_builder import DatasetBuilder
from src.service.reporter import Reporter

reporter = Reporter()


def test_report_prettify():
    assets = [
        'BTC',
    ]

    builder = DatasetBuilder(
        market='USDT',
        assets=assets,
        interval='5m',
    )

    crate_ohlc_many(asset='BTC', market='USDT', interval='5m', price=10000, quantity=100)

    collection = builder.build_dataset_predict()

    data = []
    data.append((collection[0], collection[0]))

    df = reporter.report_build(data=data)

    report = reporter.report_prettify(df)

    pos = report.find('close_price')

    assert pos == 31
