# Goal G14B Acceptance Report — Crash, Atomicity & Mid-Commit Recovery Qualification

## Status
PASS

## Objective
Prove crashes at every important commit boundary cannot leave event history and canonical state in contradictory partial states.

## Delivered
- `tests/integration/test_g14b_crash_atomicity.py` — 5 tests covering every commit boundary.
- `reports/CRASH_ATOMICITY_MATRIX.md` — boundary x recovery matrix + documented recovery policy.
- `reports/G14B_REPORT.md`.

## Findings
- Crash before append: no event, no state change; retry commits exactly once.
- Crash after append: restart reconstructs from authoritative event history (same hash).
- Checkpoint does not break recovery (snapshot = optimization).
- Retry classification after restart: acknowledged -> same event (duplicate), unknown -> fresh commit.
- Lifecycle transition (PAUSED @ tick 5) survives restart via canonical events.
- No half event/state mutation observed at any boundary; audit of the accepted path is recorded.

## Evidence
- `uv run pytest tests/integration/test_g14b_crash_atomicity.py -q` -> 5 passed.
- Fault hooks are test-only (`InMemoryEventStore.fail_append`); production defaults unaffected.

## Remaining limitations
- Real process kill signals are not simulated; deterministic fault injection at each boundary covers the semantics.

## Final checkpoint
- commit: `g14b: crash, atomicity & mid-commit recovery qualification`
