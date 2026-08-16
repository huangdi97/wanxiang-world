# Contributing to Wanxiang

Thanks for your interest. Wanxiang is an evidence-gated engineering program:
**code and tests are evidence, never permission to silently change the spec.**

## Ground rules (non-negotiable)

Read `AGENTS.md` first. In short:

- `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md` (and `WANXIANG_v5_MASTER_SPEC.md`)
  is the product source of truth.
- Only **Commit Authority** may mutate Canonical World State. LLMs, humans,
  clients, sensors, plugins, resolvers, projections and adapters produce
  Commands / Intents / Observations / ProposedWorldDeltas only.
- Canonical history is append-only and replayable; snapshots are an
  optimization, never a replacement for event history.
- Child branches never mutate parent history; stale branch revisions are
  rejected with typed conflicts; duplicate command retries never duplicate
  world effects.
- Modular monolith: domain layer must not import FastAPI/SQLAlchemy/Alembic/
  LLM SDKs; persistence stays behind ports.
- No global mutable singletons; constructors do no hidden I/O.
- Production files target ≤ 300 lines; split by concern.
- No TODO/placeholder/NotImplemented/mock-only path counts as completion.
- No LLM API key is required for core tests.

## Before you start

1. Read the relevant Goal file(s) under `goals/` and the master spec.
2. Check `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`,
   `KNOWN_FAILURES.md`, `CHANGELOG.md` for current state and open decisions.
3. Mark your Goal ACTIVE in PLAN/STATUS, write tests early, then implement the
   smallest complete architecture.

## Quality gates (must stay green)

```bash
uv sync --all-groups --all-packages
uv run ruff check .
uv run ruff format --check .
uv run pyright
uv run pytest -q
uv run python scripts/architecture_check.py   # included in scripts/quality.py
uv run python scripts/quality.py
uv run python scripts/kernel_guard.py
pnpm install --frozen-lockfile
pnpm -r lint && pnpm -r typecheck && pnpm -r test && pnpm -r build
```

A new dependency direction requires an ADR and a guard rule + negative test
(`scripts/architecture_check.py`, `docs/architecture/MODULE_BOUNDARIES.md`).

## Committing

- Run the full quality gates and write `reports/goal_<id>_report.md` before
  committing a Goal.
- Update ledgers (`STATUS.md`, `CHANGELOG.md`, and any applicable index).
- Local commits only; do **not** push/deploy unless explicitly authorized.

## Public data policy

- Never commit `.env`, tokens, credentials, private keys, databases, user
  privacy data, model caches, or large generated assets.
- Never commit restricted/copyrighted source corpora (including any
  《红楼梦》 edition text or museum/private materials). Publish only
  synthetic/deterministic samples; see `DATA_AND_ASSET_RIGHTS.md`.
- If a real source is not legally available, record `EXTERNAL_BLOCKED`
  honestly — never fake completion.

## Reporting problems

See `SECURITY.md` for security issues. For everything else, open an issue with
a minimal reproduction and the failing gate command.
