# Goals G41A-G41H Acceptance Report — Full Living Runtime (M38)

## Status
PASS (mechanism) — synthetic; real《红楼梦》text EXTERNAL_BLOCKED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/living/runtime.py` (new):
   - G41A `instantiate_scenarios` — multi-scenario from fixed Genesis snapshot.
   - G41B `resolve_population` — promotion/demotion under activation budget;
     identity/history preservation.
   - G41C `run_autonomous_loop` — deterministic scheduler loop with
     affected-entity activation + fallback.
   - G41D `build_propagation_graph` — scoped facts + propagation edges +
     correction/forgetting (history never deleted).
   - G41E `evolve_long_term` — trajectory distillation; CapabilityDelta vs
     PersonaDelta separate; relation evolution.
   - G41F `evolve_institutions` — pattern->norm->institution candidate with
     LawCommit gate.
   - G41G/H `run_long_horizon` — 30-day + 1-year accelerated summary with
     checkpoint/crash/recovery + 12-class worldness matrix.
2. `tests/unit/substrate/test_living_runtime.py` (7 tests) covering each.

## Reuse
- G36G strategies; rc001; evolution/cognition machinery patterns; no new
  registry/engine.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_living_runtime.py -q` | 7 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |
| architecture_check.py | PASS |

## Local commit
- `g41: Full Living Runtime (M38 mechanism)`
