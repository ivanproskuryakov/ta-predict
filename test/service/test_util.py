from src.service.util import diff_price


def test_price_hight():
    bnb = 0.011
    ada = 0.000023
    trx = 0.000003
    celo = 0.000045

    diff_ada = diff_price(ada)
    diff_bnb = diff_price(bnb)
    diff_trx = diff_price(trx)
    diff_celo = diff_price(celo)

    assert diff_bnb * bnb == 10000.0
    assert diff_ada * ada == 10000.0
    assert diff_trx * trx == 10000.0
    assert diff_celo * celo == 10000.0
