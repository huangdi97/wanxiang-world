# Changelog ? Wanxiang Engineering Program

## 2026-08-11 ? Batch initialization

- Repository initialized (`git init`, branch `main`).
- Pre-implementation audit written (`reports/PRE_IMPLEMENTATION_AUDIT.md`).
- Ledgers created: PLAN, STATUS, DECISIONS, BLOCKERS, KNOWN_FAILURES, CHANGELOG, AGENTS.
- Batch scope: GOAL_00A .. GOAL_01F + M1 qualification. Stop after M1 PASS.

## 2026-08-11 ? GOAL_00A PASS

- uv workspace + 7 Python packages (src layout, py.typed), strict ruff/pyright/pytest config.
- `packages/observability`: settings loading, secret redaction, structured logging.
- TypeScript baseline (`packages/sdk_ts`) with strict tsconfig, ESLint, Vitest; all gates green.
- `scripts/quality.py` stable quality gate; CI workflow; docker-compose baseline.
- Ledgers/ADR structure/runbook created; ADR-0001 accepted.
- Checkpoint: `goal 00A: establish reproducible engineering foundation`.
