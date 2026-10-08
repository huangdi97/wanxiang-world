# G92G — 24h / 7d Long Run

Date: 2026-08-26  
Status: PASS

## Real accelerated qualification

`tests/integration/test_g92g_long_run_runtime.py` creates the existing
SQLite-backed town fixture and runs the existing `AutonomousScheduler` through
one synthetic day (24h reference) and seven synthetic days with multiple
actors. Each day creates a Runtime checkpoint. This is deterministic world
time acceleration, not a claim that seven wall-clock days elapsed.

The qualification records target/observed ticks, actor count, event count,
checkpoint count, serialized-state storage bytes, replay hash, and restart
recovery hash. It then builds a reference-only compaction manifest and checks
golden replay equality.

## Evidence

- `tests/unit/substrate/test_g92g_qualification.py`: 2 passed.
- `tests/integration/test_g92g_long_run_runtime.py`: 1 passed on the real
  SQLite WorldRuntime, existing Commit Authority, EventStore, SnapshotStore,
  ReplayEngine, and AutonomousScheduler.
- Combined focused result: 3 passed, 1 existing Hypothesis collection warning.
- Replay/recovery/storage and reference compaction checks: PASS.
- Ruff check and format check: PASS.
- Pyright on changed implementation/tests: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.

G92G is PASS. Gate 21 (24h smoke) and Gate 22 (7d runtime) are now accepted
by this evidence; Gate 23/24 and the remaining M89/M90+ gates remain pending.
v5.5 is still `IN_PROGRESS / NOT_ACCEPTED`; no model training, private source
upload, or v5.6 work was performed.
