# False-Completion Audit (G13D/G29F)

- Production placeholder findings: 0
- Dead production modules (never imported): 0
- Hardcoded-state candidates: 54
- Empty-body (pass-only) findings: 0
- Static-success candidates: 9

## Production placeholders

None (architecture guard enforces this; scanner re-checks independently).

## Dead production modules

None.

## Hardcoded-state candidates

- `apps/api/src/wanxiang_api/authoring_routes.py:120` large-dict-literal (15 keys)
- `apps/api/src/wanxiang_api/authoring_routes.py:216` large-dict-literal (8 keys)
- `apps/api/src/wanxiang_api/authoring_routes.py:266` large-dict-literal (8 keys)
- `apps/api/src/wanxiang_api/candidate_serializers.py:9` large-dict-literal (10 keys)
- `apps/api/src/wanxiang_api/one_click_routes.py:36` large-dict-literal (9 keys)
- `packages/domain/src/wanxiang_domain/constitution.py:78` large-dict-literal (10 keys)
- `packages/domain/src/wanxiang_domain/constitution.py:112` large-dict-literal (11 keys)
- `packages/domain/src/wanxiang_domain/lineage.py:42` large-dict-literal (10 keys)
- `packages/domain/src/wanxiang_domain/serialization.py:163` large-dict-literal (11 keys)
- `packages/domain/src/wanxiang_domain/serialization_history.py:50` large-dict-literal (15 keys)
- `packages/domain/src/wanxiang_domain/serialization_history.py:100` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/goal_model.py:108` large-dict-literal (11 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/goal_model.py:224` large-dict-literal (10 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/projection.py:60` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/qualification_model.py:148` large-dict-literal (10 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/qualification_model.py:163` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/qualification_model.py:188` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/qualification_model.py:120` large-dict-literal (13 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/relationship_model.py:43` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/actor_continuity/reprioritization_model.py:94` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/draft_builder.py:143` large-dict-literal (11 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/living_world.py:35` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/living_world.py:62` large-dict-literal (11 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/living_world.py:89` large-dict-literal (11 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/local_semantic_provider.py:52` large-dict-literal (10 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/model.py:72` large-dict-literal (18 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/orchestration_dag.py:17` large-dict-literal (10 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/semantic_distillation.py:32` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/worldness_policy.py:68` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/worldness_scoring.py:162` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/worldness_support.py:160` large-dict-literal (10 keys)
- `packages/substrate/src/wanxiang_substrate/authoring/worldness_support.py:119` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/candidates/envelope.py:126` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/canon_graph/timeline_canon.py:129` large-dict-literal (11 keys)
- `packages/substrate/src/wanxiang_substrate/distill/gedcom.py:29` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/draft/model.py:40` large-dict-literal (10 keys)
- `packages/substrate/src/wanxiang_substrate/epistemic/components.py:36` large-dict-literal (12 keys)
- `packages/substrate/src/wanxiang_substrate/epistemic/components.py:69` large-dict-literal (10 keys)
- `packages/substrate/src/wanxiang_substrate/evolution/policy_stack.py:57` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/genealogy/gedcom_support.py:97` large-dict-literal (16 keys)
- `packages/substrate/src/wanxiang_substrate/packages/install.py:160` large-dict-literal (11 keys)
- `packages/substrate/src/wanxiang_substrate/packages/model.py:162` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/playable/action_model.py:63` large-dict-literal (11 keys)
- `packages/substrate/src/wanxiang_substrate/playable/experience.py:137` large-dict-literal (16 keys)
- `packages/substrate/src/wanxiang_substrate/playable/models.py:235` large-dict-literal (12 keys)
- `packages/substrate/src/wanxiang_substrate/sources/asset.py:41` large-dict-literal (14 keys)
- `packages/substrate/src/wanxiang_substrate/sources/model.py:174` large-dict-literal (13 keys)
- `packages/substrate/src/wanxiang_substrate/temporal/components.py:42` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/workshop/models.py:121` large-dict-literal (18 keys)
- `packages/substrate/src/wanxiang_substrate/workshop/publishing.py:68` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/workshop/publishing.py:106` large-dict-literal (8 keys)
- `packages/substrate/src/wanxiang_substrate/workshop/publishing.py:159` large-dict-literal (9 keys)
- `packages/substrate/src/wanxiang_substrate/workshop/registry.py:61` large-dict-literal (14 keys)
- `packages/substrate/src/wanxiang_substrate/workshop/service.py:217` large-dict-literal (8 keys)

## Empty-body (pass-only) findings

None. Exception markers and the SQLAlchemy declarative base are documented allowlist.

## Static-success candidates

- `packages/application/src/wanxiang_application/environment.py:84` def close (documented no-op / unsupported branch)
- `packages/research/src/wanxiang_research/digital_human.py:78` def interrupt (documented no-op / unsupported branch)
- `packages/substrate/src/wanxiang_substrate/epistemic/belief_revision.py:61` def is_world_truth (documented no-op / unsupported branch)
- `packages/substrate/src/wanxiang_substrate/epistemic/model.py:121` def is_world_truth (documented no-op / unsupported branch)
- `packages/substrate/src/wanxiang_substrate/evolution/policy_stack.py:69` def assert_world_cannot_mutate_platform (documented no-op / unsupported branch)
- `packages/substrate/src/wanxiang_substrate/sources/adapter.py:109` def resume (documented no-op / unsupported branch)
- `packages/substrate/src/wanxiang_substrate/sources/asset.py:141` def resume (documented no-op / unsupported branch)
- `packages/substrate/src/wanxiang_substrate/sources/book.py:275` def resume (documented no-op / unsupported branch)
- `packages/substrate/src/wanxiang_substrate/sources/structured.py:81` def resume (documented no-op / unsupported branch)

## Classification

- Test Fakes implement formal Port contracts and are namespaced under tests/;
  they are never selected by production default configuration.
- Any finding above not on the documented allowlist is a P0/P1 gap candidate.
