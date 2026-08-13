# Goal G07E Acceptance Report
## Status
PASS
## Objective
Experiment runtime with multi-run, metrics and ValidityEnvelope.
## Delivered
- `wanxiang_substrate.reality.experiment`: ExperimentSpec, ExperimentRuntime
  (budgeted deterministic runs), RunMetric, Finding, ValidityEnvelope.
## Test evidence
- multi-seed matrix deterministic; distribution aggregated; finding requires
  assumptions + envelope; baseline never mutated.
## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Run/seed/version metrics | PASS | RunMetric provenance |
| Assumptions + ValidityEnvelope | PASS | finding test |
| Same spec reproduces same results | PASS | determinism test |
| Baseline never mutated | PASS | hash-stable test |
## Final checkpoint
- commit: `goal g07e: experiment runtime, multi-run & validity envelope`