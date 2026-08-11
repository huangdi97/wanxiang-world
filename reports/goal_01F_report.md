# Goal 01F Acceptance Report

## Status
PASS

## Pre-goal state
- branch: main
- commit: 25256a8 (goal 01E checkpoint)
- working-tree notes: clean

## Objective
Integrate P0/P1 components into a small real deterministic synthetic world
execution path and prove Milestone M1 end-to-end.

## Delivered
- Application layer (`packages/application`): WorldRuntime (create/command/
  state/events/checkpoint/restore/branch/diff/metrics), synthetic micro-world
  resolvers (create_entity, transfer_resource, set_status), WorldEnvironment
  facade (honest subset: create/observe/legal_actions/step/checkpoint/restore/
  branch/metrics/close).
- FastAPI transport (`apps/api`): thin routes (POST /worlds, GET state/events,
  POST actions/checkpoint/replay/branches, compare, healthz), Pydantic DTOs,
  structured WanxiangError -> HTTP mapping, OpenAPI.
- M1 acceptance tests A1-A10 against the application/runtime layer with SQLite.
- API e2e tests (healthz, create+action, idempotent, stale 409, invalid 422,
  checkpoint/replay/branch, OpenAPI paths).
- WorldEnvironment unit tests (in-memory).
- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`, `reports/ACCEPTANCE_MATRIX.md`,
  `docs/IMPLEMENTATION_STATUS.md`.

## Key architecture decisions
- Composition root (`apps/api/app.py`) wires SQLAlchemy adapters; routes stay
  thin (architecture guard exempts only app.py from persistence imports).
- Resolvers are state-aware (read current state, never mutate) to enforce
  resource conservation deterministically.
- Canonical state codec lives with the state type in `wanxiang_runtime.state`.

## Test evidence
| Check | Command | Result |
|---|---|---|
| Ruff lint/format | `uv run ruff check .` / `format --check .` | PASS |
| Pyright strict | `uv run pyright` | PASS (0 errors) |
| Pytest | `uv run pytest -q` | 130 passed |
| Architecture | `uv run python scripts/architecture_check.py` | PASS |
| Full gate | `uv run python scripts/quality.py` | PASS |

## Acceptance criteria (M1)
All 17 criteria PASS (see M1 report): no LLM key; real application/runtime/
persistence code; valid commit exactly once; invalid no mutation; duplicate
idempotent; stale rejected; durable ordering; snapshot+replay same hash; full
replay; branch isolation; corrupt stream fails; SQLite migrations; no
TODO/placeholder/mock in required paths; guards pass; quality suite green;
evidence names commands/tests/commit; clean tree before checkpoint.

## Known limitations
See M1 report ?6 (PostgreSQL local validation deferred, httpx2 deprecation
warning in tests, fork restore via parent replay, synthetic resolvers in app).

## Final checkpoint
- commit: `goal 01F: qualify authoritative world milestone`
- milestone tag: `m1-authoritative-world`
