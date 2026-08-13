# Design-to-Implementation Traceability (G13B)

- Source document: `docs/spec/WANXIANG_v5_MASTER_SPEC.md`
- Requirement rows: 44
- Goals mapped (G00A-G12H): 63

Statuses: VERIFIED / PARTIAL / GAP / EXTERNAL_BLOCKED / NOT_APPLICABLE.

## Kernel coverage

| Kernel | Plane | Rows | VERIFIED | PARTIAL | GAP | EXTERNAL_BLOCKED | N/A |
|---|---|---|---|---|---|---|---|
| Canonical State Kernel (5.1) | World Reality | 5 | 5 | 0 | 0 | 0 | 0 |
| Living World Substrate (5.2) | World Reality | 7 | 7 | 0 | 0 | 0 | 0 |
| Physical Context / Reality Bridge (5.3) | World Reality | 2 | 2 | 0 | 0 | 0 | 0 |
| Co-Simulation Fabric (5.4) | World Reality | 1 | 1 | 0 | 0 | 0 | 0 |
| Event / Branch / Temporal Kernel (5.5) | World Reality | 5 | 5 | 0 | 0 | 0 | 0 |
| Perception-Belief-Memory Kernel (6.1) | Agency & Capability | 2 | 2 | 0 | 0 | 0 | 0 |
| Actor / Organization Runtime (6.2) | Agency & Capability | 1 | 1 | 0 | 0 | 0 | 0 |
| Skill-Action-Affordance Kernel (6.3) | Agency & Capability | 2 | 2 | 0 | 0 | 0 | 0 |
| Capability & Learning Kernel (6.4) | Agency & Capability | 1 | 1 | 0 | 0 | 0 | 0 |
| Opportunity-Challenge-Event Kernel (7.1) | Orchestration & Control | 1 | 1 | 0 | 0 | 0 | 0 |
| Embodiment / Director / Experiment Kernel (7.2) | Orchestration & Control | 3 | 3 | 0 | 0 | 0 | 0 |
| World Host / Lifecycle / Multiplayer Kernel (8.1) | Hosting & Experience | 5 | 5 | 0 | 0 | 0 | 0 |
| Projection / Rendering / Network Gateway (8.2) | Hosting & Experience | 3 | 2 | 0 | 0 | 1 | 0 |
| Source / Evidence Kernel (4.1) | World Definition | 4 | 3 | 0 | 0 | 1 | 0 |
| World Compiler & Completion Compiler (4.2) | World Definition | 1 | 1 | 0 | 0 | 0 | 0 |
| Package / Schema / Dependency Registry (4.3) | World Definition | 1 | 1 | 0 | 0 | 0 | 0 |

## Requirement matrix

