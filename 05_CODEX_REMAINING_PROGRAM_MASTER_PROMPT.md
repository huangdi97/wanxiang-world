# Codex Remaining Program Master Prompt — Wanxiang M2 → M9

> Continuation controller after M1 Authoritative World PASS.  
> Scope: all remaining engineering phases P2–P9 defined by `Wanxiang Engineering Program Architecture`.  
> Execution mode: continuous, checkpointed, milestone-gated, no routine user confirmation.  
> Final stop: M9 qualification report completed, or a genuinely unrecoverable repository/environment blocker prevents all further independent work.

## 0. Mission

Continue formal implementation of **Wanxiang Semantic Persistent Living World OS** from the already completed M0/M1 foundation and execute the remaining engineering program through **M9 Release-qualified Wanxiang Platform Foundation**.

This is not a request to create surface-level modules, static demo screens or placeholder adapters. Each Goal is an executable engineering contract. Each milestone must prove an integrated vertical capability before the program advances.

Do not redesign the product. Product semantics and architecture come from `docs/spec/WANXIANG_v5_MASTER_SPEC.md`.

## 1. First action: verify the actual M1 checkpoint

The user states the previous batch is complete. Do not blindly trust conversational state. Read the repository evidence:

- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`
- `reports/ACCEPTANCE_MATRIX.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `STATUS.md`
- recent Git history
- M1 core tests

Run the narrow M1 qualification/regression suite. If M1 has regressed, fix the regression before G02A. Do not redo M0/M1 from scratch when they are healthy.

## 2. Normative reading order

Before changing production code, read:

