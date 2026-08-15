# Goal G33B Acceptance Report ? Worldline ? Derived World Promotion Pipeline

## Status
PASS

## Objective
Safely freeze/distill a mature worldline into a new World Definition (derived
world) without mutating the parent definition or source worldline.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/promotion/pipeline.py`:
   - `GenesisSnapshot` ? frozen distilled content (genesis_ref, facts, hash).
   - `PromotionReview` ? Source/Rights/Invariant review with approval hook
     (reviewer/policy only).
   - `WorldlinePromotionPipeline` ? distill -> review -> assemble (Package
     Assembler compiles a new WorldDefinition with a NEW definition id) ->
     record_lineage (promotion edge; parent definition -> worldline fork edge;
     parent never modified).
   - Exported via `wanxiang_substrate.evolution.promotion` (SDK baseline +3
     non-breaking).
2. `tests/unit/substrate/test_promotion_pipeline.py` (4 tests):
   - promotion does not mutate parent definition or worldline (parent hash
     unchanged; new derived id/hash);
   - unapproved promotion rejected (no new definition);
   - derived world is re-instantiable (complete versioned birth definition with
     constitution + genesis refs);
   - lineage edge recorded without touching parent (ancestors correct).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_promotion_pipeline.py -q` | 4 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=938 (+3 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Long-horizon distill | PASS (GenesisSnapshot freeze) |
| Source/Rights/Invariant review | PASS (PromotionReview) |
| Freeze Genesis snapshot | PASS |
| Package Assembler compiles candidate | PASS (new WorldDefinition id) |
| Approval -> new Definition ID + lineage edge | PASS (record_lineage) |
| Parent definition/source worldline hash unchanged | PASS (tested) |
| Derived world re-instantiable | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/promotion/pipeline.py,
  tests/unit/substrate/test_promotion_pipeline.py, reports/G33B_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/evolution/promotion/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g33b: Worldline ? Derived World Promotion Pipeline`
