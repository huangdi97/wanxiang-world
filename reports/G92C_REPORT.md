# G92C — Checkpoint / Resume / Crash Recovery

Date: 2026-08-26  
Status: PASS

## Delivered contract

`RunCheckpoint` records only a long-run cursor boundary: world/branch refs,
checkpoint sequence, scheduler cursor, canonical state hash, and event head.
`RunCheckpointStore` publishes a validated checkpoint atomically and keeps
append-only checkpoint history; it is not a second canonical snapshot or event
store. `CrashPlan` injects a deterministic failure before publication, so a
crash cannot expose a partial cursor.

`RecurringScheduler.restore_cursor` rebuilds the exact registered pending queue.
`LongRunCheckpointService.resume` restores that cursor, while the existing
WorldRuntime event store remains the source of committed truth. Runtime command
IDs therefore provide the duplicate-commit barrier on retry.

## Evidence

- `tests/unit/substrate/test_g92c_checkpoint.py`: 3 passed.
- `tests/integration/test_g92c_checkpoint_runtime.py`: 1 passed; restart
  restored the scheduler and a retried temporal command was reported duplicate
  without a second event.
- Combined focused result: 4 passed, 1 existing Hypothesis collection warning.
- Ruff check and format check: PASS.
- Pyright on changed implementation/tests: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.

G92C is PASS. Checkpoint/resume Gate 25 remains pending until the M89 long-run
qualification assembles the complete 24h/7d/30d evidence. v5.5 remains
`IN_PROGRESS / NOT_ACCEPTED`; no model training, private source upload, or
v5.6 work was performed.
