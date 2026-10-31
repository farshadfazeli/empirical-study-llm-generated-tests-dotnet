"""Run and summarize Coverlet line/branch coverage without hiding failures."""

from __future__ import annotations

import argparse
import csv
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "results" / "coverage.csv"
RUNSETTINGS = ROOT / "data" / "raw" / "pilot" / "coverlet.runsettings"


def find_report(results_dir: Path) -> Path | None:
    reports = sorted(results_dir.rglob("coverage.cobertura.xml"))
    return reports[-1] if reports else None


def parse_report(report: Path) -> dict[str, str]:
    root = ET.parse(report).getroot()
    names = ("line-rate", "branch-rate", "lines-covered", "lines-valid",
             "branches-covered", "branches-valid")
    return {name.replace("-", "_"): root.attrib.get(name, "") for name in names}


def append_row(row: dict[str, str]) -> None:
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    fields = ["library", "suite", "line_coverage", "branch_coverage",
              "lines_covered", "lines_valid", "branches_covered",
              "branches_valid", "status", "report_path", "exit_code",
              "timestamp_utc"]
    with RESULTS.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if handle.tell() == 0:
            writer.writeheader()
        writer.writerow({field: row.get(field, "") for field in fields})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    parser.add_argument("--suite", required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--runsettings", default=str(RUNSETTINGS))
    args = parser.parse_args()

    report_dir = ROOT / "data" / "raw" / "reports" / args.library / args.suite
    report_dir.mkdir(parents=True, exist_ok=True)
    command = ["dotnet", "test", args.project, "--no-restore",
               "--collect:XPlat Code Coverage", "--settings", args.runsettings,
               "--results-directory", str(report_dir)]
    completed = subprocess.run(command, text=True, capture_output=True)
    (report_dir / "coverlet.stdout.txt").write_text(completed.stdout, encoding="utf-8")
    (report_dir / "coverlet.stderr.txt").write_text(completed.stderr, encoding="utf-8")
    report = find_report(report_dir)
    metrics = parse_report(report) if report else {}
    append_row({
        "library": args.library,
        "suite": args.suite,
        "line_coverage": metrics.get("line_rate", ""),
        "branch_coverage": metrics.get("branch_rate", ""),
        "lines_covered": metrics.get("lines_covered", ""),
        "lines_valid": metrics.get("lines_valid", ""),
        "branches_covered": metrics.get("branches_covered", ""),
        "branches_valid": metrics.get("branches_valid", ""),
        "status": "ok" if completed.returncode == 0 and report else "failed",
        "report_path": str(report.relative_to(ROOT)) if report else "",
        "exit_code": str(completed.returncode),
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    })
    print(f"status={'ok' if completed.returncode == 0 and report else 'failed'}")
    print(f"report={report if report else 'none'}")
    if metrics:
        print(f"line_coverage={metrics['line_rate']}")
        print(f"branch_coverage={metrics['branch_rate']}")
    raise SystemExit(completed.returncode)


if __name__ == "__main__":
    main()
