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


def compact_context(source: str) -> str:
    """Keep declarations and public method signatures for small local models."""
    lines = source.splitlines()
    selected: list[str] = []
    in_signature = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("using ", "namespace ", "public static partial class ")):
            selected.append(line)
        if stripped.startswith("public static"):
            in_signature = True
        if in_signature:
            if line not in selected:
                selected.append(line)
            if "{" in line:
                in_signature = False
                selected[-1] = line.split("{", 1)[0].rstrip()
    selected.append("\nUsage example: Guard.Against.Null(value, nameof(value));")
    return "\n".join(selected)


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
    <PackageReference Include=\"coverlet.collector\" Version=\"6.0.2\" />
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
    payload = {"model": model, "temperature": 0.2, "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", "700")), "messages": [{"role": "system", "content": "You are a precise C# unit-test generator. You must follow the requested output format exactly."}, {"role": "user", "content": prompt}]}
    request = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=int(os.environ.get("LLM_TIMEOUT_SECONDS", "300"))) as response:
        return json.loads(response.read())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--library", required=True)
    parser.add_argument("--strategy", choices=("basic", "feedback"), required=True)
    parser.add_argument("--repeat", type=int, choices=(1, 2, 3), required=True)
    parser.add_argument("--class-file", required=True)
    parser.add_argument("--output-name", default=None)
    parser.add_argument("--compact-context", action="store_true")
    parser.add_argument("--minimal-template", action="store_true")
    parser.add_argument("--skeleton-template", action="store_true")
    args = parser.parse_args()
    repo = ROOT / "data" / "raw" / "repos" / args.library
    class_path = Path(args.class_file)
    if not class_path.is_absolute():
        class_path = repo / class_path
    source = class_path.read_text(encoding="utf-8")
    prompt_source = compact_context(source) if args.compact_context else source
    if args.minimal_template:
        prompt = """Return only this complete, compilable C# file. Do not add explanations or Markdown fences.
Use exactly one xUnit test and preserve every brace and using directive.

using System;
using Ardalis.GuardClauses;
using Xunit;

namespace GeneratedTests
{
    public class NullTests
    {
        [Fact]
        public void Null_returns_the_original_value_when_input_is_not_null()
        {
            var value = "value";
            var result = Guard.Against.Null(value, nameof(value));
            Assert.Same(value, result);
        }
    }
}"""
    elif args.skeleton_template:
        prompt = """Return only one complete, compilable C# xUnit test file. Do not use Markdown or explanations.
Keep the following structure and using directives exactly. Replace the comment with one test body for the non-null behavior of Guard.Against.Null. Do not add production code.

using System;
using Ardalis.GuardClauses;
using Xunit;

namespace GeneratedTests
{
    public class NullTests
    {
        [Fact]
        public void Null_returns_the_original_value_when_input_is_not_null()
        {
            // replace this comment with the test body
        }
    }
}"""
    else:
        prompt = f"""You are writing unit tests, not production code.
Write a complete, compilable C# xUnit test file for the class below.
Return ONLY raw C# source code. Do not use Markdown fences, explanations, XML documentation, or production-code implementations.
Return exactly three short [Fact] tests. The first line must be `using System;`, followed by `using Ardalis.GuardClauses;` and `using Xunit;`.
The output must contain a file-scoped test namespace, a public test class, and xUnit [Fact] methods. End with all closing braces.
Test the public behavior of the supplied class. Do not reproduce or rewrite the supplied production class.
For this target, call the API as `Guard.Against.Null(value, parameterName)`; do not instantiate `GuardClauseExtensions`, which is a static class.
Use only APIs visible in the supplied source and ordinary xUnit assertions.
Use this exact brace structure; every namespace, class, and method must have opening and closing braces:
namespace GeneratedTests
{{
    public class NullTests
    {{
        [Fact]
        public void Example()
        {{
            // test body
        }}
    }}
}}

SOURCE CLASS OR API CONTEXT:
{prompt_source}"""
    if args.strategy == "feedback":
        prompt += "\n\nAdd tests that target the surviving mutants supplied in the feedback file."
    started = time.perf_counter()
    response = call_model(prompt)
    elapsed_seconds = round(time.perf_counter() - started, 3)
    content = response["choices"][0]["message"]["content"]
    stamp = datetime.now(timezone.utc).isoformat()
    output_name = args.output_name or f"repeat_{args.repeat}"
    out = ROOT / "data" / "raw" / "llm" / args.library / args.strategy / output_name
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
    context_mode = "minimal_template" if args.minimal_template else ("skeleton_template" if args.skeleton_template else ("compact" if args.compact_context else "full"))
    (out / "metadata.json").write_text(json.dumps({"model": os.environ["LLM_MODEL"], "temperature": 0.2, "max_tokens": int(os.environ.get("LLM_MAX_TOKENS", "700")), "context_mode": context_mode, "timestamp_utc": stamp, "generation_seconds": elapsed_seconds, "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens"), "total_tokens": usage.get("total_tokens"), "class_file": str(class_path.relative_to(repo)), "library_project": str(library_project.relative_to(repo)), "generated_project": str(project_file.relative_to(ROOT))}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
