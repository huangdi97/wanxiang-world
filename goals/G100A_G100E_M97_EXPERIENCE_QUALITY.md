# G100A–G100E — M97 Experience Quality Benchmark

## Principle
`Worldness != Experience Quality != Scientific Validity`.
Do not collapse them into one release score.

## G100A — Versioned ExperienceQuality schema
Implement/reuse a versioned artifact containing at least:
Agency, Coherence, CharacterConsistency, ConsequenceVisibility, NarrativeStateAlignment, GoalClarity, WorldReactivity, MemoryQuality, ContinuationQuality, NoveltyRepetition.
Each dimension must record source/method: invariant metric, behavioral trace, human rating, or optional model-judge. Model-judge cannot be the sole authority for Stable acceptance.
Commit: `g100a: define versioned experience quality benchmark`

## G100B — Benchmark scenarios
Freeze at least two benchmark families:
1. one source-driven playable world;
2. the M96 original prompt world.
Include action scripts for reproducibility plus slots for human sessions; scripts are not substitutes for humans.
Commit: `g100b: freeze v5.5 experience benchmark scenarios`

## G100C — Collector and report generator
Collect event/state/replay refs and benchmark dimensions without duplicating canonical state. Produce machine-readable per-run and aggregate reports, including missing-data handling.
Commit: `g100c: implement experience benchmark collection`

## G100D — Execute baseline
Run repeatable benchmark sessions on both world families. Use M95 genuine human data when available; otherwise record human fields as missing/USER_INPUT_REQUIRED, not inferred.
Establish v5.5 baseline distributions; do not invent a universal quality threshold.
Commit: `g100d: execute v5.5 experience quality baseline`

## G100E — M97 qualification
Write:
- `reports/M97_EXPERIENCE_QUALITY_BENCHMARK.md`
- `artifacts/v55_stable/m97/experience_quality_baseline.json`

Gates 70–72 ACCEPTED if schema, reproducibility, two-world baseline, missing-data semantics and metric separation are all real. This is a release baseline, not scientific validity.
Commit: `g100e: qualify m97 experience quality benchmark`
