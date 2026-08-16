# Wanxiang — Semantic Persistent Open-Ended Co-Evolutionary World OS

A deterministic, event-sourced, branchable **world operating system**: a
single authoritative reality where humans, agents, external models, plugins
and projections participate without ever becoming commit authority.

## Current state

- **Certified production baseline: v5.2 / M42** (tag `m42-v5.2-production`),
  reached through an evidence-gated program M0→M42 with reproducible local
  PASS records for every goal and milestone.
- Kernel v1 is frozen; canonical history is append-only and replayable;
  snapshots are an optimization, never a replacement for event history.
- Core tests require **no external LLM API key** (deterministic/fake/reference
  providers).
- GitHub Actions CI runs safety/secret scans, Python quality gates,
  PostgreSQL integration, SDK/API drift checks, TypeScript checks, and
  release/clean-room certification smoke.

## Reading order (new session)

1. `README_FIRST.md` (latest program execution pack)
2. `README_FIRST_V5_2_CN.md` / `README_EN.md`
3. `docs/spec/WANXIANG_v5_2_MASTER_SPEC.md`
4. `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`

Authority order: master spec > Engineering Program Architecture > Goal files >
architecture docs/ADRs > code & tests.

## Quick start

```bash
uv sync --all-groups --all-packages
uv run pytest -q
uv run python scripts/quality.py
uv run python scripts/kernel_guard.py
pnpm install --frozen-lockfile
pnpm -r lint && pnpm -r typecheck && pnpm -r test && pnpm -r build
```

See `README_EN.md` for the full public overview, `CONTRIBUTING.md` for
contribution rules, `SECURITY.md` for security reporting,
`DATA_AND_ASSET_RIGHTS.md` for data/asset policy, and `NOTICE`/`LICENSE` for
licensing.
