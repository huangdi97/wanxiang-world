# Belief, Memory & Temporal Epistemic Graph (G03B)

Ownership: `wanxiang_substrate.epistemic` (actor-local belief/memory; never
canonical truth).

## Model

- `MemoryRecord`: actor-local memory (observation/interpretation/belief) with
  content ref, time, salience, source observation, forgotten flag.
- `BeliefAssertion`: proposition + confidence + source + status
  (active/corrected/superseded/forgotten) with `supersedes`/`corrected_by`
  lineage links.
- Contradictory beliefs are retained; a correction marks the old belief
  corrected and links to the new one (no silent overwrite).

## Authority

- `epistemic.record_observation` / `adopt_belief` / `correct_belief` /
  `forget` / `compact_memory` / `grant_memory_access` / `instantiate` are
  resolvers through the M1 Commit Authority.
- Belief adoption never creates canonical facts (epistemic entities only).

## Retrieval & privacy

- `EpistemicQuery.beliefs/history/active_belief/contradictions/memories`.
- Memory access is actor-scoped: a requester must be the owner or hold a
  memory-access grant (`MemoryAccessDenied` otherwise).
- Compaction archives low-salience memories (bounded) while preserving audit
  lineage (forgotten records remain retrievable with `include_forgotten`).

## Compatibility

- Epistemic state rides on versioned components (`epistemic` schema v1); no new
  migration; replay deterministic.
