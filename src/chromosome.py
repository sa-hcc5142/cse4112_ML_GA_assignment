import random
from src.config import GA_PARAMS


def random_gene() -> float:
    """One gene = one real number drawn uniformly from the search range."""
    low, high = GA_PARAMS["gene_bounds"]
    return random.uniform(low, high)


def random_chromosome() -> list:
    """A full chromosome = [x1, x2, ...] with num_genes genes."""
    return [random_gene() for _ in range(GA_PARAMS["num_genes"])]


def is_within_bounds(chromosome: list) -> bool:
    """
    Sanity check used by tests (and later by Person 4's mutation) to
    confirm every gene still respects -5 <= xi <= 5 after an operation.
    """
    low, high = GA_PARAMS["gene_bounds"]
    return all(low <= gene <= high for gene in chromosome)


if __name__ == "__main__":
    c = random_chromosome()
    print("Random chromosome:", c)
    print("Within bounds?", is_within_bounds(c))
