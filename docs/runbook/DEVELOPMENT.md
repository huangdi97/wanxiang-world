# Development Runbook ? Wanxiang (M0/M1 batch)

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (>= 0.5)
- Node 20+ and pnpm 9+ (for TS baseline only)
- git

Docker is optional (compose baseline exists) ? local tests never require it.

## Bootstrap (fresh clone)

```powershell
git clone <repo> wanxiang
cd wanxiang
uv sync --all-groups --all-packages  # installs all workspace members + dev tools
pnpm install           # TS baseline
```

## Quality commands (stable names)

From repository root:

```powershell
uv run python scripts/quality.py        # full gate: ruff lint + format + pyright + pytest
uv run ruff check .                     # lint
uv run ruff format --check .            # format
uv run pyright                          # typecheck (strict)
uv run pytest -q                        # test suite
pnpm -r lint                            # TS lint (baseline)
pnpm -r typecheck                       # TS typecheck
pnpm -r test                            # TS tests
pnpm -r build                           # TS build
```

Architecture conformance is part of the normal quality command (GOAL_00B+):
`uv run python scripts/architecture_check.py` is invoked by `scripts/quality.py`.

## Deterministic test profile

pytest runs with `-p no:cacheprovider` disabled determinism issues? No ? pytest is
configured with a fixed random seed profile for Hypothesis (`hypothesis.seed`)
and `PYTHONHASHSEED` guidance in CI. See `pyproject.toml`.

## Database

- Local tests: SQLite (in-memory or `data/wanxiang.db`), foreign keys enforced.
- Production-compatible: PostgreSQL; schema is written to remain PG-compatible.
- Migrations: Alembic (`uv run alembic upgrade head`).

## Ledgers

Always update after a Goal: `PLAN.md`, `STATUS.md`, `DECISIONS.md`,
`BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`, plus `reports/goal_<id>_report.md`.

## uv cache note

On sandboxed hosts, set UV_CACHE_DIR inside the workspace so uv may write its
cache (e.g. uv cache probes/writes inside the cache dir). Example:

``powershell
$env:UV_CACHE_DIR='E:\AI\wanxiang\.uv-cache'
``
