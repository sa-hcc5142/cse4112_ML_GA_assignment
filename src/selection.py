"""
Person 3 — Selection (NOT YET IMPLEMENTED).

Owner: Person 3
Depends on: src.fitness (evaluate_population, sort_population)

TODO(Person 3):
    Implement roulette_wheel_selection(). Suggested approach:
      1. Convert each fitness value (lower Ackley f = better) into a
         selection probability where LOWER f gets a HIGHER chance,
         e.g. probability_i = (max(f) - f_i + epsilon) / sum(...).
      2. Build a cumulative probability list.
      3. Draw a random number in [0, 1) and find which "slice" it
         falls into -- that chromosome is selected as a parent.
      4. Repeat to select `num_parents` parents (with replacement).
"""


def roulette_wheel_selection(population: list, fitness_values: list, num_parents: int):
    """
    Select `num_parents` chromosomes from `population` using
    fitness-proportionate (roulette wheel) selection, favoring LOWER
    Ackley fitness values.

    Returns: list of selected chromosomes, length == num_parents.
    """
    raise NotImplementedError("Person 3: implement roulette_wheel_selection()")
