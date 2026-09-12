"""
Person 2 — Fitness evaluation.

This is a MINIMIZATION problem: the lower f(x1, x2) is, the fitter the
chromosome (0 is the theoretical best possible). Everything here is
written around that: sort_population() defaults to ascending order so
population[0] is always the best individual, and get_elite() just
reads that first slot off.

Person 3 (roulette wheel) will need to convert these raw Ackley values
into selection probabilities where LOWER f = HIGHER chance of being
picked -- that transformation belongs in Person 3's selection.py, not
here. This file only computes and orders raw fitness.
"""

from src.ackley import ackley_2d


def evaluate_population(population: list) -> list:
    """
    Compute f(x1, x2) for every chromosome in the population.

    Returns a list of floats, same order and length as `population`,
    so fitness_values[i] is always the fitness of population[i].
    """
    return [ackley_2d(chromosome[0], chromosome[1]) for chromosome in population]


def sort_population(population: list, fitness_values: list, ascending: bool = True):
    """
    Sort the population by fitness.

    ascending=True  -> best (lowest f) first. Use this for a
                       minimization problem like ours.
    ascending=False -> use only if you deliberately want worst-first
                       (e.g. to display/report the weakest individuals).

    Returns (sorted_population, sorted_fitness_values) as a matched pair.
    """
    paired = list(zip(population, fitness_values))
    paired.sort(key=lambda item: item[1], reverse=not ascending)
    sorted_population = [chromosome for chromosome, _ in paired]
    sorted_fitness = [fit for _, fit in paired]
    return sorted_population, sorted_fitness


def get_elite(population: list, fitness_values: list):
    """
    Return (elite_chromosome, elite_fitness): the single best
    individual in this generation (lowest Ackley value).

    Person 4 will compare this against the PREVIOUS generation's elite
    and only replace it if the new one is strictly better -- that
    "keep the best ever seen" logic lives in operators.py / ga.py, not
    here. This function only answers "who's best in THIS generation".
    """
    sorted_population, sorted_fitness = sort_population(population, fitness_values, ascending=True)
    return sorted_population[0], sorted_fitness[0]


if __name__ == "__main__":
    from src.population import initialize_population

    pop = initialize_population(seed=42)
    fitness = evaluate_population(pop)
    sorted_pop, sorted_fit = sort_population(pop, fitness)
    elite, elite_fit = get_elite(pop, fitness)

    print("Best 5 (ascending fitness):")
    for c, f in zip(sorted_pop[:5], sorted_fit[:5]):
        print(f"  {c} -> f = {f:.6f}")
    print(f"\nElite chromosome: {elite}")
    print(f"Elite fitness: {elite_fit:.6f}")
