"""
Demo: Person 4 genetic operators & generation transition.

Run from the repo root with:
    python -m scripts.demo_person4

Shows:
1. 1-point crossover demonstration with parent pairs.
2. Mutation demonstration (Gaussian perturbation within [-5, 5]).
3. A full generation step:
   Gen 0 -> Selection (Person 3) -> Crossover + Mutation (Person 4)
   -> Fitness Evaluation -> Elitism replacement (Person 4) -> Gen 1.
"""

import random
from src.population import initialize_population
from src.fitness import evaluate_population, sort_population, get_elite
from src.selection import roulette_wheel_selection
from src.operators import (
    one_point_crossover,
    mutate,
    apply_elitism,
    create_new_population,
)


def main():
    random.seed(42)

    print("=" * 65)
    print("DEMO: PERSON 4 GENETIC OPERATORS & GENERATION TRANSITION")
    print("=" * 65)

    # 1. 1-point Crossover Demo
    p1 = [-1.5, -1.0]
    p2 = [3.2, 4.5]
    c1, c2 = one_point_crossover(p1, p2, pc=1.0)
    print("\n[1] 1-Point Crossover (Pc = 1.0):")
    print(f"  Parent 1 : {p1}")
    print(f"  Parent 2 : {p2}")
    print(f"  Child 1  : {c1}  (swapped x2 with Parent 2)")
    print(f"  Child 2  : {c2}  (swapped x2 with Parent 1)")

    # 2. Mutation Demo
    original = [-1.5, -1.0]
    mutated_gaussian = mutate(original, pm=1.0, method="gaussian", sigma=0.5)
    print("\n[2] Mutation (Pm = 1.0, Gaussian, sigma=0.5):")
    print(f"  Original: {original}")
    print(f"  Mutated : {[round(x, 4) for x in mutated_gaussian]}")

    # 3. Full Generation Transition
    print("\n[3] Generation 0 -> Generation 1 Transition:")
    gen0_pop = initialize_population(seed=42)
    gen0_fit = evaluate_population(gen0_pop)
    gen0_sorted_pop, gen0_sorted_fit = sort_population(gen0_pop, gen0_fit)
    gen0_elite, gen0_elite_fit = get_elite(gen0_pop, gen0_fit)

    print(f"  Gen 0 Elite chromosome: {[round(x, 4) for x in gen0_elite]}")
    print(f"  Gen 0 Elite fitness   : {gen0_elite_fit:.6f}")

    # Selection (Person 3)
    parents = roulette_wheel_selection(gen0_pop, gen0_fit, num_parents=len(gen0_pop))

    # Crossover + Mutation to form offspring (Person 4)
    offspring = create_new_population(parents, population_size=len(gen0_pop), pc=0.80, pm=0.05)
    offspring_fit = evaluate_population(offspring)

    # Elitism (Person 4)
    gen1_pop, gen1_fit = apply_elitism(
        old_population=gen0_pop,
        old_fitness=gen0_fit,
        new_population=offspring,
        new_fitness=offspring_fit,
        elitism=1
    )

    gen1_elite = gen1_pop[0]
    gen1_elite_fit = gen1_fit[0]

    print(f"  Gen 1 Elite chromosome: {[round(x, 4) for x in gen1_elite]}")
    print(f"  Gen 1 Elite fitness   : {gen1_elite_fit:.6f}")

    improvement = gen0_elite_fit - gen1_elite_fit
    print(f"  Improvement           : {improvement:+.6f} (monotonic non-increasing guaranteed)")
    print(f"  Population size check : {len(gen1_pop)} individuals")
    print("=" * 65)


if __name__ == "__main__":
    main()
