import pytest
from src.config import GA_PARAMS
from src.chromosome import is_within_bounds
from src.population import initialize_population
from src.fitness import evaluate_population
from src.selection import roulette_wheel_selection
from src.operators import (
    one_point_crossover,
    mutate,
    apply_elitism,
    create_new_population,
)


def test_one_point_crossover_pc_1():
    parent1 = [1.0, 2.0]
    parent2 = [3.0, 4.0]
    child1, child2 = one_point_crossover(parent1, parent2, pc=1.0)

    # For 2-gene chromosome, 1-point crossover swaps the second gene
    assert child1 == [1.0, 4.0]
    assert child2 == [3.0, 2.0]


def test_one_point_crossover_pc_0():
    parent1 = [1.0, 2.0]
    parent2 = [3.0, 4.0]
    child1, child2 = one_point_crossover(parent1, parent2, pc=0.0)

    # When crossover does not trigger, exact copies are returned
    assert child1 == parent1
    assert child2 == parent2
    # Ensure they are independent copies
    assert child1 is not parent1
    assert child2 is not parent2


def test_one_point_crossover_immutability():
    parent1 = [1.5, -2.5]
    parent2 = [-3.0, 4.0]
    p1_copy = list(parent1)
    p2_copy = list(parent2)

    one_point_crossover(parent1, parent2, pc=1.0)
    assert parent1 == p1_copy
    assert parent2 == p2_copy


def test_mutate_pm_0():
    chromosome = [-1.5, 2.5]
    mutated = mutate(chromosome, pm=0.0)
    assert mutated == chromosome
    assert mutated is not chromosome


def test_mutate_pm_1():
    chromosome = [-1.5, 2.5]
    mutated = mutate(chromosome, pm=1.0, method="gaussian")
    # All genes should have changed
    assert mutated[0] != chromosome[0]
    assert mutated[1] != chromosome[1]
    assert is_within_bounds(mutated)


def test_mutate_boundary_clamping():
    # Extreme edge cases
    chromosome = [5.0, -5.0]
    for _ in range(20):
        mutated = mutate(chromosome, pm=1.0, method="gaussian", sigma=10.0)
        assert is_within_bounds(mutated)
        assert -5.0 <= mutated[0] <= 5.0
        assert -5.0 <= mutated[1] <= 5.0


def test_mutate_uniform_method():
    chromosome = [0.0, 0.0]
    mutated = mutate(chromosome, pm=1.0, method="uniform")
    assert is_within_bounds(mutated)


def test_apply_elitism_preserves_best():
    old_pop = [[0.0, 0.0], [2.0, 2.0], [3.0, 3.0]]
    old_fit = [0.1, 5.0, 8.0]  # [0.0, 0.0] is the best (0.1)

    new_pop = [[1.0, 1.0], [2.5, 2.5], [4.0, 4.0]]
    new_fit = [2.0, 6.0, 10.0]  # Best here is 2.0 (worse than old elite 0.1)

    updated_pop, updated_fit = apply_elitism(old_pop, old_fit, new_pop, new_fit, elitism=1)

    # The old elite [0.0, 0.0] must now be in new_pop and at position 0
    assert updated_fit[0] == 0.1
    assert updated_pop[0] == [0.0, 0.0]
    # Population size should remain constant (3)
    assert len(updated_pop) == len(new_pop)
    assert len(updated_fit) == len(new_fit)


def test_apply_elitism_when_new_is_already_better():
    old_pop = [[1.0, 1.0], [2.0, 2.0]]
    old_fit = [3.0, 5.0]

    new_pop = [[0.1, 0.1], [4.0, 4.0]]
    new_fit = [0.5, 9.0]  # 0.5 is already better than old elite 3.0

    updated_pop, updated_fit = apply_elitism(old_pop, old_fit, new_pop, new_fit, elitism=1)

    # Best must still be 0.5
    assert updated_fit[0] == 0.5
    assert updated_pop[0] == [0.1, 0.1]
    # The old elite 3.0 should replace the worst (9.0)
    assert 3.0 in updated_fit
    assert 9.0 not in updated_fit
    assert len(updated_pop) == 2


def test_create_new_population_size_and_bounds():
    pop = initialize_population(seed=42)
    fit = evaluate_population(pop)
    parents = roulette_wheel_selection(pop, fit, num_parents=50)

    offspring = create_new_population(parents, population_size=50, pc=0.8, pm=0.05)
    assert len(offspring) == 50

    for chromosome in offspring:
        assert len(chromosome) == GA_PARAMS["num_genes"]
        assert is_within_bounds(chromosome)
