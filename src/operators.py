"""
Person 4 — Crossover, Mutation, Elitism (NOT YET IMPLEMENTED).

Owner: Person 4
Depends on: src.selection (parents), src.chromosome (bounds/encoding), src.fitness (elite comparison)

TODO(Person 4):

one_point_crossover(parent1, parent2, pc):
    With probability `pc` (default GA_PARAMS["pc"] = 0.80), pick a
    single crossover point in the 2-gene chromosome and swap the
    genes after that point between the two parents. With probability
    (1 - pc), return the parents unchanged (copy them, don't mutate
    the originals in place).

mutate(chromosome, pm):
    For EACH gene independently, with probability `pm` (default
    GA_PARAMS["pm"] = 0.05), replace that gene with a new value.
    Assignment note: "changing the gene value within range" -- e.g.
    resample uniformly in [-5, 5], or perturb with a small Gaussian
    step and clip back into [-5, 5]. Use src.chromosome.is_within_bounds()
    to verify the result.

apply_elitism(old_population, old_fitness, new_population, new_fitness, elitism):
    Carry the top `elitism` chromosomes (by old_fitness, ascending)
    into `new_population` unchanged, replacing the worst `elitism`
    individuals there. This guarantees the best solution is never
    lost between generations.
"""


def one_point_crossover(parent1: list, parent2: list, pc: float = None):
    raise NotImplementedError("Person 4: implement one_point_crossover()")


def mutate(chromosome: list, pm: float = None):
    raise NotImplementedError("Person 4: implement mutate()")


def apply_elitism(old_population, old_fitness, new_population, new_fitness, elitism: int = None):
    raise NotImplementedError("Person 4: implement apply_elitism()")
