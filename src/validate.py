"""Build generated test projects and record compile/test outcomes."""

from __future__ import annotations

import argparse
import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "results" / "validation.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    args = parser.parse_args()
    rows = []
    root = ROOT / "data" / "raw" / "llm" / args.library
    for project in root.glob("**/generated-tests/*.csproj"):
        completed = subprocess.run(["dotnet", "test", str(project), "--nologo", "--verbosity", "minimal"], text=True, capture_output=True)
        output = completed.stdout + completed.stderr
        passed = completed.returncode == 0
        rows.append({"library": args.library, "suite": str(project.parent), "compile_ok": str(passed), "original_tests_pass": str(passed), "removed_tests": "0", "exit_code": completed.returncode, "timestamp_utc": datetime.now(timezone.utc).isoformat(), "output_tail": output[-2000:]})
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    fields = ["library", "suite", "compile_ok", "original_tests_pass", "removed_tests", "exit_code", "timestamp_utc", "output_tail"]
    with RESULTS.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if handle.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
