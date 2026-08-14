# PostgreSQL Production Persistence & Migration Qualification (G16B)

## Design (dialect-agnostic)
- Schema: text PKs, integer counters, JSON-as-text payloads (portable across SQLite/PostgreSQL).
- SQLite-specific `PRAGMA foreign_keys=ON` is applied only when the URL starts with `sqlite`; the
  portable persistence modules contain no SQLite-specific SQL.
- No direct DB dependency leaks into the domain layer (architecture guard enforced).

## Qualification results
| Check | Result |
|---|---|
| Migration chain compiles offline for the `postgresql` dialect (full head DDL) | PASS |
| Portable persistence path has no SQLite-specific SQL (only guarded engine factory) | PASS |
| Semantic hashes are storage-independent (golden hash reproduced on SQLite) | PASS |
| Live PostgreSQL integration profile | EXTERNAL_BLOCKED (no instance; WANXIANG_POSTGRES_TEST_URL unset) |

## Live runbook
1. Start PostgreSQL (e.g., `docker compose up postgres` or a managed instance).
2. `WANXIANG_DATABASE_URL=postgresql://wanxiang:<pass>@<host>/wanxiang uv run alembic upgrade head`
3. Set `WANXIANG_POSTGRES_TEST_URL` and run `uv run pytest tests/integration/test_g16b_postgres.py`
   to execute the live migration + replay profile.

## DB version support
- Target: PostgreSQL 16 (docker-compose profile); migrations use portable SQLAlchemy DDL.
- SQLite remains the local deterministic development adapter; world semantics are storage-independent.

## Evidence
- `uv run pytest tests/integration/test_g16b_postgres.py -q` -> 3 passed, 1 EXTERNAL_BLOCKED skip.
