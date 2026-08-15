# Goal G36C Acceptance Report — 人物职责 NPC 日程身体与社会制度

## Status
PASS (mechanism) — synthetic anonymized NPC profiles; real《红楼梦》text
EXTERNAL_BLOCKED (G35A).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/rc001/npc.py` (new):
   - `NPCProfile` — actor key/role/daily schedule (meal/rest/duty/visit/idle)
     with duty/place refs; `activity_at(tick)`.
   - `daily_schedule()` — deterministic day resolution mapping schedule to
     authority actions: duty -> institution.complete_duty, visit ->
     narrative.visit_sick, meal/rest -> body.rest, idle -> none.
   - `resolve_population()` / `resolve_population_result()` — deterministic
     population resolution (role, key) with capacity overflow reporting.
2. `tests/unit/substrate/test_rc001_npc.py` (5 tests): schedule determinism;
   duty/visit/meal action mappings (institution/narrative/body reuse);
   activity_at; population resolution under capacity; role ordering.

## Reuse
- G02F AutonomousScheduler (deterministic multi-rate); G35F narrative visit;
  institution duty; body rest. NPC policy only composes, never writes.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_rc001_npc.py tests/unit/substrate/test_rc001_spatial_run.py tests/unit/substrate/test_rc001_instantiate.py -q` | 14 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |

## Local commit
- `g36c: 人物职责 NPC 日程身体与社会制度`
