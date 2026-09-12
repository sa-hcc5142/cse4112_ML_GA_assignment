from src.config import GA_PARAMS
from src.chromosome import is_within_bounds
from src.population import initialize_population
from src.fitness import evaluate_population, sort_population, get_elite


def test_population_size_and_shape():
    pop = initialize_population(seed=42)
    assert len(pop) == GA_PARAMS["population_size"]
    for chromosome in pop:
        assert len(chromosome) == GA_PARAMS["num_genes"]


def test_population_within_bounds():
    pop = initialize_population(seed=7)
    for chromosome in pop:
        assert is_within_bounds(chromosome)


def test_reproducible_with_seed():
    pop_a = initialize_population(seed=123)
    pop_b = initialize_population(seed=123)
    assert pop_a == pop_b


def test_evaluate_population_matches_length():
    pop = initialize_population(seed=1)
    fitness = evaluate_population(pop)
    assert len(fitness) == len(pop)


def test_sort_population_ascending():
    pop = initialize_population(seed=1)
    fitness = evaluate_population(pop)
    sorted_pop, sorted_fit = sort_population(pop, fitness, ascending=True)
    assert sorted_fit == sorted(sorted_fit)


def test_get_elite_is_the_minimum():
    pop = initialize_population(seed=1)
    fitness = evaluate_population(pop)
    elite, elite_fit = get_elite(pop, fitness)
    assert elite_fit == min(fitness)
    assert elite == pop[fitness.index(min(fitness))]
