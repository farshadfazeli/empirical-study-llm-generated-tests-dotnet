"""Generate and archive one test suite using an OpenAI-compatible endpoint."""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def source_files(repo: Path) -> list[Path]:
    return [p for p in repo.rglob("*.cs") if not any(part.lower() in {"bin", "obj", "test", "tests"} for part in p.parts)]


def extract_code(text: str) -> str:
    blocks = re.findall(r"```(?:csharp|cs|c#)?\s*(.*?)```", text, flags=re.S | re.I)
    if blocks:
        return max(blocks, key=len).strip()
    cleaned = re.sub(r"^\s*```(?:csharp|cs|c#)?\s*", "", text, count=1, flags=re.I)
    return re.sub(r"\s*```\s*$", "", cleaned, count=1).strip()


def find_project_file(repo: Path, class_path: Path) -> Path:
    candidates = sorted(class_path.parent.glob("*.csproj"))
    if candidates:
        return candidates[0]
    candidates = sorted(repo.rglob("*.csproj"))
    production = [path for path in candidates if "test" not in str(path).lower()]
    if len(production) == 1:
        return production[0]
    raise RuntimeError(f"Could not identify the production project for {class_path}")


def create_test_project(output_dir: Path, library_project: Path) -> Path:
    project_file = output_dir / "GeneratedTests.csproj"
    reference = os.path.relpath(library_project, output_dir).replace("/", "\\")
    project_file.write_text(
        """<Project Sdk=\"Microsoft.NET.Sdk\">
  <PropertyGroup>
    <TargetFramework>net8.0</TargetFramework>
    <IsPackable>false</IsPackable>
    <IsTestProject>true</IsTestProject>
    <Nullable>enable</Nullable>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include=\"Microsoft.NET.Test.Sdk\" Version=\"17.12.0\" />
    <PackageReference Include=\"xunit\" Version=\"2.9.3\" />
    <PackageReference Include=\"xunit.runner.visualstudio\" Version=\"3.1.5\" />
  </ItemGroup>
  <ItemGroup>
    <ProjectReference Include=\"%s\" />
  </ItemGroup>
</Project>
""" % reference,
        encoding="utf-8",
    )
    return project_file


def call_model(prompt: str) -> dict:
    api_key = os.environ.get("LLM_API_KEY")
    model = os.environ.get("LLM_MODEL")
    if not api_key or not model:
        raise RuntimeError("LLM_API_KEY and LLM_MODEL must be set in the environment")
    base_url = os.environ.get("LLM_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {"model": model, "temperature": 0.2, "max_tokens": 700, "messages": [{"role": "user", "content": prompt}]}
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
    started = time.perf_counter()
    response = call_model(prompt)
    elapsed_seconds = round(time.perf_counter() - started, 3)
    content = response["choices"][0]["message"]["content"]
    stamp = datetime.now(timezone.utc).isoformat()
    out = ROOT / "data" / "raw" / "llm" / args.library / args.strategy / f"repeat_{args.repeat}"
    out.mkdir(parents=True, exist_ok=True)
    library_project = find_project_file(repo, class_path)
    generated_project_dir = out / "generated-tests"
    generated_project_dir.mkdir(parents=True, exist_ok=True)
    (out / "prompt.txt").write_text(prompt, encoding="utf-8")
    (out / "response.json").write_text(json.dumps(response, indent=2), encoding="utf-8")
    generated_source = extract_code(content)
    (out / "generated.cs").write_text(generated_source, encoding="utf-8")
    (generated_project_dir / "GeneratedTests.cs").write_text(generated_source, encoding="utf-8")
    project_file = create_test_project(generated_project_dir, library_project)
    usage = response.get("usage", {})
    (out / "metadata.json").write_text(json.dumps({"model": os.environ["LLM_MODEL"], "temperature": 0.2, "max_tokens": 700, "timestamp_utc": stamp, "generation_seconds": elapsed_seconds, "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens"), "total_tokens": usage.get("total_tokens"), "class_file": str(class_path.relative_to(repo)), "library_project": str(library_project.relative_to(repo)), "generated_project": str(project_file.relative_to(ROOT))}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
