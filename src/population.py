

import random
from src.config import GA_PARAMS
from src.chromosome import random_chromosome


def initialize_population(pop_size: int = None, seed: int = None) -> list:

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
