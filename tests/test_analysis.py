from pathlib import Path

from analysis.plotting import selection_probabilities
from analysis.run_analysis import run_analysis


def test_selection_probabilities_sum_to_one_and_favor_lower_fitness():
    probabilities = selection_probabilities([1.0, 2.0, 4.0])

    assert abs(sum(probabilities) - 1.0) < 1e-12
    assert probabilities[0] > probabilities[1] > probabilities[2]


def test_analysis_generates_artifacts(tmp_path: Path):
    result = run_analysis(tmp_path, seed=42)
    output_dir = result["output_dir"]

    assert result["baseline"]["best_fitness"] < 1.0
    assert len(result["experiments"]) == 6
    for filename in (
        "convergence.png",
        "selection_wheel.png",
        "parameter_comparison.png",
        "analysis.md",
    ):
        artifact = output_dir / filename
        assert artifact.exists()
        assert artifact.stat().st_size > 0
