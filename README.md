# C# LLM Test Generation: A Small Pilot

This repository contains a deliberately limited pilot investigating whether
LLM-generated tests for C# code can achieve structural coverage without
detecting mutated faults. It is an empirical check, not a novelty claim and
not a completed eight-library study.

## What was actually run

- One library: `Ardalis.GuardClauses`, pinned in `libs.csv`.
- One target file: `GuardAgainstNullExtensions.cs`.
- One human-written xUnit baseline with three tests.
- Local Qwen generation at temperature `0.2`, with prompts and raw outputs retained.
- Coverlet line/branch coverage and Stryker.NET `4.8.0` mutation testing.
- One valid template-based suite used only as a measurement smoke test.

The full Basic strategy outputs did not compile. They are retained and counted
as failures; they are not silently converted into results.

## Recorded pilot observations

| Run | Compile | Pass | Line coverage | Branch coverage | Mutation score |
| --- | ---: | ---: | ---: | ---: | ---: |
| Human baseline | yes | yes | 2.03% | 3.65% | 9.09% |
| Basic Qwen suites (4) | 0/4 | 0/4 | not measured | not measured | not measured |
| Minimal-template smoke test | yes | yes | 1.01% | 0.40% | 1.82% |

The smoke-test row is infrastructure evidence only: the prompt supplied the
complete test shape, so it is excluded from the LLM-vs-human comparison.

## Research questions and current status

- RQ1: not answerable from this pilot because the Basic Qwen suites did not compile.
- RQ2: not run; no valid Basic suite exists to provide surviving mutants.
- RQ3: not run; the pilot does not contain the required survivor sample.

## Reproduce the limited pilot

```powershell
dotnet tool restore
python src/generate.py --library Ardalis.GuardClauses --strategy basic --repeat 1 --output-name minimal_template_1 --minimal-template --class-file src/GuardClauses/GuardAgainstNullExtensions.cs
python src/validate.py --library Ardalis.GuardClauses --suite minimal_template_1 --source https://api.nuget.org/v3/index.json
python src/coverage.py --library Ardalis.GuardClauses --suite minimal_template_1_smoke --project data/raw/llm/Ardalis.GuardClauses/basic/minimal_template_1/generated-tests/GeneratedTests.csproj --runsettings data/raw/pilot/coverlet.runsettings
```

The Stryker command and raw reports are stored under
`data/raw/reports/Ardalis.GuardClauses/minimal_template_1_smoke/`.

Model configuration is environment-only: `LLM_MODEL`, `LLM_BASE_URL`, and
`LLM_API_KEY`. No API key is stored in the repository.

## Limitations

This pilot uses one model, one small library, one target file, and a very small
test sample. Public code may be present in training data. Mutation results are
limited to Stryker.NET operators, and no manual survivor classification was
performed. The template smoke test must not be interpreted as evidence for the
research question.

## Repository map

- `src/`: generation, validation, coverage, mutation, and analysis scripts
- `data/raw/`: prompts, model outputs, and tool reports
- `data/results/`: recorded CSV results
- `report/`: Markdown report and PDF report
- `libs.csv`: candidate-library screening record

## License

MIT. See `LICENSE`.
