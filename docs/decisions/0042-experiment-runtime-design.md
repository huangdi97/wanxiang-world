# ADR-0042: Experiment Runtime Design (G07E)
- Status: accepted
- Date: 2026-08-13

## Context
G07E needs multi-seed experiments from an immutable baseline with metrics,
assumptions and validity envelopes.

## Decision
1. ExperimentSpec defines baseline/variants/seeds; runs execute deterministically
   within budgets; metrics carry run/seed/rule provenance.
2. Findings include assumptions and a ValidityEnvelope; distributions aggregate
   across seeds.

## Consequences
- Same spec reproduces identical results; baselines are never mutated.