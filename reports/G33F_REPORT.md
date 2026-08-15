# Goal G33F Acceptance Report ? Lineage ? Promotion API Studio

## Status
PASS

## Objective
Provide a minimal usage surface for Promote, Derived World, and Lineage Compare:
thin API use cases, Studio candidate/approval/lineage-diff views, permission
control, UI actions through backend authority.

## Delivered
1. `apps/api/src/wanxiang_api/promotion_routes.py`:
   - `GET /lineage/promotion-candidates` (read-only candidate view);
   - `POST /lineage/promotions` (admin-gated promotion use case; 403 without
     permission);
   - `GET /lineage/compare?node_a=..&node_b=..` (lineage diff: common ancestors,
     only-a, only-b).
   - Wired into `create_app` with `studio_admin` + `promotion_candidates` state;
     OpenAPI regenerated (16 routes).
2. `StudioService` ? `promotion_candidates`, `lineage_compare` (read-only), and
   `promote` (admin-gated UI action routed through the backend; never direct
   canonical writes).
3. `tests/api/test_promotion_api.py` (5 tests):
   - unauthorized promote rejected (403);
   - admin promote goes through backend authority (pending_approval);
   - lineage compare endpoint;
   - Studio UI action routes through backend authority (admin required);
   - SDK contract includes the promotion routes.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/api/test_promotion_api.py -q` | 5 passed |
| `uv run python scripts/export_openapi.py` | 16 paths / 16 operations |
| `uv run python scripts/sdk_baseline.py` | routes=16 ts=5 py=947 |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Thin API use cases (Promote / Derived World / Lineage Compare) | PASS |
| Studio candidate/approval/lineage diff | PASS |
| Permission control | PASS (admin-gated promote; 403) |
| Unauthorized promote rejected | PASS (tested) |
| UI action through backend authority | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: apps/api/src/wanxiang_api/promotion_routes.py,
  tests/api/test_promotion_api.py, reports/G33F_REPORT.md
- modified: apps/api/src/wanxiang_api/app.py,
  apps/api/src/wanxiang_api/studio_service.py,
  packages/sdk_ts/src/openapi-contract.json, reports/sdk_api_baseline.json,
  reports/SDK_API_BASELINE.md, PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g33f: Lineage ? Promotion API Studio`
