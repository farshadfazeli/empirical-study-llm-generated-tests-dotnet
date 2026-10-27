"""Create summary tables and the coverage/mutation scatter plot."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "results"
OUT = ROOT / "analysis"


def main() -> None:
    OUT.mkdir(exist_ok=True)
    frames = [pd.read_csv(path) for path in RESULTS.glob("*.csv")]
    if not frames:
        raise SystemExit("No result CSVs exist yet; run validation and measurement first.")
    data = pd.concat(frames, ignore_index=True, sort=False)
    data.to_csv(OUT / "all_results.csv", index=False)
    numeric = data.select_dtypes(include="number")
    if not numeric.empty:
        numeric.agg(["mean", "std"]).to_csv(OUT / "summary_mean_sd.csv")
    if {"coverage", "mutation_score"}.issubset(data.columns):
        data.plot.scatter(x="coverage", y="mutation_score")
        plt.tight_layout()
        plt.savefig(OUT / "coverage_vs_mutation.png", dpi=160)


if __name__ == "__main__":
    main()
