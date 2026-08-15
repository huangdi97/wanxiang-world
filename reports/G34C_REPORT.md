# Goal G34C Acceptance Report — 数据库与 Ledger 兼容迁移

## Status
PASS

## Objective
Complete the v5.2 persistence upgrade without losing history: Alembic
migrations, lineage/constitution/evolution metadata, indexes/unique
constraints, backup/restore path.

## Delivered
1. Migration `0004_add_world_metadata` (down: `0003_add_lineage`):
   - `world_instances` gains nullable `definition_ref`, `constitution_ref`,
     `evolution_policy_ref` (v5.2 World Definition metadata).
   - Index `ix_lineage_nodes_kind` on `lineage_nodes(kind)`.
   - `downgrade()` restores the old schema (drop columns + index).
2. `packages/persistence/src/wanxiang_persistence/models.py`:
   `WorldInstanceRecord` extended with the 3 columns.
3. `tests/migration/test_g34c_db_migration.py` (3 tests):
   - old DB copy upgrade (0001 + events -> head): event count (5) and replay
     hash (7d17aba7...) unchanged; new metadata columns present;
   - downgrade 0004 -> 0003 restores the old schema (events intact);
   - backup/restore path: `scripts.backup_restore` backup + restore preserves
     event count + replay hash.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/migration -q` | 11 passed (3 new + 8 existing) |
| `uv run pytest tests/migration/test_g34c_db_migration.py -q` | 3 passed |
| `uv run python scripts/sdk_baseline.py` | routes=16 ts=5 py=952 |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Alembic migrations | PASS (0004, downgrade-safe) |
| Lineage/constitution/evolution metadata persisted | PASS |
| Indexes + unique constraints | PASS (lineage kind index; existing uniques retained) |
| Backup/restore path | PASS (tested) |
| Old DB copy upgrade | PASS (event count/hash unchanged) |
| Downgrade/restore strategy | PASS (tested) |
| Event count/hash unchanged | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: migrations/versions/0004_add_world_metadata.py,
  tests/migration/test_g34c_db_migration.py, reports/G34C_REPORT.md
- modified: packages/persistence/src/wanxiang_persistence/models.py,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g34c: 数据库与 Ledger 兼容迁移`
