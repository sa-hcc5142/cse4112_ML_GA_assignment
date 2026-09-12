"""
Person 2 — Population initialization.

Generation 0 is created by drawing `population_size` chromosomes at
random, using Person 1's random_chromosome(). There is no bias toward
the optimum here on purpose: initialization must be blind, so any
progress we see later in the GA is genuinely coming from selection +
crossover + mutation, not from a lucky starting guess.
"""

import random
from src.config import GA_PARAMS
from src.chromosome import random_chromosome


def initialize_population(pop_size: int = None, seed: int = None) -> list:
    """
    Build the initial population (generation 0).

    Args:
        pop_size: number of chromosomes to create. Defaults to
            GA_PARAMS["population_size"] (50) if not given.
        seed: optional RNG seed, so results are reproducible when we
            need to show the exact same run twice (e.g. for debugging
            or for the report's example walkthrough).

    Returns:
        A list of `pop_size` chromosomes, each a [x1, x2] list.
    """
    if seed is not None:
        random.seed(seed)

    pop_size = GA_PARAMS["population_size"] if pop_size is None else pop_size
    return [random_chromosome() for _ in range(pop_size)]


if __name__ == "__main__":
    pop = initialize_population(seed=42)
    print(f"Generated {len(pop)} chromosomes.")
    for i, c in enumerate(pop[:5]):
        print(f"  #{i}: {c}")
    print("  ...")
