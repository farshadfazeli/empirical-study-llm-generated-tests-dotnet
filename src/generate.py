"""Generate and archive one test suite using an OpenAI-compatible endpoint."""

from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source_files(repo: Path) -> list[Path]:
    return [p for p in repo.rglob("*.cs") if not any(part.lower() in {"bin", "obj", "test", "tests"} for part in p.parts)]


def extract_code(text: str) -> str:
    blocks = re.findall(r"```(?:csharp|cs|c#)?\s*(.*?)```", text, flags=re.S | re.I)
    return max(blocks, key=len).strip() if blocks else text.strip()


def call_model(prompt: str) -> dict:
    api_key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL")
    if not api_key or not model:
        raise RuntimeError("LLM_API_KEY and LLM_MODEL must be set in the environment")
    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {"model": model, "temperature": 0.2, "messages": [{"role": "user", "content": prompt}]}
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    parser.add_argument("--strategy", choices=("basic", "feedback"), required=True)
    parser.add_argument("--repeat", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--class-file", required=True)
    args = parser.parse_args()
    repo = ROOT / "data" / "raw" / "repos" / args.library
    class_path = Path(args.class_file)
    if not class_path.is_absolute():
        class_path = repo / class_path
    source = class_path.read_text(encoding="utf-8")
    prompt = f"Write xUnit tests for this C# class. Return only a complete test file.\n\n{source}"
    if args.strategy == "feedback":
        prompt += "\n\nAdd tests that target the surviving mutants supplied in the feedback file."
    response = call_model(prompt)
    content = response["choices"][0]["message"]["content"]
    stamp = datetime.now(timezone.utc).isoformat()
    out = ROOT / "data" / "raw" / "llm" / args.library / args.strategy / f"repeat_{args.repeat}"
    out.mkdir(parents=True, exist_ok=True)
    (out / "prompt.txt").write_text(prompt, encoding="utf-8")
    (out / "response.json").write_text(json.dumps(response, indent=2), encoding="utf-8")
    (out / "generated.cs").write_text(extract_code(content), encoding="utf-8")
    (out / "metadata.json").write_text(json.dumps({"model": os.environ["LLM_MODEL"], "temperature": 0.2, "timestamp_utc": stamp}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
