# G91C — DirectorPolicy Modes

Date: 2026-08-26  
Status: PASS

## Result

`DirectorPolicy` now defines explicit CANON, DIRECTED, LIVING, and EXPERIMENT
mode contracts with separate allowed proposal types. `evaluate` returns a
typed proposal decision plus an immutable audit record; it does not authorize
or execute a command. Mode transitions return a new policy and a transition
audit, leaving the prior policy unchanged.

The implementation stays in `wanxiang_substrate.reality`. It imports no
CommitAuthority, runtime state, event store, or application transport, and no
Director or policy object exposes a commit method.

## Evidence

- `tests/unit/substrate/test_g91c_director_policy.py`: 3 passed.
- Existing G07D director regression and M6 integration chain remain green.
- `uv run ruff check`, format check, and `uv run pyright` on changed files:
  PASS; 0 errors and 0 warnings.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.

G91C is complete and committed. M88 Gates 17-18 remain pending until G91H
real playable qualification; v5.5 remains `IN_PROGRESS / NOT_ACCEPTED`. No
model training or v5.6 work was performed.
