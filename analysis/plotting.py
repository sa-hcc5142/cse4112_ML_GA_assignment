"""Reusable plots for GA convergence and roulette-wheel selection."""

from pathlib import Path
from typing import Sequence

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def selection_probabilities(fitness_values: Sequence[float]) -> list[float]:
    """Convert minimization fitness values into roulette-wheel probabilities."""
    if not fitness_values:
        raise ValueError("fitness_values cannot be empty")

    maximum = max(fitness_values)
    selection_values = [(maximum - fitness) + 1e-10 for fitness in fitness_values]
    total = sum(selection_values)

    if total == 0:
        return [1.0 / len(fitness_values)] * len(fitness_values)
    return [value / total for value in selection_values]


def plot_selection_wheel(
    fitness_values: Sequence[float],
    output_path: str | Path,
    sample_size: int = 8,
) -> Path:
    """Save a pie chart showing selection probabilities for a population sample."""
    if sample_size <= 0:
        raise ValueError("sample_size must be positive")

    sample = list(fitness_values[:sample_size])
    if not sample:
        raise ValueError("fitness_values cannot be empty")

    probabilities = selection_probabilities(sample)
    deep_colors = [
        "#5080B4",
        "#BD5582",
        "#B25DCA",
        "#CB5C43",
        "#8073DE",
        "#88D41D",
        "#B9B7F3",
        "#CA6D6D",
    ]
    colors = [deep_colors[index % len(deep_colors)] for index in range(len(sample))]
    labels = [f"Individual {index + 1}\nf={fitness:.3f}" for index, fitness in enumerate(sample)]

    figure, axis = plt.subplots(figsize=(9, 7), constrained_layout=True)
    axis.pie(
        probabilities,
        labels=labels,
        colors=colors,
        startangle=90,
        counterclock=False,
        autopct=lambda value: f"{value:.1f}%" if value >= 3 else "",
        pctdistance=0.72,
        wedgeprops={"linewidth": 1.2, "edgecolor": "white"},
        textprops={"fontsize": 9, "color": "black"},
    )
    axis.set_title("Roulette-Wheel Selection Probabilities\nFinal population sample")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return path


def plot_convergence(
    fitness_history: Sequence[float],
    output_path: str | Path,
) -> Path:
    """Save the best-ever Ackley fitness against generation number."""
    if not fitness_history:
        raise ValueError("fitness_history cannot be empty")

    generations = range(1, len(fitness_history) + 1)
    figure, axis = plt.subplots(figsize=(10, 6), constrained_layout=True)
    axis.plot(
        generations,
        fitness_history,
        color="#176b87",
        linewidth=2.4,
        marker="o" if len(fitness_history) <= 40 else None,
        markersize=3,
        label="Best-so-far fitness",
    )
    axis.fill_between(generations, fitness_history, 0, color="#176b87", alpha=0.10)
    axis.set_title("GA Convergence on the 2D Ackley Function")
    axis.set_xlabel("Generation")
    axis.set_ylabel("Ackley fitness (lower is better)")
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper right")
    axis.set_ylim(bottom=0)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return path


def plot_experiment_comparison(
    histories: dict[str, Sequence[float]],
    output_path: str | Path,
) -> Path:
    """Save a comparison plot for parameter experiments."""
    if not histories:
        raise ValueError("histories cannot be empty")

    figure, axis = plt.subplots(figsize=(10, 6), constrained_layout=True)
    for label, history in histories.items():
        if not history:
            raise ValueError(f"history for {label!r} cannot be empty")
        axis.plot(range(1, len(history) + 1), history, linewidth=2, label=label)

    axis.set_title("Parameter Sensitivity: Best-So-Far Fitness")
    axis.set_xlabel("Generation")
    axis.set_ylabel("Ackley fitness (lower is better)")
    axis.grid(True, alpha=0.25)
    axis.legend(loc="upper right", fontsize=9)
    axis.set_ylim(bottom=0)

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    figure.savefig(path, dpi=180, bbox_inches="tight")
    plt.close(figure)
    return path
