# Experiment Runtime / Multi-run / ValidityEnvelope (G07E)
Ownership: `wanxiang_substrate.reality.experiment`.

## Spec & runs
`ExperimentSpec` (versioned) defines baseline ref, parameter variants and seed
sets. `ExperimentRuntime.run` executes the matrix deterministically within a
resource budget; metrics carry run/seed/rule provenance.

## Findings
`Finding` includes assumptions, supported/unsupported conclusion and a
`ValidityEnvelope` (seeds + rule versions + determinism note). Distributions
are aggregated, not only point outputs. Experiment branches never mutate the
baseline.