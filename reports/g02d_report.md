# Goal G02D Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 250dd0b (G02C checkpoint)
- working-tree notes: clean

## Objective
Model body and condition state as constraints on action, schedule and
perception rather than decorative RPG stats.

## Delivered
- `wanxiang_substrate.body`: model (BodyCondition, MobilityCapability,
  visible_facets), errors, versioned components, BodyQuery (read-only),
  resolvers (exert/rest/apply_condition/medicate/set_visibility/instantiate),
  condition fixture (healthy + fatigued actors with positions).
- Spatial move resolver now rejects movement for fatigued/immobile actors
  (`BodyConstraintViolation`).

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 192 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- unit: condition ranges, mobility capability, visible facets, immutable
  with_facet;
- integration: exert/rest deterministic; fatigued actor blocked from a valid
  spatial move; invalid range rejected; condition replay deterministic;
  private facet excluded from public projection;
- property: energy stays bounded across exerts.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | placeholder guard |
| Goal + regression tests PASS | PASS | 192 tests incl. M1 + G02A/B/C |
| Lint/type/architecture PASS | PASS | quality gate |
| Schema change has migration test | NOT_APPLICABLE | no schema change; M1 replay green |
| Mutations flow through Validate/Resolve/Commit | PASS | resolvers -> CommitAuthority |
| No domain/core dependency on FastAPI/SQLAlchemy/UI/LLM | PASS | guard |
| Capability check via port consumed by action validation | PASS | BodyQuery consulted by spatial.move |

## Key decisions
- Condition as bounded facets; fatigue blocks spatial movement (ADR-0014).

## Known limitations
- Medication effect is recorded but not yet mechanically applied (G03E/domain).

## External blockers
None.

## Final checkpoint
- commit: `goal g02d: body & condition constraints`
