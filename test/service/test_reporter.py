from src.service.reporter import Reporter
from fixture.prediction import load_predictions


def test_pick_best_option():
    reporter = Reporter()

    data = load_predictions()

    df = reporter.build_report(data=data)

    reporter.render_console_table(df)
