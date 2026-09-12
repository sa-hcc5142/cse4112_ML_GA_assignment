"""
Demo: everything Person 1 + Person 2 have built so far, run end to end.

Run from the repo root with:
    python -m scripts.demo_person1_person2

(Persons 3-5 haven't plugged in yet, so this stops at "here's
generation 0, sorted, with its elite" -- exactly the handoff point
for Person 3's selection.py.)
"""

from src.population import initialize_population
from src.fitness import evaluate_population, sort_population, get_elite


def main():
    # seed=42 so this demo is reproducible when we show it in the report
    population = initialize_population(seed=42)
    fitness_values = evaluate_population(population)
    sorted_population, sorted_fitness = sort_population(population, fitness_values)
    elite, elite_fitness = get_elite(population, fitness_values)

    print(f"Population size: {len(population)}")
    print(f"Elite chromosome (generation 0): {elite}")
    print(f"Elite fitness f(x1, x2): {elite_fitness:.6f}\n")

    print("Top 5 chromosomes (best -> worse):")
    for chromosome, fit in zip(sorted_population[:5], sorted_fitness[:5]):
        print(f"  {[round(g, 4) for g in chromosome]} -> f = {fit:.6f}")

    print("\nWorst 5 chromosomes:")
    for chromosome, fit in zip(sorted_population[-5:], sorted_fitness[-5:]):
        print(f"  {[round(g, 4) for g in chromosome]} -> f = {fit:.6f}")


if __name__ == "__main__":
    main()
