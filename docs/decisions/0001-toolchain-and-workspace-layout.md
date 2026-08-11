# ADR-0001: Toolchain and Workspace Layout (M0)

- Status: accepted
- Date: 2026-08-11
- Owners: Wanxiang Engineering Program

## Context

GOAL_00A requires a reproducible monorepo engineering base: Python 3.12 +
`uv`, a strict TypeScript/pnpm baseline, deterministic tests, quality commands,
ledgers and an ADR structure. The Program Architecture leaves the exact physical
tree adjustable via ADRs while freezing dependency direction.

## Decision

1. **Python**: uv workspace (root `pyproject.toml` with `[tool.uv] package = false`
   and members `packages/*`). Each package is an installable src-layout package
   (`packages/<name>/src/wanxiang_<name>/`) built with hatchling.
2. **Cross-cutting observability**: a new `packages/observability` package owns
   structured logging, environment settings loading and secret redaction. This is
   an addition to the recommended Program Architecture map; it is a bounded
   context, not a dumping ground.
3. **TypeScript**: pnpm workspace with `packages/sdk_ts` strict baseline
   (TypeScript strict, ESLint + typescript-eslint, Vitest). No product UI.
4. **Quality command**: `uv run python scripts/quality.py` is the stable
   repository quality gate (ruff lint + format, pyright strict, pytest, and
   architecture conformance when `scripts/architecture_check.py` exists).
5. **Deterministic tests**: pytest markers for unit/property/contract/
   integration/architecture/migration/e2e; Hypothesis `derandomize` profile;
   pytest cache provider disabled for reproducible output.
6. **Cache/venv hygiene**: `.venv`, `.uv-cache`, `node_modules`, `dist` are
   gitignored; `uv.lock` and `pnpm-lock.yaml` are committed.

## Consequences

- Later Goals implement against stable package boundaries and a single quality gate.
- The physical tree differs slightly from the recommended map (added
  `packages/observability`); dependency direction is unchanged and documented in
  `docs/architecture/MODULE_BOUNDARIES.md` (GOAL_00B).
- TS baseline exists now so future SDK/API generation has a home.

## Alternatives considered

- Single `src/wanxiang/` namespace package: simpler imports but weakens physical
  package-boundary enforcement; rejected in favor of separate workspace packages.
- Makefile/tox task runner: `uv` + a Python quality script is sufficient and
  Windows-friendly; no tox added.
