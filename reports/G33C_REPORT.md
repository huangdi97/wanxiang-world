# Goal G33C Acceptance Report ? Promotion ?????????

## Status
PASS

## Objective
Make promotion decisions auditable/replayable; withdrawal never rewrites source
world history.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/promotion/control.py`:
   - `PromotionRecord` ? append-only promotion decision (record_id, derived
     definition, source worldline, parent definition, status
     active/withdrawn, rationale, created_at).
   - `PromotionControlLedger` ? record / withdraw / status / records;
     withdrawal only changes installability/registry status; the record (and
     source history) is never deleted.
   - Exported via `wanxiang_substrate.evolution.promotion` (SDK baseline +2
     non-breaking).
2. `tests/unit/substrate/test_promotion_control.py` (3 tests):
   - ledger append-only and replayable;
   - withdraw only changes status (record retained; double-withdraw rejected);
   - withdraw derived definition does not affect parent replay (golden hash
     7d17aba7... unchanged).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_promotion_control.py -q` | 3 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=941 (+2 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Promotion record written to control ledger | PASS (append-only, replayable) |
| Cancel/withdraw only affects installability/registry status | PASS |
| Source history never deleted | PASS (record retained; parent replay unchanged) |
| Withdraw derived definition doesn't affect parent replay | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/promotion/control.py,
  tests/unit/substrate/test_promotion_control.py, reports/G33C_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/evolution/promotion/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g33c: Promotion ?????????`
