from src.service.util import Utility

utility = Utility()


def test_price_hight_btc():
    bnb = 0.011
    ada = 0.000023
    trx = 0.000003
    celo = 0.000045

    diff_ada = utility.diff_price(ada)
    diff_bnb = utility.diff_price(bnb)
    diff_trx = utility.diff_price(trx)
    diff_celo = utility.diff_price(celo)

    assert diff_ada == 434782608.6956522

    assert diff_bnb * bnb == 10000.0
    assert diff_ada * ada == 10000.0
    assert diff_trx * trx == 10000.0
    assert diff_celo * celo == 10000.0


def test_price_hight_usdt():
    bnb = 200
    ada = 0.4
    trx = 0.01
    celo = 0.8

    diff_ada = utility.diff_price(ada)
    diff_bnb = utility.diff_price(bnb)
    diff_trx = utility.diff_price(trx)
    diff_celo = utility.diff_price(celo)

    assert diff_ada == 25000.0

    assert diff_bnb * bnb == 10000.0
    assert diff_ada * ada == 10000.0
    assert diff_trx * trx == 10000.0
    assert diff_celo * celo == 10000.0