| ID | Summary | Kernel | Owner | Implementation | Test | Status |
|---|---|---|---|---|---|---|
| WX-ACT-6.2-001 | Actor and organization runtime: propose-only policies, typed lifecycle, bounded agency. | actor_organization | packages/substrate agency | wanxiang_substrate.agency.{model,policy,resolver,query,fixture,components} | tests/integration/test_agency_runtime.py; tests/unit/substrate/test_agency_model.py | VERIFIED |
| WX-AUTH-001 | Only Commit Authority may mutate canonical state; all other actors propose commands/observations. | canonical_state | packages/runtime authority | wanxiang_runtime.authority.CommitAuthority | tests/unit/runtime/test_authority.py; tests/integration/test_m1_acceptance.py | VERIFIED |
| WX-BKP-001 | Backup/restore/migration: backup restores into clean env reproducing canonical hashes; migrations replay. | event_branch_temporal | packages/persistence + migrations | wanxiang_persistence.database/event_store; migrations/versions | tests/integration/test_g12b_backup.py; tests/migration/test_migrations.py | VERIFIED |
| WX-CAP-6.4-001 | Capability & learning: bounded capability, evidence-backed deltas, deterministic clamped policy. | capability_learning | packages/substrate capability | wanxiang_substrate.capability.{model,policy,query,resolver,components} | tests/integration/test_capability_learning.py | VERIFIED |
| WX-CMP-4.2-001 | Structured compiler pipeline is deterministic, provenance-bound, safe readers; PDF/OCR/video unsupported explicitly. | world_compiler | packages/substrate compiler | wanxiang_substrate.compiler.{compiler,readers,validate,yaml_mini,export,fixture} | tests/integration/test_structured_compiler.py; tests/integration/test_package_install.py | VERIFIED |
| WX-COS-5.4-001 | SimulationAdapter contract; adapters propose deltas and never own commit authority; multi-rate orchestrator. | cosimulation | packages/substrate cosim + research | wanxiang_substrate.cosim.{adapter,orchestrator,campaign,errors}; wanxiang_substrate.research.adapters | tests/integration/test_cosim.py; tests/integration/test_g12dfg_adapters.py | VERIFIED |
| WX-DET-001 | Deterministic core tests run without paid external APIs or LLM keys. | canonical_state | repository-wide | no LLM SDK required by core tests; model_providers package empty | full pytest suite (385) runs offline | VERIFIED |
| WX-DOM-001 | Domain generality: unrelated domains (mansion, red chamber, genealogy, heritage, campaign) prove Core generality without Core hacks. | living_world_substrate | packages/substrate domain packs | wanxiang_substrate.{genealogy,heritage,cosim.campaign}; domain fixtures | tests/integration/test_m7_mansion.py; tests/integration/test_genealogy.py; tests/integration/test_heritage.py; tests/integration/test_m8_qualification.py | VERIFIED |
| WX-EMB-7.2-001 | Session/embodiment/lease: one primary embodiment controller per actor; sessions never duplicate actor state. | embodiment_director_experiment | packages/substrate session | wanxiang_substrate.session.{model,control,service} | tests/integration/test_host_session.py; tests/integration/test_m5_g06_proofs.py | VERIFIED |
| WX-EMB-7.2-002 | Shadow/human policy control handoff: advice-only shadow; deterministic controller resumes on release. | embodiment_director_experiment | packages/substrate session | wanxiang_substrate.session.control | tests/integration/test_m5_g06_proofs.py | VERIFIED |
| WX-EMB-7.2-003 | Director runtime: proposals only; experiment runtime with deterministic multi-seed runs, findings, validity envelope. | embodiment_director_experiment | packages/substrate reality | wanxiang_substrate.reality.{director,experiment} | tests/integration/test_challenge_director_experiment.py; tests/integration/test_m6_qualification.py | VERIFIED |
| WX-EVT-5.5-001 | Event history is append-only, ordered, idempotent; duplicate retries never duplicate effects. | event_branch_temporal | packages/domain + packages/persistence | wanxiang_domain.event; wanxiang_persistence.event_store | tests/unit/event_store/test_event_store.py; tests/contract/test_event_store_contract.py | VERIFIED |
| WX-EVT-5.5-002 | Snapshot is an optimization/baseline, never a replacement for event history; replay rebuilds state. | event_branch_temporal | packages/runtime | wanxiang_runtime.{replay,snapshot}; wanxiang_persistence.snapshot_store | tests/unit/runtime/test_replay.py; tests/unit/runtime/test_snapshot.py; tests/unit/runtime/test_golden_replay.py | VERIFIED |
| WX-EVT-5.5-003 | Branch isolation: child branches never mutate parent history; stale revisions rejected with typed conflict. | event_branch_temporal | packages/runtime branch | wanxiang_runtime.branch | tests/unit/runtime/test_branch.py; tests/unit/runtime/test_diff.py | VERIFIED |
| WX-EVT-5.5-004 | Deterministic replay across runs (seeded RNG, stable hashing, golden fixtures). | event_branch_temporal | packages/runtime replay | wanxiang_runtime.replay; wanxiang_domain.hashing | tests/unit/runtime/test_golden_replay.py; tests/property/test_replay_properties.py | VERIFIED |
| WX-HIER-001 | Formal hierarchy Domain Pack -> World Pack -> Scenario -> World Instance -> Branch -> Session -> Projection is distinct and enforced. | canonical_state | packages/domain hierarchy + persistence | wanxiang_domain.hierarchy; wanxiang_persistence.instance_repository; wanxiang_substrate.host | tests/unit/runtime/test_branch.py; tests/integration/test_package_install.py | VERIFIED |
| WX-HST-8.1-001 | World host is an orchestration boundary, not a second Commit Authority; lifecycle modes gate commands. | world_host_lifecycle | packages/substrate host + lifecycle | wanxiang_substrate.host.{host,model}; wanxiang_substrate.lifecycle.* | tests/integration/test_host_session.py; tests/integration/test_lifecycle.py | VERIFIED |
| WX-HST-8.1-002 | Command queue: bounded dedup intake, serialized drain, structured statuses, backpressure; idempotent multi-client semantics. | world_host_lifecycle | packages/substrate queue | wanxiang_substrate.queue.{queue,model} | tests/integration/test_command_queue.py; tests/integration/test_m5_g06_proofs.py | VERIFIED |
| WX-HST-8.1-003 | Crash recovery/checkpoint/resource budgets: committed-events boundary, snapshot/event-replay fallback. | world_host_lifecycle | packages/substrate recovery | wanxiang_substrate.recovery.{recovery,checkpoint,budget} | tests/integration/test_recovery.py; tests/integration/test_m5_g06_proofs.py | VERIFIED |
| WX-LIV-5.2-001 | Spatial substrate: topology, path/capacity/access queries, zones, portals, versioned components. | living_world_substrate | packages/substrate spatial | wanxiang_substrate.spatial.{model,query,resolver,components,fixture} | tests/integration/test_spatial_movement.py; tests/unit/substrate/test_spatial_model.py | VERIFIED |
| WX-LIV-5.2-002 | Temporal substrate: monotonic world clock, calendars, appointments/deadlines/recurring events, bounded deterministic recurrence. | living_world_substrate | packages/substrate temporal | wanxiang_substrate.temporal.{model,query,resolver,components,fixture} | tests/integration/test_temporal_advance.py; tests/unit/substrate/test_temporal_model.py | VERIFIED |
| WX-LIV-5.2-003 | Material substrate: objects, containers, custody chain, information payloads with container constraints. | living_world_substrate | packages/substrate material | wanxiang_substrate.material.* | tests/integration/test_material_custody.py; tests/property/test_material_properties.py | VERIFIED |
| WX-LIV-5.2-004 | Body substrate: condition constraints, health/exhaustion, viability checks. | living_world_substrate | packages/substrate body | wanxiang_substrate.body.{model,query,resolver,components,fixture} | tests/integration/test_body_condition.py; tests/property/test_body_properties.py | VERIFIED |
| WX-LIV-5.2-005 | Institution substrate: authority, duty, norms, role hierarchy. | living_world_substrate | packages/substrate institution | wanxiang_substrate.institution.{model,query,resolver,components,fixture} | tests/integration/test_institution_authority.py; tests/property/test_institution_properties.py | VERIFIED |
| WX-LIV-5.2-006 | Population resolution and deterministic autonomous scheduler with bounded budgets. | living_world_substrate | packages/substrate population | wanxiang_substrate.population.{model,resolver,scheduler} | tests/integration/test_autonomous_scheduler.py; tests/integration/test_g12a_stability.py | VERIFIED |
| WX-OCE-7.1-001 | Opportunity/challenge/event compiler: executable specs with prerequisites, safety, rights, evidence, outcomes. | opportunity_challenge_event | packages/substrate reality | wanxiang_substrate.reality.challenge | tests/integration/test_challenge_director_experiment.py | VERIFIED |
| WX-PER-6.1-001 | Observation and perspective isolation: derived read-models with rule_refs audit; sealed payloads never in observations. | perception_belief_memory | packages/substrate observation + epistemic | wanxiang_substrate.observation.*; wanxiang_substrate.epistemic.* | tests/integration/test_observation_perspective.py; tests/unit/substrate/test_observation_model.py | VERIFIED |
| WX-PER-6.1-002 | Belief/memory temporal epistemic graph: versioned components, corrections link without silent overwrite, actor-scoped access. | perception_belief_memory | packages/substrate epistemic | wanxiang_substrate.epistemic.{model,components,query,resolver,fixture} | tests/integration/test_epistemic_belief.py; tests/unit/substrate/test_epistemic_model.py | VERIFIED |
| WX-PKG-4.3-001 | Package registry: portable manifests, deterministic resolution, content hashes, default-deny executable trust. | package_registry | packages/substrate packages | wanxiang_substrate.packages.* | tests/integration/test_package_registry.py; tests/integration/test_package_install.py | VERIFIED |
| WX-PRJ-8.2-001 | Projection API/perspective/rights filters: server-composed DTOs with rights/knowledge filters; projection state discardable. | projection_rendering_network | packages/substrate projection + apps/api | wanxiang_substrate.projection.{service,model}; apps/api routes | tests/integration/test_projection_filters.py; tests/api/test_api.py | VERIFIED |
| WX-PRJ-8.2-002 | Network gateway/transport: FastAPI thin transport with structured errors and OpenAPI; typed TS SDK over stable document. | projection_rendering_network | apps/api + packages/sdk_ts | apps/api/src/wanxiang_api; packages/sdk_ts/src | tests/api/test_api.py; packages/sdk_ts vitest (21) | VERIFIED |
| WX-PRJ-8.2-003 | Renderers (Phaser/Godot/Babylon) and digital-human/XR presence are non-authoritative clients; contracts exist, renderers EXTERNAL_BLOCKED. | projection_rendering_network | packages/sdk_ts + packages/substrate gateway | packages/sdk_ts/src/{phaser,projection3d}.ts; wanxiang_substrate.gateway.gateway | packages/sdk_ts phaser/projection3d tests; tests/integration/test_g12dfg_adapters.py | EXTERNAL_BLOCKED |
| WX-RB-5.3-001 | Reality bridge normalizes physical observations onto a bus; observations are claims/proposals, never canonical truth. | reality_bridge | packages/substrate reality + observation | wanxiang_substrate.reality.{bridge,fusion,model}; wanxiang_substrate.observation.* | tests/integration/test_reality_bridge.py; tests/integration/test_observation_perspective.py | VERIFIED |
| WX-RB-5.3-002 | Observation fusion: dedup, conflict sets, validation, versioned policy; no silent truth mutation. | reality_bridge | packages/substrate reality | wanxiang_substrate.reality.fusion | tests/integration/test_reality_bridge.py | VERIFIED |
| WX-RGT-001 | Rights and privacy are server-enforced end-to-end: rights gate, projection filters, gateway asset/voice/face rights. | source_evidence | packages/domain rights + projection + gateway | wanxiang_domain.rights; wanxiang_substrate.projection.service; wanxiang_substrate.gateway.gateway | tests/integration/test_projection_filters.py; tests/integration/test_g12h_security.py; tests/integration/test_g12dfg_adapters.py | VERIFIED |
| WX-SEC-001 | Security: secrets redaction, upload/source injection rejection, admin/debug access control, append-only audit. | world_host_lifecycle | packages/observability + apps/api | wanxiang_observability.{secrets,config,logging}; apps/api errors/routes | tests/integration/test_g12h_security.py; tests/unit/test_config_redaction.py | VERIFIED |
| WX-SKL-6.3-001 | Action/affordance/validator: versioned action registry, side-effect-free validator. | skill_action_affordance | packages/substrate actions | wanxiang_substrate.actions.{model,registry,validator,affordance} | tests/integration/test_actions_affordance.py; tests/unit/substrate/test_actions_validator.py | VERIFIED |
| WX-SKL-6.3-002 | Skill runtime: versioned skill registry, deterministic execution state as versioned component. | skill_action_affordance | packages/substrate skills | wanxiang_substrate.skills.{registry,runtime,resolver,model,components} | tests/integration/test_skill_runtime.py | VERIFIED |
| WX-SRC-4.1-001 | Sources are immutable, reviewed (E0..E5), rights-gated; model memory is not a source. | source_evidence | packages/substrate sources+ledger | wanxiang_substrate.sources.{gate,registry,model,policy}; wanxiang_substrate.ledger | tests/integration/test_source_gate.py; tests/integration/test_completion_ledger.py | VERIFIED |
| WX-SRC-4.1-002 | Completion ledger promotes truth labels through review with immutable decisions and rights gate. | source_evidence | packages/substrate ledger | wanxiang_substrate.ledger.{model,fixture,resolver} | tests/integration/test_completion_ledger.py | VERIFIED |
| WX-SRC-EXTERNAL-001 | Real Red Chamber/Liaoshen/family/heritage source data, real IIIF endpoints, real renderers: source/rights gated. | source_evidence | EXTERNAL | generic contracts + synthetic fixtures + source-gate tests only | tests/integration/test_source_gate.py; tests/integration/test_m7_mansion.py | EXTERNAL_BLOCKED |
| WX-ST-5.1-001 | Canonical World State is event-sourced, versioned, hash-bound and writable only through Commit Authority. | canonical_state | packages/domain + packages/runtime | wanxiang_domain.{state,entity,event,command,delta,hashing}; wanxiang_runtime.{authority,state,invariants} | tests/unit/runtime/test_authority.py; tests/unit/runtime/test_state.py; tests/integration/test_m1_acceptance.py | VERIFIED |
| WX-STB-001 | Long-run stability: 30 in-world days + 1000+ commit/scheduler cycles with bounded growth. | world_host_lifecycle | packages/substrate population/host | wanxiang_substrate.population.scheduler; wanxiang_substrate.host.host | tests/integration/test_g12a_stability.py | VERIFIED |
| WX-WOR-001 | Worldness criteria: persistence, spatiotemporal/material/body/social/cognitive/causal continuity, replay, projection independence. | canonical_state | repository-wide | all substrate planes + runtime | tests/integration/test_m2_qualification.py; tests/integration/test_m5_g06_proofs.py; tests/integration/test_m7_qualification.py | VERIFIED |

