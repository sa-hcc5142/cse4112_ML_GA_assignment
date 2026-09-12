# CSE 4112 ML Lab — Genetic Algorithm on the 2D Ackley Function

Find the global minimum of the 2D Ackley function using a Genetic Algorithm (GA).

- Search space: -5 <= x1, x2 <= 5
- Global minimum: f(x1*, x2*) = f(0, 0) = 0
- Encoding: value encoding, chromosome = [x1, x2]
- GA settings: population = 50, generations = 100, Pc = 80%, Pm = 5%, elitism = 1

## Team pipeline (sequential — each person builds on the last)

| # | Owner | Scope | Status |
|---|-------|-------|--------|
| 1 | Person 1 | Ackley function, GA config, chromosome representation | ✅ Done |
| 2 | Person 2 | Population initialization, fitness evaluation, sorting, per-generation elite | ✅ Done |
| 3 | Person 3 | Roulette-wheel selection | ✅ Done |
| 4 | Person 4 | 1-point crossover, mutation, elitism carry-over | ⬜ TODO — see `src/operators.py` |
| 5 | Person 5 | Full GA loop, experiments, graphs, analysis | ⬜ TODO — see `src/ga.py` |

## Folder structure

```
cse4112_ML_GA_assignment/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── config.py        # Person 1 — all GA/Ackley parameters in one place
│   ├── ackley.py         # Person 1 — ackley_2d(), ackley_nd()
│   ├── chromosome.py     # Person 1 — value-encoded chromosome helpers
│   ├── population.py     # Person 2 — initialize_population()
│   ├── fitness.py        # Person 2 — evaluate_population(), sort_population(), get_elite()
│   ├── selection.py       # Person 3 — TODO: roulette_wheel_selection()
│   ├── operators.py       # Person 4 — TODO: one_point_crossover(), mutate(), apply_elitism()
│   └── ga.py               # Person 5 — TODO: run_ga()
├── tests/
│   ├── __init__.py
│   ├── test_ackley.py
│   └── test_population_fitness.py
└── scripts/
    ├── __init__.py
    └── demo_person1_person2.py
```

## Setup

```bash
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Running things

Run the Person 1 + 2 demo (population init -> fitness -> sorted -> elite):

```bash
python -m scripts.demo_person1_person2
```

Run the tests:

```bash
pytest -v
```

## Design notes (for the report / viva)

- **Value encoding, not binary**: a chromosome is `[x1, x2]`, real numbers directly, since
  Ackley's inputs are continuous. This avoids an unnecessary encode/decode step.
- **Minimization, not maximization**: lower `f(x1, x2)` = fitter. `sort_population()` sorts
  ascending by default so `population[0]` is always the current best. Converting this into a
  roulette-wheel *selection probability* (where lower fitness means a bigger slice) is Person
  3's job, kept separate from raw fitness computation here.
- **Reproducibility**: `initialize_population(seed=...)` accepts a seed so any run can be
  reproduced exactly — useful for the report's worked examples and for debugging with
  teammates.
- **Elite vs. elitism**: `get_elite()` (Person 2) only reports the best individual *within one
  generation*. Deciding whether to *keep* the previous best-ever across generations (only
  replacing it if the new one is strictly better) is elitism logic, implemented by Person 4 /
  Person 5 — this keeps the two concerns from being tangled in one function.
