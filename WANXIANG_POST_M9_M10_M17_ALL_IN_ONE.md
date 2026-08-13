

<!-- ===== FILE: README_FIRST_POST_M9.md ===== -->

# Wanxiang Post-M9 Execution Pack

This pack continues after the earlier M0–M9 implementation program. It contains **69 executable Goals** across M10–M17.

## Recommended use

1. Copy this directory's files into the existing Wanxiang repository root without deleting existing code, Git history, ledgers, reports or M0–M9 program files.
2. Ensure `docs/spec/WANXIANG_v5_MASTER_SPEC.md` and the earlier engineering standards remain present.
3. Open a new Codex Desktop task in the repository.
4. Paste `CODEX_COPY_PASTE_POST_M9.txt`.
5. Codex should read `11_CODEX_POST_M9_MASTER_PROMPT.md` and execute the indexed Goals continuously.

## Program outcome

M10 independent audit → M11 adversarial resilience → M12 reference-world/worldness → M13 production operations → M14 external ecosystem → M15 product surfaces → M16 isolated research expansion → M17 final certification.

No automatic push or external production deployment is authorized by this pack.


<!-- ===== FILE: 10_POST_M9_PROGRAM_ARCHITECTURE.md ===== -->

# Wanxiang Post-M9 Engineering Program Architecture — M10 → M17

> Date: 2026-08-13
> Continuation after the v5.0-R1 M0–M9 implementation program.
> This program does **not** redefine the product. `docs/spec/WANXIANG_v5_MASTER_SPEC.md` remains the product/architecture source of truth for v5.0-R1.

## 1. Why a Post-M9 Program exists

M0–M9 can establish a broad implementation, but breadth itself is not proof. The next engineering risk is false completion: interfaces with no real vertical path, mock-only product surfaces, replay compatibility that only works for current fixtures, or a platform that passes its own tests but fails under independent audit, hostile inputs, long-horizon operation or clean-room deployment.

The Post-M9 program therefore changes the execution mode from **feature construction** to **proof, closure, adversarial qualification, black-box generality, production operation and controlled research expansion**.

## 2. Milestones

- **M10 — Independent Verification & Gap Closure:** do not trust prior PASS claims; trace every normative requirement to code, test and runtime evidence; close P0 and required P1 gaps.
- **M11 — Adversarial / Failure Qualification:** concurrency, crash, corruption, hostile package/source, auth/privacy, external simulator failures and resource exhaustion.
- **M12 — Reference World & Worldness Certification:** comprehensive synthetic world, seven-day and extended runs, human leave/rejoin, material/information continuity, branching and source-gated real reference slices.
- **M13 — Productionization & Operations:** PostgreSQL profile, queues/workers only as justified, assets, observability, security, backup/DR, CI/CD, capacity and private/staging deployment.
- **M14 — SDK / Plugin / World Pack Ecosystem:** stable public extension surface, authoring CLI, third-party certification, trust model, registry lifecycle and clean-room external pack.
- **M15 — Product Surface Completion:** Studio, Experience, Strategy, Family, Heritage, Learn and operator/admin surfaces all connected to the same authoritative world.
- **M16 — v5.1/v6 Research Expansion:** experimental AI compiler, long-horizon cognition, cognitive LOD, world-model planner, generative assets, digital human/XR, multi-simulator, reality streams and distribution experiments. Stable Core remains default.
- **M17 — Final Independent Certification:** final traceability, clean-room build/restore/replay, security/chaos rerun, black-box external author/end-user test and release readiness freeze.

## 3. Non-negotiable invariants carried forward

1. `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains the formal hierarchy.
2. Only Commit Authority may mutate Canonical World State.
3. LLMs, UIs, Directors, sensors, simulators, plugins and research models only propose/observe; they never own truth.
4. Event history, replay, snapshot, branch isolation and version compatibility remain release invariants.
5. Projection state is discardable/rebuildable; it cannot become an alternate save format.
6. Real literary/history/family/heritage data must pass Source/Evidence/Rights gates. Model memory is not a source.
7. Deterministic core tests remain network/API-key independent.
8. Security, rights, observability, migration and compatibility are continuous requirements.
9. Domain-specific reference worlds may expose generic Core gaps; fixes must generalize rather than hard-code the reference world.
10. Research code is experimental until evidence promotes it; feature flags OFF must preserve stable behavior.

## 4. Execution graph

```text
M9 PASS
  ↓
M10 Independent audit + gap closure
  ↓
M11 adversarial/failure qualification
  ↓
M12 reference-world/worldness qualification
  ↓
M13 productionization/operations
  ↓
M14 SDK/ecosystem black-box extensibility
  ↓
M15 product-surface completion
  ↓
M16 isolated research expansion
  ↓
