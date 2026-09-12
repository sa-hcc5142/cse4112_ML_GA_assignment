"""Run the GA, generate plots, and write a parameter analysis report.

Run from the repository root:
    python -m analysis.run_analysis
"""

import argparse
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from src.config import GA_PARAMS
from src.fitness import evaluate_population
from src.ga import run_ga
from src.population import initialize_population

from analysis.plotting import (
    plot_convergence,
    plot_experiment_comparison,
    plot_selection_wheel,
)


@contextmanager
def temporary_parameters(overrides: dict[str, object]) -> Iterator[None]:
    """Temporarily apply GA parameters and restore them even if a run fails."""
    original = {key: GA_PARAMS[key] for key in overrides}
    GA_PARAMS.update(overrides)
    try:
        yield
    finally:
        GA_PARAMS.update(original)


def _run_variant(label: str, seed: int, overrides: dict[str, object]) -> dict:
    with temporary_parameters(overrides):
        result = run_ga(seed=seed)
    return {
        "label": label,
        "best_fitness": result["best_fitness"],
        "history": result["fitness_history"],
    }


def _write_report(
    output_path: Path,
    seed: int,
    baseline: dict,
    variants: list[dict],
) -> None:
    baseline_start = baseline["fitness_history"][0]
    baseline_end = baseline["best_fitness"]
    improvement = baseline_start - baseline_end

    lines = [
        "# Genetic Algorithm Analysis",
        "",
        "## Baseline run",
        "",
        f"- Seed: `{seed}`",
        f"- Population: `{GA_PARAMS['population_size']}`",
        f"- Generations: `{GA_PARAMS['num_generations']}`",
        f"- Crossover probability (pc): `{GA_PARAMS['pc']}`",
        f"- Mutation probability (pm): `{GA_PARAMS['pm']}`",
        f"- Elitism count: `{GA_PARAMS['elitism']}`",
        f"- Best chromosome: `{baseline['best_chromosome']}`",
        f"- Initial best fitness: `{baseline_start:.6f}`",
        f"- Final best fitness: `{baseline_end:.6f}`",
        f"- Improvement: `{improvement:.6f}`",
        "",
        "The convergence plot records the best value found up to each generation. "
        "Because the algorithm minimizes Ackley and elitism carries strong solutions "
        "forward, this curve should never increase.",
        "",
        "## Selection wheel",
        "",
        "Roulette-wheel selection converts lower Ackley values into larger selection "
        "probabilities. The pie chart uses the final population sample and applies "
        "the same inverse-fitness transformation as `src.selection`.",
        "",
        "## Parameter sensitivity",
        "",
        "| Variant | Final best fitness | Interpretation |",
        "| --- | ---: | --- |",
    ]

    interpretations = {
        "Lower crossover (pc=0.40)": "Less recombination can slow exploration of useful gene combinations.",
        "Full crossover (pc=1.00)": "More recombination increases mixing but does not itself add diversity.",
        "Lower mutation (pm=0.01)": "Less random exploration can make premature convergence more likely.",
        "Higher mutation (pm=0.20)": "More exploration can help escape local regions but may disrupt good solutions.",
        "No elitism (elitism=0)": "Good solutions can be lost, so progress is less protected.",
        "More elitism (elitism=3)": "More top individuals are preserved, which can speed exploitation and reduce diversity.",
    }
    for variant in variants:
        label = variant["label"]
        lines.append(
            f"| {label} | {variant['best_fitness']:.6f} | {interpretations[label]} |"
        )

    lines.extend(
        [
            "",
            "These comparisons use the same seed and one changed parameter per run. "
            "They are illustrative rather than a statistical benchmark; repeated runs "
            "with multiple seeds are recommended for a rigorous performance comparison.",
            "",
            "## Generated files",
            "",
            "- `convergence.png` - baseline best-fitness curve",
            "- `selection_wheel.png` - sample roulette-wheel probabilities",
            "- `parameter_comparison.png` - parameter sensitivity curves",
        ]
    )
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_analysis(output_dir: str | Path = "analysis/output", seed: int = 42) -> dict:
    """Run the baseline and parameter experiments and generate all artifacts."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    baseline = run_ga(seed=seed)
    initial_population = initialize_population(seed=seed)
    initial_fitness = evaluate_population(initial_population)
    plot_selection_wheel(initial_fitness, output_path / "selection_wheel.png")
    plot_convergence(baseline["fitness_history"], output_path / "convergence.png")

    variants = [
        ("Lower crossover (pc=0.40)", {"pc": 0.40}),
        ("Full crossover (pc=1.00)", {"pc": 1.00}),
        ("Lower mutation (pm=0.01)", {"pm": 0.01}),
        ("Higher mutation (pm=0.20)", {"pm": 0.20}),
        ("No elitism (elitism=0)", {"elitism": 0}),
        ("More elitism (elitism=3)", {"elitism": 3}),
    ]
    experiment_results = [
        _run_variant(label, seed, overrides) for label, overrides in variants
    ]
    histories = {"Baseline": baseline["fitness_history"]}
    histories.update({result["label"]: result["history"] for result in experiment_results})
    plot_experiment_comparison(histories, output_path / "parameter_comparison.png")

    baseline_report = dict(baseline)
    baseline_report["best_chromosome"] = baseline["best_chromosome"]
    _write_report(output_path / "analysis.md", seed, baseline_report, experiment_results)

    return {
        "output_dir": output_path,
        "baseline": baseline,
        "experiments": experiment_results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="analysis/output")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    result = run_analysis(args.output_dir, args.seed)
    baseline = result["baseline"]
    print(f"Analysis written to: {result['output_dir']}")
    print(f"Best chromosome: {baseline['best_chromosome']}")
    print(f"Best fitness: {baseline['best_fitness']:.6f}")
    print(f"Generated experiments: {len(result['experiments'])}")


if __name__ == "__main__":
    main()
