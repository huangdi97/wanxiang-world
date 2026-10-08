# G95D — Batch Worldlines

Date: 2026-08-27
Milestone: M92
Status: **PASS**

## Result

`BatchWorldlineExecutor` builds a deterministic queue from one version-pinned
`ExperimentDefinition` in the existing `ExperimentRegistry`. Each seed and
parameter variant becomes one registry run; workers claim and finish those
runs through the registry lease/revision path. The configured
`max_parallelism` is an upper bound, and a versioned `BatchCheckpoint` records
queued/running/completed/failed cursors and sanitized result refs after each
terminal worker result. Aggregation covers every result row and reports
count/mean/min/max per metric.

Resume reuses terminal registry runs, requires explicit recovery of in-flight
runs, and does not recreate completed work. Batch records contain refs and
metrics only; the executor owns no canonical state or event history.

## Evidence

- Unit: `tests/unit/substrate/test_g95d_batch_worldlines.py` — 2 passed,
  proving a 3-seed × 2-parameter queue, worker peak ≤2 under a requested
  parallelism of 4, checkpoint round-trip, completed-run resume, and in-flight
  recovery.
- Integration: `tests/integration/test_g95d_batch_worldlines_product_chain.py`
  — 1 passed. The same private rights-approved source and WorldPackage ran
  four seed/parameter worldlines through OneClickAuthoring → PlayableService →
  SQLite WorldRuntime, with per-run snapshot, RunArtifact, commit/replay, and
  sanitized aggregate evidence.
- Full quality: 1401 passed, 1 skipped, 2 warnings; Ruff, format, Pyright,
  architecture, SDK compatibility, duplicate-abstraction, and minimality
  checks pass. The PostgreSQL skip remains the documented EXTERNAL_BLOCKED
  profile.

## Boundary

The real SQLite product-chain qualification is intentionally serial because
parallel Alembic/SQLite initialization is an environment hazard; the unit
test is the bounded-parallelism evidence. Therefore Gate 41 (four or more
parallel worldlines) remains pending for a later qualification. G95E-G97J and
the remaining M92-M94 gates remain pending, so v5.5 remains NOT_ACCEPTED.
