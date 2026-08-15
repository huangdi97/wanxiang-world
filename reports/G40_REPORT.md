# Goals G40A-G40H Acceptance Report — Full Semantic World (M37)

## Status
PASS (mechanism) — synthetic; real《红楼梦》text EXTERNAL_BLOCKED.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/semantic_world/` (new):
   - G40A: full World Definition composition (manifest/deps/constitution/
     genesis/evolution/source/rights via WorldPackAssembler).
   - G40B `HouseholdSociety` — duty/norm/permission/reputation.
   - G40C `HistoricalChinaRules` — time/identity/transport/life rules;
     secret/scene/arc propose-only.
   - G40D `CharacterPackage` — identity/life-arc/goals/relations/knowledge/
     capabilities/evidence; persona vs state separated.
   - G40E `SpatialWorld` — rooms/portals/routes/visibility/acoustic/access.
   - G40F material bindings (item/kind/custodian).
   - G40G schedules + body/social/completion composition.
   - G40H `multi_scenario_dry_run` + `scan_core_proper_nouns`.
2. `tests/unit/substrate/test_semantic_world.py` (7 tests): full definition
   refs; persona-vs-state; reputation/rules; propose-only history; spatial +
   material bindings; multi-scenario dry-run; Core proper-noun scan empty.

## Reuse
- G35I WorldPackAssembler; G36 canon/narrative/rc001 mechanisms; no new
  registry/engine.

## Verification
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_semantic_world.py -q` | 7 passed |
| ruff / format / pyright | PASS / PASS / 0 errors |
| architecture_check.py | PASS |

## Local commit
- `g40: Full Semantic World (M37 mechanism)`
