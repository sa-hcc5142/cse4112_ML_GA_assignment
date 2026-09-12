"""
Person 4 — Crossover, Mutation, Elitism, and New Population Generation.

Owner: Person 4
Depends on: src.config (parameters), src.chromosome (bounds), src.fitness (sorting)

This module implements the core genetic operators for real-valued chromosomes
on the 2D Ackley function:
1. one_point_crossover(): recombine two parents with probability Pc (default 80%).
2. mutate(): perturb/resample genes within [-5, 5] with probability Pm (default 5%).
3. apply_elitism(): guarantee that the best solution from the previous generation
   is carried over into the next generation.
4. create_new_population(): assemble the next generation by pairing parents,
   applying crossover and mutation.
"""

import random
from typing import List, Tuple, Optional
from src.config import GA_PARAMS
from src.chromosome import is_within_bounds
from src.fitness import sort_population


def one_point_crossover(
    parent1: list,
    parent2: list,
    pc: Optional[float] = None
) -> Tuple[list, list]:
    """
    Perform 1-point crossover between two parents with probability pc.

    With probability `pc` (default GA_PARAMS["pc"] = 0.80), a crossover point
    is chosen and genes after that point are swapped between parent1 and parent2.
    For a 2-gene chromosome [x1, x2], the crossover point is always index 1,
    swapping the second gene:
        parent1 = [p1_x1, p1_x2], parent2 = [p2_x1, p2_x2]
        child1  = [p1_x1, p2_x2], child2  = [p2_x1, p1_x2]

    With probability (1 - pc), the parents are returned unchanged as fresh copies.

    Returns:
        (child1, child2): two new chromosome lists.
    """
    if pc is None:
        pc = GA_PARAMS["pc"]

    if len(parent1) != len(parent2):
        raise ValueError("Parents must have identical chromosome length")

    # If chromosome has fewer than 2 genes or crossover doesn't trigger
    if len(parent1) < 2 or random.random() >= pc:
        return list(parent1), list(parent2)

    # 1-point crossover: point is between 1 and len - 1
    point = random.randint(1, len(parent1) - 1)

    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]

    return child1, child2


def mutate(
    chromosome: list,
    pm: Optional[float] = None,
    method: str = "gaussian",
    sigma: float = 0.5
) -> list:
    """
    Mutate a chromosome with per-gene probability pm.

    For EACH gene independently:
      - With probability `pm` (default GA_PARAMS["pm"] = 0.05), perturb or resample
        the gene within the valid search space [-5.0, 5.0].
      - Supported mutation methods:
        - "gaussian": adds Gaussian noise N(0, sigma) and clamps to bounds [-5, 5].
          e.g. [-1.5, -1.0] -> [-0.5, -1.0].
        - "uniform": resamples the gene uniformly from [-5, 5].

    The resulting genes are strictly clamped to GA_PARAMS["gene_bounds"]
    so that is_within_bounds(mutated) is always True.

    Returns:
        A new mutated chromosome list (does not modify original in place).
    """
    if pm is None:
        pm = GA_PARAMS["pm"]

    low, high = GA_PARAMS["gene_bounds"]
    mutated = list(chromosome)

    for i in range(len(mutated)):
        if random.random() < pm:
            if method == "gaussian":
                val = mutated[i] + random.gauss(0, sigma)
            elif method == "uniform":
                val = random.uniform(low, high)
            else:
                raise ValueError(f"Unknown mutation method: {method}")

            # Keep strictly within search bounds [-5.0, 5.0]
            mutated[i] = max(low, min(high, val))

    return mutated


def apply_elitism(
    old_population: list,
    old_fitness: list,
    new_population: list,
    new_fitness: list,
    elitism: Optional[int] = None
) -> Tuple[list, list]:
    """
    Carry the top `elitism` individuals from old_population into new_population.

    In a minimization problem, lower fitness values are better.
    The top `elitism` best chromosomes (lowest fitness) from the old population
    replace the worst individuals in `new_population` whenever the old elite is
    better than those individuals. This guarantees:
      1. The best solution discovered so far is never lost across generations.
      2. Population size remains strictly constant (e.g. 50).

    Returns:
        (updated_population, updated_fitness): sorted ascending by fitness.
    """
    if elitism is None:
        elitism = GA_PARAMS["elitism"]

    if elitism <= 0:
        return sort_population(new_population, new_fitness, ascending=True)

    # Sort old population: best (lowest fitness) first
    sorted_old_pop, sorted_old_fit = sort_population(old_population, old_fitness, ascending=True)

    # Sort new population: best (lowest fitness) first, worst at the end
    sorted_new_pop, sorted_new_fit = sort_population(new_population, new_fitness, ascending=True)

    # Replace the worst individuals of new_population if old elites are better
    for k in range(min(elitism, len(sorted_old_pop), len(sorted_new_pop))):
        worst_idx = -(k + 1)
        if sorted_old_fit[k] < sorted_new_fit[worst_idx]:
            sorted_new_pop[worst_idx] = list(sorted_old_pop[k])
            sorted_new_fit[worst_idx] = sorted_old_fit[k]

    # Re-sort new population ascending so population[0] is guaranteed the best
    return sort_population(sorted_new_pop, sorted_new_fit, ascending=True)


def create_new_population(
    selected_parents: list,
    population_size: Optional[int] = None,
    pc: Optional[float] = None,
    pm: Optional[float] = None,
    mutation_method: str = "gaussian",
    sigma: float = 0.5
) -> list:
    """
    Generate the next generation of chromosomes from selected parents.

    Pairs up selected parents from roulette wheel selection, applies 1-point
    crossover with probability `pc`, and applies mutation with probability `pm`
    to produce exactly `population_size` offspring.

    Args:
        selected_parents: List of parent chromosomes from selection.
        population_size: Target number of offspring (default GA_PARAMS["population_size"]).
        pc: Crossover probability (default GA_PARAMS["pc"] = 0.80).
        pm: Mutation probability (default GA_PARAMS["pm"] = 0.05).
        mutation_method: "gaussian" or "uniform".
        sigma: Perturbation step size for Gaussian mutation.

    Returns:
        List of new offspring chromosomes of length `population_size`.
    """
    if population_size is None:
        population_size = GA_PARAMS["population_size"]
    if pc is None:
        pc = GA_PARAMS["pc"]
    if pm is None:
        pm = GA_PARAMS["pm"]

    if not selected_parents:
        raise ValueError("selected_parents cannot be empty")

    offspring = []
    num_parents = len(selected_parents)
    idx = 0

    while len(offspring) < population_size:
        p1 = selected_parents[idx % num_parents]
        p2 = selected_parents[(idx + 1) % num_parents]
        idx += 2

        c1, c2 = one_point_crossover(p1, p2, pc=pc)
        c1 = mutate(c1, pm=pm, method=mutation_method, sigma=sigma)
        c2 = mutate(c2, pm=pm, method=mutation_method, sigma=sigma)

        offspring.append(c1)
        if len(offspring) < population_size:
            offspring.append(c2)

    return offspring
