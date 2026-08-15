# Goal G34B Acceptance Report — WorldPack Definition schema v5.2 迁移

## Status
PASS

## Objective
Add Constitution / Genesis / Evolution / Lineage refs to WorldPack Definition
manifests while keeping old packages importable (schema bump + legacy adapter +
package migration CLI + checksum rules).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/packages/model.py`:
   - Added optional `constitution_ref` / `genesis_ref` / `evolution_policy_ref` /
     `lineage_ref` fields (default None -> backward compatible).
   - `canonical()` includes the refs ONLY when set -> legacy manifests keep
     their exact hash (golden worldpack fixture preserved).
   - `with_hash()` passes the refs through.
2. `packages/substrate/src/wanxiang_substrate/packages/migration.py` (ADAPT):
   - `V52_SCHEMA_VERSION = 3`, `LEGACY_CONSTITUTION_REF = "con_legacy_v5"`.
   - `_migrate_v2_to_v3` (adds constitution ref + rehash) registered in the
     existing `_MIGRATIONS` chain; v1->v2 now preserves refs (None for legacy).
   - `migrate_to_v52` (idempotent for v5.2 manifests), `is_v52`,
     `legacy_constitution_ref`.
3. `scripts/wxpack.py`: new `migrate` subcommand (migration CLI/use case).
4. `tests/unit/substrate/test_worldpack_migration.py` (4 tests):
   - legacy package round-trip (canonical/hash unchanged);
   - v5.2 export/import semantic equivalence (refs in canonical, stable hash,
     idempotent migration);
   - legacy vs v5.2 hashes differ but legacy stays stable;
   - wxpack CLI exposes the migrate subcommand.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_worldpack_migration.py -q` | 4 passed |
| `uv run pytest tests/unit/substrate tests/architecture/test_v52_baseline_fixtures.py tests/integration/test_g17f_registry_lifecycle.py tests/integration/test_g17d_certification.py -q` | 135 passed |
| `uv run python scripts/sdk_baseline.py` | routes=16 ts=5 py=952 (+5 non-breaking) |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Schema version bump | PASS (V52_SCHEMA_VERSION 3) |
| Legacy adapter | PASS (migrate_to_v52 / legacy constitution ref) |
| Package migration CLI/use case | PASS (wxpack migrate) |
| Checksum/signature rules updated | PASS (canonical conditionally includes refs) |
| Old package round-trip | PASS (tested; golden fixture hash preserved) |
| New package export/import semantic equivalence | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: tests/unit/substrate/test_worldpack_migration.py, reports/G34B_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/packages/model.py,
  packages/substrate/src/wanxiang_substrate/packages/migration.py,
  scripts/wxpack.py, reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g34b: WorldPack Definition schema v5.2 迁移`
