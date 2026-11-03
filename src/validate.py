"""Build generated test projects and record compile/test outcomes."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "data" / "results" / "validation.csv"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    parser.add_argument("--no-restore", action="store_true")
    parser.add_argument("--source", default="https://api.nuget.org/v3/index.json")
    parser.add_argument("--suite", default=None)
    args = parser.parse_args()
    rows = []
    root = ROOT / "data" / "raw" / "llm" / args.library
    projects = root.glob("**/generated-tests/*.csproj")
    if args.suite:
        projects = [project for project in projects if project.parent.parent.name == args.suite]
    for project in projects:
        restore = subprocess.run(["dotnet", "restore", str(project), "--source", args.source, "--ignore-failed-sources", "--nologo"], text=True, capture_output=True)
        command = ["dotnet", "test", str(project), "--nologo", "--verbosity", "minimal"]
        command.insert(2, "--no-restore")
        completed = subprocess.run(command, text=True, capture_output=True)
        output = restore.stdout + restore.stderr + completed.stdout + completed.stderr
        has_compile_error = bool(re.search(r"\berror (?:CS|MSB|NETSDK)\d*", output))
        compile_ok = restore.returncode == 0 and not has_compile_error and ("Test run for" in output or completed.returncode == 0)
        tests_pass = compile_ok and completed.returncode == 0
        rows.append({"library": args.library, "suite": str(project.parent), "restore_ok": str(restore.returncode == 0), "compile_ok": str(compile_ok), "original_tests_pass": str(tests_pass), "removed_tests": "0", "exit_code": completed.returncode, "timestamp_utc": datetime.now(timezone.utc).isoformat(), "output_tail": output[-2000:]})
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    fields = ["library", "suite", "restore_ok", "compile_ok", "original_tests_pass", "removed_tests", "exit_code", "timestamp_utc", "output_tail"]
    with RESULTS.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        if handle.tell() == 0:
            writer.writeheader()
        writer.writerows(rows)
    summary = RESULTS.with_name("validation_summary.csv")
    summary_row = {"library": args.library, "suites": len(rows), "compile_rate": sum(row["compile_ok"] == "True" for row in rows) / len(rows) if rows else 0.0, "pass_rate": sum(row["original_tests_pass"] == "True" for row in rows) / len(rows) if rows else 0.0, "timestamp_utc": datetime.now(timezone.utc).isoformat()}
    with summary.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary_row))
        if handle.tell() == 0:
            writer.writeheader()
        writer.writerow(summary_row)


if __name__ == "__main__":
    main()
