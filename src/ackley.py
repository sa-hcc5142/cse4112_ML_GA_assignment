"""
Person 1 — Ackley function.

The Ackley function is our GA's "fitness landscape". A GA never sees the
formula directly, it only ever calls this function to ask "how good is
this candidate solution?" — so getting this right, and being able to
explain every term, is the foundation everything else is built on.

f(x1, x2, ..., xn) =
    -a * exp( -b * sqrt( (1/2) * sum(xi^2) ) )
    - exp( (1/2) * sum(cos(c * xi)) )
    + a + e

For 2D with the recommended parameters (a=20, b=0.2, c=2*pi):

f(x1, x2) =
    -20 * exp( -0.2 * sqrt( 0.5 * (x1^2 + x2^2) ) )
    - exp( 0.5 * (cos(2*pi*x1) + cos(2*pi*x2)) )
    + 20 + e

Global minimum: f(0, 0) = 0.
"""

import math
from src.config import GA_PARAMS


def ackley_2d(x1: float, x2: float, a: float = None, b: float = None, c: float = None) -> float:
    """
    2D Ackley function. This is the ONE function the rest of the GA
    (fitness.py, and later selection/crossover/mutation) will call.

    Parameters default to GA_PARAMS so every teammate uses the exact
    same a, b, c unless they deliberately override them for an
    experiment (e.g. "what if b were smaller?").
    """
    a = GA_PARAMS["ackley_a"] if a is None else a
    b = GA_PARAMS["ackley_b"] if b is None else b
    c = GA_PARAMS["ackley_c"] if c is None else c

    term1 = -a * math.exp(-b * math.sqrt(0.5 * (x1 ** 2 + x2 ** 2)))
    term2 = -math.exp(0.5 * (math.cos(c * x1) + math.cos(c * x2)))
    return term1 + term2 + a + math.e


def ackley_nd(x: list, a: float = None, b: float = None, c: float = None) -> float:
    """
    General n-dimensional Ackley function, matching the formula given
    in the assignment. Included so we (and whoever grades this) can
    show ackley_2d() is just the n=2 special case of the same formula,
    not a separately made-up one.
    """
    a = GA_PARAMS["ackley_a"] if a is None else a
    b = GA_PARAMS["ackley_b"] if b is None else b
    c = GA_PARAMS["ackley_c"] if c is None else c

    n = len(x)
    sum_sq = sum(xi ** 2 for xi in x)
    sum_cos = sum(math.cos(c * xi) for xi in x)

    term1 = -a * math.exp(-b * math.sqrt(sum_sq / 2))
    term2 = -math.exp(sum_cos / 2)
    return term1 + term2 + a + math.e


if __name__ == "__main__":
    # Quick sanity check you can run directly: python -m src.ackley
    print("f(0, 0) =", ackley_2d(0.0, 0.0))          # should be ~0.0
    print("f(1, 1) =", ackley_2d(1.0, 1.0))
    print("f(-3.5, 4.2) =", ackley_2d(-3.5, 4.2))
    print("ackley_nd([0, 0]) =", ackley_nd([0.0, 0.0]))  # should match ackley_2d(0,0)
