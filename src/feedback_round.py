"""Create the second prompt from surviving mutants and archive the response."""

from __future__ import annotations

import argparse
import json
import os
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    parser.add_argument("--class-file", required=True)
    parser.add_argument("--repeat", type=int, choices=(1, 2, 3), required=True)
    args = parser.parse_args()
    key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL")
    if not key or not model:
        raise RuntimeError("LLM_API_KEY and LLM_MODEL must be set in the environment")
    source = (ROOT / "data" / "raw" / "repos" / args.library / args.class_file).read_text(encoding="utf-8")
    survivors = list((ROOT / "data" / "raw" / "reports" / args.library).glob("**/*surviv*.json"))
    feedback = "\n\n".join(path.read_text(encoding="utf-8", errors="ignore") for path in survivors)
    prompt = f"Write additional xUnit tests for this C# class. Target these surviving mutants from round one. Return only a complete test file.\n\nCLASS:\n{source}\n\nSURVIVING MUTANTS:\n{feedback}"
    payload = {"model": model, "temperature": 0.2, "messages": [{"role": "user", "content": prompt}]}
    request = urllib.request.Request(os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/") + "/chat/completions", data=json.dumps(payload).encode(), headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(request, timeout=180) as response:
        result = json.loads(response.read())
    out = ROOT / "data" / "raw" / "llm" / args.library / "feedback" / f"repeat_{args.repeat}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompt.txt").write_text(prompt, encoding="utf-8")
    (out / "response.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    (out / "metadata.json").write_text(json.dumps({"model": model, "temperature": 0.2, "timestamp_utc": datetime.now(timezone.utc).isoformat()}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
