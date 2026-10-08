# G58C Report — Rights Gate (M55)

## Status
**PASS** — Scope-aware rights checks for model/display/export/package inclusion.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rights/gate.py` (new):
   - `RightsGate.decide/require` — per-scope decisions reusing SourceRecord
     RightsEnvelope; package inclusion requires usage granting "package";
     `RightsDenied` typed failure.

## Verification
| Command | Result |
|---|---|
| `pytest tests/unit/substrate/test_review_completion_core.py -q` | 9 passed |
| ruff / pyright | PASS / 0 errors |
