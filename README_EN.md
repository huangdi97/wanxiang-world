# Wanxiang — Semantic Persistent Open-Ended Co-Evolutionary World OS

Wanxiang is a deterministic, event-sourced, branchable **world operating
system**: a single authoritative reality that stays consistent while
human actors, agents, external models, plugins and projections participate —
without any of them ever becoming commit authority.

This repository contains the **v5.2 production-certified** monorepo
(milestone M42, tag `m42-v5.2-production`). It is the result of a long,
evidence-gated engineering program (M0→M42) with reproducible local PASS
records for every goal and milestone.

## What is inside

- **Authoritative World Kernel** — append-only event history, replayable
  snapshots, idempotent command handling, typed branch conflicts.
- **Reality Root / World Semantic ISA** — a thin reduction layer on top of a
  shared semantic bedrock (no second Commit/Event/Branch/Worldline/Registry
  duplicate).
- **Worldlines, Lineage & Promotion** — branch and worldline share history
  semantics; promotion reuses Distillation / Snapshot / Package / Invariant
  mechanisms.
- **Domain runtime, packages & SDK** — authoring, validation, dry-run build,
  certification and migration for domain packages (`scripts/wxpack.py`),
  plus a typed TypeScript SDK (`packages/sdk_ts`).
- **Apps & APIs** — FastAPI application with an exported OpenAPI contract
  consumed by the TS SDK.
- **Synthetic reference worlds** — deterministic sample content; the real
  《红楼梦》 text is deliberately **not** included (see
  `DATA_AND_ASSET_RIGHTS.md`).

Core tests require **no external LLM API key**; deterministic/fake/reference
providers are used throughout.

## Repository layout

| Path | Purpose |
|---|---|
| `docs/spec/` | Master specs (source of truth) |
| `packages/` | Python workspace packages (`domain`, `runtime`, `application`, `persistence`, `substrate`, ...) |
| `apps/` | Applications (FastAPI API, etc.) |
| `packages/sdk_ts/` | TypeScript SDK |
| `tests/` | Unit / integration / contract / property / architecture tests |
| `scripts/` | Quality gates, kernel guard, release & certification tools |
| `goals/`, `milestones/` | Executable engineering contracts and qualification gates |
| `reports/` | Evidence reports per goal/milestone |

## Quick start

```bash
# Python (uv workspace)
uv sync --all-groups --all-packages
uv run pytest -q
uv run python scripts/quality.py
uv run python scripts/kernel_guard.py

# TypeScript SDK
pnpm install --frozen-lockfile
pnpm -r lint
pnpm -r typecheck
pnpm -r test
pnpm -r build
```

See `README_EN.md` (this file) for the full public overview and
`docs/runbook/` for bootstrap details.

## Status

- Certified production baseline: **v5.2 / M42** (`m42-v5.2-production`).
- CI: GitHub Actions runs safety/secret scans, Python quality gates,
  PostgreSQL integration, SDK/API drift checks, TypeScript checks, and
  release/clean-room certification smoke (`/.github/workflows/ci.yml`).
- The repository also carries **user-prepared planning documents** for the
  next program batch (v5.3 M43–M50, including the open-source delivery goals
  G53J–G53L). Those documents are planning material and are **not** marked as
  qualified/implemented.

## License & data rights

- Code: [Apache-2.0](LICENSE) (see `NOTICE`).
- Data/assets: see `DATA_AND_ASSET_RIGHTS.md`. This repository publishes only
  synthetic/deterministic sample content; restricted corpora (including any
  《红楼梦》 edition text) are explicitly excluded and are not present.
- Contributions: see `CONTRIBUTING.md`; security: see `SECURITY.md`;
  community standards: see `CODE_OF_CONDUCT.md`.
