"""Create a standalone xUnit project from an already archived generated.cs file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from generate import create_test_project, find_project_file


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    parser.add_argument("--strategy", choices=("basic", "feedback"), required=True)
    parser.add_argument("--repeat", type=int, choices=(1, 2, 3), required=True)
    args = parser.parse_args()
    output = ROOT / "data" / "raw" / "llm" / args.library / args.strategy / f"repeat_{args.repeat}"
    source = output / "generated.cs"
    repo = ROOT / "data" / "raw" / "repos" / args.library
    if not source.exists():
        raise SystemExit(f"Missing generated source: {source}")
    class_file = next(repo.rglob("*.cs"), None)
    if class_file is None:
        raise SystemExit(f"No C# source files found in {repo}")
    project = create_test_project(output / "generated-tests", find_project_file(repo, class_file))
    (output / "metadata.json").write_text(json.dumps({"generated_project": str(project.relative_to(ROOT))}, indent=2), encoding="utf-8")
    print(project)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
