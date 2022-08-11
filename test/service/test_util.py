from src.service.util import Utility

utility = Utility()


def test_diff_percentage():
    diff = utility.diff_percentage(v1=0.001, v2=0.0004)

    assert diff == -85.7143
