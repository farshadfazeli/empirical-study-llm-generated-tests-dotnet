"""Sample surviving mutants reproducibly for manual classification."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    frames = []
    for path in (ROOT / "data" / "raw" / "reports").glob("**/*surviv*.csv"):
        frames.append(pd.read_csv(path))
    if not frames:
        raise SystemExit("No surviving-mutant CSVs exist yet.")
    data = pd.concat(frames, ignore_index=True)
    for column in ("mutator_type", "file", "line"):
        if column not in data:
            data[column] = ""
    sample_size = min(60, len(data))
    sample = data.sample(sample_size, random_state=20261027)
    sample["my_category"] = ""
    sample[["mutator_type", "file", "line", "my_category"]].to_csv(ROOT / "data" / "results" / "survivors_sample.csv", index=False)


if __name__ == "__main__":
    main()
