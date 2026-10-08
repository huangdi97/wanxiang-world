# G91H — M88 Director/Pressure Qualification

Date: 2026-08-26  
Status: PASS

## Real product-chain result

The qualification starts from a private rights-approved source and runs the
existing OneClickAuthoring → WorldPackage → PreviewInstall → PlayableService
chain. A real embodied actor enters the playable instance and commits an
action through the existing runtime Commit boundary.

On that same world, the qualification verifies:

- PressureProfile is attached to the playable Scenario/Domain refs and the
  matched pressure benchmark is same-seed/profile and repeatable.
- CANON evaluates an Opportunity proposal, then switches immutably to LIVING
  with an audit record; no Director object has a commit path.
- The actor is offered an Opportunity and ignores it. The ignored decision is
  retained in the projection and does not overwrite the actor goal or parent
  canonical state.
- A reversible time-triggered Intervention is linked to a RunArtifact ref and
  forks through the existing runtime. Parent events and semantic hash remain
  unchanged, and the child replays to its own state hash.
- Canon Attractor assessment preserves the actual actor choice.

## Evidence

- `tests/integration/test_g91h_director_pressure.py`: 1 passed.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.
- Focused M88 regression (G91A-G91H plus G07C-G07E/M6): PASS.
- Full `uv run pytest -q`: 1296 passed, 1 skipped, 2 warnings in 330.95s;
  the skip is the documented external PostgreSQL profile with no
  `WANXIANG_POSTGRES_TEST_URL`.
- `uv run ruff check`, format check, and `uv run pyright` on changed files:
  PASS; 0 errors and 0 warnings.

M88 is **PASS**. Gates 16-20 are accepted in the acceptance matrix. v5.5
remains `IN_PROGRESS / NOT_ACCEPTED` because all later M89-M94 gates and final
release evidence are still pending. No model training or v5.6 work was
performed.
