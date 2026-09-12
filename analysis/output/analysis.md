# Genetic Algorithm Analysis

## Baseline run

- Seed: `42`
- Population: `50`
- Generations: `100`
- Crossover probability (pc): `0.8`
- Mutation probability (pm): `0.05`
- Elitism count: `1`
- Best chromosome: `[-0.0008109721745585378, 0.003273325897241393]`
- Initial best fitness: `5.447495`
- Final best fitness: `0.009841`
- Improvement: `5.437654`

The convergence plot records the best value found up to each generation. Because the algorithm minimizes Ackley and elitism carries strong solutions forward, this curve should never increase.

## Selection wheel

Roulette-wheel selection converts lower Ackley values into larger selection probabilities. The pie chart uses the final population sample and applies the same inverse-fitness transformation as `src.selection`.

## Parameter sensitivity

| Variant | Final best fitness | Interpretation |
| --- | ---: | --- |
| Lower crossover (pc=0.40) | 0.011393 | Less recombination can slow exploration of useful gene combinations. |
| Full crossover (pc=1.00) | 0.010678 | More recombination increases mixing but does not itself add diversity. |
| Lower mutation (pm=0.01) | 0.073762 | Less random exploration can make premature convergence more likely. |
| Higher mutation (pm=0.20) | 0.006645 | More exploration can help escape local regions but may disrupt good solutions. |
| No elitism (elitism=0) | 0.076158 | Good solutions can be lost, so progress is less protected. |
| More elitism (elitism=3) | 0.015357 | More top individuals are preserved, which can speed exploitation and reduce diversity. |

These comparisons use the same seed and one changed parameter per run. They are illustrative rather than a statistical benchmark; repeated runs with multiple seeds are recommended for a rigorous performance comparison.

## Generated files

- `convergence.png` - baseline best-fitness curve
- `selection_wheel.png` - sample roulette-wheel probabilities
- `parameter_comparison.png` - parameter sensitivity curves
