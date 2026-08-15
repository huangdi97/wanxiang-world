# Goal G36B Acceptance Report — 红楼梦空间可见可听私密运行

## Status
PASS (mechanism) — synthetic anonymized RC-001 map; real《红楼梦》text
EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/spatial/movement.py` (new):
   - `MovementProfile` — travel-cost policy (base ticks per portal + per-portal
     surcharges); `travel_time(path)` deterministic.
   - Reuses existing SpatialQuery path/visibility/acoustic/access.
2. `tests/unit/substrate/test_rc001_spatial_run.py` (5 tests): visibility and
   acoustic zones on an RC-001 synthetic map; private place requires grant;
   locked portal blocks reachability; movement time over paths (default and
   profiled); position continuity.

## Reuse
- G02A spatial model/query (PlaceTopology/PortalLink/VisibilityZone/
  AcousticZone/path/can_enter); only movement time is new.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_spatial_run.py -q` | 5 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g36b: 红楼梦空间可见可听私密运行`
