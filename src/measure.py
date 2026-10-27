"""Run Coverlet and Stryker.NET without hiding failures or timeouts."""

from __future__ import annotations

import argparse
import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "results" / "measurements.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    parser.add_argument("--suite", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--files", nargs="+", required=True)
    args = parser.parse_args()
    report_dir = ROOT / "data" / "raw" / "reports" / args.library / args.suite
    report_dir.mkdir(parents=True, exist_ok=True)
    coverage = subprocess.run(["dotnet", "test", args.project, "--collect:XPlat Code Coverage", "--results-directory", str(report_dir)], text=True, capture_output=True)
    (report_dir / "coverlet.stdout.txt").write_text(coverage.stdout, encoding="utf-8")
    (report_dir / "coverlet.stderr.txt").write_text(coverage.stderr, encoding="utf-8")
    stryker = subprocess.run(["dotnet", "stryker", "--project", args.project, "--mutate", ",".join(args.files), "--reporter", "json", "--output", str(report_dir)], text=True, capture_output=True)
    (report_dir / "stryker.stdout.txt").write_text(stryker.stdout, encoding="utf-8")
    (report_dir / "stryker.stderr.txt").write_text(stryker.stderr, encoding="utf-8")
    row = {"library": args.library, "suite": args.suite, "coverage_exit_code": coverage.returncode, "stryker_exit_code": stryker.returncode, "status": "ok" if coverage.returncode == 0 and stryker.returncode == 0 else "failed", "timestamp_utc": datetime.now(timezone.utc).isoformat()}
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    fields = list(row)
    exists = RESULTS.exists()
    with RESULTS.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if not exists:
            writer.writeheader()
        writer.writerow(row)


if __name__ == "__main__":
    main()