1. `docs/spec/WANXIANG_v5_MASTER_SPEC.md`
2. `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md`
3. `02_ENGINEERING_STANDARDS.md`
4. `03_ACCEPTANCE_TESTING_AND_EVIDENCE.md`
5. `05_CODEX_REMAINING_PROGRAM_MASTER_PROMPT.md`
6. `06_REMAINING_GOALS_INDEX.md`
7. `07_MILESTONE_GATES_M2_M9.md`
8. `08_CONTINUOUS_EXECUTION_AND_RESUME_PROTOCOL.md`
9. `09_RELEASE_AND_QUALITY_CONSTITUTION_ADDENDUM.md`
10. `AGENTS.md` and relevant repository docs
11. `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
12. current source tree, tests, migrations, OpenAPI/SDK generation and Git state
13. the current Goal file before implementing that Goal

Authority order:
1. master product specification;
2. Engineering Program Architecture;
3. Engineering/Acceptance standards;
4. current Goal contract and milestone gate;
5. ADRs/implementation docs;
6. code.

Code is evidence, not permission to silently change the specification.

## 3. Continuous execution order

Execute exactly this Goal order unless a Goal document explicitly says an internal subtask may be parallelized:

1. `G02A` — Spatial Topology & Access — `goals/GOAL_G02A_SPATIAL_TOPOLOGY_ACCESS.md`
2. `G02B` — Temporal System & Schedules — `goals/GOAL_G02B_TEMPORAL_SYSTEM_SCHEDULES.md`
3. `G02C` — Material, Container, Custody & Information Payload — `goals/GOAL_G02C_MATERIAL_CONTAINER_CUSTODY_INFORMATION_PAYLOAD.md`
4. `G02D` — Body & Condition Constraints — `goals/GOAL_G02D_BODY_CONDITION_CONSTRAINTS.md`
5. `G02E` — Institution, Authority, Duty & Norm — `goals/GOAL_G02E_INSTITUTION_AUTHORITY_DUTY_NORM.md`
6. `G02F` — Population Resolution & Autonomous Scheduler — `goals/GOAL_G02F_POPULATION_RESOLUTION_AUTONOMOUS_SCHEDULER.md`
7. `G03A` — Observation & Perspective Isolation — `goals/GOAL_G03A_OBSERVATION_PERSPECTIVE_ISOLATION.md`
8. `G03B` — Belief, Memory & Temporal Epistemic Graph — `goals/GOAL_G03B_BELIEF_MEMORY_TEMPORAL_EPISTEMIC_GRAPH.md`
9. `G03C` — Actor & Organization Runtime — `goals/GOAL_G03C_ACTOR_ORGANIZATION_RUNTIME.md`
10. `G03D` — Action, Affordance & Validator — `goals/GOAL_G03D_ACTION_AFFORDANCE_VALIDATOR.md`
11. `G03E` — Resolver, Adjudication & Deterministic Policies — `goals/GOAL_G03E_RESOLVER_ADJUDICATION_DETERMINISTIC_POLICIES.md`
12. `G03F` — Skill Runtime — `goals/GOAL_G03F_SKILL_RUNTIME.md`
13. `G03G` — Capability & Learning — `goals/GOAL_G03G_CAPABILITY_LEARNING.md`
14. `G04A` — Package, Schema & Dependency Registry — `goals/GOAL_G04A_PACKAGE_SCHEMA_DEPENDENCY_REGISTRY.md`
15. `G04B` — Source Registry & Source Gate — `goals/GOAL_G04B_SOURCE_REGISTRY_SOURCE_GATE.md`
16. `G04C` — Structured Compiler MVP — `goals/GOAL_G04C_STRUCTURED_COMPILER_MVP.md`
17. `G04D` — Completion Ledger & Review Workflow — `goals/GOAL_G04D_COMPLETION_LEDGER_REVIEW_WORKFLOW.md`
18. `G04E` — Package Install, Export & Migration Compatibility — `goals/GOAL_G04E_PACKAGE_INSTALL_EXPORT_MIGRATION_COMPATIBILITY.md`
19. `G05A` — Minimal World Host Authority Boundary — `goals/GOAL_G05A_MINIMAL_WORLD_HOST_AUTHORITY_BOUNDARY.md`
20. `G05B` — Session & Embodiment Lease — `goals/GOAL_G05B_SESSION_EMBODIMENT_LEASE.md`
21. `G05C` — Shadow/Human Policy & Control Handoff — `goals/GOAL_G05C_SHADOW_HUMAN_POLICY_CONTROL_HANDOFF.md`
22. `G05D` — Projection API & Perspective/Rights Filters — `goals/GOAL_G05D_PROJECTION_API_PERSPECTIVE_RIGHTS_FILTERS.md`
23. `G05E` — Studio Debug Vertical Slice — `goals/GOAL_G05E_STUDIO_DEBUG_VERTICAL_SLICE.md`
24. `G05F` — Phaser 2D Player Vertical Slice — `goals/GOAL_G05F_PHASER_2D_PLAYER_VERTICAL_SLICE.md`
25. `G06A` — Persistent Lifecycle / Pause / Advance / Background — `goals/GOAL_G06A_PERSISTENT_LIFECYCLE_PAUSE_ADVANCE_BACKGROUND.md`
26. `G06B` — Command Queue & Idempotent Multi-client Semantics — `goals/GOAL_G06B_COMMAND_QUEUE_IDEMPOTENT_MULTI_CLIENT_SEMANTICS.md`
27. `G06C` — Crash Recovery, Checkpoint & Resource Budget — `goals/GOAL_G06C_CRASH_RECOVERY_CHECKPOINT_RESOURCE_BUDGET.md`
28. `G07A` — PhysicalObservation & Reality Bridge — `goals/GOAL_G07A_PHYSICALOBSERVATION_REALITY_BRIDGE.md`
29. `G07B` — Observation Fusion & Validation — `goals/GOAL_G07B_OBSERVATION_FUSION_VALIDATION.md`
30. `G07C` — Opportunity / Challenge / Event Compiler — `goals/GOAL_G07C_OPPORTUNITY_CHALLENGE_EVENT_COMPILER.md`
31. `G07D` — Director Runtime — `goals/GOAL_G07D_DIRECTOR_RUNTIME.md`
32. `G07E` — Experiment Runtime / Multi-run / ValidityEnvelope — `goals/GOAL_G07E_EXPERIMENT_RUNTIME_MULTI_RUN_VALIDITYENVELOPE.md`
33. `G08A` — Synthetic Mansion Living-world Qualification — `goals/GOAL_G08A_SYNTHETIC_MANSION_LIVING_WORLD_QUALIFICATION.md`
34. `G08B` — Red Chamber Source-gated Reference Slice — `goals/GOAL_G08B_RED_CHAMBER_SOURCE_GATED_REFERENCE_SLICE.md`
35. `G09A` — GEDCOM / GEDZIP Interoperability — `goals/GOAL_G09A_GEDCOM_GEDZIP_INTEROPERABILITY.md`
36. `G09B` — Family Semantic World & Conflicting Claims — `goals/GOAL_G09B_FAMILY_SEMANTIC_WORLD_CONFLICTING_CLAIMS.md`
37. `G09C` — Family Privacy, Living Archive & Digital Persona Modes — `goals/GOAL_G09C_FAMILY_PRIVACY_LIVING_ARCHIVE_DIGITAL_PERSONA_MODES.md`
38. `G10A` — IIIF Ingest — `goals/GOAL_G10A_IIIF_INGEST.md`
39. `G10B` — Linked Art / CIDOC CRM Interoperability — `goals/GOAL_G10B_LINKED_ART_CIDOC_CRM_INTEROPERABILITY.md`
40. `G10C` — Heritage Object Semantic Twin — `goals/GOAL_G10C_HERITAGE_OBJECT_SEMANTIC_TWIN.md`
41. `G10D` — Museum, Object Biography & Reconstruction Scenarios — `goals/GOAL_G10D_MUSEUM_OBJECT_BIOGRAPHY_RECONSTRUCTION_SCENARIOS.md`
42. `G11A` — SimulationAdapter Contract & Fake Simulator — `goals/GOAL_G11A_SIMULATIONADAPTER_CONTRACT_FAKE_SIMULATOR.md`
43. `G11B` — Multi-rate / Event-driven Co-Sim Orchestrator — `goals/GOAL_G11B_MULTI_RATE_EVENT_DRIVEN_CO_SIM_ORCHESTRATOR.md`
44. `G11C` — Synthetic Campaign Domain — `goals/GOAL_G11C_SYNTHETIC_CAMPAIGN_DOMAIN.md`
45. `G11D` — Command, Logistics, Movement & Fog-of-war — `goals/GOAL_G11D_COMMAND_LOGISTICS_MOVEMENT_FOG_OF_WAR.md`
46. `G11E` — Batch Experiment & Strategy Evaluation — `goals/GOAL_G11E_BATCH_EXPERIMENT_STRATEGY_EVALUATION.md`
47. `G11F` — Liaoshen Source-gated Reference Pack — `goals/GOAL_G11F_LIAOSHEN_SOURCE_GATED_REFERENCE_PACK.md`
48. `G12A` — 30-day / 1000+ Tick Stability Qualification — `goals/GOAL_G12A_30_DAY_1000_TICK_STABILITY_QUALIFICATION.md`
49. `G12B` — Backup, Restore & Migration Qualification — `goals/GOAL_G12B_BACKUP_RESTORE_MIGRATION_QUALIFICATION.md`
50. `G12C` — Package SDK + OpenAPI / TypeScript SDK — `goals/GOAL_G12C_PACKAGE_SDK_OPENAPI_TYPESCRIPT_SDK.md`
51. `G12D` — Gymnasium / PettingZoo Research Adapters — `goals/GOAL_G12D_GYMNASIUM_PETTINGZOO_RESEARCH_ADAPTERS.md`
52. `G12E` — Godot / Babylon Projection Contracts — `goals/GOAL_G12E_GODOT_BABYLON_PROJECTION_CONTRACTS.md`
53. `G12F` — World Asset Foundry Seam — `goals/GOAL_G12F_WORLD_ASSET_FOUNDRY_SEAM.md`
54. `G12G` — Digital Human / XR Gateway Contracts — `goals/GOAL_G12G_DIGITAL_HUMAN_XR_GATEWAY_CONTRACTS.md`
55. `G12H` — Deployment, Security & Private Installation Qualification — `goals/GOAL_G12H_DEPLOYMENT_SECURITY_PRIVATE_INSTALLATION_QUALIFICATION.md`

At the end of each phase, run the corresponding milestone qualification:

- after G02F → `milestones/M2_QUALIFICATION.md`
- after G03G → `milestones/M3_QUALIFICATION.md`
- after G04E → `milestones/M4_QUALIFICATION.md`
- after G06C → `milestones/M5_QUALIFICATION.md`
- after G07E → `milestones/M6_QUALIFICATION.md`
- after G10D → `milestones/M7_QUALIFICATION.md`
- after G11F → `milestones/M8_QUALIFICATION.md`
- after G12H → `milestones/M9_QUALIFICATION.md`

A milestone must PASS before the first Goal of the next phase. After PASS, checkpoint and continue automatically. Do not stop merely to ask the user whether to proceed.

## 4. Absolute architecture rules

The following remain non-negotiable for every remaining Goal.

### 4.1 One canonical authority

`Canonical World State` has one logical Commit Authority per branch execution context.

No LLM, UI, client, actor policy, Director, Reality Bridge, source compiler, plugin, external simulator, 2D/3D engine, digital-human provider or research adapter may mutate canonical state directly.

All world-changing paths reduce to:

```text
Command / Intent / Observation / External Proposal
→ normalize
→ validate
→ resolve/adjudicate when applicable
→ ProposedWorldDelta
→ commit preconditions / expected revision
→ atomic Commit Authority
→ ordered Event Log
→ canonical state projection
→ audit/trace
```

### 4.2 Formal hierarchy

Keep distinct:

```text
Domain Pack
→ World Pack
→ Scenario
→ World Instance
→ Branch
→ Session
→ Projection
```

Red Chamber, Liaoshen Campaign, family archives, museums and synthetic qualification worlds are packages/instances above Core. Never hard-code them into Core.

### 4.3 Event-sourced continuity

Every new persisted world mechanism must remain compatible with:
- ordered committed events;
- snapshots/checkpoints;
- replay;
- branches/forks;
- deterministic seeds;
- explicit schema/rule/model/package versions;
- correction/new branch instead of silent history mutation.

Derived tables/views may be caches. They must not become irreplaceable truth.

### 4.4 Epistemic isolation

Never collapse:
- Canonical Truth;
- Public Knowledge;
- Group Knowledge;
- Observation;
- Belief;
- Private Memory;
- Rumour/Misinformation;
- Later Historical Record.

Vector retrieval may later assist recall but cannot become the authority model.

### 4.5 Source Gate

Real literary, historical, family, museum and reality-coupled data requires Source/Evidence/Rights/review handling.

When approved real data is unavailable:
- do not fabricate from model memory;
- do not make up historical/literary names and label them real;
- complete generic capability and synthetic fixtures;
- complete Source Gate negative/positive local fixtures;
- mark only the real-data slice `EXTERNAL_BLOCKED`;
- continue independent program execution.

### 4.6 Projection separation

Text, React, Phaser, Godot, Babylon, XR, digital humans and generated assets are projections/adapters. They receive rights/perspective-filtered views and submit commands. They do not own truth and do not have a private save format that supersedes world history.

### 4.7 Core tests remain independent of external LLMs

The deterministic acceptance path must work without network/API keys. Optional LLMPolicy or provider integrations are behind ports and have deterministic fakes/contract tests.

## 5. Engineering quality constitution

The program must remain readable, modifiable, upgradeable and maintainable as it grows.

### 5.1 Dependency direction

- `domain` is pure semantic/domain logic and must not import FastAPI, SQLAlchemy, Alembic, React, model SDKs or concrete network clients.
- application/use-case layers depend on domain and ports, not concrete adapters.
- runtime/host orchestrates through ports.
- persistence implements repository/event/snapshot ports.
- transport maps DTOs to commands/queries and contains no world business rules.
- plugins/domain packs cannot obtain ORM sessions or CommitRepository handles.
- projection/renderer/model/simulator adapters cannot import canonical persistence internals.

Maintain and extend automated architecture conformance tests.

### 5.2 Cohesion and size

Default production source file target: approximately <=300 lines.

Before accepting a larger file:
- determine whether it contains more than one responsibility;
- split by stable domain concept, use-case, port, adapter or schema;
- if remaining large is justified, document why in `DECISIONS.md`.

Forbidden growth patterns:
- giant Manager/Service/God Object;
- `utils.py` / `helpers.py` dumping ground;
- duplicated schema definitions;
- circular imports;
- hidden mutable module singletons;
- constructors that silently perform network/database work;
- functions with unrelated phases and many boolean flags.

### 5.3 Public contracts and upgradeability

Any persisted or externally consumed contract must have explicit version/compatibility treatment from first release.

For every relevant change:
- classify additive, compatible, deprecated or breaking;
- migrate persisted data;
- test old event/snapshot/package fixture compatibility;
- regenerate OpenAPI/SDK when transport changes;
- never silently reinterpret an old event under a new meaning;
- pin world/package/rule/model/runtime versions required for replay;
- prefer explicit new versions/adapters over conditionals scattered across Core.

### 5.4 Errors

Use typed/structured domain/application errors. Do not swallow exceptions or return fake success.

At minimum preserve categories for:
- validation/invariant violation;
- authorization/rights denial;
- stale revision/concurrency;
- duplicate/idempotent result;
- entity/package/source not found;
- unsupported/incompatible schema/version;
- replay/corrupt history;
- persistence/adapter timeout/failure;
- external-blocked capability.

### 5.5 Tests are architecture evidence

Tests must prove behavior and boundaries, not existence.

Use:
- unit tests for local invariants;
- property-based tests for state invariants and generated edge cases;
- contract tests for ports/adapters;
- migration/replay compatibility tests;
- integration tests across actual internal modules;
- E2E tests for Studio/Player/host flows;
- security/rights leakage tests;
- long-run stability tests;
- source-gate malicious-input tests;
- milestone vertical scenarios.

Do not delete/skip/relax a valid failing test merely to continue.

### 5.6 Observability

Preserve or extend structured correlation across:
- run_id;
- world_instance_id;
- branch_id;
- session_id;
- tick/world-time;
- command_id;
- actor/controller;
- observation_id;
- intent/action;
- adjudication_id;
- commit/event sequence;
- trace_id;
- package/rule/model/provider versions where relevant.

Secrets/private payloads are never dumped into logs.

## 6. Goal protocol

For every Goal:

1. read the full Goal contract and dependencies;
2. inspect current code/tests/ADRs/migrations;
3. mark Goal ACTIVE in `STATUS.md` / `PLAN.md`;
4. write or update tests early enough to expose invariant behavior;
5. implement the smallest complete architecture satisfying the Goal;
6. run narrow tests frequently;
7. run architecture/type/lint/migration/security checks as applicable;
8. fix internal failures rather than suppressing them;
9. inspect changed files for cohesion, duplication and coupling;
10. refactor while tests are green;
11. run final Goal acceptance;
12. write the Goal report with reproducible evidence;
13. update ledgers/docs;
14. create local Goal checkpoint commit after PASS;
15. if phase end, run milestone qualification;
16. if milestone PASS, create checkpoint and continue automatically.

Do not push or deploy unless explicitly asked.

## 7. Milestone protocol

A milestone is not PASS because every preceding Goal file has a report.

It passes only when the integrated milestone scenario runs successfully and earlier milestone regressions remain green.

At every milestone:
- run the dedicated `milestones/Mx_QUALIFICATION.md`;
- rerun M1 authority regression and all relevant earlier stable acceptance suites;
- update `reports/ACCEPTANCE_MATRIX.md`;
- produce `reports/Mx_ACCEPTANCE.md`;
- record performance/compatibility/security evidence appropriate to that milestone;
- create a local checkpoint;
- continue.

## 8. Real-data and external dependency policy

### 8.1 Real Red Chamber / Liaoshen / family / heritage sources

Use only source records available in the repository or user-provided approved material that passes policy. No web scraping or model-memory completion merely to make the pack look complete.

If absent:
- Source Gate path and tests still must be complete;
- manifests/template folders may be created;
- real reference slice is `EXTERNAL_BLOCKED`;
- synthetic/reference-neutral acceptance continues.

### 8.2 External services/hardware/engine binaries

If a Goal introduces a future external system:
- define the port first;
- implement a deterministic fake/fixture;
- write contract/error/timeout tests;
- keep canonical state safe when unavailable.

Only the actual environment-dependent integration check may be `EXTERNAL_BLOCKED`. Do not use that label for missing internal implementation.

## 9. UI and adapter discipline

For Studio, Phaser, Godot/Babylon, research environments, Asset Foundry and digital-human/XR:
- server/runtime remains authoritative;
- filtering occurs server-side for secrets/rights;
- clients reconstruct from projection rather than private save truth;
- client-side optimism must reconcile against authoritative commit response;
- disconnect/reconnect cannot create canonical divergence;
- adapter output never becomes canonical merely because a renderer/model produced it.

## 10. Security and rights are continuous

From now through M9, every new boundary must consider:
- access authorization;
- RightsEnvelope;
- privacy classification;
- provenance/truth labels;
- source prompt-injection isolation;
- upload type/size/malicious-content validation;
- tool/provider least privilege;
- secret management;
- audit protection;
- real-person/minor/digital-person governance where applicable.

Do not postpone these to G12H.

## 11. Performance and resource discipline

Do not prematurely distribute the system. Measure first.

Add budgets/metrics for:
- scheduler queues;
- active actors;
- simulator calls;
- optional model calls;
- event/snapshot growth;
- memory/cognition retention;
- projection payload size;
- command queue/backpressure;
- long-run latency and memory.

When a benchmark reveals pathological growth, fix the responsible abstraction rather than masking it with arbitrary cache eviction.

## 12. Compatibility discipline

Before changing an old type or behavior used in persisted events/packages:
1. inspect retained fixture versions;
2. write a compatibility/migration test;
3. implement version-aware reader/upcaster/adapter or explicit migration;
4. verify old worlds still replay or fail with a deliberate, documented incompatibility policy;
5. never reinterpret old history silently.

## 13. Blocker policy

Do not ask the user about routine technical choices.

Resolve locally:
- failing tests;
- dependency conflicts;
- typing;
- migrations;
- package layout;
- reasonable library choices consistent with existing stack;
- refactors required by architecture standards.

Stop the whole program only when:
- repository corruption or missing mandatory source-of-truth documents makes safe work impossible;
- a true specification contradiction affects all remaining work and cannot be conservatively isolated;
- the local environment cannot execute any meaningful remaining engineering and no deterministic/fake path exists.

Otherwise isolate the blocker, document it, and continue.

## 14. Completion definition for the entire remaining program

The remaining program is complete only when:

- M2, M3, M4, M5, M6, M7, M8 and M9 system qualification reports exist;
- all internal mandatory criteria are PASS;
- allowed external-only items are explicitly documented and never falsely marked complete;
- M1 authoritative-world invariants still pass on the final tree;
- full test/lint/type/architecture/migration/security suite is green;
- long-run/backup/restore/SDK/deployment release checks are complete;
- no acceptance-critical TODO/FIXME/NotImplemented/placeholder/mock-only path remains;
- `docs/IMPLEMENTATION_STATUS.md` accurately distinguishes implemented, partial and external-blocked capability;
- final repository architecture remains modular, readable and versioned;
- final local checkpoint is created.

## 15. Final M9 report

At the end create at minimum:
- `reports/M9_ACCEPTANCE.md`
- `reports/FINAL_PROGRAM_COMPLETION_REPORT.md`
- final `reports/ACCEPTANCE_MATRIX.md`
- `reports/ARCHITECTURE_CONFORMANCE_FINAL.md`
- `reports/MIGRATION_REPLAY_COMPATIBILITY_FINAL.md`
- `reports/SECURITY_RIGHTS_FINAL.md`
- `reports/LONG_RUN_STABILITY_FINAL.md`
- `docs/IMPLEMENTATION_STATUS.md`
- `docs/RELEASE_READINESS.md`

The final completion report must enumerate:
- all Goals and verdicts;
- all milestones and verdicts;
- Git checkpoint hashes;
- test commands/results;
- retained limitations;
- all EXTERNAL_BLOCKED items and exact missing dependency;
- architecture debt;
- migration/compatibility matrix;
- supported deployment/adapter status;
- what is genuinely usable versus contract-only.

Do not say “all done” if these reports show otherwise.

## 16. Final stop

After M9 qualification and the final reports/checkpoint:
- STOP;
- do not invent a G13;
- do not push/deploy;
- provide the user a concise completion summary referencing exact report paths and remaining external blockers.

Begin now by verifying the actual M1 checkpoint, then execute `G02A`.
