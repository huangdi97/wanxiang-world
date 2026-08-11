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

## 2026-08-12 ? GOAL_00B PASS (M0 PASS)

- `scripts/architecture_check.py`: forbidden imports, import cycles, file-size,
  secret and placeholder guards; integrated into `scripts/quality.py`.
- `docs/architecture/MODULE_BOUNDARIES.md`, `reports/ACCEPTANCE_MATRIX.md` created.
- Architecture guard negative tests (17 tests total green).
- Reports: `reports/goal_00B_report.md`, `reports/M0_ENGINEERING_BASE_ACCEPTANCE.md`.
- Milestone tag `m0-engineering-base` created at M0 PASS.

## 2026-08-12 ? GOAL_01A PASS

- `packages/domain` core contracts: ids, versions, time, errors, hierarchy,
  entity, command, delta, event, hashing, state, snapshot, run, evidence, rights.
- Versioned serialization (command/delta + history contracts) with schema-version
  rejection; semantic hashing excluding wall-clock/audit fields.
- `docs/architecture/CORE_CONTRACTS.md`; ADR-0003.
- 48 tests green (unit + property).

## 2026-08-12 ? GOAL_01B PASS

- Commit Authority with preconditions, immutable canonical state, pure
  apply_delta, invariant registry, append-port atomicity, audit records.
- EventAppendPort + in-memory adapter (failure injection); ResolverRegistry seam.
- ComponentData gains component_id; ADRs 0004-0005.
- 63 tests green; docs/architecture/COMMIT_AUTHORITY.md.

## 2026-08-12 ? GOAL_01C PASS

- EventStore contract (append/load/idempotency/integrity) + InMemoryEventStore.
- Optimistic concurrency via store head; stale writers raise StaleRevision.
- Reusable contract suite (in-memory now; SQLite adapter in 01E).
- 75 tests green; docs/architecture/EVENT_STORE.md; ADR-0006.
