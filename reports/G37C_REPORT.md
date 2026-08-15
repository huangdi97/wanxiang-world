# Goal G37C Acceptance Report — 红楼梦长时演化与 Promotion Candidate

## Status
PASS (mechanism) — synthetic; real《红楼梦》text EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rc001/promotion.py` (new):
   - `accelerate()` — controlled time-acceleration (bounded steps).
   - `distill_stable()` — stable structure distillation (G33B pipeline).
   - `promote_long_horizon()` — promotion candidate validated via G33A ladder;
     Derived World Definition created ONLY when the policy gate is reached;
     lineage edge recorded; parent never mutated.
2. `tests/unit/substrate/test_rc001_promotion.py` (5 tests): acceleration
   bounds; stable distillation; gate not reached -> no derived world; gate
   reached -> derived world + lineage; insufficient evidence rejected.

## Reuse
- G33B WorldlinePromotionPipeline; G33A validate_promotion; LineageGraph.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_promotion.py -q` | 5 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g37c: 红楼梦长时演化与 Promotion Candidate`
