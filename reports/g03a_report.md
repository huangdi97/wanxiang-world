# Goal G03A Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 3812911 (M2 milestone)
- working-tree notes: clean

## Objective
Introduce explicit observations and perspective boundaries so actors only
receive information they could perceive or be told.

## Delivered
- `wanxiang_substrate.observation`: model (Observation, ObservationFact,
  EntityVisibility), versioned visibility/announcement components, resolvers
  (set_visibility/announce/instantiate), PerspectiveService, confidential
  letter fixture.

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 220 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- unit: fact field lookup, channel confidence, visibility validation;
- integration: same-place visual observation; sealed payload content never
  leaks; observer outside zone sees nothing; branch perspectives differ only
  when justified; private visibility hides events.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | placeholder guard |
| Goal + regression tests PASS | PASS | 220 tests incl. M1 + M2 |
| Lint/type/architecture PASS | PASS | quality gate |
| Schema change has migration test | NOT_APPLICABLE | no new table; replay green |
| Observations derived via ports; no canonical truth copied wholesale | PASS | PerspectiveService reads events + queries |
| Confirmed/overheard fixtures | PASS | confidential letter + announce tests |

## Key decisions
- Observations derived on demand; rule_refs audit; sealed payload hidden (ADR-0018).

## Known limitations
- Belief/memory interpretation is G03B.

## External blockers
None.

## Final checkpoint
- commit: `goal g03a: observation & perspective isolation`
