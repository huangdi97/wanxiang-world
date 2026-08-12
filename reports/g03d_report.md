# Goal G03D Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: c7790ff (G03C checkpoint)
- working-tree notes: clean

## Objective
Create structured action definitions and current-state affordances, then reject
impossible, unauthorized or epistemically invalid actions before resolution.

## Delivered
- `wanxiang_substrate.actions`: ActionDefinition/ParameterSpec, ActionRegistry +
  reference actions (move, read_payload, deliver_message, rest, inspect),
  ActionValidator (side-effect-free), ValidationResult/Issue, Affordance +
  compute_affordances.

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 244 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- unit: unknown action rejected; missing/wrong parameter; missing actor;
  validation side-effect-free;
- integration: validated move candidate commits; affordances available for
  actor; invisible knowledge reference rejected (no_knowledge).

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | placeholder guard |
| Goal + regression tests PASS | PASS | 244 tests incl. M1/M2/G03A-C |
| Lint/type/architecture PASS | PASS | quality gate |
| Schema change has migration test | NOT_APPLICABLE | no new table |
| Validation side-effect free | PASS | hash-unchanged test |
| Unknown action/version fails explicitly | PASS | unit test |
| Invisible knowledge reference rejected | PASS | no_knowledge test |

## Key decisions
- Versioned action registry + side-effect-free validator (ADR-0021).

## Known limitations
- deliver_message is a definition; its resolver is domain/world-pack specific.

## External blockers
None.

## Final checkpoint
- commit: `goal g03d: action, affordance & validator`
