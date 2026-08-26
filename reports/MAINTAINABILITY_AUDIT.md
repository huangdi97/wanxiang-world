# Maintainability Audit (G13G)

- Production files: 502; total lines: 53287; functions: 2630
- Mean max-function complexity: 4.6
- Files over 300 lines: 0
- High-complexity hotspots (>=15): 19
- Long-function hotspots (>=120 lines): 8
- Import cycles: 0
- Public `Any`-typed parameters: 30
- Exception swallows (except: pass): 0

## Files over the 300-line threshold

None (architecture guard enforces the target; exceptions must be documented).

## High-complexity hotspots

- `packages/substrate/src/wanxiang_substrate/genealogy/gedcom.py` max_complexity=47 functions=4
- `packages/substrate/src/wanxiang_substrate/distill/passes_relations.py` max_complexity=23 functions=1
- `packages/substrate/src/wanxiang_substrate/sources/book.py` max_complexity=21 functions=12
- `packages/substrate/src/wanxiang_substrate/spatial/resolver.py` max_complexity=21 functions=5
- `packages/substrate/src/wanxiang_substrate/authoring/worldness_scoring.py` max_complexity=20 functions=2
- `packages/substrate/src/wanxiang_substrate/authoring/local_semantic_gedcom.py` max_complexity=19 functions=2
- `packages/substrate/src/wanxiang_substrate/heritage/iiif.py` max_complexity=19 functions=6
- `packages/substrate/src/wanxiang_substrate/material/query.py` max_complexity=19 functions=14
- `packages/substrate/src/wanxiang_substrate/playable/state_diff.py` max_complexity=19 functions=11
- `packages/substrate/src/wanxiang_substrate/distill/passes_events.py` max_complexity=18 functions=1
- `packages/substrate/src/wanxiang_substrate/domains/recommender.py` max_complexity=18 functions=4
- `packages/substrate/src/wanxiang_substrate/authoring/completion_engine.py` max_complexity=17 functions=6
- `packages/substrate/src/wanxiang_substrate/distill/passes_identity.py` max_complexity=17 functions=1
- `packages/substrate/src/wanxiang_substrate/parsing/parser.py` max_complexity=17 functions=8
- `packages/substrate/src/wanxiang_substrate/genealogy/gedcom_serialization.py` max_complexity=16 functions=2
- `packages/substrate/src/wanxiang_substrate/institution/query.py` max_complexity=16 functions=15
- `packages/substrate/src/wanxiang_substrate/actor_continuity/goal_model.py` max_complexity=15 functions=11
- `packages/substrate/src/wanxiang_substrate/distill/passes_knowledge.py` max_complexity=15 functions=2
- `packages/substrate/src/wanxiang_substrate/sources/security.py` max_complexity=15 functions=7

## Long-function hotspots

- `packages/substrate/src/wanxiang_substrate/distill/passes_events.py` max_func_len=202
- `packages/substrate/src/wanxiang_substrate/authoring/semantic.py` max_func_len=184
- `packages/substrate/src/wanxiang_substrate/authoring/local_semantic_gedcom.py` max_func_len=182
- `packages/substrate/src/wanxiang_substrate/distill/passes_relations.py` max_func_len=174
- `packages/substrate/src/wanxiang_substrate/distill/passes_identity.py` max_func_len=143
- `packages/substrate/src/wanxiang_substrate/authoring/worldness_scoring.py` max_func_len=138
- `packages/substrate/src/wanxiang_substrate/authoring/draft_builder.py` max_func_len=122
- `packages/substrate/src/wanxiang_substrate/genealogy/gedcom.py` max_func_len=120

## Typing / exception-swallowing signals

- Any param: `apps/api/src/wanxiang_api/experience_player_service.py:43:act`
- Any param: `apps/api/src/wanxiang_api/learn_service.py:39:_apply`
- Any param: `apps/api/src/wanxiang_api/operator_console_service.py:33:source_review_status`
- Any param: `apps/api/src/wanxiang_api/strategy_workbench_service.py:21:__init__`
- Any param: `packages/application/src/wanxiang_application/snapshot_policy.py:19:snapshot_is_valid`
- Any param: `packages/domain/src/wanxiang_domain/serialization.py:42:expect_version`
- Any param: `packages/domain/src/wanxiang_domain/serialization.py:70:_decode_components`
- Any param: `packages/domain/src/wanxiang_domain/serialization.py:123:delta_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization.py:178:command_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization_history.py:71:event_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization_history.py:113:snapshot_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization_history.py:139:run_from_primitive`
- Any param: `packages/domain/src/wanxiang_domain/serialization_history.py:162:ancestry_from_primitive`
- Any param: `packages/persistence/src/wanxiang_persistence/database.py:20:_enable_sqlite_foreign_keys`
- Any param: `packages/research/src/wanxiang_research/planner.py:26:propose`
- Any param: `packages/research/src/wanxiang_research/planner.py:36:propose`
- Any param: `packages/research/src/wanxiang_research/planner.py:51:propose`
- Any param: `packages/research/src/wanxiang_research/planner.py:63:rollout`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_living.py:19:instantiate_living`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_living.py:33:living`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_living.py:36:evaluate_worldness`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_living.py:53:worldness`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_package.py:23:build_package`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_package.py:57:package_validation`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_package.py:61:publish`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_package.py:78:preview`
- Any param: `packages/substrate/src/wanxiang_substrate/authoring/service_status.py:11:status`
- Any param: `packages/substrate/src/wanxiang_substrate/kernel/abi.py:77:verify_abi_golden`
- Any param: `packages/substrate/src/wanxiang_substrate/playable/factory.py:10:profile_from_world_package`
- Any param: `packages/substrate/src/wanxiang_substrate/sources/structured.py:126:_canonical`
- No `except: pass` swallowing in production.

## Import cycles

None.

Hotspots are candidates for G13H/G13I closure tasks with owner and rationale;
no 'rewrite later' hotspot is left untracked.
