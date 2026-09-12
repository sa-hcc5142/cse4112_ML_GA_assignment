"""
Person 5 — Full GA loop, experiments, graphs, analysis.

Owner: Person 5
Depends on: src.population, src.fitness, src.selection, src.operators

TODO(Person 5):
    Wire everything together into run_ga():
      1. population = initialize_population()
      2. For each generation in range(num_generations):
           a. fitness = evaluate_population(population)
           b. sorted_population, sorted_fitness = sort_population(...)
           c. track best-ever ("elite") using apply_elitism logic
           d. parents = roulette_wheel_selection(...)
           e. build next generation via one_point_crossover + mutate
           f. apply_elitism to carry the best individual over
           g. record best fitness this generation (for the convergence graph)
      3. Stop after num_generations (or another agreed stopping rule).
      4. Record the convergence history for plotting and analysis.
"""

from src.config import GA_PARAMS
from src.fitness import evaluate_population, get_elite
from src.operators import apply_elitism, create_new_population
from src.population import initialize_population
from src.selection import roulette_wheel_selection


def run_ga(seed: int = None):
    """Run the configured genetic algorithm on the Ackley function.

    Args:
        seed: Optional random seed used for reproducible initialization and
            all subsequent selection, crossover, and mutation operations.

    Returns:
        A dictionary containing the best chromosome and fitness found, the
        final sorted population and fitness values, and the best fitness from
        each evaluated generation in ``fitness_history``.
    """
    population = initialize_population(
        pop_size=GA_PARAMS["population_size"],
        seed=seed,
    )

    best_chromosome = None
    best_fitness = float("inf")
    fitness_history = []

    for _ in range(GA_PARAMS["num_generations"]):
        fitness_values = evaluate_population(population)
        elite, elite_fitness = get_elite(population, fitness_values)

        if elite_fitness < best_fitness:
            best_chromosome = list(elite)
            best_fitness = elite_fitness

        fitness_history.append(best_fitness)

        parents = roulette_wheel_selection(
            population,
            fitness_values,
            num_parents=GA_PARAMS["population_size"],
        )
        offspring = create_new_population(
            parents,
            population_size=GA_PARAMS["population_size"],
            pc=GA_PARAMS["pc"],
            pm=GA_PARAMS["pm"],
        )
        offspring_fitness = evaluate_population(offspring)
        population, fitness_values = apply_elitism(
            old_population=population,
            old_fitness=fitness_values,
            new_population=offspring,
            new_fitness=offspring_fitness,
            elitism=GA_PARAMS["elitism"],
        )

    return {
        "best_chromosome": best_chromosome,
        "best_fitness": best_fitness,
        "fitness_history": fitness_history,
        "population": population,
        "fitness": fitness_values,
    }
