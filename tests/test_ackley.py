from src.ackley import ackley_2d, ackley_nd


def test_global_minimum_is_zero():
    # f(0, 0) should be (numerically) exactly 0
    assert abs(ackley_2d(0.0, 0.0)) < 1e-9


def test_nd_matches_2d_at_origin():
    # ackley_2d is the n=2 special case of ackley_nd
    assert abs(ackley_nd([0.0, 0.0]) - ackley_2d(0.0, 0.0)) < 1e-9


def test_away_from_origin_is_positive():
    # Everywhere except the global minimum, Ackley should be > 0
    assert ackley_2d(1.0, 1.0) > 0
    assert ackley_2d(-3.5, 4.2) > 0
    assert ackley_2d(5.0, -5.0) > 0
