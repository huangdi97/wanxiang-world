# G92D — Snapshot / Compaction Policy

Date: 2026-08-26  
Status: PASS

## Delivered contract

`CompactionPolicy` defines snapshot cadence, recent-event retention,
memory-summary window, and archive threshold. `CompactionService` creates a
reference-only `CompactionManifest` containing event archive refs, retained
event sequences, memory-summary refs, archive URI, snapshot metadata, and the
golden replay hash.

This is logical compaction: the existing Runtime SnapshotStore remains the
checkpoint baseline and the authoritative EventStore remains append-only. No
event payload is deleted, rewritten, or copied into a second event store.

## Evidence

- `tests/unit/substrate/test_g92d_compaction.py`: 2 passed, including replay
  mismatch rejection and deterministic summary boundaries.
- `tests/integration/test_g92d_compaction_runtime.py`: 1 passed; real SQLite
  Runtime replay hash is equal before/after and event sequence/count is
  unchanged.
- Combined focused result: 3 passed, 1 existing Hypothesis collection warning.
- Ruff check and format check: PASS.
- Pyright on changed implementation/tests: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.

G92D is PASS. Compaction Gate 26 remains pending until the complete M89
qualification records the long-run golden replay evidence. v5.5 remains
`IN_PROGRESS / NOT_ACCEPTED`; no model training, private source upload, or
v5.6 work was performed.