M17 final independent certification
```

Milestones are gates. A failing stable-path gate blocks advancement. A narrowly external real-data/hardware/provider dependency may be `EXTERNAL_BLOCKED` only for that slice if generic capability and deterministic substitutes are fully implemented and tested.

## 5. Definition of Done for every Goal

Every Goal file is an executable engineering contract and must contain/obey:

- Objective
- Scope
- Non-goals
- Required reading
- Architecture constraints
- Deliverables
- Implementation tasks
- Tests
- Acceptance criteria
- Failure / blocker handling
- Documentation updates
- Git / checkpoint requirements

A Goal is not complete when code exists. It is complete when the requested behavior is integrated, negative paths are tested, architecture rules still pass, docs/ledgers are updated and evidence can be reproduced.

## 6. Quality model

Maintainability is a release property. Continue enforcing the existing Engineering Standards. In particular:

- domain code remains framework/storage/model-SDK independent;
- business logic stays out of routes/UI;
- public contracts are typed/versioned;
- default production file size target remains about 300 lines unless a coherent exception is documented;
- no giant manager/service/utils/helper dumping grounds;
- no mutable global authority;
- no hidden I/O constructors;
- no swallowed exceptions;
- no broad `Any` escape hatch;
- no TODO/FIXME/placeholder/static fake that is required for acceptance;
- architecture conformance and import-cycle checks remain continuous;
- generated clients/schemas are generated, not manually forked;
- event/package/API/database migrations are explicit and tested.

## 7. Audit evidence statuses

Use only:

- `PASS` / `VERIFIED`
- `FAIL` / `GAP`
- `PARTIAL`
- `EXTERNAL_BLOCKED`
- `NOT_APPLICABLE`
- `EXPERIMENTAL` for M16 research scope

`EXTERNAL_BLOCKED` means a real external dependency is missing: legal source, credentials, unavailable hardware/provider/environment. It never means “too much work”, “ran out of context”, “difficult”, or an internal bug.

## 8. Stable vs research completion

M10–M15 and M17 certify stable platform behavior. M16 is different: a research Goal may end in `PROMOTE`, `KEEP_EXPERIMENTAL` or `REJECT`. A well-run experiment that demonstrates a bad tradeoff is still a successful research Goal. Rejected experiments must not contaminate stable defaults.


<!-- ===== FILE: 11_CODEX_POST_M9_MASTER_PROMPT.md ===== -->

# Codex Post-M9 Continuous Master Prompt — M10 → M17

> Mission: continue Wanxiang after a claimed M9 completion and execute the entire Post-M9 Program through final M17 certification.
> Do not redesign the product.
> Do not trust conversational completion claims. Verify repository evidence first.

## 0. Start condition

The user states M0–M9/G00A–G12H are complete. Before changing code:

1. read `docs/spec/WANXIANG_v5_MASTER_SPEC.md`;
2. read existing engineering program/standards/acceptance docs;
3. read M9 and final reports, `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`;
4. inspect Git status/history, source, tests, migrations, deployment and generated SDK/API artifacts;
5. run the narrow critical M9 regression suite.

If M9 is materially regressed, repair the regression as part of the baseline before G13A and record it. Do not redo M0–M9 from scratch when healthy.

## 1. Normative new files

Read in this order:

- `10_POST_M9_PROGRAM_ARCHITECTURE.md`
- `11_CODEX_POST_M9_MASTER_PROMPT.md`
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- `14_AUDIT_TRACEABILITY_PROTOCOL.md`
- `15_ADVERSARIAL_CHAOS_PROTOCOL.md`
- `16_REFERENCE_WORLD_QUALIFICATION_STANDARD.md`
- `17_PRODUCTION_OPERATIONS_STANDARD.md`
- `18_SDK_ECOSYSTEM_STANDARD.md`
- `19_PRODUCT_SURFACE_COMPLETION_STANDARD.md`
- `20_RESEARCH_EXPANSION_V5_1_V6.md`
- `21_FINAL_CERTIFICATION_STANDARD.md`
- current Goal file

Product authority remains `docs/spec/WANXIANG_v5_MASTER_SPEC.md`. Existing M0–M9 standards remain in force unless a later ADR explicitly strengthens them without contradicting the mother spec.

## 2. Execution mode

Execute every Goal in `12_POST_M9_GOALS_INDEX.md` in order. At the end of each milestone execute the corresponding `milestones/Mxx_QUALIFICATION.md`.

A milestone PASS automatically continues to the next milestone. Do not stop for routine user confirmation. If context compresses/restarts, recover from Git + ledgers + latest Goal/milestone report, never chat memory.

Stop only when:

- M17 is completed; or
- a genuinely unrecoverable repository/environment blocker prevents **all** further independent work.

A narrow real-data/provider/hardware blocker does not stop unrelated work.

## 3. Never trust previous PASS blindly

M10 explicitly performs an independent audit. Existing reports are evidence candidates, not authority. Every important requirement must map to:

`spec requirement → implementation owner → test → reproducible runtime/build evidence`.

A class/interface/route/file name by itself is not evidence of completion.

## 4. Core mutation rule

All world-changing input continues through the single authority pipeline:

```text
Command / Intent / Observation / External Proposal
→ normalize
→ validate
→ resolve/adjudicate
→ ProposedWorldDelta
→ expected-revision / invariant checks
→ Commit Authority
→ ordered committed Event
→ canonical state projection
→ audit/trace
```

No UI, LLM, Actor policy, Director, Reality Bridge, plugin, simulator, SDK client, research model, Godot/Babylon/XR/digital-human integration or package compiler may directly mutate Canonical World State.

## 5. Continuous regression rule

After any change touching stable Core, persistence, package contracts, rights, host, SDK or product surfaces, run the smallest affected suite plus the relevant global regression before closing the Goal. At milestone gates run the broad suite defined in the milestone file.

Never make tests green by:

- deleting a failing test;
- reducing an assertion that represented the requirement;
- adding broad skips/xfails;
- disabling type/architecture checks;
- catching and ignoring errors;
- replacing real integration with static fake data.

## 6. Gap closure priority

- P0: correctness, authority, data loss, replay/branch, critical security/rights, fake completion of mandatory path. Must close before M11.
- P1: required maintainability/integration/compatibility/observability/security/release defect. Must close before relevant later gate.
- P2: useful but non-blocking debt/optimization. Track explicitly; do not smuggle into DONE.

## 7. Real-data Source Gate

Red Chamber, Liaoshen, real family records, real heritage collections, real sensors and real-person digital human assets remain source/rights gated.

If missing, complete generic contracts, synthetic fixtures, source-gate tests, rights checks and external-blocker report. Never fabricate canonical real content from model memory.

## 8. M16 research rule

M16 is allowed to experiment, but:

- experimental features are OFF by default;
- they live behind explicit Port/feature flags/experimental namespaces;
- stable data schemas are not silently repurposed;
- research model output remains proposal/candidate/observation;
- stable regression with flags OFF must pass;
- each track ends with `PROMOTE`, `KEEP_EXPERIMENTAL` or `REJECT` and evidence.

## 9. Per-goal reporting and Git

For each Goal:

1. read Goal completely;
2. inspect current relevant code/tests;
3. update `PLAN.md` and `STATUS.md`;
4. implement in small cohesive changes;
5. run requested tests + quality gates;
6. update traceability/acceptance artifacts where applicable;
7. write `reports/<goal_id>_REPORT.md` (or the Goal-specific report names);
8. update `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`;
9. create a local Git checkpoint only when Goal acceptance passes.

Do not push or deploy externally unless the user separately authorizes it.

## 10. Final stop condition

Do not claim completion until M17 generated at least:

- `reports/FINAL_DESIGN_TRACEABILITY.md`
- `reports/CLEAN_ROOM_CERTIFICATION.md`
- `reports/FINAL_SECURITY_RELIABILITY_CERTIFICATION.md`
- `reports/BLACKBOX_FINAL_ACCEPTANCE.md`
- `reports/M17_FINAL_CERTIFICATION.md`
- `reports/FINAL_PROGRAM_COMPLETION_REPORT.md`
- `docs/RELEASE_READINESS.md`
- `docs/POST_V5_ROADMAP.md`

Stable P0/P1 gaps must be zero. `EXTERNAL_BLOCKED` and M16 experimental/rejected items must be explicit and must not be described as complete stable functionality.

Then stop after a local checkpoint and report to the user.


<!-- ===== FILE: 12_POST_M9_GOALS_INDEX.md ===== -->

# Wanxiang Post-M9 Goals Index — M10 to M17

> Normative continuous execution order after a verified M9 checkpoint.

## M10

- `G13A` — Post-M9 Baseline Freeze & Independent Evidence Capture — `goals/GOAL_G13A_POST_M9_BASELINE_FREEZE_INDEPENDENT_EVIDENCE_CAPTURE.md`
- `G13B` — Design-to-Implementation Traceability Matrix — `goals/GOAL_G13B_DESIGN_TO_IMPLEMENTATION_TRACEABILITY_MATRIX.md`
- `G13C` — Architecture, Dependency & Canonical-Mutation Forensics — `goals/GOAL_G13C_ARCHITECTURE_DEPENDENCY_CANONICAL_MUTATION_FORENSICS.md`
- `G13D` — Placeholder, Fake, Dead-path & Surface Integration Audit — `goals/GOAL_G13D_PLACEHOLDER_FAKE_DEAD_PATH_SURFACE_INTEGRATION_AUDIT.md`
- `G13E` — Event, Replay, Branch, Migration & Version Forensics — `goals/GOAL_G13E_EVENT_REPLAY_BRANCH_MIGRATION_VERSION_FORENSICS.md`
- `G13F` — Security, Rights, Provenance, Privacy & Source-Gate Forensics — `goals/GOAL_G13F_SECURITY_RIGHTS_PROVENANCE_PRIVACY_SOURCE_GATE_FORENSICS.md`
- `G13G` — Maintainability, Complexity, Test Quality & Upgradeability Audit — `goals/GOAL_G13G_MAINTAINABILITY_COMPLEXITY_TEST_QUALITY_UPGRADEABILITY_AUDIT.md`
- `G13H` — P0 Gap Closure Wave — `goals/GOAL_G13H_P0_GAP_CLOSURE_WAVE.md`
- `G13I` — P1/P2 Gap Closure & M10 Independent Requalification — `goals/GOAL_G13I_P1_P2_GAP_CLOSURE_M10_INDEPENDENT_REQUALIFICATION.md`
- Milestone Gate — `milestones/M10_QUALIFICATION.md`

## M11

- `G14A` — Concurrency, Race, Idempotency & Lost-update Adversarial Qualification — `goals/GOAL_G14A_CONCURRENCY_RACE_IDEMPOTENCY_LOST_UPDATE_ADVERSARIAL_QUALIFICATION.md`
- `G14B` — Crash, Atomicity & Mid-Commit Recovery Qualification — `goals/GOAL_G14B_CRASH_ATOMICITY_MID_COMMIT_RECOVERY_QUALIFICATION.md`
- `G14C` — Database, Storage, Network & Dependency Fault Injection — `goals/GOAL_G14C_DATABASE_STORAGE_NETWORK_DEPENDENCY_FAULT_INJECTION.md`
- `G14D` — Event, Snapshot, Branch & History Corruption Adversarial Qualification — `goals/GOAL_G14D_EVENT_SNAPSHOT_BRANCH_HISTORY_CORRUPTION_ADVERSARIAL_QUALIFICATION.md`
- `G14E` — World Host, Multiplayer, Reconnect, Ordering & Backpressure Chaos — `goals/GOAL_G14E_WORLD_HOST_MULTIPLAYER_RECONNECT_ORDERING_BACKPRESSURE_CHAOS.md`
- `G14F` — Hostile Package, Plugin & Source Input Qualification — `goals/GOAL_G14F_HOSTILE_PACKAGE_PLUGIN_SOURCE_INPUT_QUALIFICATION.md`
- `G14G` — Authorization, Rights, Privacy & Data-leak Adversarial Qualification — `goals/GOAL_G14G_AUTHORIZATION_RIGHTS_PRIVACY_DATA_LEAK_ADVERSARIAL_QUALIFICATION.md`
- `G14H` — SimulationAdapter & External-system Byzantine Behavior Qualification — `goals/GOAL_G14H_SIMULATIONADAPTER_EXTERNAL_SYSTEM_BYZANTINE_BEHAVIOR_QUALIFICATION.md`
- `G14I` — Resource Exhaustion, Fuzz, Long-run Chaos & M11 Qualification — `goals/GOAL_G14I_RESOURCE_EXHAUSTION_FUZZ_LONG_RUN_CHAOS_M11_QUALIFICATION.md`
- Milestone Gate — `milestones/M11_QUALIFICATION.md`

## M12

- `G15A` — Reference World Contract & External Pack Boundary — `goals/GOAL_G15A_REFERENCE_WORLD_CONTRACT_EXTERNAL_PACK_BOUNDARY.md`
- `G15B` — Comprehensive Synthetic Reference World Package — `goals/GOAL_G15B_COMPREHENSIVE_SYNTHETIC_REFERENCE_WORLD_PACKAGE.md`
- `G15C` — Seven-day Autonomous Living-world Qualification — `goals/GOAL_G15C_SEVEN_DAY_AUTONOMOUS_LIVING_WORLD_QUALIFICATION.md`
- `G15D` — Human Embodiment, Exit, Re-entry & Control Continuity Qualification — `goals/GOAL_G15D_HUMAN_EMBODIMENT_EXIT_RE_ENTRY_CONTROL_CONTINUITY_QUALIFICATION.md`
- `G15E` — Material Custody, Information Propagation & Social Continuity Qualification — `goals/GOAL_G15E_MATERIAL_CUSTODY_INFORMATION_PROPAGATION_SOCIAL_CONTINUITY_QUALIFICATION.md`
- `G15F` — Branch, Time-travel & Counterfactual Worldline Comparison Qualification — `goals/GOAL_G15F_BRANCH_TIME_TRAVEL_COUNTERFACTUAL_WORLDLINE_COMPARISON_QUALIFICATION.md`
- `G15G` — Extended 90-day Virtual Run & Population-LOD Qualification — `goals/GOAL_G15G_EXTENDED_90_DAY_VIRTUAL_RUN_POPULATION_LOD_QUALIFICATION.md`
- `G15H` — Red Chamber Source-gated Qualified Reference Slice — `goals/GOAL_G15H_RED_CHAMBER_SOURCE_GATED_QUALIFIED_REFERENCE_SLICE.md`
- `G15I` — Family, Heritage & Campaign Source-gated Reference Suites — `goals/GOAL_G15I_FAMILY_HERITAGE_CAMPAIGN_SOURCE_GATED_REFERENCE_SUITES.md`
- `G15J` — Cross-domain Worldness Certification & M12 Qualification — `goals/GOAL_G15J_CROSS_DOMAIN_WORLDNESS_CERTIFICATION_M12_QUALIFICATION.md`
- Milestone Gate — `milestones/M12_QUALIFICATION.md`

## M13

- `G16A` — Production Topology, Configuration & Secret-management Foundation — `goals/GOAL_G16A_PRODUCTION_TOPOLOGY_CONFIGURATION_SECRET_MANAGEMENT_FOUNDATION.md`
- `G16B` — PostgreSQL Production Persistence & Migration Qualification — `goals/GOAL_G16B_POSTGRESQL_PRODUCTION_PERSISTENCE_MIGRATION_QUALIFICATION.md`
- `G16C` — Background Execution, Work Queue & Scheduler Reliability — `goals/GOAL_G16C_BACKGROUND_EXECUTION_WORK_QUEUE_SCHEDULER_RELIABILITY.md`
- `G16D` — Asset/Object Storage, Media Rights & Durable Artifact Handling — `goals/GOAL_G16D_ASSET_OBJECT_STORAGE_MEDIA_RIGHTS_DURABLE_ARTIFACT_HANDLING.md`
- `G16E` — OpenTelemetry Observability, SLOs & Operational Diagnostics — `goals/GOAL_G16E_OPENTELEMETRY_OBSERVABILITY_SLOS_OPERATIONAL_DIAGNOSTICS.md`
- `G16F` — Production Security Hardening, AuthN/AuthZ, Rate Limits & Supply-chain Controls — `goals/GOAL_G16F_PRODUCTION_SECURITY_HARDENING_AUTHN_AUTHZ_RATE_LIMITS_SUPPLY_CHAIN_CONTROLS.md`
- `G16G` — Backup, Restore, PITR-like Recovery & Disaster Game Day — `goals/GOAL_G16G_BACKUP_RESTORE_PITR_LIKE_RECOVERY_DISASTER_GAME_DAY.md`
- `G16H` — CI/CD, Release Artifacts, Rolling Migration & Rollback Qualification — `goals/GOAL_G16H_CI_CD_RELEASE_ARTIFACTS_ROLLING_MIGRATION_ROLLBACK_QUALIFICATION.md`
- `G16I` — Performance, Capacity, Cost & Resource-budget Qualification — `goals/GOAL_G16I_PERFORMANCE_CAPACITY_COST_RESOURCE_BUDGET_QUALIFICATION.md`
- `G16J` — Private/Staging Deployment, Operator Runbooks & M13 Production Qualification — `goals/GOAL_G16J_PRIVATE_STAGING_DEPLOYMENT_OPERATOR_RUNBOOKS_M13_PRODUCTION_QUALIFICATION.md`
- Milestone Gate — `milestones/M13_QUALIFICATION.md`

## M14

- `G17A` — Public SDK Contract, Semantic Versioning & Compatibility Policy — `goals/GOAL_G17A_PUBLIC_SDK_CONTRACT_SEMANTIC_VERSIONING_COMPATIBILITY_POLICY.md`
- `G17B` — Package Authoring CLI, Scaffolder & Schema Validation — `goals/GOAL_G17B_PACKAGE_AUTHORING_CLI_SCAFFOLDER_SCHEMA_VALIDATION.md`
- `G17C` — External Author Documentation & Reference Templates — `goals/GOAL_G17C_EXTERNAL_AUTHOR_DOCUMENTATION_REFERENCE_TEMPLATES.md`
- `G17D` — Third-party Package Conformance & Certification Harness — `goals/GOAL_G17D_THIRD_PARTY_PACKAGE_CONFORMANCE_CERTIFICATION_HARNESS.md`
- `G17E` — Plugin Trust, Signing, Capability Permissions & Isolation Policy — `goals/GOAL_G17E_PLUGIN_TRUST_SIGNING_CAPABILITY_PERMISSIONS_ISOLATION_POLICY.md`
- `G17F` — Registry Publish, Install, Upgrade, Deprecation & Dependency Resolution — `goals/GOAL_G17F_REGISTRY_PUBLISH_INSTALL_UPGRADE_DEPRECATION_DEPENDENCY_RESOLUTION.md`
- `G17G` — Black-box External Sample Pack Built Outside Core Repository Internals — `goals/GOAL_G17G_BLACK_BOX_EXTERNAL_SAMPLE_PACK_BUILT_OUTSIDE_CORE_REPOSITORY_INTERNALS.md`
- `G17H` — Ecosystem Documentation, Certification & M14 Qualification — `goals/GOAL_G17H_ECOSYSTEM_DOCUMENTATION_CERTIFICATION_M14_QUALIFICATION.md`
- Milestone Gate — `milestones/M14_QUALIFICATION.md`

## M15

- `G18A` — Product Surface Information Architecture & Server-truth Contract — `goals/GOAL_G18A_PRODUCT_SURFACE_INFORMATION_ARCHITECTURE_SERVER_TRUTH_CONTRACT.md`
- `G18B` — Studio / World IDE Completion — `goals/GOAL_G18B_STUDIO_WORLD_IDE_COMPLETION.md`
- `G18C` — Experience Player Web/2D Continuity Completion — `goals/GOAL_G18C_EXPERIENCE_PLAYER_WEB_2D_CONTINUITY_COMPLETION.md`
- `G18D` — Strategy / Experiment Workbench Completion — `goals/GOAL_G18D_STRATEGY_EXPERIMENT_WORKBENCH_COMPLETION.md`
- `G18E` — Family Portal Completion — `goals/GOAL_G18E_FAMILY_PORTAL_COMPLETION.md`
- `G18F` — Heritage / Museum Workbench Completion — `goals/GOAL_G18F_HERITAGE_MUSEUM_WORKBENCH_COMPLETION.md`
- `G18G` — Learn / Challenge Experience Completion — `goals/GOAL_G18G_LEARN_CHALLENGE_EXPERIENCE_COMPLETION.md`
- `G18H` — Operator/Admin/Source/Rights/Evaluation Console & M15 Qualification — `goals/GOAL_G18H_OPERATOR_ADMIN_SOURCE_RIGHTS_EVALUATION_CONSOLE_M15_QUALIFICATION.md`
- Milestone Gate — `milestones/M15_QUALIFICATION.md`

## M16

- `G19A` — Research Namespace, Feature Flags, Benchmarks & Promotion Rules — `goals/GOAL_G19A_RESEARCH_NAMESPACE_FEATURE_FLAGS_BENCHMARKS_PROMOTION_RULES.md`
- `G19B` — AI-assisted World Compiler Semantic Extraction Research — `goals/GOAL_G19B_AI_ASSISTED_WORLD_COMPILER_SEMANTIC_EXTRACTION_RESEARCH.md`
- `G19C` — Long-horizon Persona, Memory Metabolism & Drift Evaluation Research — `goals/GOAL_G19C_LONG_HORIZON_PERSONA_MEMORY_METABOLISM_DRIFT_EVALUATION_RESEARCH.md`
- `G19D` — Cognitive LOD & Large-population Scheduling Research — `goals/GOAL_G19D_COGNITIVE_LOD_LARGE_POPULATION_SCHEDULING_RESEARCH.md`
- `G19E` — World-model / Planner Proposal Engine Research — `goals/GOAL_G19E_WORLD_MODEL_PLANNER_PROPOSAL_ENGINE_RESEARCH.md`
- `G19F` — Generative Asset / Scene Pipeline & Semantic Binding Research — `goals/GOAL_G19F_GENERATIVE_ASSET_SCENE_PIPELINE_SEMANTIC_BINDING_RESEARCH.md`
- `G19G` — Advanced Digital Human / XR Presence Research — `goals/GOAL_G19G_ADVANCED_DIGITAL_HUMAN_XR_PRESENCE_RESEARCH.md`
- `G19H` — Multi-simulator Federation & Co-Simulation Research — `goals/GOAL_G19H_MULTI_SIMULATOR_FEDERATION_CO_SIMULATION_RESEARCH.md`
- `G19I` — Reality/Digital-twin Streaming & Observation Fusion Research — `goals/GOAL_G19I_REALITY_DIGITAL_TWIN_STREAMING_OBSERVATION_FUSION_RESEARCH.md`
- `G19J` — Distributed World Host / Sharding Experiment & M16 Research Qualification — `goals/GOAL_G19J_DISTRIBUTED_WORLD_HOST_SHARDING_EXPERIMENT_M16_RESEARCH_QUALIFICATION.md`
- Milestone Gate — `milestones/M16_QUALIFICATION.md`

## M17

- `G20A` — Final Mother-spec Traceability & Requirement Closure — `goals/GOAL_G20A_FINAL_MOTHER_SPEC_TRACEABILITY_REQUIREMENT_CLOSURE.md`
- `G20B` — Clean-room Build, Install, Upgrade, Restore & Replay Certification — `goals/GOAL_G20B_CLEAN_ROOM_BUILD_INSTALL_UPGRADE_RESTORE_REPLAY_CERTIFICATION.md`
- `G20C` — Final Independent Security, Reliability & Chaos Re-run — `goals/GOAL_G20C_FINAL_INDEPENDENT_SECURITY_RELIABILITY_CHAOS_RE_RUN.md`
- `G20D` — Black-box External Author + Reference World Final Acceptance — `goals/GOAL_G20D_BLACK_BOX_EXTERNAL_AUTHOR_REFERENCE_WORLD_FINAL_ACCEPTANCE.md`
- `G20E` — Final Release Readiness, Version Freeze & Post-v5 Roadmap — `goals/GOAL_G20E_FINAL_RELEASE_READINESS_VERSION_FREEZE_POST_V5_ROADMAP.md`
- Milestone Gate — `milestones/M17_QUALIFICATION.md`


<!-- ===== FILE: 13_MILESTONE_GATES_M10_M17.md ===== -->

# Milestone Gates M10–M17

## M10 — Independent Verification & Gap Closure

P0=0; required P1=0; traceability complete; M1-M9 critical regressions independently reproduced.

Gate file: `milestones/M10_QUALIFICATION.md`

## M11 — Adversarial / Failure Qualification

No high/critical stable-path failure under declared chaos profiles; world truth remains consistent during concurrency/crash/corruption/hostile inputs.

Gate file: `milestones/M11_QUALIFICATION.md`

## M12 — Reference World & Worldness Certification

Comprehensive synthetic world passes worldness criteria and long-run/replay/branch/human-control tests; real reference slices are PASS or narrow EXTERNAL_BLOCKED.

Gate file: `milestones/M12_QUALIFICATION.md`

## M13 — Productionization & Operations

Private/staging deployment is reproducible, observable, secure, recoverable, upgradeable and capacity-qualified at a declared profile.

Gate file: `milestones/M13_QUALIFICATION.md`

## M14 — SDK / Ecosystem Qualification

External developer can author/certify/publish/install/upgrade a package through public SDK/contracts without modifying Core.

Gate file: `milestones/M14_QUALIFICATION.md`

## M15 — Product Surface Qualification

Major product faces are real projections/control surfaces over one server truth with critical E2E/accessibility/authz flows passing.

Gate file: `milestones/M15_QUALIFICATION.md`

## M16 — Research Expansion Qualification

All research tracks executed with evidence and explicit PROMOTE/KEEP_EXPERIMENTAL/REJECT; stable flags-off regression remains green.

Gate file: `milestones/M16_QUALIFICATION.md`

## M17 — Final Independent Certification

Stable P0/P1=0; clean-room, security/reliability, black-box author/user/operator and final traceability all PASS; release readiness bundle complete.

Gate file: `milestones/M17_QUALIFICATION.md`


<!-- ===== FILE: 14_AUDIT_TRACEABILITY_PROTOCOL.md ===== -->

# Audit & Traceability Protocol

## Purpose
Independent verification must be requirement-driven, not file-count-driven.

## Requirement extraction
Create stable requirement IDs from the mother specification and engineering contracts. Prioritize normative language and architecture invariants. Preserve original meaning; do not silently “fix” the specification during audit.

## Required trace fields
- requirement_id
- source_document + section/line or heading reference
- requirement summary
- kernel/cross-cutting owner
- implementation path/symbol
- public contract/API/schema
- test path/name
- runtime/build evidence
- status
- severity if gap
- notes/blocker

## Evidence hierarchy
Strongest evidence is an executable black-box/integration/property test over a real vertical path. Unit tests support but do not replace integration proof. Class/interface existence is weak evidence. Comments, TODOs and prior reports are not sufficient.

## Gap severity
P0: world truth/data-loss/security-critical/authority/replay/branch/mandatory-path false completion.
P1: required integration, maintainability, compatibility, rights, observability or release defect.
P2: non-blocking optimization/polish/research.

## False-completion indicators
- production path selects a Fake/static fixture;
- UI shows canned JSON rather than server projection;
- adapter interface exists but no contract/integration test;
- API route returns success without authoritative commit;
- migration claims without old-version fixture;
- replay test starts from already-derived current state;
- branch test shares mutable references;
- rights checked only in UI;
- source provenance lost after compile;
- generated SDK manually diverges from OpenAPI.

## Closure
Every P0/P1 fix should link root cause, code diff, regression test and affected requirement IDs. Never delete baseline audit evidence.


<!-- ===== FILE: 15_ADVERSARIAL_CHAOS_PROTOCOL.md ===== -->

# Adversarial & Chaos Qualification Protocol

## Principle
The purpose is not maximum random failure. It is controlled fault injection around semantic authority, persistence boundaries, concurrency, rights and external adapters.

## Required fault families
1. concurrent/stale/duplicate commands;
2. crash before/during/after commit;
3. DB/network/storage timeout and unavailable states;
4. corrupt events/snapshots/branch ancestry/version;
5. reconnect, reordering, slow consumer, queue pressure;
6. hostile package/source/prompt injection;
7. authorization/privacy/rights bypass attempts;
8. Byzantine simulator/sensor proposals;
9. resource exhaustion, fuzz and long-run memory growth.

## Invariant monitor
Chaos tests must continuously watch event ordering, branch isolation, canonical semantic hash validity, custody/container constraints, permissions, time monotonicity and information isolation as applicable.

## Safety
Fault hooks must be test-only or protected by explicit non-production configuration. Never ship a debug endpoint that can corrupt authoritative state.

## Reporting
Record seed, profile, environment, injected fault, expected behavior, actual behavior, invariant results, recovery path and residual risk.


<!-- ===== FILE: 16_REFERENCE_WORLD_QUALIFICATION_STANDARD.md ===== -->

# Reference World & Worldness Qualification Standard

A serious reference world is a black-box client of Wanxiang Core, not a collection of Core special cases.

## Mandatory synthetic reference world
The synthetic world is release-critical because it is legally clean, deterministic and fully controllable. It must include multiple places, people, organizations, schedules, objects with custody and information payloads, public/private knowledge, body constraints, duties/norms, events/challenges and at least one human embodiment scenario.

## Required worldness evidence
- persistence independent of session;
- spatiotemporal continuity;
- material/container/custody continuity;
- life/body continuity;
- social/organizational continuity;
- cognitive/knowledge continuity;
- causal continuity;
- character/persona continuity where applicable;
- control handoff continuity;
- canon/source continuity for source-backed worlds;
- replay/verifiability;
- projection independence.

## Required scenario shape
Build/install package → instantiate → autonomous advance → human takeover → object/message transfer → user exit → background advance → re-entry → fork branch → counterfactual/no-intervention run → replay → semantic diff.

## Real reference worlds
Red Chamber, family, heritage and campaign slices are source/rights gated. Real-data absence may be EXTERNAL_BLOCKED for that slice only. Synthetic domain fixtures must still exercise the generic capability.


<!-- ===== FILE: 17_PRODUCTION_OPERATIONS_STANDARD.md ===== -->

# Production & Operations Standard

Productionization means reproducible operation, not merely Docker files.

Required concerns: typed config, secret handling, health/readiness, production DB qualification, background work semantics, durable assets, observability, authz, rate/resource controls, backup/restore, release artifacts, migration preflight, rollback/fallback policy, capacity benchmarks and operator runbooks.

The baseline private/staging profile should stay as simple as evidence permits. Do not introduce microservices, queues or caches without a failure-domain/performance reason. Every additional stateful component creates new migration, backup, security and observability obligations.

Production deployments must never default to deterministic test Fakes. Development/tests must remain runnable without paid external services.


<!-- ===== FILE: 18_SDK_ECOSYSTEM_STANDARD.md ===== -->

# SDK, Plugin & World Pack Ecosystem Standard

The ecosystem claim is proven only when an external project can build a package without importing repository-private code or changing Core.

Required: stable public SDK boundary, semver/deprecation policy, authoring CLI/scaffold, schema validation, package conformance certification, plugin trust/capability policy, registry lifecycle, version pinning, dependency resolution, external black-box sample and tested documentation.

Executable plugins are a security boundary. If strong sandboxing is not implemented, say so and use a trusted/signed executable extension policy. Data-only packages must not gain code execution.

Publishing a new package version must never silently alter an existing World Instance pinned to an older version.


<!-- ===== FILE: 19_PRODUCT_SURFACE_COMPLETION_STANDARD.md ===== -->

# Product Surface Completion Standard

All product faces are projections/control surfaces over the same server truth. Studio, Experience, Strategy, Family, Heritage, Learn and operator/admin tools must not create parallel domain models or persistence authorities.

Required UX engineering properties: generated/shared types, explicit world/instance/branch/session/perspective context, revision-aware commands, reconnect/resync, loading/error/empty states, server-side authorization, auditable privileged operations, responsive baseline and critical-path E2E tests.

A surface is not complete if it displays a static fixture while the backend feature exists elsewhere. Production paths must call real APIs/use-cases; test demos are clearly separated.


<!-- ===== FILE: 20_RESEARCH_EXPANSION_V5_1_V6.md ===== -->

# v5.1 / v6 Research Expansion Rules

M16 explores capabilities beyond the release-qualified v5.0-R1 stable baseline. It is an experiment program, not permission to destabilize Core.

Every track requires: baseline, hypothesis, implementation seam, deterministic fallback/fake where applicable, benchmark, failure analysis, data/model/seed/version provenance and a final decision: PROMOTE, KEEP_EXPERIMENTAL or REJECT.

Experiments include AI-assisted compilation, persona/memory research, cognitive LOD, world-model planning, generative assets, digital human/XR, multi-simulator federation, reality/digital-twin streams and distributed hosting.

No research model has Commit Authority. No model output becomes source-backed fact without Source/Evidence/Review. Stable feature flags OFF must keep M15 behavior and regression green.


<!-- ===== FILE: 21_FINAL_CERTIFICATION_STANDARD.md ===== -->

# Final Certification Standard

M17 is independent from “the developer says it works.” It must reproduce the platform from clean artifacts and use black-box public contracts.

Minimum final evidence:
- complete mother-spec traceability;
- clean-room build/deploy/upgrade/restore/replay;
- final security/reliability/chaos rerun;
- external-author SDK/package flow;
- end-user persistent reference-world flow;
- operator recovery flow;
- final performance/capacity and known limitations;
- exact EXTERNAL_BLOCKED items;
- M16 research promotion/rejection decisions;
- local release checkpoint with no automatic push/deploy.

Stable P0/P1 gaps must be zero for M17 PASS.


<!-- ===== FILE: 22_FULL_PROGRAM_MAP_M0_M17.md ===== -->

# Wanxiang Full Engineering Program Map — M0 → M17

## Stable implementation program already defined before this pack

- M0 — reproducible engineering foundation
- M1 — authoritative canonical world kernel
- M2 — living world substrate
- M3 — agency, cognition and action runtime
- M4 — world definition/compiler/evidence/packages
- M5 — host, human embodiment and projection
- M6 — reality bridge, challenge, Director and experiment runtime
- M7 — domain generality: literature/family/heritage
- M8 — co-simulation and campaign/strategy
- M9 — release qualification, SDK baseline and advanced projection seams

M0–M9 establish the broad v5.0-R1 implementation. They are not repeated by this pack.

## Post-M9 proof and completion program

- M10 — independent verification and P0/P1 gap closure
- M11 — adversarial/failure/security/resilience qualification
- M12 — full synthetic reference world, source-gated real reference slices and worldness certification
- M13 — productionization, operations, deployment, backup, security, observability and capacity
- M14 — stable SDK/plugin/package ecosystem and black-box third-party authoring
- M15 — product surface completion over one authoritative world
- M16 — isolated v5.1/v6 research expansion with promote/keep/reject decisions
- M17 — final clean-room, black-box, security/reliability and release certification

## Why M10–M17 are separate

The original v5.0-R1 G0–G12 roadmap remains the implementation roadmap. M10–M17 are a verification/productization/research continuation program. This avoids retroactively changing the meaning of G0–G12 and allows all post-M9 evidence to be audited independently.

## Final stable completion rule

Stable Wanxiang completion does not mean every M16 experiment is promoted. It means:

1. M10–M15 stable gates PASS;
2. M16 research tracks are executed and honestly classified;
3. M17 final certification PASS;
4. stable P0/P1 gaps are zero;
5. real-source/provider blockers are explicit rather than fabricated;
6. the release candidate can be reproduced from repository artifacts and local Git history.


<!-- ===== FILE: 23_POST_M9_HANDOFF_PROTOCOL.md ===== -->

# Post-M9 Handoff & Repository Integration Protocol

## Purpose
This pack must be merged into the **existing** Wanxiang repository after the M0–M9 program. It is not a new repository bootstrap.

## Preserve
Never delete/reinitialize merely to install this pack:

- `.git/` and current branch/history;
- production source and tests;
- migrations and persisted test fixtures;
- `docs/spec/WANXIANG_v5_MASTER_SPEC.md`;
- previous Engineering Program Architecture/standards/acceptance files;
- `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`;
- existing `reports/` and acceptance evidence.

## First Codex action
The first action remains independent verification, not new feature coding. Read M9 evidence and run critical regressions, then begin G13A baseline capture.

## If M9 is not actually healthy
Do not blindly continue. Record the regression in the post-M9 baseline and repair the smallest root cause needed to restore the claimed stable checkpoint. Do not restart G0–G12 or replace the repository wholesale.

## Naming and versioning
M10–M17 are program milestones, not a silent change to the v5.0-R1 product specification. Stable code/version changes follow the repository's existing release/version policy. M16 experiments remain explicitly experimental unless promoted by ADR and final regression.

## External blockers
Approved source corpora, private family records, real museum data, Liaoshen sources, external digital-human providers, physical sensors or cloud infrastructure may be unavailable. Such absence blocks only the exact real integration slice. Generic platform behavior, synthetic fixtures, interfaces, deterministic adapters, Source Gate and failure tests must still be completed.


<!-- ===== FILE: CODEX_COPY_PASTE_POST_M9.txt ===== -->

Continue the Wanxiang project after the claimed M0-M9 completion. Do not restart G0 and do not trust prior PASS claims blindly.

First read `11_CODEX_POST_M9_MASTER_PROMPT.md`, then all normative files it references, current repository ledgers/reports/Git state, and verify the M9 checkpoint.

Then execute `12_POST_M9_GOALS_INDEX.md` continuously from G13A through G20E, running each `milestones/M10_QUALIFICATION.md` through `M17_QUALIFICATION.md` gate in order.

Do not stop for routine confirmation between milestones. Keep all existing architecture invariants, tests, migrations, replay/branch compatibility, rights/source gates and code-quality rules. Real external data/provider/hardware may narrowly become EXTERNAL_BLOCKED, but internal generic capability and deterministic tests must continue.

M16 research must remain experimental/feature-flagged and cannot destabilize stable defaults.

Do not push or deploy externally unless separately authorized. Stop only after M17 final certification and local checkpoint, then report exact PASS/FAIL/EXTERNAL_BLOCKED evidence, remaining limitations and research promotion decisions.


<!-- ===== FILE: goals/GOAL_G13A_POST_M9_BASELINE_FREEZE_INDEPENDENT_EVIDENCE_CAPTURE.md ===== -->

# G13A — Post-M9 Baseline Freeze & Independent Evidence Capture

> Milestone: M10
> Depends on: M9 qualified checkpoint
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Establish an independent, reproducible post-M9 audit baseline before any new fixes, so later claims can be compared against immutable repository and runtime evidence.

## Scope

- Capture Git branch/HEAD/worktree, dependency lock state, schema/migration heads, generated OpenAPI/SDK state, test inventory and deployment manifests.
- Run all currently advertised M9 qualification commands without editing production code first.
- Inventory every report that claims PASS and map it to concrete tests, commands and artifacts.
- Create machine-readable audit baseline with hashes for key specs, schemas, migrations and generated contracts.

## Non-goals

- Do not fix defects during the first evidence pass except if a command cannot run because the audit harness itself is missing.
- Do not reinterpret missing evidence as PASS.
- Do not delete or rewrite prior M0-M9 reports.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- This Goal is read-mostly: preserve the baseline so later closure work can be compared against it.

## Deliverables

- reports/POST_M9_BASELINE.md
- reports/post_m9_baseline.json
- reports/POST_M9_COMMAND_MATRIX.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create reports/POST_M9_BASELINE.md and reports/post_m9_baseline.json.
- Record exact command lines, exit codes and summarized outputs.
- Record test collection counts and skipped/xfail tests with reasons.
- Record all TODO/FIXME/NotImplemented/pass/placeholder/static-fake signals without yet classifying severity.
- Record current DB migration head and perform a disposable clean bootstrap.
- Record current API schema hash and SDK generation hash if applicable.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Baseline command rerun must be reproducible from a clean shell.
- A clean checkout/bootstrap smoke test must either PASS or produce a concrete blocker.
- No prior PASS may be accepted without an evidence pointer.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- POST_M9_BASELINE has repository SHA, environment assumptions, command matrix and evidence locations.
- All missing/ambiguous evidence is marked GAP_CANDIDATE rather than silently accepted.
- Baseline is committed before gap fixes begin.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13a: post-m9 baseline freeze & independent evidence capture`.
- Record final commit SHA in `reports/G13A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G13B_DESIGN_TO_IMPLEMENTATION_TRACEABILITY_MATRIX.md ===== -->

# G13B — Design-to-Implementation Traceability Matrix

> Milestone: M10
> Depends on: G13A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Build a clause-level traceability system from the v5.0-R1 mother specification and M0-M9 program contracts to production implementation, tests and runtime evidence.

## Scope

- Extract normative MUST/SHALL/不可/必须/only-authority style requirements from the design and engineering program.
- Map each requirement to owner package/module, public contract, tests, migration/version implications and runtime evidence.
- Classify each as VERIFIED, PARTIAL, GAP, EXTERNAL_BLOCKED or NOT_APPLICABLE with rationale.
- Include the 5 Planes/16 Kernels, hierarchy, one Commit Authority, Source Gate, Rights, Event/Replay/Branch, Host, Projection, CoSim and worldness criteria.

## Non-goals

- Do not mark a requirement VERIFIED solely because a class/interface exists.
- Do not use model knowledge to fill missing product requirements.
- Do not collapse multiple independent requirements into a vague single row.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Traceability is an audit artifact, not a substitute for tests.

## Deliverables

- reports/DESIGN_IMPLEMENTATION_TRACEABILITY.md
- reports/design_implementation_traceability.json
- reports/KERNEL_COVERAGE_SUMMARY.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create a stable requirement ID scheme (e.g. WX-SPEC-...).
- Generate reports/DESIGN_IMPLEMENTATION_TRACEABILITY.md plus machine-readable JSON/CSV-like representation.
- Link requirements to exact test names and implementation symbols/paths.
- Flag orphan production features that have no design owner and design requirements with no implementation owner.
- Create a coverage summary by Kernel, cross-cutting concern and product surface.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Traceability parser/validator checks unique IDs and valid statuses.
- Every G00A-G12H claimed deliverable has at least one trace row or explicit supersession note.
- Every one of the 16 logical kernels has concrete implementation and test ownership or a GAP.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No P0 architecture requirement is left UNMAPPED.
- The matrix can drive deterministic gap extraction in G13H/G13I.
- External-data requirements remain distinctly EXTERNAL_BLOCKED and do not mask generic capability gaps.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13b: design-to-implementation traceability matrix`.
- Record final commit SHA in `reports/G13B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G13C_ARCHITECTURE_DEPENDENCY_CANONICAL_MUTATION_FORENSICS.md ===== -->

# G13C — Architecture, Dependency & Canonical-Mutation Forensics

> Milestone: M10
> Depends on: G13B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Independently prove that the implemented repository still obeys the architecture boundaries after M0-M9 growth, especially the single Commit Authority and dependency direction.

## Scope

- Trace every production write path that can affect world state.
- Audit imports/dependencies between domain/application/runtime/persistence/API/projection/plugin/model-provider packages.
- Detect direct ORM/DB access from forbidden layers, route business logic, mutable global state and hidden side effects.
- Audit package/domain plugin extension points for accidental privileged mutation.

## Non-goals

- Do not rely only on existing architecture tests; inspect source graph and runtime call graph where feasible.
- Do not refactor unrelated style issues in this audit-only Goal.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Never “solve” an architecture test by weakening the test or adding allowlists without ADR evidence.

## Deliverables

- reports/ARCHITECTURE_FORENSICS.md
- reports/DEPENDENCY_GRAPH.md
- reports/CANONICAL_MUTATION_PATHS.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Generate an import/dependency graph and forbidden-edge report.
- Search for direct repository/session usage outside approved adapters/use-cases.
- Instrument or test commit entry points to prove canonical mutations have one authority path.
- Audit projections, simulators, Reality Bridge, Director, LLM/model providers and clients for mutation bypasses.
- Record cycle, ownership and privilege findings.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Architecture tests intentionally introduce representative forbidden imports in test fixtures and must detect them.
- Mutation-bypass tests attempt direct state writes from projection/model/plugin paths and must fail.
- Import-cycle detector runs on production packages.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No unapproved canonical mutation path exists.
- Any architecture violation becomes P0 or P1 gap with owner and fix target.
- The report distinguishes logical kernel boundaries from physical package layout.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13c: architecture, dependency & canonical-mutation forensics`.
- Record final commit SHA in `reports/G13C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G13D_PLACEHOLDER_FAKE_DEAD_PATH_SURFACE_INTEGRATION_AUDIT.md ===== -->

# G13D — Placeholder, Fake, Dead-path & Surface Integration Audit

> Milestone: M10
> Depends on: G13C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Find false completion: placeholders, mock-only paths, static responses, unconnected UI, dead adapters, duplicated schemas and code that exists but is not reachable in a real vertical slice.

## Scope

- Scan production code, routes, frontend data sources, adapters, sample worlds and generated SDKs.
- Differentiate legitimate deterministic Fake adapters in tests from fake production behavior.
- Verify Studio/Phaser/Host/API paths consume real server state and submit real commands where design says they should.
- Identify dead code and duplicate or drifting models.

## Non-goals

- Do not delete test Fakes that implement a formal Port contract.
- Do not demand real external services where the spec allows a Fake for deterministic qualification.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Prefer removal of unused speculative abstractions over preserving dead complexity.

## Deliverables

- reports/FALSE_COMPLETION_AUDIT.md
- reports/SURFACE_INTEGRATION_MAP.md
- reports/SCHEMA_DRIFT_AUDIT.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create automated placeholder/dead-code scanning rules with allowlisted documented exceptions.
- Trace UI API calls to server handlers/use cases and back to canonical projections.
- Inspect hardcoded JSON/static world state and ensure it is fixture content, not production truth.
- Compare Python/OpenAPI/TypeScript schemas for drift.
- Classify dead adapters as remove, wire, or explicitly experimental.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- E2E smoke test must fail if frontend is switched to canned data.
- Schema generation drift test must detect manually edited generated clients.
- Production placeholder scanner has zero unexplained high-confidence findings.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No P0/P1 feature is “complete” only through static/mock behavior.
- All disconnected production paths are placed in gap backlog.
- Test fakes are clearly namespaced and never selected by production default configuration.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13d: placeholder, fake, dead-path & surface integration audit`.
- Record final commit SHA in `reports/G13D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G13E_EVENT_REPLAY_BRANCH_MIGRATION_VERSION_FORENSICS.md ===== -->

# G13E — Event, Replay, Branch, Migration & Version Forensics

> Milestone: M10
> Depends on: G13D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Re-verify the semantic-history foundation under all features added after M1 and detect any event/version/migration behavior that could silently corrupt historical worlds.

## Scope

- Audit event schemas and evolution, snapshot schemas, package versions, DB migrations, replay upcasters if any, branch ancestry and deterministic semantic hashes.
- Replay representative M2-M9 world histories from clean state.
- Verify old instance/package version pinning does not silently adopt new semantics.
- Audit correction-event and immutable-history policy.

## Non-goals

- Do not rewrite historical fixtures to make new runtime tests pass without recording an intentional migration/upcast.
- Do not treat current-state database rows as authoritative history.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Historical truth is corrected with new events/branches or explicit migration semantics, never silent mutation.

## Deliverables

- reports/HISTORY_COMPATIBILITY_FORENSICS.md
- reports/REPLAY_GOLDEN_CORPUS.md
- reports/VERSION_COMPATIBILITY_MATRIX.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Collect persisted event versions and compare to runtime handlers.
- Build a compatibility matrix: old events/snapshots/packages/DB → current runtime.
- Replay parent/child branches and verify ancestry/isolation.
- Run migration forward, restore backup, and where supported downgrade/rollback policy tests.
- Detect silent defaulting of unknown/new fields that changes semantic meaning.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Golden replay corpus produces stable semantic hashes.
- Unsupported event version fails explicitly.
- Version-pinned instance behavior test protects against package upgrade drift.
- Migration on representative old DB fixtures preserves event/replay invariants.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No unresolved P0 replay or migration corruption risk.
- All supported/unsupported compatibility ranges are documented.
- Every schema change mechanism has an explicit owner and test.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13e: event, replay, branch, migration & version forensics`.
- Record final commit SHA in `reports/G13E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G13F_SECURITY_RIGHTS_PROVENANCE_PRIVACY_SOURCE_GATE_FORENSICS.md ===== -->

# G13F — Security, Rights, Provenance, Privacy & Source-Gate Forensics

> Milestone: M10
> Depends on: G13E
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Independently audit whether security and epistemic safeguards survive end-to-end integration, including source prompt-injection isolation and rights enforcement at import, storage, projection and export.

## Scope

- Audit authn/authz boundaries, RightsEnvelope evaluation, provenance retention, source review gates, privacy classes and projection/export filters.
- Test malicious source content that attempts to instruct the compiler/model.
- Inspect logs/traces/backups for secrets or private data leakage.
- Audit generated/digital-human labels and real-person/minor safeguards where implemented.

## Non-goals

- Do not mark real-world source correctness PASS without approved sources.
- Do not weaken rights checks to make reference packs easier to load.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Security fixes that change public behavior require ADR/API compatibility review.

## Deliverables

- reports/SECURITY_RIGHTS_SOURCE_FORENSICS.md
- reports/THREAT_MODEL_POST_M9.md
- reports/RIGHTS_ENFORCEMENT_MATRIX.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13F_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create threat model/update existing threat model.
- Run source-gate adversarial fixtures: unapproved, revoked, denied-commercial, conflicting claims, malicious prompt content.
- Trace rights decisions from import to projection/export.
- Scan repository/config/log examples for secrets.
- Audit normal-user ability to delete/alter audit records.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Unapproved sources cannot enter canonical compiled facts.
- Conflicting claims coexist with provenance.
- Denied rights block relevant export/projection.
- Prompt-injection text in a source remains data, not instruction.
- Secret scanning and privacy-log tests pass.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No P0/P1 rights/source/security bypass remains unclassified.
- External real-source availability is separate from gate correctness.
- Security findings have severity, exploit path and closure owner.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13f: security, rights, provenance, privacy & source-gate forensics`.
- Record final commit SHA in `reports/G13F_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G13G_MAINTAINABILITY_COMPLEXITY_TEST_QUALITY_UPGRADEABILITY_AUDIT.md ===== -->

# G13G — Maintainability, Complexity, Test Quality & Upgradeability Audit

> Milestone: M10
> Depends on: G13F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Measure whether the codebase remains readable, modifiable and upgradeable rather than merely functional after broad implementation.

## Scope

- Audit file/function/class size, cyclomatic complexity, duplication, unstable dependency direction, generic utils/managers/services, test brittleness, fixture coupling and generated-code boundaries.
- Audit Python/JS dependency freshness constraints without forcing risky upgrades.
- Review public typing and error model consistency.
- Identify refactoring hotspots before product/reference-world growth.

## Non-goals

- Do not upgrade every dependency simply because a newer version exists.
- Do not split coherent code mechanically just to satisfy line counts.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Prefer explicit small domain concepts to generic abstractions with broad responsibility.

## Deliverables

- reports/MAINTAINABILITY_AUDIT.md
- reports/UPGRADEABILITY_AUDIT.md
- reports/TEST_QUALITY_AUDIT.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Produce complexity/size/duplication/import-cycle reports.
- List files over the engineering threshold and classify justified vs refactor-needed.
- Find broad Any/untyped public APIs and exception swallowing.
- Detect tests that only assert implementation details rather than behavior.
- Create upgrade seams report for DB, API, event schema, package SDK and projections.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Quality tooling runs in CI or a documented local gate.
- Representative architecture/behavior tests survive safe refactor of internals.
- No unexplained God Object or giant generic module remains P0/P1.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- P0/P1 maintainability risks are converted to concrete closure tasks.
- Code-quality exceptions have owner, rationale and expiry/review trigger.
- No “rewrite later” hotspot is left untracked.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13g: maintainability, complexity, test quality & upgradeability audit`.
- Record final commit SHA in `reports/G13G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G13H_P0_GAP_CLOSURE_WAVE.md ===== -->

# G13H — P0 Gap Closure Wave

> Milestone: M10
> Depends on: G13G
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Close every internally actionable P0 gap found by G13A-G13G before any adversarial or reference-world expansion.

## Scope

- Fix canonical mutation bypass, data-loss/replay corruption, branch contamination, security/rights critical bypass, migration data loss, fake production truth, critical crash inconsistency and build/test blockers.
- Add regression tests before/with fixes.
- Update traceability statuses only after evidence exists.

## Non-goals

- Do not defer P0 to later milestones.
- Do not use EXTERNAL_BLOCKED for internal engineering defects.
- Do not perform unrelated feature expansion.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- A failing P0 acceptance blocks the program from M11.

## Deliverables

- reports/P0_GAP_BACKLOG.md
- reports/P0_CLOSURE_REPORT.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13H_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create reports/P0_GAP_BACKLOG.md with IDs, owners, root cause and closure evidence.
- Fix in small reviewable commits/checkpoints.
- Run affected regression plus full core invariant suite after each cluster.
- Update ADRs when architecture behavior changes.
- Re-run security/replay/migration checks touched by fixes.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Each fixed P0 has a regression test reproducing the original failure when practical.
- Full M1-M9 critical regression remains green after closure.
- No P0 status remains OPEN.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- P0 open count = 0.
- No fix introduces a canonical bypass or compatibility regression.
- Traceability and acceptance matrix point to post-fix evidence.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13h: p0 gap closure wave`.
- Record final commit SHA in `reports/G13H_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G13I_P1_P2_GAP_CLOSURE_M10_INDEPENDENT_REQUALIFICATION.md ===== -->

# G13I — P1/P2 Gap Closure & M10 Independent Requalification

> Milestone: M10
> Depends on: G13H
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Close all P1 gaps required for a trustworthy platform, triage P2 debt explicitly, and independently requalify the repository before adversarial testing.

## Scope

- Fix P1 integration, maintainability, observability, rights, compatibility and operational defects.
- Resolve or explicitly schedule P2 items that are not required for M11-M17.
- Re-run traceability and M1-M9 qualification from clean environment.
- Produce M10 verdict.

## Non-goals

- Do not mark P1 DONE without executable evidence.
- Do not force speculative P2 features into stable core.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M10

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- M10 PASS gates M11.

## Deliverables

- reports/P1_P2_GAP_BACKLOG.md
- reports/M10_INDEPENDENT_REQUALIFICATION.md
- reports/DESIGN_IMPLEMENTATION_TRACEABILITY_FINAL_M10.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G13I_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Maintain reports/P1_P2_GAP_BACKLOG.md.
- Re-run clean build, migrations, replay corpus, core worldness tests, source-gate tests, security checks and UI integration smoke.
- Regenerate DESIGN_IMPLEMENTATION_TRACEABILITY with final M10 statuses.
- Create M10 acceptance report and freeze baseline SHA.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- P1 open count required by stable platform = 0.
- All remaining P2 items have explicit rationale and do not invalidate existing design acceptance.
- Clean-room bootstrap and representative M1-M9 flows PASS.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M10 = PASS only when P0=0 and required P1=0.
- No prior report is overwritten; post-M10 evidence is additive.
- Program checkpoint is reproducible from Git.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g13i: p1/p2 gap closure & m10 independent requalification`.
- Record final commit SHA in `reports/G13I_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14A_CONCURRENCY_RACE_IDEMPOTENCY_LOST_UPDATE_ADVERSARIAL_QUALIFICATION.md ===== -->

# G14A — Concurrency, Race, Idempotency & Lost-update Adversarial Qualification

> Milestone: M11
> Depends on: G13I
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Attack concurrent command submission and revision semantics to prove that multi-client activity cannot fork reality accidentally or duplicate effects.

## Scope

- Generate conflicting/non-conflicting concurrent commands across one branch and multiple branches.
- Exercise retries, duplicate command IDs, out-of-order delivery and stale expected revisions.
- Test scheduler/background events racing human commands.

## Non-goals

- Do not rely only on sequential unit tests.
- Do not solve conflicts by globally serializing unrelated worlds unless architecture requires it and benchmark justifies it.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Never weaken expected-revision semantics to improve throughput.

## Deliverables

- reports/CONCURRENCY_ADVERSARIAL.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build deterministic concurrency test harness.
- Inject barriers to force race windows around validation, append and state publication.
- Verify idempotency store semantics across process restart.
- Measure contention and record lock/transaction strategy.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- No lost update.
- Duplicate command produces one semantic effect.
- Stale conflict is explicit and does not append invalid event.
- Independent branches/instances can progress without cross-contamination.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Canonical event sequence remains valid under stress.
- All race failures produce structured errors and audit traces.
- Concurrency strategy documented with performance tradeoffs.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14a: concurrency, race, idempotency & lost-update adversarial qualification`.
- Record final commit SHA in `reports/G14A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14B_CRASH_ATOMICITY_MID_COMMIT_RECOVERY_QUALIFICATION.md ===== -->

# G14B — Crash, Atomicity & Mid-Commit Recovery Qualification

> Milestone: M11
> Depends on: G14A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove that crashes at every important commit boundary cannot leave event history and canonical state in contradictory partial states.

## Scope

- Inject process failure before append, after append, before snapshot/current-state publication, during checkpoint and during host lifecycle transitions.
- Test restart recovery and idempotent retry.

## Non-goals

- Do not fake crash recovery by catching all exceptions inside one process.
- Do not delete corrupt evidence automatically.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Fault-injection hooks must not be enabled in production by default.

## Deliverables

- reports/CRASH_ATOMICITY_MATRIX.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Add fault-injection points or test hooks outside production behavior.
- Run crash matrix across storage adapters used in tests/production.
- Verify recovery chooses authoritative event history.
- Document exactly-once vs at-least-once boundaries.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- After restart, world reconstructs to a valid committed revision.
- No half event/state mutation.
- Retry of acknowledged/unknown command is safely classified.
- Audit log records recovery.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Crash matrix has PASS evidence for every supported transaction boundary.
- Recovery policy is deterministic and documented.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14b: crash, atomicity & mid-commit recovery qualification`.
- Record final commit SHA in `reports/G14B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14C_DATABASE_STORAGE_NETWORK_DEPENDENCY_FAULT_INJECTION.md ===== -->

# G14C — Database, Storage, Network & Dependency Fault Injection

> Milestone: M11
> Depends on: G14B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Verify graceful behavior under unavailable/slow/intermittent persistence and external dependencies without corrupting world truth.

## Scope

- Inject DB disconnect, timeout, disk-full-like errors, object/media storage failure, network delay and dependency cancellation.
- Test background workers and API behavior during faults.

## Non-goals

- Do not require unavailable proprietary chaos tooling; local deterministic fault adapters are acceptable.
- Do not silently drop commands/events.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Prefer fail-closed for canonical mutation when authority cannot be proven.

## Deliverables

- reports/DEPENDENCY_FAULT_INJECTION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create fault profiles and retry/backoff policies.
- Ensure unsafe retries are prevented by idempotency keys.
- Verify degraded/read-only modes where supported.
- Capture operator-visible health state.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Persistence failure never produces success response for an uncommitted command.
- Retry storms are bounded.
- Service can recover without manual DB mutation.
- Health/readiness differentiate degraded from healthy.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Fault policy and recovery runbook are actionable.
- No data-loss defect remains open.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14c: database, storage, network & dependency fault injection`.
- Record final commit SHA in `reports/G14C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14D_EVENT_SNAPSHOT_BRANCH_HISTORY_CORRUPTION_ADVERSARIAL_QUALIFICATION.md ===== -->

# G14D — Event, Snapshot, Branch & History Corruption Adversarial Qualification

> Milestone: M11
> Depends on: G14C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Attack persisted history with gaps, duplicates, wrong branch IDs, hash mismatches, unsupported versions and damaged snapshots to prove corruption is detected rather than normalized away.

## Scope

- Create a versioned corruption fixture corpus.
- Test snapshot fallback/replay policy.
- Test branch ancestry inconsistencies and correction workflow.

## Non-goals

- Do not auto-repair unknown corruption without an explicit repair tool and audit record.
- Do not modify golden fixtures in place.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- History immutability outranks convenience.

## Deliverables

- reports/HISTORY_CORRUPTION_ADVERSARIAL.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Implement validation/diagnostic tooling for event streams and snapshots.
- Generate corruption fixtures for sequence, schema, payload, hash, ancestry and version errors.
- Exercise restore from older checkpoint where policy permits.
- Document operator remediation flow.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Every corruption type is detected with precise error.
- Valid history remains replayable after diagnostic scan.
- Repair actions, if implemented, create auditable new artifacts/events rather than silent mutation.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No corruption test results in silent semantic drift.
- Tooling can identify affected instance/branch/revision.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14d: event, snapshot, branch & history corruption adversarial qualification`.
- Record final commit SHA in `reports/G14D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14E_WORLD_HOST_MULTIPLAYER_RECONNECT_ORDERING_BACKPRESSURE_CHAOS.md ===== -->

# G14E — World Host, Multiplayer, Reconnect, Ordering & Backpressure Chaos

> Milestone: M11
> Depends on: G14D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Stress host lifecycle and network command ordering to prove sessions/projections can disconnect and recover without becoming alternative authorities.

## Scope

- Simulate many clients, reconnects, duplicated messages, slow consumers, projection lag, queue pressure, pause/resume and background simulation.
- Verify EmbodimentLease handoff under disconnect.

## Non-goals

- Do not let client cache become authoritative.
- Do not hide backpressure by unbounded queues.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Correctness before smooth animation.

## Deliverables

- reports/HOST_MULTIPLAYER_CHAOS.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build host chaos harness.
- Test authoritative resync from revision cursor.
- Define queue limits, drop/reject semantics for non-authoritative projection updates vs commands.
- Test lease expiry and shadow/human policy recovery.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Reconnect rebuilds from server projection/history.
- Commands preserve idempotency/revision semantics.
- Slow clients cannot block canonical world indefinitely.
- Lease ownership remains unique according to policy.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Host remains correct under configured stress profile.
- Backpressure/resource limits are observable.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14e: world host, multiplayer, reconnect, ordering & backpressure chaos`.
- Record final commit SHA in `reports/G14E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14F_HOSTILE_PACKAGE_PLUGIN_SOURCE_INPUT_QUALIFICATION.md ===== -->

# G14F — Hostile Package, Plugin & Source Input Qualification

> Milestone: M11
> Depends on: G14E
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Treat packages, compiler inputs and optional plugin code as hostile/untrusted according to the chosen trust model and verify parsing, review and execution boundaries.

## Scope

- Malformed archives, path traversal, oversized files, schema bombs, malicious metadata, prompt injection, dependency conflicts and unauthorized executable extensions.
- Validate package signing/trust metadata where supported.

## Non-goals

- Do not claim OS-level sandboxing unless actually implemented/tested.
- Do not execute arbitrary package code during metadata inspection.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- If strong sandboxing is absent, default to trusted/signed executable plugins and state the limitation.

## Deliverables

- reports/HOSTILE_PACKAGE_SOURCE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14F_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Add package/source fuzz fixtures.
- Enforce file type/size/path constraints.
- Ensure compiler treats source text as data.
- Test dependency resolver conflicts and install rollback.
- Document trusted-code boundary explicitly.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- No path traversal/write outside package staging.
- Rejected package leaves registry/instance unchanged.
- Prompt injection cannot alter system/compiler instructions.
- Executable extension policy is explicit and enforced.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No critical hostile-input bypass.
- Trust model matches implementation, not aspiration.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14f: hostile package, plugin & source input qualification`.
- Record final commit SHA in `reports/G14F_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14G_AUTHORIZATION_RIGHTS_PRIVACY_DATA_LEAK_ADVERSARIAL_QUALIFICATION.md ===== -->

# G14G — Authorization, Rights, Privacy & Data-leak Adversarial Qualification

> Milestone: M11
> Depends on: G14F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Attempt privilege escalation and information leakage across branches, sessions, perspectives, living-person privacy classes and export paths.

## Scope

- Cross-user/session access, guessed IDs, branch leakage, hidden knowledge leakage, private memory access, rights-revoked asset export, audit deletion and backup exposure.
- Exercise API and projection layers.

## Non-goals

- Do not accept UI hiding as authorization.
- Do not use production personal data for tests.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Explicitly document historical/audit retention exceptions to revocation where legally/architecturally required.

## Deliverables

- reports/AUTH_RIGHTS_PRIVACY_ADVERSARIAL.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build adversarial identities/roles with synthetic data.
- Test every sensitive API with insufficient privilege.
- Test rights changes invalidate future projection/export access.
- Inspect caches for cross-tenant/branch leakage.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Unauthorized access consistently denied server-side.
- Perspective filters prevent knowledge leakage.
- Revocation is enforced according to documented semantics.
- Normal users cannot alter audit truth.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- No high/critical authorization or privacy bypass.
- Security evidence is repeatable in CI/staging.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14g: authorization, rights, privacy & data-leak adversarial qualification`.
- Record final commit SHA in `reports/G14G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14H_SIMULATIONADAPTER_EXTERNAL_SYSTEM_BYZANTINE_BEHAVIOR_QUALIFICATION.md ===== -->

# G14H — SimulationAdapter & External-system Byzantine Behavior Qualification

> Milestone: M11
> Depends on: G14G
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove external simulators/sensors can be slow, inconsistent or malicious without owning world truth.

## Scope

- Timeouts, invalid deltas, impossible time ranges, non-monotonic timestamps, conflicting observations, excessive payloads, checkpoint mismatch and simulator crash.
- Reality Bridge observation confidence/provenance handling.

## Non-goals

- Do not auto-commit external simulator output.
- Do not assume external time semantics are trustworthy.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Fail closed on unverifiable canonical mutation proposals.

## Deliverables

- reports/EXTERNAL_SIMULATOR_ADVERSARIAL.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14H_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create Byzantine fake simulator/sensor adapters.
- Validate ValidityEnvelope and assumptions.
- Reject/route invalid proposed deltas through adjudication.
- Test timeout/cancellation and checkpoint restore.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- External bad output cannot mutate canonical state directly.
- Invalid proposal is rejected/audited.
- Timeout does not deadlock host.
- Checkpoint mismatch detected.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Simulation boundary remains a Port/Adapter with explicit failure semantics.
- No external component becomes hidden authority.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14h: simulationadapter & external-system byzantine behavior qualification`.
- Record final commit SHA in `reports/G14H_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G14I_RESOURCE_EXHAUSTION_FUZZ_LONG_RUN_CHAOS_M11_QUALIFICATION.md ===== -->

# G14I — Resource Exhaustion, Fuzz, Long-run Chaos & M11 Qualification

> Milestone: M11
> Depends on: G14H
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Combine load, malformed inputs and long-running faults to establish a resilient operating envelope and complete M11.

## Scope

- CPU/memory pressure, actor/tick volume, event-stream length, branch count, client count, package size, repeated failures and fuzzed structured commands.
- Run representative long chaos session with invariant monitoring.

## Non-goals

- Do not invent production capacity numbers; measure current environment and state assumptions.
- Do not turn off invariants for load tests.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M11

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- M11 PASS gates reference-world qualification.

## Deliverables

- reports/RESOURCE_EXHAUSTION_CHAOS.md
- reports/M11_ADVERSARIAL_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G14I_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Define stress profiles and budgets.
- Run property/fuzz tests over commands/deltas/package inputs.
- Track memory growth and queue depth.
- Re-run M10 critical suites after chaos fixes.
- Create M11 qualification report.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- No invariant violation or unbounded leak under the declared qualification profile.
- Over-budget load fails predictably with backpressure/rejection rather than corruption.
- M11 critical security/history/host adversarial suites PASS.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M11 PASS with explicit tested envelope.
- Unproven scale claims are excluded from release docs.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g14i: resource exhaustion, fuzz, long-run chaos & m11 qualification`.
- Record final commit SHA in `reports/G14I_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15A_REFERENCE_WORLD_CONTRACT_EXTERNAL_PACK_BOUNDARY.md ===== -->

# G15A — Reference World Contract & External Pack Boundary

> Milestone: M12
> Depends on: G14I
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Define the black-box contract a serious reference World Pack must satisfy so world content proves platform generality without being hard-coded into Core.

## Scope

- Specify package composition, sources/evidence/rights, scenarios, fixtures, evaluation cases, assets, domain dependencies and install/upgrade behavior.
- Define black-box acceptance from public SDK/API only.
- Create a reference-world certification manifest.

## Non-goals

- Do not create a Core import dependency on reference content.
- Do not require real copyrighted/historical data for synthetic qualification.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- World Pack is definition; World Instance owns mutable runtime state.

## Deliverables

- docs/REFERENCE_WORLD_CONTRACT.md
- reports/REFERENCE_WORLD_CONTRACT_ACCEPTANCE.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create docs/REFERENCE_WORLD_CONTRACT.md and schema if useful.
- Define required worldness scenarios and evidence output.
- Define version pinning and reproducible package build.
- Create conformance test harness callable against any World Pack.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- A tiny external synthetic pack can be built and installed without modifying Core.
- Conformance harness catches missing rights/source/eval metadata where required.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Reference-world success is measured through public package/runtime contracts.
- Core remains domain-neutral.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15a: reference world contract & external pack boundary`.
- Record final commit SHA in `reports/G15A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15B_COMPREHENSIVE_SYNTHETIC_REFERENCE_WORLD_PACKAGE.md ===== -->

# G15B — Comprehensive Synthetic Reference World Package

> Milestone: M12
> Depends on: G15A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Build a nontrivial synthetic world outside Core that exercises space, time, material custody, bodies, institutions, cognition, action, host, evidence, challenges and projections together.

## Scope

- Use invented people/places/organizations and label all content synthetic.
- Include multiple locations, schedules, roles, private/public knowledge, objects with payload/custody, rules/norms and at least one organization.
- Package via normal compiler/registry install path.

## Non-goals

- Do not encode special-case Core logic for the synthetic world.
- Do not use real-world names presented as factual.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Keep content rich enough to exercise systems but small enough for deterministic CI slices.

## Deliverables

- reference_worlds/synthetic_full/
- reports/SYNTHETIC_REFERENCE_WORLD_BUILD.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Author package content in a separate examples/reference-worlds area.
- Compile, review, install and instantiate through public path.
- Create scenario seeds for autonomous living, human takeover, branching and failure cases.
- Bind evaluation cases into the package.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Fresh checkout can build/install/instantiate the pack.
- Package uninstall/upgrade leaves other worlds intact.
- No import from Core into content code beyond public SDK.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Synthetic reference world becomes the mandatory regression world for future releases.
- All content is clearly synthetic and source-gate semantics are still exercised with synthetic provenance.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15b: comprehensive synthetic reference world package`.
- Record final commit SHA in `reports/G15B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15C_SEVEN_DAY_AUTONOMOUS_LIVING_WORLD_QUALIFICATION.md ===== -->

# G15C — Seven-day Autonomous Living-world Qualification

> Milestone: M12
> Depends on: G15B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Run the comprehensive synthetic world for seven simulated days without a continuously present user and prove continuity of schedules, bodies, relationships, organizations, objects and knowledge.

## Scope

- Autonomous scheduler, actor policies, multi-rate cognition/LOD, events/challenges and host background mode.
- Periodic checkpoints and replay verification.
- Worldness metrics over the run.

## Non-goals

- Do not rely on external LLM for the mandatory deterministic run.
- Do not pre-script every event as a fixed narrative timeline.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- A world that only advances when a user sends chat is a failure.

## Deliverables

- reports/SEVEN_DAY_AUTONOMOUS_WORLDNESS.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create deterministic seven-day scenario with seed.
- Capture periodic semantic hashes/checkpoints.
- Track deadlocks, impossible schedules, object duplication/loss, knowledge leaks and actor starvation.
- Replay final state from authoritative history.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Seven-day run completes with invariants green.
- Replay final semantic hash matches.
- At least several emergent/conditional events arise from rules/policies rather than a single hardcoded script.
- World continues while no user session exists.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Seven-day living-world acceptance PASS.
- Any LLM-enhanced optional run is separately labeled non-deterministic.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15c: seven-day autonomous living-world qualification`.
- Record final commit SHA in `reports/G15C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15D_HUMAN_EMBODIMENT_EXIT_RE_ENTRY_CONTROL_CONTINUITY_QUALIFICATION.md ===== -->

# G15D — Human Embodiment, Exit, Re-entry & Control Continuity Qualification

> Milestone: M12
> Depends on: G15C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove a human can take over a character/body, leave, and later return while the world and shadow/autonomous policy continue coherently.

## Scope

- EmbodimentLease acquisition/release/expiry, first-person perception, human command validation, shadow policy resumption and session reconnection.
- Test conflicting takeover attempts.

## Non-goals

- Do not let user control bypass actor capabilities, physical constraints or Commit Authority.
- Do not freeze the entire world when one user exits.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Session is ephemeral; world instance/branch persists independently.

## Deliverables

- reports/EMBODIMENT_CONTINUITY_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create scenario: user takes role on day 1, exits day 3, world advances, re-enters later.
- Verify role continuity, memory/knowledge boundary and body state.
- Test lease race/expiry and reconnect.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- World advances after user exit.
- Re-entry receives authoritative current perspective.
- No duplicate controller according to policy.
- Human actions remain normal committed actions.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Control continuity worldness criterion PASS.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15d: human embodiment, exit, re-entry & control continuity qualification`.
- Record final commit SHA in `reports/G15D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15E_MATERIAL_CUSTODY_INFORMATION_PROPAGATION_SOCIAL_CONTINUITY_QUALIFICATION.md ===== -->

# G15E — Material Custody, Information Propagation & Social Continuity Qualification

> Milestone: M12
> Depends on: G15D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove objects, messages and information persist and propagate through explicit world mechanisms rather than narrative text shortcuts.

## Scope

- Create letter/document/package custody chains, reading state, secrecy, message transmission delays and social consequences.
- Track relationships/organization duties influenced by information.

## Non-goals

- Do not update every actor belief globally when a message exists.
- Do not represent custody only as prose.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Knowledge propagation must be evidence of perception/communication, not omniscient convenience.

## Deliverables

- reports/MATERIAL_INFORMATION_SOCIAL_CONTINUITY.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create multi-day message scenario with transfers, unread/read states and partial knowledge.
- Assert container/custody invariants.
- Verify observation/belief updates only for actors with access.
- Branch before delivery and compare outcomes.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Object never exists in two exclusive containers simultaneously.
- Unread actor cannot act on hidden message content unless another causal path exists.
- Branch outcomes diverge causally and replay.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Material, information, social and cognitive continuity criteria PASS.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15e: material custody, information propagation & social continuity qualification`.
- Record final commit SHA in `reports/G15E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15F_BRANCH_TIME_TRAVEL_COUNTERFACTUAL_WORLDLINE_COMPARISON_QUALIFICATION.md ===== -->

# G15F — Branch, Time-travel & Counterfactual Worldline Comparison Qualification

> Milestone: M12
> Depends on: G15E
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Demonstrate canon/baseline, intervention and no-intervention worldlines from shared history with reproducible branch comparison.

## Scope

- Fork at chosen revision, apply interventions, run equal horizon, compare semantic state and events.
- Time-travel/read-only historical projection and correction-event policy.
- Experiment result provenance.

## Non-goals

- Do not mutate parent history to create an alternative.
- Do not compare branches using only narrative summaries.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Counterfactuals are simulations, not claims about real history.

## Deliverables

- reports/WORLDLINE_COMPARISON_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15F_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Implement/verify semantic diff reports across branches.
- Run at least three worldlines.
- Persist experiment configuration, package/runtime versions and seeds.
- Verify parent hash unchanged.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Branch ancestry is explicit.
- Each worldline independently replayable.
- Diff highlights causal state/event differences.
- Historical read projection is consistent with revision.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Causal continuity and branch isolation criteria PASS.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15f: branch, time-travel & counterfactual worldline comparison qualification`.
- Record final commit SHA in `reports/G15F_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15G_EXTENDED_90_DAY_VIRTUAL_RUN_POPULATION_LOD_QUALIFICATION.md ===== -->

# G15G — Extended 90-day Virtual Run & Population-LOD Qualification

> Milestone: M12
> Depends on: G15F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Extend worldness beyond a seven-day showcase and verify long-horizon stability, memory metabolism and population scheduling under controlled scale.

## Scope

- Run 90 simulated days or an equivalent deterministic horizon feasible in CI/staging.
- Use active/background/dormant population LOD.
- Measure memory/event growth, scheduler fairness and replay checkpoint strategy.

## Non-goals

- Do not claim real-time 90-day hosting if only accelerated simulation was tested.
- Do not retain every ephemeral cognition artifact forever without policy.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Scale claims always state hardware/profile/seed/runtime versions.

## Deliverables

- reports/NINETY_DAY_WORLDNESS_AND_LOD.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Define scalable profiles (small CI, larger staging).
- Track event count, snapshot interval, memory size, actor update distribution and CPU/memory.
- Test LOD transitions preserve semantic continuity.
- Replay sampled checkpoints.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- No unbounded growth beyond documented retention/model assumptions.
- Dormant actors resume consistently.
- No scheduler starvation for required duties/events.
- Semantic replay spot checks match.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Long-horizon operating envelope documented and PASS at declared profile.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15g: extended 90-day virtual run & population-lod qualification`.
- Record final commit SHA in `reports/G15G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15H_RED_CHAMBER_SOURCE_GATED_QUALIFIED_REFERENCE_SLICE.md ===== -->

# G15H — Red Chamber Source-gated Qualified Reference Slice

> Milestone: M12
> Depends on: G15G
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Build or requalify the mother-spec Red Chamber minimal seven-day reference slice using only approved source material and explicit canon/completion/model provenance.

## Scope

- Source Gate, versioned literary sources, character/world packages, schedules, etiquette/duties, objects/messages, takeover, branch comparison and seven-day scenario.
- Preserve canon vs completion vs generated content labels.

## Non-goals

- Do not fabricate canon from model memory.
- Do not attempt the entire novel unless approved sources and separate scope exist.
- Do not let this real-data slice block synthetic M12 acceptance.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- The mother-spec minimal slice is the acceptance scope, not “whole Red Chamber.”

## Deliverables

- reports/RED_CHAMBER_REFERENCE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15H_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Audit sources/red_chamber manifests and rights.
- If approved sources exist, compile pack and run reference cases from mother spec.
- If unavailable, keep generic compiler/tests complete and mark only content slice EXTERNAL_BLOCKED with exact missing source/rights needs.
- Generate provenance report for every canonical claim used.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Unapproved material cannot compile as canonical.
- When sources are available, seven-day reference acceptance passes.
- Canon/completion/model-derived content remains distinguishable in projection/audit.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Status is PASS or narrowly EXTERNAL_BLOCKED; never fabricated PASS.
- Core changes for Red Chamber are prohibited unless they generalize and pass synthetic world regression.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15h: red chamber source-gated qualified reference slice`.
- Record final commit SHA in `reports/G15H_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15I_FAMILY_HERITAGE_CAMPAIGN_SOURCE_GATED_REFERENCE_SUITES.md ===== -->

# G15I — Family, Heritage & Campaign Source-gated Reference Suites

> Milestone: M12
> Depends on: G15H
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove domain generality across genealogy/family, museum/heritage and campaign/co-simulation using approved real data where available and synthetic black-box fixtures otherwise.

## Scope

- GEDCOM roundtrip/conflicting claims/privacy; IIIF/Linked Art/CIDOC/semantic twin/reconstruction; campaign logistics/fog-of-war/co-sim/validity envelope.
- Use public domain-package interfaces only.

## Non-goals

- Do not invent real family facts, museum facts or campaign history.
- Do not share domain-specific database tables directly with Core.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Domain generality is a core architecture claim; special-case hacks are P0/P1 gaps.

## Deliverables

- reports/MULTI_DOMAIN_REFERENCE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15I_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Run synthetic conformance suites for all three domains.
- Attempt source-gated real pack import if approved fixtures exist.
- Verify rights/privacy/source provenance and export boundaries.
- Run branch/replay on each domain.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Synthetic suites PASS for all domains.
- Real slices are PASS or precisely EXTERNAL_BLOCKED.
- No domain requires Core special casing.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- At least four distinct domain families (literature, family, heritage, campaign) prove package generality.
- Blocked real content does not invalidate platform generality.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15i: family, heritage & campaign source-gated reference suites`.
- Record final commit SHA in `reports/G15I_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G15J_CROSS_DOMAIN_WORLDNESS_CERTIFICATION_M12_QUALIFICATION.md ===== -->

# G15J — Cross-domain Worldness Certification & M12 Qualification

> Milestone: M12
> Depends on: G15I
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Consolidate reference-world evidence against the mother-spec true-world criteria and certify that the platform behaves as a Persistent Living World OS rather than an interactive narrative application.

## Scope

- Evaluate persistence, spatiotemporal/material/life/social/cognitive/causal/character/control/canon continuity, verifiability/replay and projection independence.
- Run black-box public-API tests against synthetic reference world.
- Summarize source-gated reference statuses.

## Non-goals

- Do not mark a criterion PASS from architecture diagrams alone.
- Do not make real-world factual claims from synthetic tests.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M12

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- M12 PASS gates productionization.

## Deliverables

- reports/WORLDNESS_CERTIFICATION.md
- reports/M12_REFERENCE_WORLD_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G15J_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create criterion-by-criterion evidence matrix.
- Run clean build → install pack → instantiate → operate → leave → advance → rejoin → fork → replay → compare.
- Have tests assert projections can be discarded/rebuilt.
- Create M12 report.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- All mandatory synthetic worldness criteria PASS.
- No projection owns exclusive state.
- Reference packs remain portable/versioned.
- Real data blocks are isolated.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M12 PASS and reference-world certification artifact produced.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g15j: cross-domain worldness certification & m12 qualification`.
- Record final commit SHA in `reports/G15J_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16A_PRODUCTION_TOPOLOGY_CONFIGURATION_SECRET_MANAGEMENT_FOUNDATION.md ===== -->

# G16A — Production Topology, Configuration & Secret-management Foundation

> Milestone: M13
> Depends on: G15J
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Freeze production/staging/private-deploy topology and configuration contracts so the same application can be deployed reproducibly without secrets in code.

## Scope

- Environment profiles, config validation, secrets injection, service boundaries justified by actual scaling/isolation needs, health/readiness and runtime feature flags.
- Document modular-monolith vs worker separation decisions.

## Non-goals

- Do not split into microservices merely for appearance.
- Do not commit real credentials.
- Do not make local dev require production infrastructure.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Only split components when performance, isolation, deployment or failure-domain evidence justifies it.

## Deliverables

- docs/PRODUCTION_TOPOLOGY.md
- reports/CONFIG_SECRET_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create deployment ADR/topology diagrams.
- Centralize typed configuration and validation.
- Provide example env without secrets.
- Verify startup fails clearly for missing required production config.
- Document process/service ownership.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Secret scanner passes.
- Dev/test still run offline with deterministic defaults.
- Production profile does not silently use test Fake adapters.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Topology is reproducible and minimal for current evidence.
- Configuration changes are versioned/documented.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16a: production topology, configuration & secret-management foundation`.
- Record final commit SHA in `reports/G16A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16B_POSTGRESQL_PRODUCTION_PERSISTENCE_MIGRATION_QUALIFICATION.md ===== -->

# G16B — PostgreSQL Production Persistence & Migration Qualification

> Milestone: M13
> Depends on: G16A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Qualify the authoritative persistence model on PostgreSQL while preserving SQLite/local deterministic development where supported.

## Scope

- Schema creation, migrations, transactions, concurrency semantics, indexes, backups and replay on PostgreSQL.
- Compare semantic behavior across supported persistence adapters.

## Non-goals

- Do not rewrite domain models around PostgreSQL-specific ORM behavior.
- Do not claim production DB support from dialect compilation alone.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Storage adapter differences must not change world semantics.

## Deliverables

- reports/POSTGRES_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create integration profile using ephemeral/containerized PostgreSQL when environment permits.
- Run full migration chain from empty and representative old versions.
- Run concurrency/atomicity/replay suites.
- Review indexes/query plans for hot paths.
- Document DB version support.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- PostgreSQL integration PASS in reproducible environment or precise EXTERNAL_BLOCKED only if container/runtime unavailable.
- Semantic hashes match storage-independent expectations.
- No direct DB dependency leaks into domain.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Production persistence acceptance produced.
- Migration and restore procedures tested.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16b: postgresql production persistence & migration qualification`.
- Record final commit SHA in `reports/G16B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16C_BACKGROUND_EXECUTION_WORK_QUEUE_SCHEDULER_RELIABILITY.md ===== -->

# G16C — Background Execution, Work Queue & Scheduler Reliability

> Milestone: M13
> Depends on: G16B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Productionize background world advancement and long-running jobs with explicit delivery/idempotency semantics and bounded resource use.

## Scope

- Host scheduler, package compilation jobs, batch experiments and asset tasks as applicable.
- Choose in-process vs external queue based on measured need and deployment topology.
- Retry/dead-letter/cancellation semantics.

## Non-goals

- Do not introduce Redis/Celery/Kafka by default without evidence.
- Do not let a worker bypass Commit Authority.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Select the simplest reliable queue consistent with tested deployment needs.

## Deliverables

- reports/BACKGROUND_EXECUTION_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Document work-item contract and idempotency key.
- Implement reliable queue adapter appropriate to architecture.
- Test duplicate delivery, worker crash, cancellation and backpressure.
- Expose job status/trace.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- At-least-once delivery cannot duplicate semantic effects.
- Failed job is diagnosable/retryable according to policy.
- Queue pressure cannot corrupt world.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Background operations are production-operable with clear ownership.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16c: background execution, work queue & scheduler reliability`.
- Record final commit SHA in `reports/G16C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16D_ASSET_OBJECT_STORAGE_MEDIA_RIGHTS_DURABLE_ARTIFACT_HANDLING.md ===== -->

# G16D — Asset/Object Storage, Media Rights & Durable Artifact Handling

> Milestone: M13
> Depends on: G16C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Productionize durable storage for package assets, media, generated artifacts and museum/digital-human resources without conflating blobs with canonical semantic truth.

## Scope

- Content addressing/checksums, metadata/provenance, signed/authorized access, retention, deletion/revocation semantics and backup.
- Local filesystem adapter for dev and object-storage-compatible production seam where needed.

## Non-goals

- Do not store large binaries in event payloads.
- Do not expose asset URLs without rights/perspective checks.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Semantic truth remains in canonical state/events; blob store is durable content storage.

## Deliverables

- reports/ASSET_STORAGE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Define AssetRef contract and integrity hash.
- Implement/test storage Port adapters.
- Verify upload type/size/malicious path checks.
- Test missing/corrupt blob behavior and rights-filtered access.
- Document retention/backups.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Blob corruption detected.
- Asset metadata remains replayable/referentially valid.
- Denied rights prevent delivery.
- Canonical events refer to immutable identity/version, not mutable anonymous paths.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Durable artifact storage qualified at declared profile.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16d: asset/object storage, media rights & durable artifact handling`.
- Record final commit SHA in `reports/G16D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16E_OPENTELEMETRY_OBSERVABILITY_SLOS_OPERATIONAL_DIAGNOSTICS.md ===== -->

# G16E — OpenTelemetry Observability, SLOs & Operational Diagnostics

> Milestone: M13
> Depends on: G16D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Make runtime behavior operable: traces, metrics and structured logs correlate world commands through adjudication/commit/host/background jobs without exposing sensitive data.

## Scope

- OpenTelemetry-compatible tracing, metrics for commit/replay/host/queue/resource budgets, structured logs and dashboards/runbook queries.
- Define initial SLO/SLA-like internal targets as engineering objectives, not marketing claims.

## Non-goals

- Do not log private memory/source secrets by default.
- Do not require a specific commercial observability backend.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Observability must not become a new authority or leak private state.

## Deliverables

- docs/OBSERVABILITY_RUNBOOK.md
- reports/OBSERVABILITY_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Propagate trace/run/world/branch/command/commit IDs.
- Instrument latency/error/queue/replay/actor-call/cost metrics.
- Provide local collector or no-op/exporter option.
- Create diagnostic runbook and example queries.
- Test redaction.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- A failing E2E command can be traced across layers.
- Metrics expose failure and saturation signals.
- Sensitive fixture data is redacted according to policy.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Operational observability is sufficient to diagnose qualified failure scenarios.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16e: opentelemetry observability, slos & operational diagnostics`.
- Record final commit SHA in `reports/G16E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16F_PRODUCTION_SECURITY_HARDENING_AUTHN_AUTHZ_RATE_LIMITS_SUPPLY_CHAIN_CONTROLS.md ===== -->

# G16F — Production Security Hardening, AuthN/AuthZ, Rate Limits & Supply-chain Controls

> Milestone: M13
> Depends on: G16E
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Harden the production boundary with explicit identity/authorization, abuse controls and software supply-chain evidence.

## Scope

- Authentication integration seam, RBAC/ABAC according to Rights/role model, CSRF/CORS/session policy as applicable, rate/resource limits, secret scanning, dependency audit, SBOM and container/user hardening.
- Protect admin/source-review/audit operations.

## Non-goals

- Do not invent SSO provider secrets.
- Do not rely on frontend authorization.
- Do not auto-upgrade vulnerable major versions without compatibility testing.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Security exceptions require severity, owner, mitigation and review date.

## Deliverables

- reports/PRODUCTION_SECURITY_QUALIFICATION.md
- artifacts/SBOM_INFO.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16F_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create security configuration guide.
- Add server-side authorization tests.
- Add rate/size limits for sensitive endpoints.
- Generate SBOM and dependency vulnerability report using available tooling.
- Harden containers/process privileges.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Unauthorized actions denied.
- Abusive request profile bounded.
- No known critical unmitigated dependency issue in shipped profile or explicit documented exception.
- Secrets not baked into images.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Production security gate PASS at current release scope.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16f: production security hardening, authn/authz, rate limits & supply-chain controls`.
- Record final commit SHA in `reports/G16F_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16G_BACKUP_RESTORE_PITR_LIKE_RECOVERY_DISASTER_GAME_DAY.md ===== -->

# G16G — Backup, Restore, PITR-like Recovery & Disaster Game Day

> Milestone: M13
> Depends on: G16F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove recoverability of authoritative events, snapshots, package metadata and required assets through documented backup/restore procedures.

## Scope

- Full backup, incremental/log-based recovery where supported, restore to clean environment, branch/world validation and asset integrity.
- Run disaster scenarios.

## Non-goals

- Do not claim true PITR if the chosen storage/DB profile does not implement it.
- Do not test backup by checking only file existence.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Backups themselves follow encryption/access/privacy policy.

## Deliverables

- docs/DISASTER_RECOVERY_RUNBOOK.md
- reports/DISASTER_GAME_DAY.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Define RPO/RTO engineering targets for current profile.
- Automate backup and integrity verification.
- Restore into isolated environment.
- Replay worlds and compare semantic hashes.
- Run accidental deletion/corrupt-current-state game day.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Restored canonical worlds match expected semantic hashes to recovery point.
- Backup includes required package/schema/version metadata.
- Restore runbook is executable by a fresh operator.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Disaster recovery PASS at declared capability.
- Unimplemented advanced PITR is named accurately.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16g: backup, restore, pitr-like recovery & disaster game day`.
- Record final commit SHA in `reports/G16G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16H_CI_CD_RELEASE_ARTIFACTS_ROLLING_MIGRATION_ROLLBACK_QUALIFICATION.md ===== -->

# G16H — CI/CD, Release Artifacts, Rolling Migration & Rollback Qualification

> Milestone: M13
> Depends on: G16G
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Create a release pipeline that builds, tests, signs/hashes and promotes reproducible artifacts while protecting schema/event compatibility.

## Scope

- CI quality gates, container/package builds, migration preflight, deployment smoke, rollback strategy, release notes and artifact provenance.
- Staging promotion path.

## Non-goals

- Do not auto-deploy to a real production environment without user authorization.
- Do not allow release pipeline to bypass failing core tests.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Deployment execution to external infrastructure remains user-controlled.

## Deliverables

- docs/RELEASE_PROCESS.md
- reports/CI_CD_RELEASE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16H_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Define required CI jobs and branch/release gates.
- Build reproducible-ish artifacts with version/SHA metadata.
- Test upgrade from previous release fixture and rollback/fallback policy.
- Generate release manifest/checksums.
- Create local/staging deployment smoke script.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- A clean tag/SHA produces the same declared build inputs and traceable artifact metadata.
- Migration preflight blocks incompatible deployment.
- Rollback/fallback behavior documented and tested for supported cases.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Release pipeline can produce a candidate without manual code edits.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16h: ci/cd, release artifacts, rolling migration & rollback qualification`.
- Record final commit SHA in `reports/G16H_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16I_PERFORMANCE_CAPACITY_COST_RESOURCE_BUDGET_QUALIFICATION.md ===== -->

# G16I — Performance, Capacity, Cost & Resource-budget Qualification

> Milestone: M13
> Depends on: G16H
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Measure and document operating envelopes for commits, replay, hosting, actor scheduling, projections, batch experiments and package operations.

## Scope

- Benchmarks for latency/throughput/memory/storage growth under named profiles.
- Optional model-provider cost hooks without requiring paid APIs.
- Identify bottlenecks before distributed redesign.

## Non-goals

- Do not claim internet-scale or MMO-scale without measurements.
- Do not optimize by weakening invariants/evidence/rights.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Optimize evidence-based bottlenecks, not speculative abstractions.

## Deliverables

- reports/PERFORMANCE_CAPACITY_COST.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16I_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create repeatable benchmark suite.
- Profile hot paths.
- Measure snapshot/replay tradeoffs.
- Measure active/background/dormant actor scheduling.
- Define resource budgets and regression thresholds.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Benchmark results include hardware/environment.
- No severe regression against M9/M12 baseline without ADR.
- Budget violations are visible in CI/staging where feasible.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Capacity report drives future scaling decisions.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16i: performance, capacity, cost & resource-budget qualification`.
- Record final commit SHA in `reports/G16I_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G16J_PRIVATE_STAGING_DEPLOYMENT_OPERATOR_RUNBOOKS_M13_PRODUCTION_QUALIFICATION.md ===== -->

# G16J — Private/Staging Deployment, Operator Runbooks & M13 Production Qualification

> Milestone: M13
> Depends on: G16I
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove a clean operator can deploy, initialize, monitor, back up, upgrade and recover a private/staging Wanxiang installation using documented procedures.

## Scope

- Docker Compose/private install path from mother spec, optional separate workers as justified, health checks, seed admin, source/package install, reference world smoke, backup/restore and upgrade.
- Operational documentation and release readiness.

## Non-goals

- Do not claim public SaaS production launch.
- Do not require proprietary cloud services for the baseline private deployment.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M13

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- External production DNS/cloud billing/TLS issuance may remain environment-specific.

## Deliverables

- reports/M13_PRODUCTION_QUALIFICATION.md
- docs/OPERATIONS_INDEX.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G16J_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Run clean-room deployment in disposable environment.
- Instantiate synthetic reference world and run core flow.
- Exercise logs/metrics/backup/upgrade.
- Have scripts fail clearly on missing prerequisites.
- Create M13 report.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- A new environment can be brought up from repository/release artifacts and docs.
- Reference world survives restart/upgrade.
- Operator can diagnose a seeded failure using runbook.
- Security baseline enabled.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M13 PASS; production foundation is release-operable at declared private/staging scope.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g16j: private/staging deployment, operator runbooks & m13 production qualification`.
- Record final commit SHA in `reports/G16J_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G17A_PUBLIC_SDK_CONTRACT_SEMANTIC_VERSIONING_COMPATIBILITY_POLICY.md ===== -->

# G17A — Public SDK Contract, Semantic Versioning & Compatibility Policy

> Milestone: M14
> Depends on: G16J
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Freeze the stable extension surface for third-party Domain/World/Experience/Projection packages without exposing internal implementation details.

## Scope

- Public Python SDK, OpenAPI/TypeScript SDK boundaries, event/package schema compatibility policy, deprecation and support ranges.
- Separate stable vs experimental namespaces.

## Non-goals

- Do not expose ORM sessions, Commit internals or private runtime objects as SDK convenience.
- Do not promise indefinite compatibility beyond documented policy.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M14

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- SDK does not grant canonical mutation authority.

## Deliverables

- docs/SDK_COMPATIBILITY_POLICY.md
- reports/SDK_API_BASELINE.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G17A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Inventory public symbols/endpoints.
- Mark internal APIs.
- Create semantic versioning/deprecation policy.
- Add API/SDK compatibility snapshot tests.
- Document extension points and forbidden dependencies.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Third-party code can perform supported operations through SDK only.
- Breaking changes are detected by compatibility tests.
- Experimental APIs are clearly labeled.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Stable extension surface documented and test-enforced.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g17a: public sdk contract, semantic versioning & compatibility policy`.
- Record final commit SHA in `reports/G17A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G17B_PACKAGE_AUTHORING_CLI_SCAFFOLDER_SCHEMA_VALIDATION.md ===== -->

# G17B — Package Authoring CLI, Scaffolder & Schema Validation

> Milestone: M14
> Depends on: G17A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Make it practical to create a new Domain/World/Scenario/Experience package with correct structure, manifests, schemas, tests and local validation.

## Scope

- CLI scaffold commands, schema generation/templates, validate/build/test/pack commands, deterministic fixtures and docs.
- Support current compiler v0.1 formats and package standards.

## Non-goals

- Do not generate giant boilerplate.
- Do not hide schema errors behind auto-fixing that changes semantics.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M14

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Generated templates prefer explicit examples over magic.

## Deliverables

- docs/PACKAGE_AUTHORING_CLI.md
- reports/PACKAGE_CLI_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G17B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Implement CLI scaffold for representative package types.
- Generate minimal tests and manifests.
- Provide validate/build dry-run.
- Integrate dependency/source/rights checks.
- Create upgrade helper seam.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Generated package passes baseline lint/schema/conformance without manual repair.
- Invalid manifest produces actionable errors.
- Scaffold has no dependency on Wanxiang internal modules.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Authoring workflow usable from clean external directory.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g17b: package authoring cli, scaffolder & schema validation`.
- Record final commit SHA in `reports/G17B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G17C_EXTERNAL_AUTHOR_DOCUMENTATION_REFERENCE_TEMPLATES.md ===== -->

# G17C — External Author Documentation & Reference Templates

> Milestone: M14
> Depends on: G17B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Create documentation that allows a developer unfamiliar with Core internals to build a correct package from public contracts.

## Scope

- Quickstart, conceptual hierarchy, source/evidence/rights, state/action boundaries, tests, versioning, publishing, debugging and migration.
- Reference templates for at least one simple domain/world/experience.

## Non-goals

- Do not require reading internal source code as a normal authoring step.
- Do not duplicate the entire mother spec.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M14

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Documentation examples are version-pinned and tested.

## Deliverables

- docs/sdk/EXTERNAL_AUTHOR_GUIDE.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G17C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Write external-author guide.
- Create diagrams/examples.
- Add troubleshooting and common anti-patterns.
- Ensure commands in docs are executable in tests/doc CI where possible.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- A clean-room authoring exercise follows docs successfully.
- Examples use only public SDK.
- Docs distinguish definition content from runtime instance state.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Documentation is sufficient for black-box third-party use.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g17c: external author documentation & reference templates`.
- Record final commit SHA in `reports/G17C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G17D_THIRD_PARTY_PACKAGE_CONFORMANCE_CERTIFICATION_HARNESS.md ===== -->

# G17D — Third-party Package Conformance & Certification Harness

> Milestone: M14
> Depends on: G17C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Provide an automated suite that certifies package structure, schemas, dependencies, rights/source metadata, deterministic install/instantiate behavior and forbidden privileged access.

## Scope

- Static validation plus runtime black-box tests.
- Certification result machine-readable and human-readable.
- Profiles for Domain/World/Experience/Projection packages.

## Non-goals

- Do not certify real-world factual correctness beyond provided evidence/source metadata.
- Do not execute untrusted arbitrary code without chosen trust controls.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M14

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Certification covers platform conformance, not legal endorsement.

## Deliverables

- reports/PACKAGE_CERTIFICATION_HARNESS.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G17D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build `wanxiang package certify` or equivalent.
- Run package in isolated temp environment.
- Check install/uninstall/upgrade and smoke instance.
- Check forbidden imports/private API use.
- Emit certification report.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Known-bad fixtures fail for expected reasons.
- Reference external package passes.
- Certification output includes runtime/SDK/package versions.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Conformance harness becomes release gate for bundled examples.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g17d: third-party package conformance & certification harness`.
- Record final commit SHA in `reports/G17D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G17E_PLUGIN_TRUST_SIGNING_CAPABILITY_PERMISSIONS_ISOLATION_POLICY.md ===== -->

# G17E — Plugin Trust, Signing, Capability Permissions & Isolation Policy

> Milestone: M14
> Depends on: G17D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Resolve the executable-extension trust model and enforce permissions so plugin convenience cannot become unrestricted filesystem/network/database/commit access.

## Scope

- Trusted vs data-only packages, signing/verifier seam, capability declarations, install authorization, optional subprocess isolation and audit.
- Document unsupported sandbox guarantees honestly.

## Non-goals

- Do not claim secure sandboxing if only Python imports are restricted.
- Do not allow unsigned arbitrary executable code by default in protected profiles.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M14

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- OS-level sandboxing may be future work unless actually delivered.

## Deliverables

- docs/PLUGIN_TRUST_MODEL.md
- reports/PLUGIN_TRUST_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G17E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create plugin trust ADR.
- Implement metadata/signature verification seam with deterministic test keys.
- Declare capabilities and enforce at adapter boundary.
- Audit plugin calls.
- Test denied filesystem/network/commit capabilities at application boundary.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Protected profile rejects unauthorized executable plugin.
- Capability escalation fails.
- Data-only packages cannot execute code.
- Audit identifies plugin/version/action.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Trust model is implementable, tested and documented.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g17e: plugin trust, signing, capability permissions & isolation policy`.
- Record final commit SHA in `reports/G17E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G17F_REGISTRY_PUBLISH_INSTALL_UPGRADE_DEPRECATION_DEPENDENCY_RESOLUTION.md ===== -->

# G17F — Registry Publish, Install, Upgrade, Deprecation & Dependency Resolution

> Milestone: M14
> Depends on: G17E
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Complete lifecycle semantics for sharing versioned packages through a registry without silently changing running worlds.

## Scope

- Publish metadata/artifact hashes, dependency constraints, install, pin, upgrade candidate, deprecation/yank policy, compatibility checks and rollback.
- Local/private registry baseline.

## Non-goals

- Do not auto-upgrade running instances.
- Do not allow yanking to erase historical reproducibility.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M14

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Version reproducibility outranks auto-update convenience.

## Deliverables

- reports/REGISTRY_LIFECYCLE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G17F_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Implement/test registry lifecycle.
- Pin instance to package versions.
- Resolve conflicts deterministically.
- Preserve old artifact metadata for replay when policy requires.
- Provide offline/private registry mode.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Existing instance behavior unchanged when new package version published.
- Upgrade requires explicit action/migration.
- Dependency conflict produces actionable failure.
- Deprecated package remains identifiable for old world history.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Registry lifecycle qualified.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g17f: registry publish, install, upgrade, deprecation & dependency resolution`.
- Record final commit SHA in `reports/G17F_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G17G_BLACK_BOX_EXTERNAL_SAMPLE_PACK_BUILT_OUTSIDE_CORE_REPOSITORY_INTERNALS.md ===== -->

# G17G — Black-box External Sample Pack Built Outside Core Repository Internals

> Milestone: M14
> Depends on: G17F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prove the SDK/ecosystem claim by authoring a nontrivial sample package as if by a third party, using only installed public artifacts and docs.

## Scope

- Create in an external temp/project directory, package/build/certify/publish to local registry/install into Wanxiang/instantiate/run.
- Include at least one custom domain rule or skill through permitted extension mechanism.

## Non-goals

- Do not import repository-private modules or use relative path hacks.
- Do not edit Core to make the sample pass.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M14

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Any required Core change must be generalized and re-run M10-M13 regression.

## Deliverables

- reports/EXTERNAL_SAMPLE_PACK_BLACKBOX.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G17G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Automate clean-room external project creation.
- Use published/local-built SDK package.
- Run certification and reference scenario.
- Upgrade sample v1→v2 with pinned old instance.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Sample works without Core source-tree imports.
- Old instance remains pinned/replayable.
- New instance can use v2 after explicit install/upgrade.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- External extensibility is demonstrated, not assumed.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g17g: black-box external sample pack built outside core repository internals`.
- Record final commit SHA in `reports/G17G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G17H_ECOSYSTEM_DOCUMENTATION_CERTIFICATION_M14_QUALIFICATION.md ===== -->

# G17H — Ecosystem Documentation, Certification & M14 Qualification

> Milestone: M14
> Depends on: G17G
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Consolidate SDK, authoring, trust, registry and black-box evidence into an ecosystem-ready qualification.

## Scope

- Run full external author flow from clean environment.
- Validate all docs links/commands and compatibility snapshots.
- Produce support/deprecation matrix.

## Non-goals

- Do not equate technical certification with marketplace/legal approval.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M14

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- M14 PASS gates product-surface completion.

## Deliverables

- reports/M14_SDK_ECOSYSTEM_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G17H_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Run docs/SDK examples.
- Rebuild/publish/install external sample.
- Run conformance harness.
- Re-run Core architecture boundary tests.
- Create M14 report.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- A third-party developer can add a world without modifying Core.
- Stable public APIs have compatibility tests.
- Trust/registry policy enforced.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M14 PASS.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g17h: ecosystem documentation, certification & m14 qualification`.
- Record final commit SHA in `reports/G17H_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G18A_PRODUCT_SURFACE_INFORMATION_ARCHITECTURE_SERVER_TRUTH_CONTRACT.md ===== -->

# G18A — Product Surface Information Architecture & Server-truth Contract

> Milestone: M15
> Depends on: G17H
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Map the mother-spec product faces to concrete applications/routes/use-cases while ensuring every surface consumes the same authoritative server world and shared design system.

## Scope

- Studio, Experience, Strategy, Heritage, Family, Learn, SDK/operator/admin surfaces as applicable.
- Define shared navigation, auth, world/instance/branch context and projection contracts.
- Audit duplicate frontend state models.

## Non-goals

- Do not build separate backend truth stores per product surface.
- Do not redesign Core semantics for UI convenience.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M15

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- UI is projection/control plane, never canonical authority.

## Deliverables

- docs/PRODUCT_SURFACE_ARCHITECTURE.md
- reports/PRODUCT_SURFACE_CONTRACT_AUDIT.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G18A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create product-surface map and route ownership.
- Freeze frontend domain types from generated schemas.
- Define loading/error/empty/offline states.
- Create shared context selectors for world/branch/session/perspective.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Changing branch/session context updates surfaces from server truth.
- No surface writes world state outside command APIs.
- Shared types do not drift from OpenAPI/SDK.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Product UI architecture is coherent and maintainable.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g18a: product surface information architecture & server-truth contract`.
- Record final commit SHA in `reports/G18A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G18B_STUDIO_WORLD_IDE_COMPLETION.md ===== -->

# G18B — Studio / World IDE Completion

> Milestone: M15
> Depends on: G18A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Turn the debug Studio vertical slice into a maintainable World IDE for package inspection, instance control, branch/replay debugging and evidence-aware world authoring workflows.

## Scope

- World/package browser, entity/state/projection inspector, event timeline, branch diff, command console with validation, source/evidence/rights views, compiler/review status and diagnostics.
- Preserve role/perspective restrictions.

## Non-goals

- Do not add arbitrary DB editing.
- Do not let debug tools bypass Commit Authority in normal mode.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M15

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Keep components small and state ownership explicit.

## Deliverables

- reports/STUDIO_WORLD_IDE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G18B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Implement modular Studio panels/routes.
- Use server APIs/SDK only.
- Add deep links to world/branch/revision/entity.
- Add safe read-only historical views.
- Add Playwright E2E flows.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Studio can diagnose a failed command and replay/branch state without direct DB access.
- Dangerous admin actions require explicit privilege and audited use-case.
- No canned world data in production path.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Studio supports engineering/authoring operations without becoming a backdoor.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g18b: studio / world ide completion`.
- Record final commit SHA in `reports/G18B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G18C_EXPERIENCE_PLAYER_WEB_2D_CONTINUITY_COMPLETION.md ===== -->

# G18C — Experience Player Web/2D Continuity Completion

> Milestone: M15
> Depends on: G18B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Complete the end-user experience path so text/React/Phaser projections can enter, observe, act, disconnect and return to the same living world.

## Scope

- World/scenario selection, session start, perspective, embodiment, movement/actions, messages, branch selection where allowed, reconnect/resync and accessibility baseline.
- Responsive/loading/error states.

## Non-goals

- Do not duplicate game-state simulation on the client.
- Do not require 3D/XR to pass.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M15

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Visual polish must not compromise semantic correctness.

## Deliverables

- reports/EXPERIENCE_PLAYER_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G18C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Replace any residual fake data.
- Implement revision-aware command submission.
- Handle stale command/reconnect UX.
- Verify projection filters.
- Add E2E leave-and-return flow while background world advances.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- User returns to authoritative advanced world.
- Client resync works after dropped connection.
- All actions route through server command pipeline.
- Keyboard/basic accessibility checks pass.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Experience surface demonstrates persistent-world continuity.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g18c: experience player web/2d continuity completion`.
- Record final commit SHA in `reports/G18C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G18D_STRATEGY_EXPERIMENT_WORKBENCH_COMPLETION.md ===== -->

# G18D — Strategy / Experiment Workbench Completion

> Milestone: M15
> Depends on: G18C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Provide an operator/research surface for branching, batch experiments, CoSim runs, validity envelopes and worldline comparison without confusing simulation results with canonical real-world truth.

## Scope

- Experiment definition, seed/version capture, run status, metrics/results, branch diff, validity assumptions, export and rerun.
- Campaign and generic scenarios.

## Non-goals

- Do not present counterfactual result as historical fact.
- Do not let workbench directly edit event history.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M15

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Distinguish exploratory simulation from evidence-backed historical mode.

## Deliverables

- reports/STRATEGY_WORKBENCH_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G18D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build experiment forms from typed contracts.
- Show assumptions/ValidityEnvelope prominently.
- Support deterministic rerun and result provenance.
- Add cancellation/retry UX consistent with backend jobs.
- E2E experiment flow.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Same experiment config/seed reproduces deterministic result where applicable.
- Result links to package/runtime versions and branch ancestry.
- Invalid simulator proposal is visible as rejected, not hidden.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Strategy surface is evidence-aware and reproducible.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g18d: strategy / experiment workbench completion`.
- Record final commit SHA in `reports/G18D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G18E_FAMILY_PORTAL_COMPLETION.md ===== -->

# G18E — Family Portal Completion

> Milestone: M15
> Depends on: G18D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Provide a privacy-first family/genealogy experience using the family domain contracts, conflicting claims and living-person rights rather than flattening everything into a single tree truth.

## Scope

- GEDCOM import/export status, person/relationship views, claim/evidence conflicts, timelines, media rights, living-person privacy and branch/scenario exploration.
- Digital persona modes only within existing rights policy.

## Non-goals

- Do not invent missing family facts.
- Do not expose living-person private data by default.
- Do not merge conflicting claims silently.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M15

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Privacy and provenance are product behavior, not footnotes.

## Deliverables

- reports/FAMILY_PORTAL_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G18E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build views from rights-filtered API.
- Show provenance/confidence/conflict state.
- Implement private/public perspective tests.
- Add GEDCOM roundtrip UX and error reporting.
- E2E privacy tests.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Conflicting claims remain visible as conflicts.
- Unauthorized user cannot see protected living-person fields/media.
- Export preserves supported source references.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Family surface respects evidence/privacy semantics end-to-end.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g18e: family portal completion`.
- Record final commit SHA in `reports/G18E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G18F_HERITAGE_MUSEUM_WORKBENCH_COMPLETION.md ===== -->

# G18F — Heritage / Museum Workbench Completion

> Milestone: M15
> Depends on: G18E
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Provide museum/heritage workflows for object semantic twins, IIIF/Linked Art/CIDOC mappings, conservation/reconstruction scenarios and rights-aware public/curator projections.

## Scope

- Object biography/timeline, source metadata, digital/physical/reconstruction separation, 3D asset binding, conservation history, scenario assumptions and rights/cultural restrictions.
- Curator vs public modes.

## Non-goals

- Do not present reconstructions as original fact.
- Do not bypass cultural/rights restrictions for rich media.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M15

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Projection richness cannot erase evidence uncertainty.

## Deliverables

- reports/HERITAGE_WORKBENCH_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G18F_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build object and scenario views.
- Render IIIF/media through authorized asset path.
- Expose model/version/assumptions for reconstruction.
- Add E2E public vs curator tests.
- Verify links back to evidence.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Physical/digital/reconstruction states are visibly distinct.
- Rights prevent restricted projection/export.
- Conservation history remains auditable.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Heritage surface preserves semantic and rights distinctions.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g18f: heritage / museum workbench completion`.
- Record final commit SHA in `reports/G18F_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G18G_LEARN_CHALLENGE_EXPERIENCE_COMPLETION.md ===== -->

# G18G — Learn / Challenge Experience Completion

> Milestone: M15
> Depends on: G18F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Complete learning/challenge product flows using LearnerState, PracticeRecord, AssessmentEvidence, capability progression and Opportunity/Challenge runtime rather than isolated quizzes.

## Scope

- Challenge discovery, attempt, world action, evidence capture, assessment, capability delta and learning biography.
- Synthetic/reference learning scenarios.

## Non-goals

- Do not equate reward points with capability evidence.
- Do not mutate persona because a skill score changed unless separate justified PersonaDelta exists.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M15

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Learning claims must be tied to evidence and declared assessment logic.

## Deliverables

- reports/LEARN_CHALLENGE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G18G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Build learner dashboard and challenge flow.
- Connect assessment to Evidence/Capability contracts.
- Show longitudinal learning worldline.
- Add deterministic challenge tests and E2E flow.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Learning artifact/assessment evidence is traceable.
- Capability changes are separated from persona changes.
- Challenge affects world through normal action/commit path.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Learn surface demonstrates integrated world-based learning.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g18g: learn / challenge experience completion`.
- Record final commit SHA in `reports/G18G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G18H_OPERATOR_ADMIN_SOURCE_RIGHTS_EVALUATION_CONSOLE_M15_QUALIFICATION.md ===== -->

# G18H — Operator/Admin/Source/Rights/Evaluation Console & M15 Qualification

> Milestone: M15
> Depends on: G18G
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Complete operational product surfaces for source review, package registry, rights decisions, evaluation runs, world host lifecycle and health while enforcing least privilege and auditability.

## Scope

- Admin roles, source review queue, completion ledger, rights decisions, package lifecycle, host controls, evaluation reports, health/metrics links and audit browsing.
- Accessibility and responsive baseline across product surfaces.

## Non-goals

- Do not expose raw secret/config mutation casually.
- Do not allow audit deletion by normal operators.
- Do not bypass normal use-cases with direct DB tools.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M15

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- M15 is productization of existing semantics, not a redefinition of the product.

## Deliverables

- reports/M15_PRODUCT_SURFACE_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G18H_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Implement/administer privileged actions through audited application services.
- Add role matrix tests.
- Run cross-surface Playwright suite.
- Run accessibility checks.
- Create M15 product qualification report.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- All major product faces connect to same backend truth.
- Privileged operations are server-authorized/audited.
- No major surface relies on placeholder data.
- Critical E2E flows PASS.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M15 PASS with product-surface evidence matrix.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g18h: operator/admin/source/rights/evaluation console & m15 qualification`.
- Record final commit SHA in `reports/G18H_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19A_RESEARCH_NAMESPACE_FEATURE_FLAGS_BENCHMARKS_PROMOTION_RULES.md ===== -->

# G19A — Research Namespace, Feature Flags, Benchmarks & Promotion Rules

> Milestone: M16
> Depends on: G18H
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Create a safe experimental architecture for v5.1/v6 research so new AI/world-model/distributed ideas can be tested without destabilizing the release-qualified core.

## Scope

- Experimental package namespace, feature flags, benchmark datasets/fixtures, result registry, reproducibility metadata and promote/reject ADR template.
- Stable/experimental API separation.

## Non-goals

- Do not enable experimental features by production default.
- Do not grant experiments Commit Authority bypass.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Research code is disposable until evidence justifies promotion.

## Deliverables

- docs/RESEARCH_GOVERNANCE.md
- reports/M16_RESEARCH_BASELINE.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create research governance docs.
- Add feature flag/config boundaries.
- Define baseline benchmarks from M12/M13.
- Create experiment result manifest with code/data/model/seed versions.
- Add regression gate comparing stable-off behavior.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Turning all experimental flags off yields M15-equivalent behavior.
- Experimental failure cannot corrupt canonical worlds.
- Every research track has promote/reject criteria.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Research environment is isolated and reproducible.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19a: research namespace, feature flags, benchmarks & promotion rules`.
- Record final commit SHA in `reports/G19A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19B_AI_ASSISTED_WORLD_COMPILER_SEMANTIC_EXTRACTION_RESEARCH.md ===== -->

# G19B — AI-assisted World Compiler Semantic Extraction Research

> Milestone: M16
> Depends on: G19A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prototype model-assisted extraction of entities, claims, relations and candidate world definitions while preserving source spans, uncertainty, review and Source Gate.

## Scope

- Optional LLM/model provider behind Port, deterministic fake, structured candidate outputs, evidence-span binding and human review.
- Evaluate extraction quality on synthetic/public fixtures when available.

## Non-goals

- Do not auto-promote model extraction to canonical truth.
- Do not require paid API for core tests.
- Do not use unapproved copyrighted sources.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- No model memory is a source.

## Deliverables

- reports/AI_COMPILER_RESEARCH.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Define extraction schema.
- Implement provider interface and deterministic fixture provider.
- Bind each candidate to source location/provenance/confidence.
- Create review diff and rejection flow.
- Benchmark precision/recall-like metrics where labels exist.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Model output remains Candidate/Claim.
- Prompt injection source fixture cannot change system behavior.
- Core compiler works with AI disabled.
- Evaluation report includes uncertainty/failure modes.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Research prototype either meets promotion threshold or remains experimental with clear findings.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19b: ai-assisted world compiler semantic extraction research`.
- Record final commit SHA in `reports/G19B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19C_LONG_HORIZON_PERSONA_MEMORY_METABOLISM_DRIFT_EVALUATION_RESEARCH.md ===== -->

# G19C — Long-horizon Persona, Memory Metabolism & Drift Evaluation Research

> Milestone: M16
> Depends on: G19B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Research stronger long-horizon character continuity with persona graph/life arc/dual memory while measuring drift rather than hiding it behind summaries.

## Scope

- Memory retrieval/metabolism, fact vs interpretation separation, identity kernel, persona delta gating and anonymous decision consistency tests.
- Optional LLMPolicy evaluation behind adapters.

## Non-goals

- Do not overwrite factual memory with persona summary.
- Do not make persona mutable on every skill update.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Fact memory and persona-conditioned interpretation remain distinct.

## Deliverables

- reports/PERSONA_MEMORY_RESEARCH.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create long-horizon character benchmark scenarios.
- Measure persona consistency, knowledge boundary and relationship update correctness.
- Prototype memory compaction/metabolism strategy with reversible provenance.
- Compare deterministic baseline vs optional model policy.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- No private/unknown facts leak through memory retrieval.
- Compaction preserves required provenance and key events.
- Persona drift metric is reported.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Research result includes promote/reject decision.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19c: long-horizon persona, memory metabolism & drift evaluation research`.
- Record final commit SHA in `reports/G19C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19D_COGNITIVE_LOD_LARGE_POPULATION_SCHEDULING_RESEARCH.md ===== -->

# G19D — Cognitive LOD & Large-population Scheduling Research

> Milestone: M16
> Depends on: G19C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Explore scaling actor cognition and scheduling to much larger populations without pretending every actor runs a full LLM every tick.

## Scope

- Active/background/dormant/crowd aggregate LOD, promotion/demotion triggers, event-driven wakeup, organizational aggregation and fairness.
- Benchmark against M12 profile.

## Non-goals

- Do not trade semantic continuity for silent actor deletion.
- Do not require LLM calls for dormant population.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Aggregate models cannot invent private knowledge for individual actors.

## Deliverables

- reports/COGNITIVE_LOD_RESEARCH.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Prototype alternative LOD scheduler strategies.
- Create population benchmark profiles.
- Measure cost/latency/state error and wakeup correctness.
- Test actor continuity across LOD transitions.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- LOD transition preserves identity/required obligations.
- Declared scale profile improves resource use without invariant failures.
- Benchmark is reproducible.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Winning strategy remains experimental until promotion ADR.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19d: cognitive lod & large-population scheduling research`.
- Record final commit SHA in `reports/G19D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19E_WORLD_MODEL_PLANNER_PROPOSAL_ENGINE_RESEARCH.md ===== -->

# G19E — World-model / Planner Proposal Engine Research

> Milestone: M16
> Depends on: G19D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prototype a learned or heuristic world-model/planner that proposes multi-step actions or deltas while remaining subordinate to Validator/Resolver/Commit Authority.

## Scope

- Proposal API, rollout/simulation branch, uncertainty, plan scoring and safe handoff to action pipeline.
- Deterministic heuristic baseline plus optional learned provider.

## Non-goals

- Do not let planner mutate canonical state.
- Do not train on private/restricted data without rights.
- Do not equate predicted rollout with truth.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Commit Authority remains final authority.

## Deliverables

- reports/WORLD_MODEL_PLANNER_RESEARCH.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Define planner Port and proposal schema.
- Run plans on disposable branches/sandboxes.
- Score validity/goal achievement/cost.
- Reject impossible actions through existing validators.
- Record model/version/seed.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Bad proposal cannot bypass invariants.
- Planner can be disabled with no core regression.
- Rollout results are labeled predictions/simulations.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Research value measured against deterministic baseline.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19e: world-model / planner proposal engine research`.
- Record final commit SHA in `reports/G19E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19F_GENERATIVE_ASSET_SCENE_PIPELINE_SEMANTIC_BINDING_RESEARCH.md ===== -->

# G19F — Generative Asset / Scene Pipeline & Semantic Binding Research

> Milestone: M16
> Depends on: G19E
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prototype generation/import of visual/audio/3D assets that remain semantically bound to canonical entities, versions, rights and provenance.

## Scope

- Asset foundry jobs, generated-asset metadata, scene layout candidates, 3D semantic anchors and regeneration/versioning.
- Use local/fake generators when external APIs unavailable.

## Non-goals

- Do not make generated scene graph the canonical semantic world.
- Do not remove generated-content labels/provenance.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Assets are projections/artifacts, not authority.

## Deliverables

- reports/GENERATIVE_ASSET_RESEARCH.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19F_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Define generated asset manifest.
- Bind assets to entity/revision/package and rights.
- Test regeneration creates new version not silent overwrite.
- Prototype one web/3D projection path.
- Evaluate missing asset fallback.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Asset can be discarded/regenerated without losing world truth.
- Rights/provenance travel with asset.
- Projection remains rebuildable from semantic state.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Research seam proven without Core contamination.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19f: generative asset / scene pipeline & semantic binding research`.
- Record final commit SHA in `reports/G19F_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19G_ADVANCED_DIGITAL_HUMAN_XR_PRESENCE_RESEARCH.md ===== -->

# G19G — Advanced Digital Human / XR Presence Research

> Milestone: M16
> Depends on: G19F
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Explore richer digital-human and XR embodiment/presence while preserving session/lease/perspective/rights semantics and explicit synthetic/generated labels.

## Scope

- Speech/avatar adapter, latency, interruption, identity/voice asset rights, WebXR/Godot/Babylon integration where available.
- Deterministic text fallback remains baseline.

## Non-goals

- Do not clone real people/voices without rights.
- Do not let avatar provider own memory or world state.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Identity/biometric rights are first-class constraints.

## Deliverables

- reports/DIGITAL_HUMAN_XR_RESEARCH.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19G_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Extend gateway contracts experimentally.
- Test disconnect/reconnect and fallback.
- Measure latency and command ordering.
- Verify generated-human labeling and rights metadata.
- Create optional demo on synthetic character.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Provider outage falls back without world corruption.
- All actions remain normal commands.
- No real-person likeness used without explicit approved fixture.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Research result clearly scoped.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19g: advanced digital human / xr presence research`.
- Record final commit SHA in `reports/G19G_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19H_MULTI_SIMULATOR_FEDERATION_CO_SIMULATION_RESEARCH.md ===== -->

# G19H — Multi-simulator Federation & Co-Simulation Research

> Milestone: M16
> Depends on: G19G
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Extend CoSim research toward multiple heterogeneous simulators with time coordination, validity envelopes and conflict resolution while keeping one semantic world authority.

## Scope

- Multiple SimulationAdapters, multi-rate scheduler, checkpoint/restore federation, conflicting delta proposals, causality/time ordering and experiment provenance.
- FMI-inspired contracts where useful.

## Non-goals

- Do not let fastest simulator win conflicts implicitly.
- Do not claim physical validity beyond declared models.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Simulation output is proposed evidence/state change, not unquestioned truth.

## Deliverables

- reports/MULTI_SIM_FEDERATION_RESEARCH.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19H_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create at least two deterministic fake simulators with different rates.
- Test conflict/adjudication policies.
- Benchmark time coordination.
- Persist assumptions/validity envelopes.
- Test partial simulator failure.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Federation can checkpoint/restore reproducibly.
- Conflicts resolved explicitly before commit.
- Failed simulator does not corrupt others/world.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Research findings identify scalability/validity limits.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19h: multi-simulator federation & co-simulation research`.
- Record final commit SHA in `reports/G19H_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19I_REALITY_DIGITAL_TWIN_STREAMING_OBSERVATION_FUSION_RESEARCH.md ===== -->

# G19I — Reality/Digital-twin Streaming & Observation Fusion Research

> Milestone: M16
> Depends on: G19H
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Prototype richer reality coupling using synthetic/local sensor streams and, where available, real authorized feeds while preserving observation provenance/confidence and non-authoritative status.

## Scope

- Streaming ingestion, clock skew, dedupe, confidence, sensor identity, fusion, replayable observation log and privacy.
- Map reality objects to semantic entities.

## Non-goals

- Do not turn sensor stream directly into canonical truth.
- Do not require unavailable hardware for qualification.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Reality bridge observes/proposes; Commit Authority decides world mutation.

## Deliverables

- reports/REALITY_DIGITAL_TWIN_RESEARCH.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19I_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Create synthetic sensor stream generator.
- Test out-of-order/skew/duplicate readings.
- Implement experimental fusion policy.
- Store provenance and validity.
- Run branch-safe reality replay.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Bad/stale observation is rejected or down-weighted per policy.
- Observation history replay is reproducible.
- Real-feed absence is narrowly EXTERNAL_BLOCKED.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Research coupling works with synthetic streams and preserves authority boundaries.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19i: reality/digital-twin streaming & observation fusion research`.
- Record final commit SHA in `reports/G19I_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G19J_DISTRIBUTED_WORLD_HOST_SHARDING_EXPERIMENT_M16_RESEARCH_QUALIFICATION.md ===== -->

# G19J — Distributed World Host / Sharding Experiment & M16 Research Qualification

> Milestone: M16
> Depends on: G19I
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Test whether evidence justifies splitting selected hosting workloads across processes/nodes while preserving branch ordering, ownership and replay semantics; do not distribute by default without benefit.

## Scope

- Partitioning candidates by world/instance/branch, single-writer lease/leader semantics, message ordering, failover experiment, cache invalidation and benchmark.
- Compare against modular-monolith baseline.

## Non-goals

- Do not build a general distributed database.
- Do not sacrifice correctness for synthetic throughput.
- Do not promote distribution if benchmark benefit is marginal.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M16

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Evidence decides architecture.

## Deliverables

- reports/DISTRIBUTED_HOST_RESEARCH.md
- reports/M16_RESEARCH_EXPANSION_QUALIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G19J_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Prototype minimal multi-process/node host adapter if current environment permits.
- Define branch ownership/lease.
- Test failover and duplicate delivery.
- Compare complexity/performance/recovery with baseline.
- Create promotion ADR and M16 report.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- No split-brain canonical commits.
- Failover preserves event order/idempotency.
- If benefit is insufficient, REJECTED is a valid research result and stable system stays monolithic.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M16 PASS means research tracks were executed/evaluated, not that all experiments were promoted.
- Each track has PROMOTE / KEEP_EXPERIMENTAL / REJECT with evidence.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g19j: distributed world host / sharding experiment & m16 research qualification`.
- Record final commit SHA in `reports/G19J_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G20A_FINAL_MOTHER_SPEC_TRACEABILITY_REQUIREMENT_CLOSURE.md ===== -->

# G20A — Final Mother-spec Traceability & Requirement Closure

> Milestone: M17
> Depends on: G19J
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Re-run the complete design-to-implementation matrix after M10-M16 and prove every v5.0-R1 requirement is implemented, explicitly external-blocked, or intentionally experimental/future with non-contradictory rationale.

## Scope

- All 5 Planes/16 Kernels, cross-cutting concerns, product faces, worldness criteria, reference packs and engineering appendices.
- Include post-M9 additions but do not rewrite mother spec silently.

## Non-goals

- Do not convert research-only M16 ideas into v5.0 requirements.
- Do not hide open stable-platform gaps as future work.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M17

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Mother spec remains the product authority for v5.0-R1.

## Deliverables

- reports/FINAL_DESIGN_TRACEABILITY.md
- reports/final_design_traceability.json
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G20A_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Regenerate traceability from source.
- Validate evidence links exist.
- Review requirement status changes since M10.
- List exact external blockers.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- No stable-platform P0/P1 requirement is GAP.
- Every VERIFIED row has executable evidence.
- Research tracks clearly separate.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Final traceability matrix is release evidence.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g20a: final mother-spec traceability & requirement closure`.
- Record final commit SHA in `reports/G20A_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G20B_CLEAN_ROOM_BUILD_INSTALL_UPGRADE_RESTORE_REPLAY_CERTIFICATION.md ===== -->

# G20B — Clean-room Build, Install, Upgrade, Restore & Replay Certification

> Milestone: M17
> Depends on: G20A
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Certify reproducibility from a clean environment: build artifacts, deploy private/staging profile, migrate/restore, install external pack, instantiate reference world and replay history.

## Scope

- No local untracked state or developer caches.
- Use documented release artifacts/scripts.
- Exercise previous-version upgrade fixture.

## Non-goals

- Do not fix the environment manually without documenting/automating the fix.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M17

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Any environment-specific prerequisite is explicitly documented.

## Deliverables

- reports/CLEAN_ROOM_CERTIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G20B_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Run clean-room script from scratch.
- Restore backup.
- Replay golden history.
- Install external sample pack.
- Run reference world smoke and E2E surfaces.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- All declared supported workflows reproduce.
- Semantic hashes match.
- No hidden local path dependency.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Clean-room certification PASS.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g20b: clean-room build, install, upgrade, restore & replay certification`.
- Record final commit SHA in `reports/G20B_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G20C_FINAL_INDEPENDENT_SECURITY_RELIABILITY_CHAOS_RE_RUN.md ===== -->

# G20C — Final Independent Security, Reliability & Chaos Re-run

> Milestone: M17
> Depends on: G20B
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Re-run the highest-risk M11/M13 security, crash, concurrency, corruption, backup and resource tests against final code to catch regressions introduced by productization or research seams.

## Scope

- Core mutation authority, authz, rights, source injection, crash atomicity, DB failure, reconnect, plugin trust and resource exhaustion.
- Run experimental flags both off and selected on.

## Non-goals

- Do not waive failures because an earlier milestone passed.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M17

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Stable safety wins over research feature retention.

## Deliverables

- reports/FINAL_SECURITY_RELIABILITY_CERTIFICATION.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G20C_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Execute curated final chaos/security suite.
- Compare with M11 baselines.
- Fix stable-path regressions.
- Disable/reject experimental features that violate stable guarantees.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Stable configuration passes all critical tests.
- No high/critical unresolved security/reliability issue.
- Experimental failures cannot affect stable default.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Final resilience certification PASS.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g20c: final independent security, reliability & chaos re-run`.
- Record final commit SHA in `reports/G20C_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G20D_BLACK_BOX_EXTERNAL_AUTHOR_REFERENCE_WORLD_FINAL_ACCEPTANCE.md ===== -->

# G20D — Black-box External Author + Reference World Final Acceptance

> Milestone: M17
> Depends on: G20C
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Perform a black-box final acceptance as two external personas: a package author and an end user/operator, using only public docs/SDK/UI/API and release artifacts.

## Scope

- Author creates/publishes/installs a package; operator deploys and runs; end user enters synthetic living world, exits/rejoins, branches/replays; curator/family/strategy surfaces smoke.
- No internal imports/DB edits.

## Non-goals

- Do not use repository-private shortcuts.
- Do not rely on previous interactive state.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M17

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Usability issues that prevent core workflow are release blockers.

## Deliverables

- reports/BLACKBOX_FINAL_ACCEPTANCE.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G20D_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Automate or document clean personas/projects.
- Run package certification.
- Run worldness black-box scenario.
- Capture usability/friction gaps and fix P0/P1.
- Record evidence/video/screenshot only if tooling exists; tests remain primary.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- External author succeeds without Core modification.
- End user interacts with persistent world through normal surfaces.
- Operator can diagnose/recover using docs.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- Black-box platform claim proven.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g20d: black-box external author + reference world final acceptance`.
- Record final commit SHA in `reports/G20D_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: goals/GOAL_G20E_FINAL_RELEASE_READINESS_VERSION_FREEZE_POST_V5_ROADMAP.md ===== -->

# G20E — Final Release Readiness, Version Freeze & Post-v5 Roadmap

> Milestone: M17
> Depends on: G20D
> Execution mode: formal engineering Goal; integrated implementation + tests + evidence + local checkpoint.

## Objective

Produce the final certification bundle, freeze the current stable version, distinguish external blockers/experimental tracks, and leave the repository ready for controlled release or the next design cycle.

## Scope

- Final acceptance matrix, architecture conformance, migration/replay compatibility, security/rights, performance/capacity, long-run stability, reference-world status, SDK/ecosystem, product surfaces and research decisions.
- Version/tag proposal and release notes; no automatic remote push/deploy.

## Non-goals

- Do not claim unresolved EXTERNAL_BLOCKED real data as completed.
- Do not auto-push/tag/deploy without user authorization.
- Do not invent G21 work inside this Goal.

## Required reading

- docs/spec/WANXIANG_v5_MASTER_SPEC.md
- 10_POST_M9_PROGRAM_ARCHITECTURE.md
- 11_CODEX_POST_M9_MASTER_PROMPT.md
- existing 02_ENGINEERING_STANDARDS.md
- existing 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md
- current STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG
- current Git state and the relevant production/tests/migrations
- `12_POST_M9_GOALS_INDEX.md`
- `13_MILESTONE_GATES_M10_M17.md`
- the specialized standard relevant to this Goal
- reports produced by preceding Goals in M17

## Architecture constraints

- Canonical World State remains writable only through Commit Authority.
- `Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection` remains distinct.
- New external/model/plugin/UI behavior must enter through a Port/Adapter or application use-case; no private backdoor.
- Event/replay/branch/version/migration compatibility must be preserved whenever persisted semantics are touched.
- Source/Evidence/Rights/Privacy rules remain end-to-end and server-enforced.
- Deterministic stable tests must not require paid external APIs.
- Completion means proven stable scope, not every imaginable future feature.

## Deliverables

- reports/M17_FINAL_CERTIFICATION.md
- reports/FINAL_PROGRAM_COMPLETION_REPORT.md
- docs/RELEASE_READINESS.md
- docs/POST_V5_ROADMAP.md
- Updated relevant production code/tests/migrations/docs where required.
- `reports/G20E_REPORT.md` summarizing implementation, commands, evidence, failures, fixes, remaining limitations and Git checkpoint.

## Implementation tasks

- Run final full suite.
- Generate FINAL_PROGRAM_COMPLETION_REPORT and RELEASE_READINESS.
- List exact tested environments and known limitations.
- List M16 PROMOTE/KEEP/REJECT decisions as v5.1/v6 roadmap.
- Ensure STATUS/PLAN/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG are current.
- Before editing, identify the smallest coherent module owners and avoid adding a generic manager/service/utils dumping ground.
- Keep public types explicit and versioned. If a persisted/public schema changes, add compatibility/migration tests in the same Goal.
- Add observability/audit fields for new authoritative workflows where applicable.
- Update architecture/dependency checks if a new package boundary is introduced.

## Tests

- Stable P0/P1 gap count = 0.
- All final reports internally consistent.
- Release candidate can be reproduced from local Git checkpoint.
- External blockers and experimental items are explicit.
- Run the narrow affected unit/contract/integration/property/E2E suites as appropriate.
- Run architecture conformance and import-cycle checks when production package dependencies change.
- Run replay/branch/determinism regression when canonical/event behavior is affected.
- Run rights/security/source-gate regression when data exposure/import/export is affected.
- Run lint, typecheck and schema/client drift checks applicable to changed code.

## Acceptance criteria

- M17 PASS; Post-M9 Program complete.
- Repository stops after local checkpoint and awaits user review.
- No acceptance-critical TODO/FIXME/NotImplemented/pass/placeholder/mock-only production path remains.
- All internally actionable P0/P1 failures introduced or discovered in this Goal are fixed or explicitly carried according to milestone policy; `EXTERNAL_BLOCKED` is not used for internal defects.
- Evidence is reproducible from repository state, not dependent on chat memory.

## Failure / blocker handling

1. Reproduce and classify the failure before patching.
2. Prefer root-cause fixes over weakening assertions or hiding errors.
3. If a real external source/provider/hardware is missing, implement/verify the generic contract and deterministic substitute, mark only that slice `EXTERNAL_BLOCKED`, and continue.
4. If a stable architecture invariant fails, stop this Goal from PASS until fixed.
5. Record newly discovered cross-goal defects in the gap/known-failure ledgers with severity and owner.

## Documentation updates

- Update `PLAN.md` and `STATUS.md` before/after work.
- Update `DECISIONS.md` for nontrivial architectural decisions.
- Update `BLOCKERS.md` / `KNOWN_FAILURES.md` honestly.
- Update `CHANGELOG.md` for user/developer-visible contract or behavior changes.
- Update traceability/acceptance matrices when this Goal closes or changes a requirement.

## Git / checkpoint requirements

- Do not rewrite prior history.
- Keep changes scoped/cohesive; use intermediate local commits if the Goal is large.
- After acceptance passes, create a local checkpoint commit such as: `g20e: final release readiness, version freeze & post-v5 roadmap`.
- Record final commit SHA in `reports/G20E_REPORT.md`.
- Do not push or deploy externally unless separately authorized by the user.


<!-- ===== FILE: milestones/M10_QUALIFICATION.md ===== -->

# M10 Qualification — Independent Verification & Gap Closure

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G13A, G13B, G13C, G13D, G13E, G13F, G13G, G13H, G13I.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M10_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

P0=0; required P1=0; traceability complete; M1-M9 critical regressions independently reproduced.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M10 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.


<!-- ===== FILE: milestones/M11_QUALIFICATION.md ===== -->

# M11 Qualification — Adversarial / Failure Qualification

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G14A, G14B, G14C, G14D, G14E, G14F, G14G, G14H, G14I.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M11_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

No high/critical stable-path failure under declared chaos profiles; world truth remains consistent during concurrency/crash/corruption/hostile inputs.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M11 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.


<!-- ===== FILE: milestones/M12_QUALIFICATION.md ===== -->

# M12 Qualification — Reference World & Worldness Certification

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G15A, G15B, G15C, G15D, G15E, G15F, G15G, G15H, G15I, G15J.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M12_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

Comprehensive synthetic world passes worldness criteria and long-run/replay/branch/human-control tests; real reference slices are PASS or narrow EXTERNAL_BLOCKED.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M12 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.


<!-- ===== FILE: milestones/M13_QUALIFICATION.md ===== -->

# M13 Qualification — Productionization & Operations

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G16A, G16B, G16C, G16D, G16E, G16F, G16G, G16H, G16I, G16J.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M13_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

Private/staging deployment is reproducible, observable, secure, recoverable, upgradeable and capacity-qualified at a declared profile.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M13 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.


<!-- ===== FILE: milestones/M14_QUALIFICATION.md ===== -->

# M14 Qualification — SDK / Ecosystem Qualification

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G17A, G17B, G17C, G17D, G17E, G17F, G17G, G17H.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M14_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

External developer can author/certify/publish/install/upgrade a package through public SDK/contracts without modifying Core.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M14 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.


<!-- ===== FILE: milestones/M15_QUALIFICATION.md ===== -->

# M15 Qualification — Product Surface Qualification

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G18A, G18B, G18C, G18D, G18E, G18F, G18G, G18H.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M15_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

Major product faces are real projections/control surfaces over one server truth with critical E2E/accessibility/authz flows passing.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M15 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.


<!-- ===== FILE: milestones/M16_QUALIFICATION.md ===== -->

# M16 Qualification — Research Expansion Qualification

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G19A, G19B, G19C, G19D, G19E, G19F, G19G, G19H, G19I, G19J.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M16_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

All research tracks executed with evidence and explicit PROMOTE/KEEP_EXPERIMENTAL/REJECT; stable flags-off regression remains green.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M16 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.


<!-- ===== FILE: milestones/M17_QUALIFICATION.md ===== -->

# M17 Qualification — Final Independent Certification

## Entry criteria

- All Goals in this milestone completed with local checkpoints: G20A, G20B, G20C, G20D, G20E.
- Previous milestone PASS (or M9 for M10).
- Working tree state is understood; no hidden acceptance-critical changes.

## Required qualification actions

1. Re-read the milestone Goal reports and unresolved blockers/known failures.
2. Run the milestone's broad regression set, not only the last Goal's tests.
3. Re-run architecture conformance, type/lint and schema/client drift checks.
4. Re-run replay/branch/determinism tests whenever this milestone touched stable world semantics.
5. Re-run rights/security/source tests whenever this milestone touched data exposure/import/export.
6. Update `reports/ACCEPTANCE_MATRIX.md` and design traceability artifacts.
7. Produce `reports/M17_ACCEPTANCE.md` with exact commands, environment, PASS/FAIL/EXTERNAL_BLOCKED evidence and residual risks.

## Gate-specific PASS condition

Stable P0/P1=0; clean-room, security/reliability, black-box author/user/operator and final traceability all PASS; release readiness bundle complete.

## Stop/continue rule

- If stable-path acceptance fails, fix before continuing.
- Narrow external real-data/provider/hardware blockers may remain explicit when generic capability is already proven and the milestone definition allows it.
- On PASS, create a local checkpoint and automatically continue to the next milestone, except M17 if it is M17 where the program stops.

## Prohibited shortcuts

- no blanket skips/xfails;
- no static/mock production success path;
- no weakening of Commit Authority, event history, branch isolation, rights/source gates or version/migration guarantees;
- no claiming research experiments as stable without promotion evidence.
