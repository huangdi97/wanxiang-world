# G92A — Long-Horizon Scheduler

Date: 2026-08-26  
Status: PASS

## Delivered contract

`wanxiang_substrate.long_horizon.scheduler` now provides an immutable
recurring schedule contract, deterministic priority ordering, monotonic world
ticks, actor availability windows, and explicit catch-up/availability fields
on every emitted occurrence. Payloads and queue cursors are deterministic.

The scheduler is proposal-side only. It does not import or call Commit
Authority, mutate canonical state, or create a second event store. The real
runtime test adapts its occurrences into existing `temporal.advance_to`
commands, which are validated and committed by the existing WorldRuntime.

## Evidence

- `tests/unit/substrate/test_g92a_scheduler.py`: 3 passed.
- `tests/integration/test_g92a_scheduler_runtime.py`: 1 passed through the
  existing SQLite WorldRuntime and temporal resolver.
- Combined focused result: 4 passed, 1 existing Hypothesis collection warning.
- Ruff check and format check: PASS.
- Pyright on changed implementation/tests: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.

G92A is PASS and v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`; the 24h/7d
qualification gate remains pending until G92G. No model training, private
source upload, or v5.6 work was performed.