## Goal-to-requirement mapping (G00A-G12H)

| Goal | Requirement IDs |
|---|---|
| G00A | WX-HIER-001, WX-DET-001 |
| G00B | WX-AUTH-001, WX-DET-001, WX-SEC-001 |
| G01A | WX-ST-5.1-001, WX-HIER-001 |
| G01B | WX-AUTH-001, WX-ST-5.1-001 |
| G01C | WX-EVT-5.5-001, WX-EVT-5.5-002 |
| G01D | WX-EVT-5.5-002, WX-EVT-5.5-003, WX-EVT-5.5-004 |
| G01E | WX-BKP-001, WX-EVT-5.5-001 |
| G01F | WX-PRJ-8.2-001, WX-PRJ-8.2-002, WX-WOR-001 |
| G02A | WX-LIV-5.2-001 |
| G02B | WX-LIV-5.2-002 |
| G02C | WX-LIV-5.2-003 |
| G02D | WX-LIV-5.2-004 |
| G02E | WX-LIV-5.2-005 |
| G02F | WX-LIV-5.2-006 |
| G03A | WX-PER-6.1-001 |
| G03B | WX-PER-6.1-002 |
| G03C | WX-ACT-6.2-001 |
| G03D | WX-SKL-6.3-001 |
| G03E | WX-ST-5.1-001, WX-EVT-5.5-004 |
| G03F | WX-SKL-6.3-002 |
| G03G | WX-CAP-6.4-001 |
| G04A | WX-PKG-4.3-001 |
| G04B | WX-SRC-4.1-001 |
| G04C | WX-CMP-4.2-001 |
| G04D | WX-SRC-4.1-002 |
| G04E | WX-PKG-4.3-001, WX-BKP-001 |
| G05A | WX-HST-8.1-001 |
| G05B | WX-EMB-7.2-001 |
| G05C | WX-EMB-7.2-002 |
| G05D | WX-PRJ-8.2-001, WX-RGT-001 |
| G05E | WX-PRJ-8.2-002 |
| G05F | WX-PRJ-8.2-003 |
| G06A | WX-HST-8.1-001 |
| G06B | WX-HST-8.1-002 |
| G06C | WX-HST-8.1-003 |
| G07A | WX-RB-5.3-001 |
| G07B | WX-RB-5.3-002 |
| G07C | WX-OCE-7.1-001 |
| G07D | WX-EMB-7.2-003 |
| G07E | WX-EMB-7.2-003 |
| G08A | WX-DOM-001 |
| G08B | WX-SRC-EXTERNAL-001 |
| G09A | WX-DOM-001 |
| G09B | WX-DOM-001, WX-RGT-001 |
| G09C | WX-RGT-001 |
| G10A | WX-DOM-001, WX-SRC-EXTERNAL-001 |
| G10B | WX-DOM-001 |
| G10C | WX-DOM-001 |
| G10D | WX-DOM-001 |
| G11A | WX-COS-5.4-001 |
| G11B | WX-COS-5.4-001 |
| G11C | WX-DOM-001 |
| G11D | WX-DOM-001 |
| G11E | WX-EMB-7.2-003 |
| G11F | WX-SRC-EXTERNAL-001 |
| G12A | WX-STB-001 |
| G12B | WX-BKP-001 |
| G12C | WX-PRJ-8.2-002 |
| G12D | WX-COS-5.4-001 |
| G12E | WX-PRJ-8.2-003 |
| G12F | WX-PRJ-8.2-003, WX-RGT-001 |
| G12G | WX-PRJ-8.2-003, WX-RGT-001 |
| G12H | WX-SEC-001, WX-RGT-001 |

Machine-readable copy: `reports/design_implementation_traceability.json`.
