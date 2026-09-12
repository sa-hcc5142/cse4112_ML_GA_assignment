import math

GA_PARAMS = {
    # --- Problem definition ---
    "num_genes": 2,              # chromosome = [x1, x2]
    "gene_bounds": (-5.0, 5.0),  # search space: -5 <= x1, x2 <= 5

    # --- Ackley function parameters (recommended values) ---
    "ackley_a": 20.0,
    "ackley_b": 0.2,
    "ackley_c": 2 * math.pi,

    # --- GA hyperparameters ---
    "population_size": 50,
    "num_generations": 100,
    "pc": 0.80,   # crossover probability
    "pm": 0.05,   # mutation probability (per gene)
    "elitism": 1, # number of best individuals carried over unchanged
}
