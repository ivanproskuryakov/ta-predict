from src.service.reporter import Reporter
from fixture.prediction import load_predictions


def test_report_prettify():
    reporter = Reporter()

    data = load_predictions()

    df = reporter.report_build(data=data)

    report = reporter.report_prettify(df)

    pos = report.find('volume_market')

    assert pos == 40
