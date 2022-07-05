from src.service.reporter import Reporter
from fixture.prediction import load_predictions

reporter = Reporter()


def test_report_prettify():
    data = load_predictions()

    df = reporter.report_build(data=data)

    report = reporter.report_prettify(df)

    pos = report.find('close_price')

    assert pos == 20
