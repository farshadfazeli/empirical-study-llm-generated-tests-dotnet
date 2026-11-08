# C# LLM-Generated Tests: A Limited Pilot

**Date:** 8 November 2026  
**Study status:** pilot only; no full-study claims

## Abstract

This pilot tests a reproducible pipeline for comparing LLM-generated and
human-written C# tests using code coverage and mutation testing. The pilot
uses one .NET library, one target source file, one human baseline, and local
Qwen generation. The human baseline produced 2.03% line coverage, 3.65% branch
coverage, and a 9.09% Stryker mutation score. Four Basic Qwen suites failed to
compile, so no valid LLM comparison is available. A template-based smoke test
passed and produced 1.01% line coverage, 0.40% branch coverage, and a 1.82%
mutation score, but it is excluded from the research comparison.

## 1. Question and scope

The motivating question is whether LLM-generated tests can show high
structural coverage while missing faults exposed by mutation testing. This is
an empirical check of an existing concern in C#/.NET, not a novelty claim. The
intended research questions concern coverage and mutation score, one feedback
round, and manual classification of surviving mutants. This document reports
only the limited pilot.

## 2. Method

The subject was `Ardalis.GuardClauses`, checked out at the pinned commit in
`libs.csv`. The target was `src/GuardClauses/GuardAgainstNullExtensions.cs`.
The human baseline used three xUnit tests in a separate .NET 8 test project.
The model was a locally served Qwen model configured through environment
variables at temperature 0.2. Prompts, raw responses, timestamps, and token
counts were retained under `data/raw/llm/`.

Generated projects were restored, compiled, and tested against the original
library. Restore failures, compiler failures, and test failures were retained
in `data/results/validation.csv`. Coverlet collected Cobertura line and branch
coverage. Stryker.NET 4.8.0 mutated the selected source file and retained its
JSON report.

## 3. Results

### 3.1 Validation

The ordinary Basic prompt was attempted four times: three requested
repetitions and one repaired-prompt output. All four restored but none
compiled. Thus the observed compile rate was `0/4` and pass rate was `0/4`.
Errors included Markdown fences, incomplete braces, missing xUnit imports,
invalid identifiers, and invalid assertions.

### 3.2 Human baseline

Coverlet reported 12 of 591 lines covered and 9 of 246 branches covered. The
aggregate rates were 2.03% and 3.65%. Stryker created 352 mutants. Five were
killed, three survived, 47 had no coverage, two caused mutant compile errors,
and 295 were ignored by Stryker filters. The reported mutation score was 9.09%.

### 3.3 Smoke test

One template-based suite with one passing test was measured separately. It
reached 6/591 lines and 1/246 branches, or 1.01% and 0.40%. Stryker reported
1.82% mutation score. This is an infrastructure check, not an LLM strategy
result, because the prompt supplied the complete test shape.

## 4. Interpretation

The pilot does not answer whether LLM tests have a coverage-versus-mutation
gap. The human baseline and smoke-test measurements demonstrate that Coverlet
and Stryker can run end to end, while the Basic Qwen failures demonstrate that
compile validity is a necessary outcome to report. It would be misleading to
compare the smoke-test score with the human score as if both represented the
specified generation strategy.

## 5. Threats to validity

The pilot has one library, one target file, one model, and very few tests.
Public libraries may have appeared in model training data. Mutation results
depend on Stryker.NET's available operators and filters. No manual survivor
classification was performed, and there is no second annotator. The local Qwen
model may not represent larger or hosted models. The low coverage values are
aggregate values for the library assembly and should not be generalized.

## 6. Conclusion

The reproducible pilot pipeline is implemented and its failures are visible in
the repository. The human baseline and measurement smoke test ran, but the
ordinary Qwen-generated suites did not compile. Therefore this pilot provides
no evidence for or against the proposed coverage-versus-mutation relationship.
Any larger study should begin only after a valid, genuinely model-generated
test suite can be produced and validated.
