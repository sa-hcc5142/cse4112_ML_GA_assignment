# GA Analysis

This folder contains the plotting and experiment layer for the 2D Ackley genetic algorithm. It does not change the implementation in `src/`.

## Generate the plots and report

From the repository root:

```bash
python -m analysis.run_analysis
```

Optional arguments:

```bash
python -m analysis.run_analysis --seed 42 --output-dir analysis/output
```

The command creates:

- `output/convergence.png`: best-so-far fitness by generation.
- `output/selection_wheel.png`: roulette-wheel probabilities for a population sample.
- `output/parameter_comparison.png`: baseline and parameter sensitivity curves.
- `output/analysis.md`: numerical results and interpretation of `pc`, `pm`, and elitism.

The output directory is generated and can be deleted and recreated at any time.
