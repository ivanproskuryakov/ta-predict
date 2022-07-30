from src.service.trade_finder import TradeFinder
from src.service.reporter import Reporter
from fixture.prediction import load_predictions

reporter = Reporter()
trade_finder = TradeFinder()

def test_pick_best_options():
    data = load_predictions()

    df = reporter.report_build(data=data)

    db_best = trade_finder.pick_best_options(df, diff=0, diff_sum=100)

    best = db_best.loc[0]

    assert best['asset'] == 'BTC'
