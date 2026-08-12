# ADR-0019: Belief, Memory & Temporal Epistemic Graph Design (G03B)

- Status: accepted
- Date: 2026-08-13

## Context

G03B needs actor-local belief and memory evolution with corrections, conflicts
and forgetting, separated from canonical truth.

## Decision

1. Beliefs and memories are versioned entity components; a correction marks the
   old belief corrected and links to the new one (no silent overwrite).
2. Contradictory beliefs are retained; the active belief is the latest by
   time/confidence.
3. Memory access is actor-scoped with explicit grants; compaction archives
   low-salience memories while preserving audit lineage.
4. Belief adoption creates epistemic entities only ? never canonical facts.

## Consequences

- Deterministic, replayable epistemic graphs; beliefs never become truth.
