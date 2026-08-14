# Goal G31G Acceptance Report ? Lineage API SDK Studio ????

## Status
PASS

## Objective
Expose lineage queries (ancestor/descendant/promotion origin) through the API,
regenerate SDK types from OpenAPI, and give the Studio a read-only lineage view
reusing the shared lineage graph.

## Delivered
1. API: `apps/api/src/wanxiang_api/lineage_routes.py`:
   - `GET /lineage/nodes/{node_id}/ancestors`
   - `GET /lineage/nodes/{node_id}/descendants`
   - `GET /lineage/nodes/{node_id}/promotion-origin`
   - Wired into `create_app(runtime, lineage_graph=None)` (default empty graph).
   - Routes are GET-only (read-only; UI never holds authority).
2. SDK types from OpenAPI: `scripts/export_openapi.py` regenerated
   `packages/sdk_ts/src/openapi-contract.json` (13 paths / 13 operations);
   drift test green.
3. Studio: `StudioService.lineage_projection(graph, node_id)` ? read-only
   projection (ancestors/descendants/promotion-origin) over the shared
   LineageGraph; records an audit entry; never commits.
4. `tests/api/test_lineage_api.py` (2 tests):
   - API queries return correct ancestors/descendants/promotion-origin; unknown
     node -> 404;
   - lineage surface is GET-only (no authority in the UI surface).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/api -q` | 21 passed (incl. lineage + existing API) |
| `uv run pytest tests/architecture/test_false_completion.py tests/integration/test_g17a_sdk_contract.py -q` | drift + contract green |
| `uv run python scripts/export_openapi.py` | 13 paths / 13 operations |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=903 |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| API: ancestor/descendant/promotion-origin | PASS |
| SDK types generated from OpenAPI | PASS (contract regenerated, drift green) |
| Studio shared graph component (read-only) | PASS |
| UI does not hold authority | PASS (GET-only + read-only projection) |
| API contract tests | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: apps/api/src/wanxiang_api/lineage_routes.py,
  tests/api/test_lineage_api.py, reports/G31G_REPORT.md
- modified: apps/api/src/wanxiang_api/app.py,
  apps/api/src/wanxiang_api/studio_service.py,
  packages/sdk_ts/src/openapi-contract.json, reports/sdk_api_baseline.json,
  reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g31g: Lineage API SDK Studio ????`
