# G92B — Background Simulation

Date: 2026-08-26  
Status: PASS

## Delivered contract

`BackgroundPolicy` reuses the existing versioned Playable `RuntimeProfile`
and defines paused, realtime, accelerated, background, and full-autonomy
offline modes. The policy converts detached elapsed ticks into monotonic world
ticks using the profile time scale; paused mode advances zero ticks.

`SessionCursor` is a serializable leave-world boundary containing only world,
branch, session, world tick, and scheduler cursor refs. `BackgroundSimulation`
can consume that cursor without an active UI session, returns immutable
occurrence proposals, and exposes a re-entry cursor. It never mutates
canonical state or bypasses the existing runtime authority.

## Evidence

- `tests/unit/substrate/test_g92b_background.py`: 3 passed.
- `tests/integration/test_g92b_background_runtime.py`: 1 passed; accelerated
  offline occurrences resumed through the existing temporal Commit path.
- Combined focused result: 4 passed, 1 existing Hypothesis collection warning.
- Ruff check and format check: PASS.
- Pyright on changed implementation/tests: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.

G92B is PASS. The 24h/7d and later long-run gates remain pending; v5.5 is
still `IN_PROGRESS / NOT_ACCEPTED`. No model training, private source upload,
or v5.6 work was performed.
