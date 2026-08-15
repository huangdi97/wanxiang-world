# Goals G43A-G43G Acceptance Report — Long-Horizon & Derived Worlds (M40)

## Status
PASS (mechanism) — synthetic; real《红楼梦》text EXTERNAL_BLOCKED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/long_horizon/` (new):
   - G43A `windowed_distill` — dedupe/origin/evidence + cost budget.
   - G43B `evaluate_candidates` — multi-window stability + counterfactual +
     approval.
   - G43C `run_living_open` — new orgs/institutions, character stages,
     generated-entity markers.
   - G43D `prepare_promotion_candidate` — freeze + rights/invariant review +
     package candidate.
   - G43E `create_derived_world` — new Definition ID + lineage edge +
     inherited history (only from frozen/invariant-clean candidate).
   - G43F `run_population_benchmark` — 100 actors / 1000 duties aggregate.
2. `tests/unit/substrate/test_long_horizon.py` (6 tests).

## Reuse
- G33 promotion/ladder + G37C long-horizon patterns; no new registry/engine.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_long_horizon.py -q` | 6 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |
| architecture_check.py | PASS |

## Local commit
- `g43: Long-Horizon & Derived Worlds (M40 mechanism)`
