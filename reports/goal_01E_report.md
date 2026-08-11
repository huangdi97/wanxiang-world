# Goal 01E Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: cee6f93 (goal 01D checkpoint)
- working-tree notes: clean

## Objective
Provide a real local durable persistence implementation for M1 with
SQLAlchemy 2/Alembic, clean repository ports, transactional commit
compatibility, migration tests and a PostgreSQL-compatible foundation.

## Delivered
- `packages/persistence`: ORM models, engine/session factory (SQLite FK),
  `SqlAlchemyEventStore` (EventStore contract), `SqlAlchemySnapshotStore`,
  `SqlAlchemyBranchRepository`, `WorldInstanceRepository`, `AuditTraceRepository`,
  `state_codec` (canonical state <-> JSON).
- Alembic migrations `0001_initial` + `0002_add_event_seq_index`; alembic.ini.
- SqlAlchemyEventStore registered against the shared EventStore contract suite.
- Integration tests: durable commit + reload replay, duplicate/out-of-order
  rejection, transaction rollback, snapshot save/load/latest, branch/instance
  repositories, audit traces.
- Migration tests: fresh upgrade to head, pre-head (0001) fixture upgrade keeps
  data + index, downgrade round trip.
- `docs/architecture/PERSISTENCE.md`.

## Key architecture decisions
- ORM confined to persistence; runtime `EventStore`/`SnapshotStore`/
  `BranchRepository` ports implemented by SQLAlchemy adapters.
- Ordering/idempotency enforced in the adapter before insert AND by DB unique
  constraints (defense in depth).
- JSON-as-text payloads for PG compatibility.

## Test evidence
| Check | Command | Result | Evidence path |
|---|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS | |
| Pyright strict | `uv run pyright` | PASS (0 errors) | |
| Pytest | `uv run pytest -q` | 111 passed | tests/integration, tests/migration, tests/contract |
| Architecture | `uv run python scripts/architecture_check.py` | PASS | |
| Full gate | `uv run python scripts/quality.py` | PASS | |

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|
| M1 works with actual SQLite persistence | PASS | durable replay test (golden hash) |
| No ORM types escape into domain/runtime public API | PASS | adapters map records <-> domain types |
| Migrations reproducible | PASS | fresh/upgrade/downgrade tests |
| Failed transaction no state/event mismatch | PASS | rollback + no-partial-row test |
| Durable replay passes | PASS | store recreation + replay == golden hash |
| Schema/version documented | PASS | PERSISTENCE.md |

## Migrations / compatibility
- 0001 initial; 0002 adds ordered stream index; pre-head fixture upgrade tested.
- Golden replay fixture replayed from the durable store.

## Security / rights impact
- No secrets persisted; audit traces are structured and durable.

## Known limitations
- PostgreSQL not exercised locally (compatible SQL; documented). Docker compose
  Postgres available for later validation.
- JSON columns are text (JSONB is a later optimization).

## External blockers
None.

## Final checkpoint
- commit: `goal 01E: add durable persistence and migration foundation`
