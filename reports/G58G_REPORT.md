# G58G Report — Review APIs (M55)

## Status
**PASS** — Forge review/conflict/completion/evidence API surface (thin
transport over the review core; no Canon promotion through routes).

## Delivered
1. `apps/api/src/wanxiang_api/review_routes.py` (new, prefix /forge):
   - POST /forge/reviews — record ReviewDecision (append-only history)
   - GET /forge/reviews/{target_id} — review history
   - POST /forge/conflicts + GET /forge/conflicts — conflict sets
   - POST /forge/completions/plan — completion plan (keep-unknown)
   - GET /forge/candidates/{candidate_id}/evidence — evidence bindings
2. `apps/api/src/wanxiang_api/app.py` — wired router + app.state ledgers/
   bindings/planner.
3. `tests/api/test_review_api.py` — 4 e2e tests.

## Contract
- OpenAPI regenerated (22 paths / 23 operations); SDK baseline routes 17->23,
  py 1309; drift tests PASS.

## Verification
| Command | Result |
|---|---|
| `pytest tests/api/test_review_api.py -q` | 4 passed |
| API + drift suites (api x5 + false_completion + sdk_contract) | 33 passed |
| ruff / pyright | PASS / 0 errors |
