# Goal G34E Acceptance Report — API SDK Client 兼容

## Status
PASS

## Objective
Extend the API for v5.2 resources (constitution/lineage/promotion) without
breaking existing clients: generate the TS SDK and keep old world/branch
endpoints (or a deprecation adapter).

## Delivered
1. `apps/api/src/wanxiang_api/constitution_routes.py`: `GET
   /constitutions/{constitution_id}` (read-only, returns the manifest primitive;
   404 for unknown). Wired into `create_app`.
2. TS SDK: `packages/sdk_ts/src/constitution.ts` (typed
   `ConstitutionManifest` + `constitutionId` + `assertConstitutionManifest`),
   exported from `index.ts`.
3. OpenAPI regenerated (17 paths / 17 operations); lineage + promotion
   endpoints already present (G31G/G33F); old world/branch endpoints untouched.
4. `tests/api/test_constitution_api.py` (3 tests):
   - constitution endpoint returns the platform-root manifest (404 for unknown);
   - OpenAPI includes new resources AND keeps every old endpoint (no breaking
     removal);
   - old-client smoke: world create + action + state still work.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/api/test_constitution_api.py -q` | 3 passed |
| `uv run python scripts/export_openapi.py` | 17 paths / 17 operations |
| `uv run python scripts/sdk_baseline.py` | routes=17 ts=5 py=952 |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Constitution/lineage/promotion endpoints | PASS |
| TS SDK generated | PASS |
| Old world/branch endpoints preserved | PASS (no breaking removal; smoke test) |
| OpenAPI diff review | PASS (new + old all present) |
| Old client smoke tests | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: apps/api/src/wanxiang_api/constitution_routes.py,
  packages/sdk_ts/src/constitution.ts, tests/api/test_constitution_api.py,
  reports/G34E_REPORT.md
- modified: apps/api/src/wanxiang_api/app.py, packages/sdk_ts/src/index.ts,
  packages/sdk_ts/src/openapi-contract.json, reports/sdk_api_baseline.json,
  reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g34e: API SDK Client 兼容`
