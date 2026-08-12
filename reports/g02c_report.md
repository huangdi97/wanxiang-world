# Goal G02C Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 38acada (G02B checkpoint)
- working-tree notes: clean

## Objective
Create material continuity so objects, containers, custody, ownership and
information payloads obey explicit conservation and knowledge boundaries.

## Delivered
- `wanxiang_substrate.material`: model (MaterialItem, ContainerSpec, Custody,
  Ownership, Containment, InfoPayload), errors, versioned components,
  MaterialQuery (read-only), resolvers (create item/container, transfer,
  move-into, consume, damage, seal/read payload, give ownership, instantiate),
  letter/package fixture (writer -> messenger -> recipient).
- No new persisted schema (material rides on versioned components).

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 182 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |

Goal-specific tests:
- unit: item/container/payload validation, custody-vs-ownership, container
  chain custody resolution, cycle detection;
- integration: transfer requires custodian; sealed letter not revealed by
  custody; recipient reads after receiving; container full/cycle rejected;
  consume/damage transitions; replay + branch custody isolation;
- property: custody conserved (single holder) across transfers.

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| Tasks complete; no TODO/placeholder | PASS | placeholder guard |
| Goal + regression tests PASS | PASS | 182 tests incl. M1 + G02A/B |
| Lint/type/architecture PASS | PASS | quality gate |
| Schema change has migration test | NOT_APPLICABLE | no schema change; M1 replay green |
| Mutations flow through Validate/Resolve/Commit | PASS | resolvers -> CommitAuthority |
| No domain/core dependency on FastAPI/SQLAlchemy/UI/LLM | PASS | guard |

## Key decisions
- Custody != ownership; custody != knowledge (ADR-0013).

## Known limitations
- Inventory UI / real museum behavior out of scope (later goals).

## External blockers
None.

## Final checkpoint
- commit: `goal g02c: material, container, custody & information payload`
