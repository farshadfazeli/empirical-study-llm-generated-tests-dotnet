"""Verify selected repositories and record reproducibility metadata."""

from __future__ import annotations

import csv
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOS = ROOT / "data" / "raw" / "repos"
LIBS = ROOT / "libs.csv"


def run(*args: str, cwd: Path | None = None) -> tuple[int, str]:
    completed = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    return completed.returncode, (completed.stdout + completed.stderr).strip()


def count_loc(path: Path) -> int:
    total = 0
    for source in path.rglob("*.cs"):
        if any(part.lower() in {"bin", "obj", "test", "tests"} for part in source.parts):
            continue
        total += sum(1 for line in source.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip())
    return total


def main() -> None:
    rows = list(csv.DictReader(LIBS.open(encoding="utf-8", newline="")))
    for row in rows:
        repo = REPOS / row["name"]
        if not (repo / ".git").exists():
            row["verification_status"] = "excluded: repository not cloned"
            continue
        code, commit = run("git", "-c", "safe.directory=*", "-C", str(repo), "rev-parse", "HEAD")
        if code:
            row["verification_status"] = "excluded: commit lookup failed"
            continue
        row["commit"] = commit.splitlines()[-1]
        row["size_loc"] = str(count_loc(repo))
        row["verification_status"] = "cloned; build/test verification pending"
    with LIBS.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
