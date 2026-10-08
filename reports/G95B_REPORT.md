# G95B — Experiment Registry

Date: 2026-08-27
Milestone: M92
Status: **PASS**

## Result

ExperimentDefinition records pin the WorldPackage/scenario versions, seeds,
parameter variants, provider matrix, population policy, interventions,
horizon, metrics, validation profile, owner, and rights refs. Definitions are
versioned and cannot be overwritten. ExperimentRun records carry a run lease,
definition version, status, worker, revision, worldline ref, and RunArtifact
ref.

ExperimentRegistry is an in-memory metadata boundary with atomic locking.
Duplicate definition/run writes are rejected; only one concurrent worker can
claim a queued run; completion is worker-owned; and in-flight work can be
recovered to the queue without losing revision history. Registry snapshots
round-trip through the explicit v1 schema and validate run-to-definition refs.

## Evidence

- Unit: tests/unit/substrate/test_g95b_experiment_registry.py — 5 passed,
  including concurrent claim safety, append-only definition versions,
  optimistic revision rejection, and in-flight recovery.
- Integration: tests/integration/test_g95b_experiment_registry_product_chain.py
  — 1 passed with a private rights-approved source through
  OneClickAuthoring → WorldPackage → Preview → PlayableService → SQLite
  WorldRuntime; the completed run references real event/snapshot/branch
  evidence through a verified RunArtifact.
- Full quality: 1395 passed, 1 skipped, 2 warnings; Ruff, format, Pyright,
  architecture, SDK compatibility, and minimality checks pass. The PostgreSQL
  skip remains the documented EXTERNAL_BLOCKED profile.

## Boundary

The registry owns experiment metadata only. It is not a second canonical
state, event store, branch system, source registry, or commit path. G95C-G97J
remain pending; v5.5 remains IN_PROGRESS / NOT_ACCEPTED.
