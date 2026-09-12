"""
Person 5 — Full GA loop, experiments, graphs, analysis (NOT YET IMPLEMENTED).

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
      4. Plot: pie chart of a sample selection wheel, convergence
         curve (best fitness vs. generation), and write up the
         analysis (why convergence looks the way it does, what
         happens if pc/pm/elitism change, etc.)
"""


def run_ga(seed: int = None):
    raise NotImplementedError("Person 5: implement run_ga()")
