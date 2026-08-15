# Goal G36H Acceptance Report — 红楼梦 Experience Studio 最小可用面

## Status
PASS (mechanism) — read-only Studio surface over synthetic RC-001; real
《红楼梦》text EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rc001/experience.py` (new):
   - `ExperienceStudio` — read-only Studio queries: map (places/portals),
     characters, available actions, committed events, source canon (runtime
     view only), completion pending, branch baseline comparison.
   - `ExperienceViews` — aggregated frozen snapshot of the views.
2. `tests/unit/substrate/test_rc001_experience.py` (3 tests): map/characters/
   actions views; source + completion + events views; branch compare
   (match + divergence).

## Reuse
- SpatialQuery, ActionRegistry, G35E CompiledCanon runtime view, G35H
  CompletionStudio, G36G compare_to_baseline. No write path.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_experience.py ... (all rc001 tests) -q` | 34 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g36h: 红楼梦 Experience Studio 最小可用面`
