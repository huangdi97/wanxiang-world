# Goal G03C Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 00419ef (G03B checkpoint)
- working-tree notes: clean

## Objective
Implement actors, organizations, controller policies, membership, command flow
and information flow without treating organizations as giant chat agents.

## Delivered
- `wanxiang_substrate.agency`: model (IntentCandidate, Order, ExecutionReport),
  policy ports (Deterministic/Rule/Human), versioned order/actor-state
  components, AgencyQuery, resolvers (order lifecycle, set_actor_state,
  instantiate), organization fixture.

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 236 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- unit: order lifecycle transitions, order validation, policies return
  IntentCandidate only, rule policy needs observation;
- integration: full order lifecycle with deviation; invalid transition
  rejected; actor states + organization views; deterministic policy stable;
  propose-only (no mutation).

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | placeholder guard |
| Goal + regression tests PASS | PASS | 236 tests incl. M1/M2/G03A-B |
| Lint/type/architecture PASS | PASS | quality gate |
| Schema change has migration test | NOT_APPLICABLE | no new table; replay green |
| Policies return Intent/Action candidate only | PASS | policy tests |
| Policy cannot access commit repository through interface | PASS | propose-only context |
| Order lifecycle + org membership views | PASS | order + org tests |

## Key decisions
- Propose-only policies; order lifecycle with typed transitions (ADR-0020).

## Known limitations
- LLM policy remains a replaceable port (not implemented).

## External blockers
None.

## Final checkpoint
- commit: `goal g03c: actor & organization runtime`
