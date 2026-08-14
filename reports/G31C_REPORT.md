# Goal G31C Acceptance Report ? Lineage Repository ???

## Status
PASS

## Objective
Persist lineage with minimal new tables/indexes, without copying Event history,
reusing the existing branches table for branch lineage.

## Delivered
1. Migration `0003_add_lineage` (down: `0002_add_event_seq_index`):
   - `lineage_nodes` (node_id PK, kind, definition_ref, inherited_history_ref,
     constitution/domain/runtime versions, evolution_policy, rights_ref,
     provenance_json) and `lineage_edges` (parent/child FKs, edge_kind,
     origin_ref; child index).
   - `downgrade()` drops both tables (compatible rollback).
2. `packages/persistence/src/wanxiang_persistence/models.py`: `LineageNodeRecord`
   + `LineageEdgeRecord`.
3. `packages/persistence/src/wanxiang_persistence/lineage_repository.py`:
   - `LineageRepository` ? save_node/save_edge/load_graph (SQLite/PostgreSQL-
     compatible SQLAlchemy).
   - `branch_lineage_from_branches` ? derives branch-fork edges from the EXISTING
     `branches` table (parent_branch_id/fork_revision/fork_event_seq), so branch
     lineage is NOT duplicated into a second system.
4. `tests/migration/test_lineage_migration.py` (5 tests):
   - fresh upgrade to head includes lineage tables;
   - old DB (0001 + events) upgraded to head keeps branch history (replay hash
     unchanged: 7d17aba7...);
   - downgrade from 0003 to 0002 removes lineage tables;
   - repository save/load graph round-trip;
   - branch lineage derived from existing branches table.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/migration -q` | 8 passed (5 new + 3 existing) |
| `uv run pytest tests/migration/test_lineage_migration.py -q` | 5 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=892 (+4 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Reuse existing world_definitions/branches | PASS (branch lineage derived from branches table; no duplication) |
| Minimal new tables/indexes for lineage | PASS (2 tables + 1 index) |
| Alembic migration + downgrade/compatibility | PASS (tested) |
| SQLite/PostgreSQL-compatible | PASS (SQLAlchemy types; SQLite tested; PG EXTERNAL_BLOCKED as before) |
| Old DB upgrade keeps branch history | PASS (replay hash unchanged) |
| No Event history copied | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: migrations/versions/0003_add_lineage.py,
  packages/persistence/src/wanxiang_persistence/lineage_repository.py,
  tests/migration/test_lineage_migration.py, reports/G31C_REPORT.md
- modified: packages/persistence/src/wanxiang_persistence/models.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g31c: Lineage Repository ???`
