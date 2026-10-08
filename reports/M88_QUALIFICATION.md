# M88 — World Pressure / Opportunity / Director Modes Qualification

Date: 2026-08-26  
Status: PASS

## Scope result

G91A-G91H are complete. The qualification preserves the v5.4 Kernel, Reality
Root, Commit, Ledger, Branch, and Lineage semantics. Pressure, Director,
Opportunity, Canon Attractor, Intervention, Quest, and benchmark types remain
in the substrate reality/Scenario plane; no pressure-specific type entered
`packages/domain` or `packages/runtime`.

## Real product-chain evidence

`tests/integration/test_g91h_director_pressure.py` starts with a private,
rights-approved source, creates a WorldPackage through OneClickAuthoring,
enters the isolated Preview through PlayableService, and commits one embodied
actor action through the existing runtime. On that same world it verifies:

- PressureProfile refs and matched deterministic behavior benchmark;
- CANON proposal evaluation and audited CANON→LIVING mode switch;
- eligible Opportunity offered to the actor and explicitly ignored;
- Quest status remains ignored and no actor goal/canonical state is written;
- Canon Attractor keeps the observed actor choice;
- artifact-linked reversible time Intervention forks a child using the
  existing runtime branch boundary; parent events/hash remain unchanged and
  child replay equals child current state.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| 16 PressureProfile outside Kernel | ACCEPTED | G91A + G91H + Kernel guard |
| 17 Four Director modes | ACCEPTED | G91C + G91H |
| 18 Director has no Commit authority | ACCEPTED | proposal-only audit and architecture review |
| 19 Opportunity can be ignored | ACCEPTED | G91B + G91H actor decision |
| 20 Intervention branch/artifact isolation | ACCEPTED | G91E + G91H parent/replay proof |

## Required architecture and quality evidence

- Full Python regression: `uv run pytest -q` → 1296 passed, 1 skipped,
  2 warnings in 330.95s; the skip is the documented external PostgreSQL
  profile with no `WANXIANG_POSTGRES_TEST_URL`.
- `uv run python scripts/kernel_guard.py`: 0 violations.
- `uv run python scripts/architecture_check.py`: PASS.
- Duplicate abstraction scan: PASS; no unallowed duplicates.
- Minimality snapshot: registries 16, services 23, engines 5, ports 41,
  cycles 0, commit paths 1, oversized modules 0.
- Ruff, Pyright, SDK/minimality snapshots, and v5.4 critical tests pass.

M88 is PASS. v5.5 remains `IN_PROGRESS / NOT_ACCEPTED` because M89-M94 and
the final remote/Actions/release gates are not complete. No model training,
private source upload, or v5.6 work was performed.
