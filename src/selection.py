import random


def roulette_wheel_selection(population: list, fitness_values: list, num_parents: int):
    if len(population) != len(fitness_values):
        raise ValueError("Population and fitness values must have the same length")

    if num_parents <= 0:
        return []

    max_fitness = max(fitness_values)

    selection_values = [
        (max_fitness - fitness) + 1e-10
        for fitness in fitness_values
    ]

    total = sum(selection_values)

    if total == 0:
        probabilities = [1 / len(population)] * len(population)
    else:
        probabilities = [
            value / total
            for value in selection_values
        ]

    cumulative_probabilities = []
    cumulative = 0

    for probability in probabilities:
        cumulative += probability
        cumulative_probabilities.append(cumulative)

    selected_parents = []

    for _ in range(num_parents):
        r = random.random()

        for i, cumulative_probability in enumerate(cumulative_probabilities):
            if r <= cumulative_probability:
                selected_parents.append(population[i])
                break

    return selected_parents
