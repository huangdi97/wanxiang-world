# WANXIANG v5.1 MINIMAL-CORE CONSOLIDATION & MIGRATION — ALL IN ONE


---

# FILE: README_FIRST_V5_1.md

# README FIRST — Wanxiang v5.1 Minimal-Core Consolidation & Migration Program

This pack is the **post-M17 v5.1 compatibility/consolidation program** for Wanxiang.

It assumes M0–M17 were previously implemented/certified, but **does not trust those claims blindly**. It first freezes and audits the repository, then performs a compatibility-first migration to the v5.1-R1 mother spec.

## Mission

Implement the complete v5.1-R1 semantic/runtime delta with the **smallest durable code surface** possible:

- keep proven v5.0/M0–M17 capabilities;
- merge duplicate abstractions, registries, managers, state models and infrastructure;
- delete dead, fake, shadow or superseded implementations;
- adapt existing Commit/Event/Replay/Branch/Host/Compiler/SDK code instead of rewriting healthy systems;
- add only irreducible v5.1 semantics: Reality Calculus contracts, three World Commit kinds, Genesis semantics, Distillation Fabric, Runtime Capability Fabric, Stable World ABI, triple ledgers, bounded runtime evolution;
- preserve v5.0 persisted worlds, event histories, packages and SDK behavior through explicit migration/compatibility tests;
- finish with cross-domain, clean-room and code-minimality qualification.

## Execution order

Read:

1. `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
2. `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
3. `02_CODEX_V5_1_MASTER_PROMPT.md`
4. `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
5. `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
6. `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
7. `06_V5_1_GOALS_INDEX.md`
8. `07_MILESTONE_GATES_M18_M25.md`
9. `08_CONTINUOUS_EXECUTION_RESUME_PROTOCOL.md`
10. `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
11. current Goal file

Then execute **G21A → G28I continuously**, running each milestone gate M18 → M25 in order.

## Critical rule

Do **not** convert every design noun into a class/service/package. The mother spec defines logical semantics. Physical code must remain minimal.

`World Reality Calculus` is a semantic contract, not a reason to create a new giant engine.

`Meaning / Reality / Experience Engine` are architecture views/facades, not three mandatory physical services.

`5 Planes / 16 Kernels` remain logical boundaries, not 16 services.

## Final stop

Stop only when M25 passes or a repository/environment blocker prevents all further independent work. Do not push or production-deploy unless the user separately authorizes it.


---

# FILE: 01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md

# Wanxiang v5.1 Minimal-Core Consolidation & Migration Program Architecture

## 1. Program intent

v5.1-R1 is an architectural deepening of v5.0, not a greenfield rewrite. The program therefore uses **compatibility-first consolidation**:

`VERIFY → CLASSIFY → DELETE/MERGE → ADAPT → ADD IRREDUCIBLE SEMANTICS → MIGRATE → REQUALIFY`.

The default action for an existing healthy capability is `KEEP` or `ADAPT`, never `REPLACE`.

## 2. Target physical architecture

The logical 5 Planes / 16 Kernels are retained, but the durable physical Python/business-code surface should converge toward five cohesive packages plus infrastructure/adapters:

```text
packages/
  core/            # identity/fact/transition/commit/authority/ledger/replay/branch/invariants
  definition/      # source/evidence/rights/candidates/distillation/genesis/compiler/packages
  runtime/         # host/substrate/scheduler/cosim/reality bridge/orchestration/runtime capabilities
  agency/          # perception/belief/memory/actor/org/skills/harness/trajectory
  experience/      # session/embodiment/projection/director/experiment
  infrastructure/  # persistence/API/providers/simulators/sensors/rendering/assets
```

This is a **target dependency topology**, not a forced rename of every existing module. If the current repository already satisfies the same boundaries with fewer/smaller moves, preserve it and document the mapping.

## 3. Minimal semantic core

The stable core must be able to express:

```text
Distinction  -> stable Identity semantics
Relation     -> typed Relation / scoped Fact semantics
Transition   -> Delta / Event semantics
Commitment   -> one Commit Authority / one World mutation boundary
```

The core must not know Red Chamber, Liaoshen, GEDCOM, museum object classes, specific LLM SDKs, Godot, Babylon, DeepSeek Harness, or concrete simulators.

## 4. One-principle architecture

- **One Reality**: one authoritative committed world history.
- **One Commit Boundary**: every world mutation passes the same authority pipeline.
- **One Event Semantics**: one ordered committed-history model; specialized ledgers may share append-only infrastructure.
- **One Branch Model**: one fork/isolation/replay model.
- **One Candidate Envelope**: generated/distilled/reconstructed proposals share a common candidate contract.
- **One Package System**: Genesis, Heritage, AI or runtime features do not invent parallel package registries.
- **One Runtime Composition Root**: runtime provider composition is centralized and typed, not a global service-locator scattered across business code.
- **One Stable World ABI**: external providers/adapters speak a narrow, versioned contract.
- **One Schema Pipeline**: Python/API/TypeScript schemas have one source/generation path.

## 5. Commit model

World reality supports exactly three semantic commit kinds:

```text
WorldCommit
  STATE      -> facts/state within existing ontology/laws
  ONTOLOGY   -> semantic/ontology-space change
  LAW        -> effective-law/rule-set change
```

These use **one authority pipeline**, not three engines/repositories.

Runtime provider installation/reload/rollback is **not** a World Commit. It uses `RuntimeControlTransaction` and the Runtime Control Ledger.

## 6. Current state

`CurrentWorldState` remains useful as a materialized projection/cache, but authority is the committed history plus the semantic/law version context required to fold it. Derived state must be discardable and reconstructable.

## 7. Fact Space

Use a shared semantic Fact contract with explicit scope/provenance/time, while keeping authority separated by policy/repository/use-case boundaries. Changing a Fact scope must never silently promote belief/hypothesis/reconstruction to canonical reality.

## 8. Genesis

Do not build a second package ecosystem. `GenesisSpec` is an initialization specification consumed from WorldPack + Scenario + overrides. Designer Genesis is stable; Evolutionary Genesis may be experimental; True Genesis remains a research contract unless evidence supports a real implementation.

## 9. Distillation

The existing compiler/source/evidence pipeline should be reused and generalized. `Distiller` produces `CandidateEnvelope`; it does not commit reality. LLM/vision/audio/rule extractors are providers, not separate engines.

## 10. Runtime Capability Fabric

Use typed service contracts, provider descriptors, explicit scopes, dependency DAGs and reversible runtime lifecycle. Business code receives dependencies through explicit construction; it must not call a global registry/service locator.

Distinguish:

- `Actor Capability`: what an in-world actor can do/learn;
- `Runtime Capability`: what provider/service the host has installed.

## 11. Triple ledgers

Keep three logical responsibilities:

- World Ledger — what became real;
- Actor Trajectory Ledger — why an actor chose/proposed something;
- Runtime Control Ledger — what runtime/provider configuration was active.

They may share append-only storage infrastructure but must not become one untyped audit blob.

## 12. Bounded runtime evolution

New runtime capabilities and new world structures enter through candidate/evaluation/promotion paths. Shadow branches, existing invariant tests, chaos tests and experiment runtime must be reused. Ordinary agents can never alter World Constitution, Commit Authority, branch semantics or Evidence/Rights contracts.

## 13. Milestones

- **M18 — Minimal-Core Consolidation Baseline**
- **M19 — Authority Microkernel & Reality Semantics**
- **M20 — Genesis / Ontology / Law Evolution**
- **M21 — Distillation Fabric & Meaning Pipeline**
- **M22 — Runtime Capability Fabric & Stable World ABI**
- **M23 — Triple Ledgers & Reproducibility**
- **M24 — Bounded Runtime Evolution**
- **M25 — Backward Migration, Cross-domain Qualification & v5.1 Certification**

## 14. Definition of minimality

Minimality does not mean compressing unrelated responsibilities into giant files. It means:

- no duplicate authoritative models;
- no duplicate registries for the same lifecycle problem;
- no parallel package systems;
- no class/interface that exists only to mirror a design noun;
- no adapter abstraction unless an unstable/external/replaced implementation boundary actually exists;
- no mandatory dependency on experimental providers;
- no duplicated schema definitions across backend/frontend.

The correct solution may contain more small files while still having fewer concepts and less total duplicated logic.


---

# FILE: 02_CODEX_V5_1_MASTER_PROMPT.md

# Codex Master Prompt — Wanxiang v5.1 Minimal-Core Consolidation & Migration, M18 → M25

## Mission

Upgrade the already-built Wanxiang repository from the verified v5.0/M0–M17 implementation to the v5.1-R1 mother specification **without a greenfield rewrite**, while reducing duplicate architecture and keeping the permanent core as small, readable, upgradeable and testable as possible.

Execute every Goal in `06_V5_1_GOALS_INDEX.md` in order and every Milestone Gate M18–M25. Do not stop for routine confirmation.

## Source of truth

Highest product/architecture authority:

`docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`

Engineering execution authority for this migration:

- this master prompt;
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`;
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`;
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`;
- current Goal;
- milestone qualification.

Existing M0–M17 engineering standards remain in force when not superseded by a stricter v5.1 rule.

## Start protocol

Before changing production code:

1. inspect Git status/history and repository layout;
2. read M17 certification/release-readiness artifacts if present;
3. run the narrow critical regression proving Commit/Event/Replay/Branch/Persistence/Host/Package/SDK still work;
4. create `reports/V5_1_PRE_MIGRATION_BASELINE.md` with commit hash, schema versions, event fixture hashes, package fixture hashes, test commands/results and known blockers;
5. do not trust old PASS labels without reproducible evidence.

If M17 is materially broken, repair baseline regressions first and document them. Do not reimplement M0–M17 when healthy.

## Change classification rule

Every meaningful existing implementation encountered in M18 must be classified:

`KEEP_AS_IS | KEEP | MERGE | ADAPT | DELETE | REPLACE | EXPERIMENTAL`.

`REPLACE` requires an ADR explaining why adaptation cannot preserve the v5.0 contract safely.

## Minimal-code rule

A new abstraction is allowed only if it does at least one of the following:

- carries a new irreducible v5.1 semantic contract;
- replaces/merges two or more duplicate concepts;
- isolates an unstable/external provider boundary;
- is required to preserve version/migration/replay compatibility;
- materially improves testability without duplicating behavior.

Do not create classes/services/packages merely because their names appear in the design document.

## Absolute invariants

- one world mutation boundary;
- one authoritative committed history;
- no LLM/UI/Director/Sensor/Simulator/Provider/Compiler direct canonical mutation;
- child branch cannot mutate parent;
- committed history is not silently rewritten;
- v5.0 event histories remain replayable or have explicit deterministic migration;
- Runtime Effect and World Effect remain separate;
- package/provider/runtime upgrades cannot bypass Evidence/Rights/Security/Invariant checks;
- core tests do not require external LLM/API keys.

## Commit semantics

Implement exactly three **World** commit kinds through one pipeline:

`STATE | ONTOLOGY | LAW`.

Do **not** implement `CapabilityCommit` as a fourth World Commit. Runtime provider changes are `RuntimeControlTransaction` records.

## Physical architecture rule

Do not force a directory rewrite if current modules already satisfy the target dependency boundaries. Prefer import-boundary enforcement and selective moves over repository-wide renames.

Never create 16 services for the 16 logical kernels. Never create three giant Meaning/Reality/Experience services.

## Capability runtime rule

Runtime composition must be typed and explicit. A central composition root may resolve/construct providers, but domain/runtime business code must not repeatedly query a global service locator.

## Continuous execution

For each Goal:

1. read it fully;
2. inspect relevant implementation/tests;
3. update PLAN/STATUS;
4. implement smallest coherent change;
5. delete superseded/dead code in the same Goal when safe;
6. run focused tests and applicable architecture/type/lint/migration/replay checks;
7. update traceability and code-minimality inventory;
8. write the Goal report;
9. update DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG;
10. create local Git checkpoint only after acceptance passes;
11. continue automatically.

At each milestone execute its qualification file. PASS continues automatically.

## External blockers

Missing real Red Chamber/Liaoshen/family/heritage sources, provider credentials, real sensors, commercial digital-human services or unavailable hardware may be `EXTERNAL_BLOCKED` for that narrow integration only. Generic contracts, deterministic fakes, source gates, rights/security tests and synthetic qualification must still be completed.

## Never fake completion

Do not count as completion:

- interface without a used implementation;
- route returning static JSON;
- test-only fake on a mandatory production path;
- TODO/FIXME/pass/NotImplemented in acceptance path;
- renamed old code without semantic migration;
- a new registry that simply wraps an old registry;
- a new Engine facade with no required behavior;
- benchmark/report text without reproducible command/evidence.

## Git

Local commits are required after passing Goals. Do not push, force-push, deploy, publish packages or mutate external systems unless separately authorized by the user.

## Final stop

Stop only after M25 qualification and final reports are complete, including:

- `reports/V5_1_FINAL_TRACEABILITY.md`
- `reports/V5_1_BACKWARD_COMPATIBILITY.md`
- `reports/V5_1_MINIMAL_CORE_AUDIT.md`
- `reports/V5_1_REPLAY_MIGRATION_CERTIFICATION.md`
- `reports/V5_1_CROSS_DOMAIN_CERTIFICATION.md`
- `reports/M25_V5_1_FINAL_CERTIFICATION.md`
- `reports/V5_1_PROGRAM_COMPLETION_REPORT.md`
- `docs/V5_1_IMPLEMENTATION_STATUS.md`
- `docs/V5_1_RELEASE_READINESS.md`

Stable P0/P1 gaps must be zero. Experimental/External-Blocked items must be explicit and not described as stable completion.


---

# FILE: 03_MINIMAL_CORE_CODE_CONSTITUTION.md

# Minimal-Core Code Constitution

## 1. Prime directive

Prefer **semantic richness in data/contracts** and **implementation minimalism in permanent core code**.

## 2. Hard anti-bloat rules

- No design-noun-driven class creation.
- No `WorldRealityCalculusEngine` unless executable behavior exists that cannot live in current core semantics.
- No separate `StateCommitEngine`, `OntologyCommitEngine`, `LawCommitEngine`; use one commit pipeline with typed payloads.
- No `GenesisPackageRegistry`; Genesis is a spec/initialization contract under the existing package system.
- No separate registries for models, simulators, projections, plugins and providers when one typed Runtime Capability Catalog can express them.
- No giant `Manager`, `Service`, `Utils`, `Helpers`, `Engine` God objects.
- No global mutable singleton registry/service locator.
- No ORM session exposure to domain/provider/plugin code.
- No second authoritative UI/client state.
- No duplicated Python/OpenAPI/TypeScript schemas.

## 3. File/function/class quality

- Keep modules cohesive and normally <= ~300 production lines; larger modules require an ADR or clear cohesion argument.
- Prefer pure functions/value objects for deterministic semantic operations.
- Prefer composition over inheritance hierarchies.
- Public contracts and event schemas are typed/versioned.
- Constructors should not hide I/O.
- Errors are explicit domain/application exceptions; no broad silent catch.
- `Any` is exceptional, localized and justified.

## 4. Interface rule

Create a Port/Protocol when the boundary is actually replaceable, external, nondeterministic or independently versioned. Do not create Port→Service→Manager→Adapter chains for internal pure logic with one implementation.

Primary justified ports include persistence, LLM/model provider, Agent Harness, Simulator, Sensor/Reality Connector, Renderer/Projection, Asset Store, external Search/Retrieval and external network APIs.

## 5. Dependency rule

Core/domain semantic code must not import FastAPI, SQLAlchemy/Alembic, React/TS, concrete LLM SDKs, DeepSeek Harness/Cordis, Godot/Babylon, cloud SDKs or concrete simulator SDKs.

Architecture tests must enforce forbidden imports and forbidden direct canonical writes.

## 6. Minimality evidence

Maintain `reports/V5_1_CODE_MINIMALITY_LEDGER.md` with:

- production LOC by top-level package;
- count of public classes/protocols;
- registries/catalogs;
- managers/services/engines;
- duplicate schema definitions;
- dependency cycles;
- unused public interfaces;
- dead-code candidates;
- additions/deletions per Goal;
- justification for every new long-lived abstraction.

Raw LOC reduction is not allowed to destroy readability or correctness. The desired outcome is fewer concepts/duplications and a stable or smaller core surface.

## 7. Consolidation preference

When two old abstractions overlap:

1. identify semantic owner;
2. migrate call sites/tests;
3. preserve compatibility adapter only if externally required;
4. deprecate with explicit sunset;
5. delete old implementation once evidence proves no live path depends on it.

## 8. Schema/migration rule

Every persisted/event/public schema change includes versioning and migration/replay compatibility. Never reinterpret old events silently with new semantics.

## 9. Test quality

Tests must prove behavior, not line coverage. Prefer invariant/property/contract/replay/migration/negative tests around semantic boundaries. Never weaken a requirement to make a test green.


---

# FILE: 04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md

# v5.1 Design Conflict Resolutions for Engineering

These resolutions prevent ambiguous parts of the v5.1 mother spec from causing duplicate runtime systems.

## R1 — CapabilityCommit

**Resolution:** World reality has exactly three commit kinds: StateCommit, OntologyCommit, LawCommit. `CapabilityCommit` references in evolutionary-distillation prose are interpreted as **runtime capability activation/promotion**, implemented through `RuntimeControlTransaction`, not World Commit.

## R2 — GenesisPackage

**Resolution:** Do not create a second package registry. Implement `GenesisSpec`/`GenesisManifest` consumed from WorldPack + Scenario + overrides. Existing package/version/dependency/rights infrastructure remains authoritative.

## R3 — Fact Space

**Resolution:** Share one semantic Fact shape/scope model where useful, but authority remains separated. A scope change cannot promote belief/hypothesis/reconstruction to canonical truth. Canonical promotion requires the normal Commit boundary.

## R4 — Ω / Possibility Space

**Resolution:** Ω is primarily candidate/derived possibility state. Do not persist a complete enumerable possibility universe. Persist only explicit proposals/candidates/plans/experiments required for audit/recovery. Recompute other possibility views from current facts/laws/affordances where practical.

## R5 — Σ / Γ replay context

**Resolution:** committed events/snapshots must carry or resolve stable semantic-space/law-set/constitution versions sufficient for deterministic interpretation/replay. Old events are never silently interpreted using only latest laws/schema.

## R6 — Meaning/Reality/Experience Engine

**Resolution:** these are conceptual architecture views/facades. They do not mandate three services or three God objects. Existing definition/core/runtime/agency/experience modules implement them.

## R7 — Capability naming

**Resolution:** distinguish `ActorCapability` (in-world learned/usable ability) from `RuntimeCapability` (installed provider/service). Avoid unqualified `Capability` types when ambiguity exists.

## R8 — Triple ledgers

**Resolution:** three logical streams may share append-only persistence infrastructure, but must keep typed schemas, retention/rights policies and query boundaries. Do not merge them into one untyped audit-event table.

## R9 — DeepSeek Harness/Cordis

**Resolution:** optional AgentHarness provider/reference only. Core/authority/persistence/history must function without it. Do not fork it as Wanxiang's base runtime.

## R10 — True Genesis

**Resolution:** preserve a research-grade contract/adapter seam; do not fake open-ended universe/life emergence. Stable implementation is not required unless the repository contains independently validated research evidence satisfying the Goal.

## R11 — 5 Planes / 16 Kernels

**Resolution:** logical responsibility/test boundaries only. Do not create 16 deployable services or packages solely to mirror the diagram.

## R12 — CurrentWorldState

**Resolution:** keep as derived/materialized state for efficient runtime. The authoritative semantics are committed history + version context. Derived state must be rebuildable.


---

# FILE: 05_M0_M17_TO_V5_1_MIGRATION_MAP.md

# M0–M17 → v5.1 Migration Map

## Keep / adapt map

| Existing capability | Action | v5.1 role |
|---|---|---|
| Commit Authority | KEEP + ADAPT | Authority Microkernel implementation |
| Event Store | KEEP | World Ledger storage foundation |
| Snapshot / Replay / Branch | KEEP + VERSION-CONTEXT EXTEND | committed-history reconstruction |
| Persistence / migrations | KEEP | schema/event/runtime compatibility |
| Living World Substrate | KEEP | Reality Engine capability |
| World Host / scheduler | KEEP | Runtime host |
| Perception / Belief / Memory | KEEP | Agent Harness inputs / actor trajectory |
| Actor / Organization | KEEP | Agency runtime |
| Skill / Action / Affordance | KEEP | Agency/world action contracts |
| Source / Evidence / Rights | KEEP | Meaning/Distillation evidence boundary |
| Compiler / Completion | ADAPT | Foundational Distillation pipeline |
| Package Registry | KEEP + EXTEND | World/Domain/Scenario + RuntimeProfile metadata |
| Reality Bridge | KEEP | observation provider |
| Co-Simulation | KEEP | Simulation provider |
| Projection / Embodiment | KEEP | Experience layer |
| SDK / package tooling | KEEP + ABI UPDATE | external ecosystem |
| Security / chaos / evaluation | KEEP | bounded-evolution promotion gates |
| experimental M16 research | AUDIT | adapt, keep experimental or reject |

## Merge candidates

- overlapping plugin/provider/model/simulator/projection registries → Runtime Capability Catalog;
- duplicate append-only/audit storage machinery → shared stream infrastructure with typed ledger facades;
- duplicate current-state caches/read models → one authoritative projection strategy per concern;
- duplicate API/TS schemas → generated schema pipeline;
- duplicate manager/service wrappers → direct application use cases or explicit composition root.

## Delete candidates

Delete only after call-site/test evidence proves safe:

- second canonical-state implementations;
- direct-mutation bypasses;
- dead/unused interfaces;
- fake production paths;
- static JSON runtime substitutes;
- giant legacy managers superseded by cohesive modules;
- untyped global service locators;
- duplicate registries with no independent semantics;
- experimental provider forks used as core dependencies.

## New irreducible v5.1 additions

- semantic-space/law/constitution version context;
- three World Commit kinds in one authority pipeline;
- GenesisSpec;
- Ontology/Law candidates and commits;
- CandidateEnvelope + Distiller protocol;
- Evolutionary Distillation;
- Runtime Capability model/composition/lifecycle;
- RuntimeProfile;
- Stable World ABI;
- Actor Trajectory Ledger;
- Runtime Control Ledger;
- Bounded Runtime Evolution orchestration.


---

# FILE: 06_V5_1_GOALS_INDEX.md

# Wanxiang v5.1 Goals Index — M18 to M25

> Execute in this exact order. Each milestone gate must PASS before continuing.

## M18

- `G21A` — v5.0/M17 Baseline Freeze & Repository Inventory — `goals/GOAL_G21A_V5_0_M17_BASELINE_FREEZE___REPOSITORY_INVENTORY.md`
- `G21B` — v5.1 Delta Traceability & Existing-code Classification — `goals/GOAL_G21B_V5_1_DELTA_TRACEABILITY___EXISTING_CODE_CLASSIFICATION.md`
- `G21C` — Duplicate Abstraction, Registry, State & Manager Forensics — `goals/GOAL_G21C_DUPLICATE_ABSTRACTION__REGISTRY__STATE___MANAGER_FORENSICS.md`
- `G21D` — Dependency Graph & Physical Package Simplification Plan — `goals/GOAL_G21D_DEPENDENCY_GRAPH___PHYSICAL_PACKAGE_SIMPLIFICATION_PLAN.md`
- `G21E` — Dead, Fake, Placeholder & Shadow-path Removal — `goals/GOAL_G21E_DEAD__FAKE__PLACEHOLDER___SHADOW_PATH_REMOVAL.md`
- `G21F` — Registry, Provider & Manager Consolidation — `goals/GOAL_G21F_REGISTRY__PROVIDER___MANAGER_CONSOLIDATION.md`
- `G21G` — State, Event, Audit & Projection Consolidation — `goals/GOAL_G21G_STATE__EVENT__AUDIT___PROJECTION_CONSOLIDATION.md`
- `G21H` — Frontend/SDK Shared Contract Consolidation — `goals/GOAL_G21H_FRONTEND_SDK_SHARED_CONTRACT_CONSOLIDATION.md`
- `G21I` — Minimal-Core Target Freeze & M18 Qualification — `goals/GOAL_G21I_MINIMAL_CORE_TARGET_FREEZE___M18_QUALIFICATION.md`
- Milestone Gate — `milestones/M18_QUALIFICATION.md`

## M19

- `G22A` — Reality Calculus Semantic Mapping Without New God Engine — `goals/GOAL_G22A_REALITY_CALCULUS_SEMANTIC_MAPPING_WITHOUT_NEW_GOD_ENGINE.md`
- `G22B` — Scoped Fact Contract & Authority Partition — `goals/GOAL_G22B_SCOPED_FACT_CONTRACT___AUTHORITY_PARTITION.md`
- `G22C` — Unified World Commit Kinds: State / Ontology / Law — `goals/GOAL_G22C_UNIFIED_WORLD_COMMIT_KINDS__STATE___ONTOLOGY___LAW.md`
- `G22D` — Authority Microkernel Contract & Existing CommitAuthority Adaptation — `goals/GOAL_G22D_AUTHORITY_MICROKERNEL_CONTRACT___EXISTING_COMMITAUTHORITY_ADAPTATION.md`
- `G22E` — Semantic Space, Law Set & Constitution Version Context — `goals/GOAL_G22E_SEMANTIC_SPACE__LAW_SET___CONSTITUTION_VERSION_CONTEXT.md`
- `G22F` — Committed Event Envelope & Replay-context Migration — `goals/GOAL_G22F_COMMITTED_EVENT_ENVELOPE___REPLAY_CONTEXT_MIGRATION.md`
- `G22G` — Three-tier World Invariant Registry — `goals/GOAL_G22G_THREE_TIER_WORLD_INVARIANT_REGISTRY.md`
- `G22H` — Derived Current State / Materialized Projection Contract — `goals/GOAL_G22H_DERIVED_CURRENT_STATE___MATERIALIZED_PROJECTION_CONTRACT.md`
- `G22I` — M19 Authority Compatibility Qualification — `goals/GOAL_G22I_M19_AUTHORITY_COMPATIBILITY_QUALIFICATION.md`
- Milestone Gate — `milestones/M19_QUALIFICATION.md`

## M20

- `G23A` — GenesisSpec Integration with Existing WorldPack / Scenario — `goals/GOAL_G23A_GENESISSPEC_INTEGRATION_WITH_EXISTING_WORLDPACK___SCENARIO.md`
- `G23B` — Designer Genesis Stable Path — `goals/GOAL_G23B_DESIGNER_GENESIS_STABLE_PATH.md`
- `G23C` — Ontology Candidate & OntologyCommit — `goals/GOAL_G23C_ONTOLOGY_CANDIDATE___ONTOLOGYCOMMIT.md`
- `G23D` — Law Candidate & LawCommit — `goals/GOAL_G23D_LAW_CANDIDATE___LAWCOMMIT.md`
- `G23E` — Branch-local Ontology / Law Evolution & Merge Policy — `goals/GOAL_G23E_BRANCH_LOCAL_ONTOLOGY___LAW_EVOLUTION___MERGE_POLICY.md`
- `G23F` — Possibility Space Ω as Candidate/Derived Policy — `goals/GOAL_G23F_POSSIBILITY_SPACE_Ω_AS_CANDIDATE_DERIVED_POLICY.md`
- `G23G` — Evolutionary Genesis Experimental Seam — `goals/GOAL_G23G_EVOLUTIONARY_GENESIS_EXPERIMENTAL_SEAM.md`
- `G23H` — True Genesis Research Contract — No Fake Completion — `goals/GOAL_G23H_TRUE_GENESIS_RESEARCH_CONTRACT___NO_FAKE_COMPLETION.md`
- `G23I` — M20 Genesis / Ontology / Law Qualification — `goals/GOAL_G23I_M20_GENESIS___ONTOLOGY___LAW_QUALIFICATION.md`
- Milestone Gate — `milestones/M20_QUALIFICATION.md`

## M21

- `G24A` — CandidateEnvelope, Origin Class & Provenance Contract — `goals/GOAL_G24A_CANDIDATEENVELOPE__ORIGIN_CLASS___PROVENANCE_CONTRACT.md`
- `G24B` — Minimal Distiller Protocol & Orchestration — `goals/GOAL_G24B_MINIMAL_DISTILLER_PROTOCOL___ORCHESTRATION.md`
- `G24C` — Foundational Distillation — Reuse Existing Compiler — `goals/GOAL_G24C_FOUNDATIONAL_DISTILLATION___REUSE_EXISTING_COMPILER.md`
- `G24D` — Reusable Typed Distillers for Identity / Relation / Event / Persona / Rule / Skill / Ontology — `goals/GOAL_G24D_REUSABLE_TYPED_DISTILLERS_FOR_IDENTITY___RELATION___EVENT___PERSONA___RULE___SKILL___ONTOLOGY.md`
- `G24E` — Evidence Binding, Review & Completion-level Consolidation — `goals/GOAL_G24E_EVIDENCE_BINDING__REVIEW___COMPLETION_LEVEL_CONSOLIDATION.md`
- `G24F` — Evolutionary Distillation from Committed History — `goals/GOAL_G24F_EVOLUTIONARY_DISTILLATION_FROM_COMMITTED_HISTORY.md`
- `G24G` — Anti-self-evidence, Canon Escalation & Feedback-loop Protection — `goals/GOAL_G24G_ANTI_SELF_EVIDENCE__CANON_ESCALATION___FEEDBACK_LOOP_PROTECTION.md`
- `G24H` — Domain Distillation Profiles without Core Hardcoding — `goals/GOAL_G24H_DOMAIN_DISTILLATION_PROFILES_WITHOUT_CORE_HARDCODING.md`
- `G24I` — M21 Distillation / Meaning Qualification — `goals/GOAL_G24I_M21_DISTILLATION___MEANING_QUALIFICATION.md`
- Milestone Gate — `milestones/M21_QUALIFICATION.md`

## M22

- `G25A` — RuntimeCapability Semantic Model & Naming Separation — `goals/GOAL_G25A_RUNTIMECAPABILITY_SEMANTIC_MODEL___NAMING_SEPARATION.md`
- `G25B` — Typed Service Contracts & Single Composition Root — `goals/GOAL_G25B_TYPED_SERVICE_CONTRACTS___SINGLE_COMPOSITION_ROOT.md`
- `G25C` — Dependency DAG, Scope & Provider Lifecycle — `goals/GOAL_G25C_DEPENDENCY_DAG__SCOPE___PROVIDER_LIFECYCLE.md`
- `G25D` — RuntimeProfile Separation from WorldPack — `goals/GOAL_G25D_RUNTIMEPROFILE_SEPARATION_FROM_WORLDPACK.md`
- `G25E` — Stable World ABI v1 — `goals/GOAL_G25E_STABLE_WORLD_ABI_V1.md`
- `G25F` — AgentHarnessProvider Adaptation of Existing Policies — `goals/GOAL_G25F_AGENTHARNESSPROVIDER_ADAPTATION_OF_EXISTING_POLICIES.md`
- `G25G` — Runtime Capability Catalog & Legacy Registry Merge — `goals/GOAL_G25G_RUNTIME_CAPABILITY_CATALOG___LEGACY_REGISTRY_MERGE.md`
- `G25H` — RuntimeControlTransaction & Reversible Runtime Effects — `goals/GOAL_G25H_RUNTIMECONTROLTRANSACTION___REVERSIBLE_RUNTIME_EFFECTS.md`
- `G25I` — Runtime Architecture Conformance & Service-locator/Permission Guards — `goals/GOAL_G25I_RUNTIME_ARCHITECTURE_CONFORMANCE___SERVICE_LOCATOR_PERMISSION_GUARDS.md`
- `G25J` — M22 Runtime Capability / ABI Qualification — `goals/GOAL_G25J_M22_RUNTIME_CAPABILITY___ABI_QUALIFICATION.md`
- Milestone Gate — `milestones/M22_QUALIFICATION.md`

## M23

- `G26A` — Shared Append-only Stream Infrastructure for Typed Ledgers — `goals/GOAL_G26A_SHARED_APPEND_ONLY_STREAM_INFRASTRUCTURE_FOR_TYPED_LEDGERS.md`
- `G26B` — World Ledger Facade over Existing Event Store — `goals/GOAL_G26B_WORLD_LEDGER_FACADE_OVER_EXISTING_EVENT_STORE.md`
- `G26C` — Actor Trajectory Ledger with Privacy / Retention Controls — `goals/GOAL_G26C_ACTOR_TRAJECTORY_LEDGER_WITH_PRIVACY___RETENTION_CONTROLS.md`
- `G26D` — Runtime Control Ledger — `goals/GOAL_G26D_RUNTIME_CONTROL_LEDGER.md`
- `G26E` — Cross-ledger Correlation & Trace Identity — `goals/GOAL_G26E_CROSS_LEDGER_CORRELATION___TRACE_IDENTITY.md`
- `G26F` — Reproducibility Manifest & Runtime Revision Pinning — `goals/GOAL_G26F_REPRODUCIBILITY_MANIFEST___RUNTIME_REVISION_PINNING.md`
- `G26G` — Ledger Integrity, Query, Export & Retention Qualification — `goals/GOAL_G26G_LEDGER_INTEGRITY__QUERY__EXPORT___RETENTION_QUALIFICATION.md`
- `G26H` — M23 Triple-ledger Reproducibility Qualification — `goals/GOAL_G26H_M23_TRIPLE_LEDGER_REPRODUCIBILITY_QUALIFICATION.md`
- Milestone Gate — `milestones/M23_QUALIFICATION.md`

## M24

- `G27A` — Runtime Capability Proposal Model — `goals/GOAL_G27A_RUNTIME_CAPABILITY_PROPOSAL_MODEL.md`
- `G27B` — Sandbox & Shadow-branch Evaluation Environment — `goals/GOAL_G27B_SANDBOX___SHADOW_BRANCH_EVALUATION_ENVIRONMENT.md`
- `G27C` — Promotion Evaluation Gate: Invariant / Regression / Security / Cost / Determinism — `goals/GOAL_G27C_PROMOTION_EVALUATION_GATE__INVARIANT___REGRESSION___SECURITY___COST___DETERMINISM.md`
- `G27D` — Approval & Promotion Policy — `goals/GOAL_G27D_APPROVAL___PROMOTION_POLICY.md`
- `G27E` — Transactional Activation & Rollback — `goals/GOAL_G27E_TRANSACTIONAL_ACTIVATION___ROLLBACK.md`
- `G27F` — Post-activation Observation & Automatic/Manual Rollback Policy — `goals/GOAL_G27F_POST_ACTIVATION_OBSERVATION___AUTOMATIC_MANUAL_ROLLBACK_POLICY.md`
- `G27G` — Candidate→Skill / Rule / Institution / Ontology / Law Paths — `goals/GOAL_G27G_CANDIDATE_SKILL___RULE___INSTITUTION___ONTOLOGY___LAW_PATHS.md`
- `G27H` — Constitutional Attack & Self-modification Adversarial Qualification — `goals/GOAL_G27H_CONSTITUTIONAL_ATTACK___SELF_MODIFICATION_ADVERSARIAL_QUALIFICATION.md`
- `G27I` — M24 Bounded Runtime Evolution Qualification — `goals/GOAL_G27I_M24_BOUNDED_RUNTIME_EVOLUTION_QUALIFICATION.md`
- Milestone Gate — `milestones/M24_QUALIFICATION.md`

## M25

- `G28A` — v5.0 Persisted-world / Event / Snapshot Backward Compatibility — `goals/GOAL_G28A_V5_0_PERSISTED_WORLD___EVENT___SNAPSHOT_BACKWARD_COMPATIBILITY.md`
- `G28B` — Schema / API / SDK Compatibility & Deprecation Qualification — `goals/GOAL_G28B_SCHEMA___API___SDK_COMPATIBILITY___DEPRECATION_QUALIFICATION.md`
- `G28C` — Synthetic Reference World Full v5.1 Regression — `goals/GOAL_G28C_SYNTHETIC_REFERENCE_WORLD_FULL_V5_1_REGRESSION.md`
- `G28D` — Family / Heritage / Campaign Cross-domain Qualification — `goals/GOAL_G28D_FAMILY___HERITAGE___CAMPAIGN_CROSS_DOMAIN_QUALIFICATION.md`
- `G28E` — Narrative / Red Chamber Source-gated v5.1 Qualification — `goals/GOAL_G28E_NARRATIVE___RED_CHAMBER_SOURCE_GATED_V5_1_QUALIFICATION.md`
- `G28F` — Product Surfaces / Host / External Adapter Compatibility — `goals/GOAL_G28F_PRODUCT_SURFACES___HOST___EXTERNAL_ADAPTER_COMPATIBILITY.md`
- `G28G` — Final Minimal-Core, Complexity & Dead-code Reduction Audit — `goals/GOAL_G28G_FINAL_MINIMAL_CORE__COMPLEXITY___DEAD_CODE_REDUCTION_AUDIT.md`
- `G28H` — Clean-room Build / Upgrade / Restore / Replay Certification — `goals/GOAL_G28H_CLEAN_ROOM_BUILD___UPGRADE___RESTORE___REPLAY_CERTIFICATION.md`
- `G28I` — Final v5.1 Traceability, Certification & Program Stop — `goals/GOAL_G28I_FINAL_V5_1_TRACEABILITY__CERTIFICATION___PROGRAM_STOP.md`
- Milestone Gate — `milestones/M25_QUALIFICATION.md`


---

# FILE: 07_MILESTONE_GATES_M18_M25.md

# Milestone Gates — M18 to M25

Each milestone PASS automatically continues to the next milestone. Detailed gate files are under `milestones/`.

## M18 — Minimal-Core Consolidation Baseline

- Verified v5.0/M17 baseline and golden fixtures exist.
- Every v5.1 delta is classified.
- Duplicate/dead/fake architecture P0/P1 findings are closed.
- Overlapping runtime registries/managers/state paths are consolidated.
- Target dependency boundaries are executable via architecture tests.
- Code-minimality ledger contains before/after metrics.

## M19 — Authority Microkernel & Reality Semantics

- One authority pipeline supports State/Ontology/Law commits.
- No CapabilityCommit World semantics exist.
- Fact scopes cannot escalate authority by field mutation.
- Semantic/law/constitution versions make replay interpretation explicit.
- v5.0 golden event streams replay correctly.
- Kernel/Domain/World invariants share one registry model.

## M20 — Genesis / Ontology / Law Evolution

- GenesisSpec reuses existing package/scenario systems.
- Designer Genesis is stable/deterministic.
- Ontology/Law evolution is branch-local and replayable.
- Ω is non-authoritative and minimally persisted.
- Evolutionary/True Genesis status is honestly experimental/research where applicable.

## M21 — Distillation Fabric & Meaning Pipeline

- Existing compiler is reused under Candidate/Distiller semantics.
- One CandidateEnvelope and minimal Distiller protocol exist.
- Evidence/rights/completion/source gates remain intact.
- Evolutionary distillation produces candidates only.
- Self-evidence/canon escalation is prevented.
- Domain profiles do not hardcode world names into core.

## M22 — Runtime Capability Fabric & Stable World ABI

- RuntimeCapability is distinct from ActorCapability.
- One typed composition root and runtime capability catalog exist.
- Provider lifecycle/dependency/scope/reload/rollback work.
- WorldPack and RuntimeProfile are separated.
- Stable World ABI exposes no mutable authority/ORM handles.
- Existing policies operate through AgentHarnessProvider adapters.
- No service-locator/global registry pattern exists in business code.

## M23 — Triple Ledgers & Reproducibility

- World/Actor/Runtime ledgers remain semantically separate.
- Append-only infrastructure is shared where appropriate.
- Actor trajectory respects privacy/retention.
- Runtime control history explains active provider/profile revisions.
- Cross-ledger trace correlation works.
- Reproducibility manifests accurately describe deterministic/nondeterministic providers.

## M24 — Bounded Runtime Evolution

- Capability proposal→sandbox→evaluation→approval→activation→observation→rollback works.
- Shadow branch isolates candidate effects.
- Promotion gate reuses invariant/regression/security/cost/determinism suites.
- Runtime rollback cannot undo world history.
- Ordinary agents/providers cannot modify constitution/authority/branch/evidence-rights semantics.

## M25 — v5.1 Backward Migration & Final Certification

- v5.0 persisted worlds/events/snapshots/packages upgrade/replay deterministically.
- Public API/SDK/ABI changes are compatible or explicitly migrated/deprecated.
- Synthetic full reference world passes v5.1 end-to-end.
- Family/Heritage/Campaign/Narrative paths pass generic/source-gated qualification.
- Product surfaces/adapters still consume one server truth.
- Minimal-core final audit has zero stable P0/P1 duplication/dead-path findings.
- Clean-room build/upgrade/restore/replay passes.
- All final reports exist and stable P0/P1 gaps are zero.


---

# FILE: 08_CONTINUOUS_EXECUTION_RESUME_PROTOCOL.md

# Continuous Execution & Resume Protocol — v5.1 M18→M25

Codex may continue automatically through all Goals and milestones.

If context is compressed/restarted, recover in this order:

1. `git status` / current branch / last local commit;
2. `STATUS.md` and `PLAN.md`;
3. latest `reports/Gxx_REPORT.md`;
4. latest milestone report;
5. `reports/V5_1_TRACEABILITY_MATRIX.md`;
6. `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
7. `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`;
8. current Goal file;
9. rerun the narrow acceptance test for the last claimed PASS before continuing.

Never reconstruct state from chat memory.

A Goal is resumable only from committed/reported evidence. Uncommitted partial work must be inspected before reuse.


---

# FILE: 09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md

# v5.1 Final Acceptance & Evidence Standard

## Evidence statuses

`PASS | FAIL | EXTERNAL_BLOCKED | NOT_APPLICABLE | EXPERIMENTAL`

Every PASS needs reproducible evidence: test name/path, command, result summary, relevant hash/version/migration id, and report path.

## Global mandatory regression axes

- canonical mutation exclusivity;
- commit atomicity/idempotency/stale revision;
- branch isolation;
- replay determinism;
- old-event interpretation under versioned semantics;
- DB/package/event migrations;
- source/evidence/rights enforcement;
- runtime provider isolation;
- runtime dispose cannot undo world history;
- LLM-independent deterministic path;
- architecture import boundaries;
- generated API/TS schema consistency;
- backward compatibility with v5.0 fixtures;
- cross-domain reference worlds;
- minimal-core metrics and dead-code inventory.

## Code-minimality pass conditions

M25 cannot PASS if any of these remain without a documented, justified exception:

- two authoritative world-state implementations;
- multiple overlapping runtime provider registries;
- a global mutable service locator used by business code;
- separate commit engines/repositories for State/Ontology/Law without irreducible justification;
- a parallel Genesis package/registry ecosystem;
- a giant Meaning/Reality/Experience God service;
- unused public interfaces or dead production paths classified P0/P1;
- duplicate backend/frontend schemas maintained manually;
- direct provider/plugin ORM write access to authoritative tables.

## Final reports

M25 must produce:

- `reports/V5_1_FINAL_TRACEABILITY.md`
- `reports/V5_1_BACKWARD_COMPATIBILITY.md`
- `reports/V5_1_MINIMAL_CORE_AUDIT.md`
- `reports/V5_1_REPLAY_MIGRATION_CERTIFICATION.md`
- `reports/V5_1_CROSS_DOMAIN_CERTIFICATION.md`
- `reports/M25_V5_1_FINAL_CERTIFICATION.md`
- `reports/V5_1_PROGRAM_COMPLETION_REPORT.md`
- `docs/V5_1_IMPLEMENTATION_STATUS.md`
- `docs/V5_1_RELEASE_READINESS.md`


---

# FILE: goals/GOAL_G21A_V5_0_M17_BASELINE_FREEZE___REPOSITORY_INVENTORY.md

# G21A — v5.0/M17 Baseline Freeze & Repository Inventory

**Milestone:** M18

## Objective

Freeze reproducible pre-v5.1 evidence so consolidation cannot accidentally destroy a working M0–M17 implementation.

## Scope

- Git/build/test/schema/package/event baselines
- top-level source/package inventory
- current public API/SDK/event/schema versions
- critical v5.0 fixtures and hashes

## Non-goals

- No architecture refactor yet
- No v5.1 feature implementation

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21A_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Capture current commit/branch/dirty state and preserve user work.
- Run narrow M17 critical regression and record exact commands/results.
- Inventory production packages, public contracts, migrations, event schemas, package schemas, SDK outputs and reference worlds.
- Create immutable/golden copies or hashes of representative v5.0 event streams, snapshots, world packages and SDK/API schemas.
- Create `reports/V5_1_PRE_MIGRATION_BASELINE.md` and initialize code-minimality ledger.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Baseline regression repeats successfully.
- Golden v5.0 event/snapshot/package fixtures can be read by current code.
- Hash manifest is deterministic.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- A reproducible before-state exists.
- No user changes lost.
- All later migration tests have concrete v5.0 inputs.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21a: v5.0/m17 baseline freeze & repository inventory`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G21B_V5_1_DELTA_TRACEABILITY___EXISTING_CODE_CLASSIFICATION.md

# G21B — v5.1 Delta Traceability & Existing-code Classification

**Milestone:** M18

## Objective

Map every material v5.1 delta to existing code and classify the smallest required action.

## Scope

- Reality Calculus
- three commit kinds
- Genesis
- Distillation
- Runtime Capability Fabric
- Stable World ABI
- triple ledgers
- bounded runtime evolution

## Non-goals

- Do not implement yet except tiny audit tooling

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21B_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Build `reports/V5_1_TRACEABILITY_MATRIX.md`: spec requirement → current owner → current evidence → action.
- Classify each owner KEEP_AS_IS/KEEP/MERGE/ADAPT/DELETE/REPLACE/EXPERIMENTAL.
- Flag conflicts with previous M16 experiments and existing plugin/provider abstractions.
- Identify requirements already satisfied semantically despite different names.
- Require ADR candidate for every proposed REPLACE.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Traceability completeness check against mother-spec headings/keywords.
- No required delta left UNCLASSIFIED.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Every v5.1 delta has an owner/action.
- No greenfield rewrite is proposed without evidence.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21b: v5.1 delta traceability & existing-code classification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G21C_DUPLICATE_ABSTRACTION__REGISTRY__STATE___MANAGER_FORENSICS.md

# G21C — Duplicate Abstraction, Registry, State & Manager Forensics

**Milestone:** M18

## Objective

Find architectural duplication that would make v5.1 additive rather than consolidating.

## Scope

- registries/catalogs
- canonical/current/read-state models
- event/audit stores
- managers/services/engines
- ports/adapters
- schema duplicates
- provider catalogs

## Non-goals

- No deletion before dependency evidence

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21C_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Generate static/import/reference inventory for candidate duplicate abstractions.
- Locate all registries and categorize package registry vs runtime provider catalog vs domain-local data.
- Find multiple authoritative-state or commit paths.
- Find duplicated event/audit append infrastructure.
- Find giant Manager/Service/Utils/Engine modules and dead interfaces.
- Write merge/delete candidates with references and risk level.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Architecture scan has deterministic output.
- Direct canonical mutation search/regression remains green.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- All duplicate candidates have explicit disposition.
- No hidden second authority path remains undocumented.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21c: duplicate abstraction, registry, state & manager forensics`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G21D_DEPENDENCY_GRAPH___PHYSICAL_PACKAGE_SIMPLIFICATION_PLAN.md

# G21D — Dependency Graph & Physical Package Simplification Plan

**Milestone:** M18

## Objective

Define the minimum physical dependency topology without forcing cosmetic repository churn.

## Scope

- core/definition/runtime/agency/experience/infrastructure mapping
- forbidden dependencies
- composition root location

## Non-goals

- No mass rename solely for aesthetics

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21D_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Map current packages onto target responsibilities.
- Detect cycles and reverse dependencies.
- Choose minimal package moves only where boundary violations exist.
- Define architecture tests for forbidden imports.
- Document logical 16-kernel → physical-package mapping.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Import-cycle test.
- Forbidden-dependency tests.
- Existing public imports remain compatible or have deprecation adapter.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Dependency direction is acyclic and documented.
- No requirement to create 16 packages/services.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21d: dependency graph & physical package simplification plan`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G21E_DEAD__FAKE__PLACEHOLDER___SHADOW_PATH_REMOVAL.md

# G21E — Dead, Fake, Placeholder & Shadow-path Removal

**Milestone:** M18

## Objective

Remove code that inflates apparent capability without serving a verified production path.

## Scope

- TODO/FIXME/pass/NotImplemented
- static runtime JSON
- unused interfaces/adapters
- mock-only production path
- shadow duplicate implementations

## Non-goals

- Do not remove legitimate deterministic test fakes

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Search and classify every placeholder/dead-path occurrence.
- Delete unused code only after reference/test evidence.
- Replace mandatory-path placeholders with real implementation or mark EXTERNAL_BLOCKED only when truly external.
- Remove duplicate static/demo state that competes with server truth.
- Update tests/imports/docs after deletion.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Full focused regressions after each deletion wave.
- No mandatory acceptance path contains placeholder markers.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- P0/P1 fake/dead production paths = 0.
- Net deletion evidence recorded.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21e: dead, fake, placeholder & shadow-path removal`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G21F_REGISTRY__PROVIDER___MANAGER_CONSOLIDATION.md

# G21F — Registry, Provider & Manager Consolidation

**Milestone:** M18

## Objective

Collapse overlapping infrastructure concepts before adding Runtime Capability Fabric.

## Scope

- model/plugin/simulator/projection/provider registries
- manager/service wrapper duplication

## Non-goals

- PackageRegistry remains separate because it has different semantics

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21F_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Choose single Runtime Capability Catalog seam for runtime providers.
- Migrate call sites from overlapping registries.
- Replace generic managers with direct use-cases/composition where possible.
- Keep compatibility wrappers only for public external imports and mark deprecation.
- Delete superseded registries/managers.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Provider discovery behavior unchanged for existing features.
- No business code depends on multiple overlapping registries.
- Architecture test forbids new global registry access.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Exactly one runtime-provider catalog concept remains.
- Package registry remains separate and focused.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21f: registry, provider & manager consolidation`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G21G_STATE__EVENT__AUDIT___PROJECTION_CONSOLIDATION.md

# G21G — State, Event, Audit & Projection Consolidation

**Milestone:** M18

## Objective

Ensure there is one authority/history model and eliminate duplicate state/event machinery.

## Scope

- canonical vs derived state
- event store vs audit trace
- client/server projections

## Non-goals

- Do not erase typed audit/trajectory semantics needed later

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21G_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Identify authoritative World Ledger foundation.
- Reclassify current state as derived/materialized where appropriate.
- Unify duplicated append-only storage primitives while preserving typed streams.
- Remove UI/local authoritative copies; preserve optimistic/read caches only.
- Document reconstruction path from snapshot+events.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Discard/rebuild derived state test.
- Client reconnect rebuild test.
- Event/replay regression.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- One authoritative history model remains.
- Derived state can be rebuilt.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21g: state, event, audit & projection consolidation`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G21H_FRONTEND_SDK_SHARED_CONTRACT_CONSOLIDATION.md

# G21H — Frontend/SDK Shared Contract Consolidation

**Milestone:** M18

## Objective

Reduce duplicate client schemas/state and prepare one Stable World ABI/API pipeline.

## Scope

- OpenAPI/TS generation
- shared API client
- world/branch/projection identifiers
- feature-specific duplicated DTOs

## Non-goals

- No full UI redesign

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21H_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Inventory duplicated frontend DTOs and hand-maintained schemas.
- Generate or centralize shared API types.
- Consolidate server-truth client cache patterns.
- Remove feature-local authoritative world state.
- Preserve product feature modules while sharing transport/identity/projection primitives.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Type generation diff stable.
- Frontend typecheck/build.
- Reconnect/server-truth e2e.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- No manually duplicated public schema P0/P1.
- UI continues to render from server projections.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21h: frontend/sdk shared contract consolidation`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G21I_MINIMAL_CORE_TARGET_FREEZE___M18_QUALIFICATION.md

# G21I — Minimal-Core Target Freeze & M18 Qualification

**Milestone:** M18

## Objective

Freeze the reduced architecture as the migration baseline before semantic additions.

## Scope

- minimality ledger
- ADRs
- dependency boundaries
- deletion/merge evidence

## Non-goals

- No M19 semantic features except those required to keep code compiling

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G21I_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Re-run all M18 architecture/minimality checks.
- Record before/after package/LOC/class/registry metrics.
- Freeze target boundaries and compatibility adapters.
- Close M18 P0/P1 findings or explicitly fail.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Critical M17 regression.
- Architecture/dead-code/schema checks.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- M18 PASS only with zero consolidation P0/P1 gaps.
- Repository is smaller/clearer in concepts even if raw LOC is not strictly lower.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g21i: minimal-core target freeze & m18 qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: milestones/M18_QUALIFICATION.md

# M18 Qualification — Minimal-Core Consolidation Baseline

## Preconditions

All Goals in M18 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M18 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M18.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M18_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- Verified v5.0/M17 baseline and golden fixtures exist.
- Every v5.1 delta is classified.
- Duplicate/dead/fake architecture P0/P1 findings are closed.
- Overlapping runtime registries/managers/state paths are consolidated.
- Target dependency boundaries are executable via architecture tests.
- Code-minimality ledger contains before/after metrics.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- create a local milestone checkpoint;
- continue automatically to the first Goal of the next milestone.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.


---

# FILE: goals/GOAL_G22A_REALITY_CALCULUS_SEMANTIC_MAPPING_WITHOUT_NEW_GOD_ENGINE.md

# G22A — Reality Calculus Semantic Mapping Without New God Engine

**Milestone:** M19

## Objective

Represent Distinction/Relation/Transition/Commitment using existing core contracts and tests, not a parallel runtime.

## Scope

- identity semantics
- relation/fact semantics
- transition semantics
- commitment semantics

## Non-goals

- No WorldRealityCalculusEngine service
- No mass rename

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22A_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Write semantic mapping ADR from mother-spec primitives to concrete existing types/functions.
- Strengthen identity/reference invariants where missing.
- Ensure Transition contract explicitly describes before/trigger/constraints/result/scope.
- Add tests proving generated text/proposal/observation is not committed reality.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Identity stability/property tests.
- Transition contract tests.
- No direct-mutation architecture test.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- All four primitives have executable semantics/evidence without duplicate engine code.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22a: reality calculus semantic mapping without new god engine`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G22B_SCOPED_FACT_CONTRACT___AUTHORITY_PARTITION.md

# G22B — Scoped Fact Contract & Authority Partition

**Milestone:** M19

## Objective

Add/normalize the v5.1 scoped Fact semantics while preventing scope-based authority escalation.

## Scope

- Fact subject/predicate/object-value/scope/valid_time/provenance
- canonical/public/org/actor/hypothesis/reconstruction scopes

## Non-goals

- No universal EAV database rewrite unless already justified

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22B_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Audit existing Fact/Claim/Belief models and reuse shared value objects.
- Introduce minimal Fact/FactScope contract or adapters.
- Define canonical promotion use case that must go through Commit.
- Define read filters for actor/org/public/reconstruction views.
- Preserve domain-specific structured tables/components where they are clearer.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Changing scope directly cannot create canonical fact.
- Actor belief remains isolated.
- Reconstruction cannot overwrite physical/canonical fact.
- Serialization/version tests.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Unified semantic fact language exists.
- Authority remains separated.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22b: scoped fact contract & authority partition`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G22C_UNIFIED_WORLD_COMMIT_KINDS__STATE___ONTOLOGY___LAW.md

# G22C — Unified World Commit Kinds: State / Ontology / Law

**Milestone:** M19

## Objective

Extend the existing single Commit Authority to three semantic World Commit kinds without three parallel engines.

## Scope

- CommitRequest discriminant
- StateDelta/OntologyDelta/LawDelta payloads
- shared expected revision/idempotency/audit

## Non-goals

- No CapabilityCommit
- No separate commit repositories

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22C_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Add versioned commit-kind schema.
- Route all three through existing validation/adjudication/atomic append pipeline.
- Keep common transaction/idempotency/concurrency semantics centralized.
- Add kind-specific invariant dispatch only where necessary.
- Migrate existing state commits without changing historical meaning.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- State commit legacy tests unchanged.
- Ontology/Law positive/negative tests.
- Duplicate/stale/idempotency tests for all kinds.
- Atomic failure rollback for all kinds.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- One commit pipeline serves all three kinds.
- No fourth World commit kind exists.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22c: unified world commit kinds: state / ontology / law`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G22D_AUTHORITY_MICROKERNEL_CONTRACT___EXISTING_COMMITAUTHORITY_ADAPTATION.md

# G22D — Authority Microkernel Contract & Existing CommitAuthority Adaptation

**Milestone:** M19

## Objective

Make the existing authority implementation conform to the minimal v5.1 microkernel responsibilities without replacing proven internals.

## Scope

- identity/ref checks
- commit boundary
- invariant execution
- ledger append
- branch/version context
- replay references

## Non-goals

- No product/domain knowledge in microkernel

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22D_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define narrow authority contract and map existing implementation.
- Move only boundary-violating code out of authority.
- Ensure provider/plugin/compiler APIs expose proposal only.
- Add architecture tests preventing ORM/direct write bypass.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Mutation path tests across API/agent/simulator/compiler/provider.
- Domain-specific names absent from core dependency graph.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- CommitAuthority remains the sole authority and satisfies microkernel contract.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22d: authority microkernel contract & existing commitauthority adaptation`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G22E_SEMANTIC_SPACE__LAW_SET___CONSTITUTION_VERSION_CONTEXT.md

# G22E — Semantic Space, Law Set & Constitution Version Context

**Milestone:** M19

## Objective

Version Σ/Γ/World Constitution so old history can be interpreted deterministically after ontology/law evolution.

## Scope

- SemanticSpaceVersion
- LawSetVersion
- ConstitutionVersion
- domain rule versions
- snapshot/event references

## Non-goals

- Do not persist an entire duplicated ontology per event

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define stable identifiers/version manifests and resolution repository.
- Attach version context to new committed events/snapshots.
- Define default migration mapping for legacy v5.0 events.
- Pin instances/branches to explicit context revisions.
- Prevent ordinary LawCommit from mutating immutable constitution rules.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Legacy event context resolution.
- Unknown/missing version fails diagnostically.
- Constitution mutation rejection.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Every new commit can resolve exact semantic/law context.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22e: semantic space, law set & constitution version context`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G22F_COMMITTED_EVENT_ENVELOPE___REPLAY_CONTEXT_MIGRATION.md

# G22F — Committed Event Envelope & Replay-context Migration

**Milestone:** M19

## Objective

Upgrade event interpretation metadata while keeping v5.0 event histories replayable.

## Scope

- event version
- commit kind
- semantic/law/constitution refs
- provenance/adjudication/trace refs

## Non-goals

- No silent rewrite of historical event payloads

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22F_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Extend event envelope minimally.
- Implement legacy adapter/upcaster only where required.
- Version event deserialization explicitly.
- Update snapshots/checkpoint watermark semantics.
- Preserve semantic hash rules and document excluded metadata.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Golden v5.0 stream replays under v5.1.
- New mixed State/Ontology/Law stream replays.
- Missing upcaster/version fails explicitly.
- Deterministic semantic hash.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- v5.0 and v5.1 streams have deterministic, documented interpretation.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22f: committed event envelope & replay-context migration`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G22G_THREE_TIER_WORLD_INVARIANT_REGISTRY.md

# G22G — Three-tier World Invariant Registry

**Milestone:** M19

## Objective

Formalize Kernel/Domain/World invariants as reusable pre-commit contracts without three separate engines.

## Scope

- invariant metadata
- scope
- version
- priority/severity
- applicable commit kinds

## Non-goals

- No world invariant may override kernel constitution

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22G_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Adapt existing validators/invariants into one registry abstraction.
- Define deterministic ordering and failure aggregation.
- Load domain/world invariants through package/runtime composition without direct authority access.
- Reuse same checks in replay/migration/provider upgrade tests.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Kernel invariant cannot be overridden.
- Domain/world invariant versioning.
- Replay reuses historical invariant context as designed.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- One registry concept with three scopes.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22g: three-tier world invariant registry`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G22H_DERIVED_CURRENT_STATE___MATERIALIZED_PROJECTION_CONTRACT.md

# G22H — Derived Current State / Materialized Projection Contract

**Milestone:** M19

## Objective

Make authority-vs-current-state semantics explicit and minimize duplicate state stores.

## Scope

- fold/project from history
- snapshot restore
- derived caches
- read models

## Non-goals

- No requirement to rebuild every read model on every request

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22H_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Label authoritative vs derived repositories.
- Ensure derived state can be discarded/rebuilt.
- Remove mutation APIs on read-only projections.
- Add consistency watermark/revision semantics.
- Document cache invalidation after ontology/law changes.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Delete derived state and rebuild.
- Projection revision consistency.
- Ontology/Law change invalidates/reprojects correctly.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Current state is efficient but not an independent truth source.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22h: derived current state / materialized projection contract`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G22I_M19_AUTHORITY_COMPATIBILITY_QUALIFICATION.md

# G22I — M19 Authority Compatibility Qualification

**Milestone:** M19

## Objective

Prove v5.1 semantic authority changes preserve all M1/M17 guarantees.

## Scope

- full authority/replay/branch/version/invariant regression

## Non-goals

- No M20 features

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G22I_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Run mixed-commit world fixture.
- Re-run golden v5.0 event streams.
- Audit code minimality after new semantic contracts.
- Close M19 P0/P1 gaps.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Full core unit/property/contract/migration/replay suite.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- M19 PASS with one authority pipeline, deterministic legacy replay and zero semantic bypasses.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g22i: m19 authority compatibility qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: milestones/M19_QUALIFICATION.md

# M19 Qualification — Authority Microkernel & Reality Semantics

## Preconditions

All Goals in M19 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M19 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M19.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M19_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- One authority pipeline supports State/Ontology/Law commits.
- No CapabilityCommit World semantics exist.
- Fact scopes cannot escalate authority by field mutation.
- Semantic/law/constitution versions make replay interpretation explicit.
- v5.0 golden event streams replay correctly.
- Kernel/Domain/World invariants share one registry model.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- create a local milestone checkpoint;
- continue automatically to the first Goal of the next milestone.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.


---

# FILE: goals/GOAL_G23A_GENESISSPEC_INTEGRATION_WITH_EXISTING_WORLDPACK___SCENARIO.md

# G23A — GenesisSpec Integration with Existing WorldPack / Scenario

**Milestone:** M20

## Objective

Introduce Genesis semantics without creating a parallel package ecosystem.

## Scope

- GenesisSpec schema
- WorldPack/Scenario/override resolution
- rights/source/seed/version refs

## Non-goals

- No GenesisPackageRegistry

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23A_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Map existing instance creation/scenario bootstrap to GenesisSpec.
- Define schema for semantic seed, initial conditions, laws, possibility policy, meta-law refs, resolution/randomness policy.
- Reuse package dependency/version/rights machinery.
- Persist genesis event/reference on instance creation.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Existing world instantiation still works.
- GenesisSpec validation/version tests.
- Package export/import round trip.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- One package system; GenesisSpec is composable initialization data.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23a: genesisspec integration with existing worldpack / scenario`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G23B_DESIGNER_GENESIS_STABLE_PATH.md

# G23B — Designer Genesis Stable Path

**Milestone:** M20

## Objective

Make mature author-defined worlds instantiate through the Genesis semantics while reusing current bootstrap code.

## Scope

- synthetic reference world
- scenario initial snapshot
- deterministic seed/laws

## Non-goals

- No True Genesis research

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23B_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Adapt current instantiate() path to emit/record GenesisEvent.
- Validate initial ontology/laws/state against invariants.
- Ensure seed/version/source/rights are captured.
- Provide minimal authoring schema/example.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Same GenesisSpec + seed yields same initial semantic state.
- Invalid initial law/identity fails before instance activation.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Designer Genesis is stable and backward-compatible.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23b: designer genesis stable path`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G23C_ONTOLOGY_CANDIDATE___ONTOLOGYCOMMIT.md

# G23C — Ontology Candidate & OntologyCommit

**Milestone:** M20

## Objective

Support explicit, auditable ontology-space expansion under one authority pipeline.

## Scope

- OntologyCandidate
- new entity/relation/type definitions
- compatibility/stability metadata

## Non-goals

- No LLM summary direct commit

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23C_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define minimal candidate payload and validation hooks.
- Check namespace/type conflicts and backwards compatibility.
- Commit accepted ontology change with semantic-space version bump.
- Reject changes that break core identity/branch/rights contracts.
- Expose read-only ontology version history.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Conflict/redefinition negative tests.
- Branch-local ontology commit test.
- Replay across ontology versions.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- OntologyCommit changes Σ only through authority and is replayable.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23c: ontology candidate & ontologycommit`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G23D_LAW_CANDIDATE___LAWCOMMIT.md

# G23D — Law Candidate & LawCommit

**Milestone:** M20

## Objective

Support versioned effective-law/rule-set changes while protecting World Constitution.

## Scope

- LawCandidate
- law-set version bump
- domain/scenario rule change
- effective-time semantics

## Non-goals

- No ordinary agent constitution rewrite

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23D_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define LawDelta semantics.
- Validate authority/rights/applicability/effective time.
- Separate mutable social/domain/scenario laws from immutable kernel constitution.
- Record law provenance and version.
- Update resolver lookup to historical law context.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Constitution mutation rejected.
- Historical event replay uses historical laws.
- Branch-local law divergence.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- LawCommit is auditable and cannot alter immutable constitution.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23d: law candidate & lawcommit`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G23E_BRANCH_LOCAL_ONTOLOGY___LAW_EVOLUTION___MERGE_POLICY.md

# G23E — Branch-local Ontology / Law Evolution & Merge Policy

**Milestone:** M20

## Objective

Ensure evolving semantics remain branch-isolated and do not corrupt parent/canon worlds.

## Scope

- fork semantic/law context
- child-only commits
- compare/diff
- explicit merge policy

## Non-goals

- No automatic semantic merge across incompatible branches

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Extend branch metadata with semantic/law context refs.
- Define ontology/law diff representation.
- Prevent child version changes from mutating parent manifests.
- If merge exists, require explicit compatibility validation and new commits.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Parent hash/context unchanged after child evolution.
- Incompatible merge rejected.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Branch isolation holds for state, ontology and laws.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23e: branch-local ontology / law evolution & merge policy`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G23F_POSSIBILITY_SPACE_Ω_AS_CANDIDATE_DERIVED_POLICY.md

# G23F — Possibility Space Ω as Candidate/Derived Policy

**Milestone:** M20

## Objective

Implement only the persistent seams needed for proposals/candidates without materializing an infinite possibility universe.

## Scope

- proposal/candidate persistence
- affordance/planner views
- expiration/status

## Non-goals

- No exhaustive Ω database
- No second canonical state

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23F_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define what explicit possibility objects are persisted and why.
- Reuse Candidate/Intent/Experiment stores where possible.
- Define TTL/status/branch/version context.
- Ensure discarded possibilities never mutate reality.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Proposal persistence/recovery.
- Expired/rejected candidate cannot commit without revalidation.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Ω remains minimal and non-authoritative.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23f: possibility space ω as candidate/derived policy`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G23G_EVOLUTIONARY_GENESIS_EXPERIMENTAL_SEAM.md

# G23G — Evolutionary Genesis Experimental Seam

**Milestone:** M20

## Objective

Provide a safe experimental path for worlds whose ontology/laws can grow from runtime history.

## Scope

- feature flag
- candidate generation hooks
- shadow branch
- promotion to Ontology/Law commit

## Non-goals

- Do not claim open-ended emergence solved

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23G_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Expose experimental provider protocol producing ontology/law candidates from history.
- Run only in sandbox/shadow branch by default.
- Reuse M24 promotion gates where available; stub contract now if M24 not yet implemented.
- Keep stable runtime behavior unchanged when feature flag off.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Feature-off regression identical.
- Experimental candidate cannot auto-commit.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Experimental seam exists without contaminating stable core.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23g: evolutionary genesis experimental seam`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G23H_TRUE_GENESIS_RESEARCH_CONTRACT___NO_FAKE_COMPLETION.md

# G23H — True Genesis Research Contract — No Fake Completion

**Milestone:** M20

## Objective

Represent True Genesis as a research adapter/validity contract, not a fabricated stable engine.

## Scope

- initial low-level simulator contract
- validity envelope
- co-simulation/provider seam

## Non-goals

- No toy rules presented as validated emergence
- No stable promotion without evidence

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23H_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define research-only interface and required evidence/validity metadata.
- Reuse SimulationAdapter/CoSim where applicable.
- Document explicit NOT_IMPLEMENTED_RESEARCH capability status if no validated provider exists.
- Ensure product/API does not advertise stable True Genesis falsely.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Stable tests pass with no provider installed.
- Research provider contract fake can exercise lifecycle without claiming scientific validity.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- No fake stable True Genesis.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23h: true genesis research contract — no fake completion`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G23I_M20_GENESIS___ONTOLOGY___LAW_QUALIFICATION.md

# G23I — M20 Genesis / Ontology / Law Qualification

**Milestone:** M20

## Objective

Prove Designer Genesis and semantic/law evolution integrate with legacy worlds and branch/replay semantics.

## Scope

- designer genesis
- ontology/law commits
- branch isolation
- legacy instantiate

## Non-goals

- No Distillation Fabric yet required

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G23I_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Run old and new world initialization paths.
- Run mixed ontology/law branch scenario.
- Audit no parallel package registry was introduced.
- Close M20 P0/P1 gaps.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Genesis round-trip, replay, branch, migration suites.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- M20 PASS with one package system and no fake research claims.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g23i: m20 genesis / ontology / law qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: milestones/M20_QUALIFICATION.md

# M20 Qualification — Genesis / Ontology / Law Evolution

## Preconditions

All Goals in M20 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M20 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M20.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M20_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- GenesisSpec reuses existing package/scenario systems.
- Designer Genesis is stable/deterministic.
- Ontology/Law evolution is branch-local and replayable.
- Ω is non-authoritative and minimally persisted.
- Evolutionary/True Genesis status is honestly experimental/research where applicable.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- create a local milestone checkpoint;
- continue automatically to the first Goal of the next milestone.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.


---

# FILE: goals/GOAL_G24A_CANDIDATEENVELOPE__ORIGIN_CLASS___PROVENANCE_CONTRACT.md

# G24A — CandidateEnvelope, Origin Class & Provenance Contract

**Milestone:** M21

## Objective

Create one candidate contract for distillation/generated/reconstructed/world-emergent structures.

## Scope

- candidate type/payload/source refs/evidence/confidence/origin/method/status/version

## Non-goals

- Candidate is never canonical reality

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24A_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Audit existing compiler/completion candidate models and merge/adapt.
- Define OriginClass: external source, human-created, simulated, model-generated, world-emergent, reconstructed as applicable.
- Add branch/semantic/law context.
- Add immutable provenance references and review status.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Serialization/version tests.
- Candidate cannot be queried through canonical-only path.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- One CandidateEnvelope covers new distillation paths without erasing typed payloads.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24a: candidateenvelope, origin class & provenance contract`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G24B_MINIMAL_DISTILLER_PROTOCOL___ORCHESTRATION.md

# G24B — Minimal Distiller Protocol & Orchestration

**Milestone:** M21

## Objective

Generalize current extraction/compiler components into a small provider protocol rather than many engines.

## Scope

- Distiller input/output contract
- deterministic/LLM provider variants
- composition/order

## Non-goals

- No per-distiller pipeline framework

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24B_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define a small typed Distiller protocol.
- Adapt existing extractors instead of rewriting them.
- Create minimal orchestration that composes distillers and validators.
- Use explicit dependencies, no global registry.
- Record provider/model/version/provenance.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Deterministic distiller tests.
- Provider substitution contract test.
- No external API required in CI.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Multiple distiller types run through one orchestration seam.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24b: minimal distiller protocol & orchestration`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G24C_FOUNDATIONAL_DISTILLATION___REUSE_EXISTING_COMPILER.md

# G24C — Foundational Distillation — Reuse Existing Compiler

**Milestone:** M21

## Objective

Turn the v5.0 source/compiler pipeline into Source→Candidate→Review→Package without duplicating parsers/assemblers.

## Scope

- TXT/MD/JSON/YAML existing support
- source registry
- entity/event/relation extraction
- package assembler

## Non-goals

- No unapproved real-data canonicalization
- No forced OCR/video implementation unless already available

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24C_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Route parser/extractor outputs through CandidateEnvelope.
- Preserve evidence and completion levels.
- Reuse package assembler and review workflow.
- Separate explicit/canonical vs interpretive/reconstructed/generated candidates.
- Keep source gate unchanged or stronger.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Existing compiler fixtures pass.
- Unapproved source cannot produce canonical package facts.
- Conflicting claims remain distinct.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Compiler functionality is preserved under Distillation semantics.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24c: foundational distillation — reuse existing compiler`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G24D_REUSABLE_TYPED_DISTILLERS_FOR_IDENTITY___RELATION___EVENT___PERSONA___RULE___SKILL___ONTOLOGY.md

# G24D — Reusable Typed Distillers for Identity / Relation / Event / Persona / Rule / Skill / Ontology

**Milestone:** M21

## Objective

Implement only reusable typed strategies necessary to cover v5.1 candidate categories.

## Scope

- adapters around existing extractors
- typed candidate payloads
- shared evidence hooks

## Non-goals

- No separate engine/repository per distiller

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24D_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Inventory which candidate types already have extraction logic.
- Adapt existing implementations first.
- Implement missing minimal deterministic/reference distillers where feasible.
- Allow LLM-based distillers only behind provider ports.
- Reuse candidate validation and evidence binding.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Each candidate type has at least contract + deterministic fixture path.
- No type bypasses CandidateEnvelope.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- v5.1 distiller taxonomy is representable without architecture explosion.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24d: reusable typed distillers for identity / relation / event / persona / rule / skill / ontology`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G24E_EVIDENCE_BINDING__REVIEW___COMPLETION_LEVEL_CONSOLIDATION.md

# G24E — Evidence Binding, Review & Completion-level Consolidation

**Milestone:** M21

## Objective

Preserve source/claim/evidence/rights semantics across all distillation candidates.

## Scope

- E0–E5/completion levels
- explicit vs inferred vs interpretive vs reconstructed vs generated
- review policy

## Non-goals

- No silent upgrade to E0/canonical

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Map existing completion/evidence labels to v5.1 candidates.
- Require evidence references where claimed.
- Preserve conflicting candidate claims.
- Enforce rights/source review before package/canonical use.
- Add human-review seam without making it mandatory for synthetic fixtures.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Model-generated candidate cannot become E0.
- Denied rights blocks export/use.
- Conflicting claims coexist.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Evidence semantics remain traceable across distillation.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24e: evidence binding, review & completion-level consolidation`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G24F_EVOLUTIONARY_DISTILLATION_FROM_COMMITTED_HISTORY.md

# G24F — Evolutionary Distillation from Committed History

**Milestone:** M21

## Objective

Extract long-term relation/skill/persona/institution/ontology candidates from runtime history without direct write-back.

## Scope

- history window/query
- pattern provider
- candidate emission
- branch/version context

## Non-goals

- No automatic world self-modification

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24F_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Create history-query seam reusing World Ledger.
- Implement deterministic reference pattern distillers for at least two categories (e.g., repeated relation/skill pattern).
- Emit CandidateEnvelope with origin=world-emergent/simulated as appropriate.
- Record supporting event refs/time windows.
- Send accepted candidates to existing review/commit paths only after validation.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Same history yields deterministic reference candidates.
- Candidate references valid committed events.
- No candidate auto-commits.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- World history can feed Meaning pipeline safely.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24f: evolutionary distillation from committed history`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G24G_ANTI_SELF_EVIDENCE__CANON_ESCALATION___FEEDBACK_LOOP_PROTECTION.md

# G24G — Anti-self-evidence, Canon Escalation & Feedback-loop Protection

**Milestone:** M21

## Objective

Prevent model-generated content from recursively validating itself into external/canonical truth.

## Scope

- origin lineage
- evidence independence
- promotion policy
- cycle detection

## Non-goals

- No blanket ban on world-emergent fictional structures

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24G_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Track candidate/evidence ancestry.
- Detect evidence chains that only originate from the same generated/model lineage.
- Require independent source/domain/human validation for promotions that claim external truth.
- Allow synthetic/world-internal emergence under clearly scoped world rules.
- Add loop diagnostics.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Generated self-loop cannot promote to external canonical claim.
- Synthetic fictional ontology may promote under world-scoped policy.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- No self-proving canon escalation.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24g: anti-self-evidence, canon escalation & feedback-loop protection`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G24H_DOMAIN_DISTILLATION_PROFILES_WITHOUT_CORE_HARDCODING.md

# G24H — Domain Distillation Profiles without Core Hardcoding

**Milestone:** M21

## Objective

Package Red Chamber/Family/Heritage/Campaign distillation composition as profiles/configuration, not core conditionals.

## Scope

- profile declares distillers/providers/review/source gates
- generic profile schema

## Non-goals

- Do not fabricate real source content

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24H_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define profile schema/config.
- Create synthetic/reference-neutral profiles for narrative, family, heritage, campaign.
- If approved real sources exist, wire them through Source Gate; otherwise mark only real-data slice EXTERNAL_BLOCKED.
- Ensure profile-specific behavior lives in domain packages/configuration.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Core contains no world-name conditionals.
- Profiles validate and run on synthetic fixtures.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Four domains use the same Distillation Fabric.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24h: domain distillation profiles without core hardcoding`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G24I_M21_DISTILLATION___MEANING_QUALIFICATION.md

# G24I — M21 Distillation / Meaning Qualification

**Milestone:** M21

## Objective

Qualify Source→Candidate→Review→Package and History→Candidate flows while measuring code consolidation.

## Scope

- foundational/evolutionary distillation
- evidence/rights
- minimality

## Non-goals

- No M22 runtime provider work

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G24I_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Run compiler backward compatibility.
- Run evolutionary distillation fixtures.
- Audit number of new engines/registries/managers.
- Close M21 P0/P1 gaps.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Full definition/compiler/evidence contract suite.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- M21 PASS with one candidate/orchestration model and no direct candidate commit.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g24i: m21 distillation / meaning qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: milestones/M21_QUALIFICATION.md

# M21 Qualification — Distillation Fabric & Meaning Pipeline

## Preconditions

All Goals in M21 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M21 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M21.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M21_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- Existing compiler is reused under Candidate/Distiller semantics.
- One CandidateEnvelope and minimal Distiller protocol exist.
- Evidence/rights/completion/source gates remain intact.
- Evolutionary distillation produces candidates only.
- Self-evidence/canon escalation is prevented.
- Domain profiles do not hardcode world names into core.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- create a local milestone checkpoint;
- continue automatically to the first Goal of the next milestone.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.


---

# FILE: goals/GOAL_G25A_RUNTIMECAPABILITY_SEMANTIC_MODEL___NAMING_SEPARATION.md

# G25A — RuntimeCapability Semantic Model & Naming Separation

**Milestone:** M22

## Objective

Introduce runtime-provider capability semantics without colliding with in-world ActorCapability.

## Scope

- RuntimeCapabilityId
- contract version
- permissions
- scope
- determinism/replay characteristics
- health/readiness metadata

## Non-goals

- Do not rename ActorCapability generically

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25A_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Audit existing plugin/provider descriptors.
- Create/adapt minimal RuntimeCapability descriptor.
- Rename ambiguous shared types only where needed.
- Document actor-vs-runtime capability distinction.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Type/import tests prevent ambiguous cross-use.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Runtime and actor capability semantics are unambiguous.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25a: runtimecapability semantic model & naming separation`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25B_TYPED_SERVICE_CONTRACTS___SINGLE_COMPOSITION_ROOT.md

# G25B — Typed Service Contracts & Single Composition Root

**Milestone:** M22

## Objective

Provide runtime composition without a global service-locator pattern.

## Scope

- ServiceKey/Protocol
- provider construction
- constructor injection
- composition root

## Non-goals

- No business-layer registry.resolve calls scattered everywhere

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25B_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Adapt existing Port/Adapter interfaces as service contracts where appropriate.
- Create one composition root responsible for constructing providers.
- Inject dependencies explicitly into runtime/application components.
- Restrict catalog resolution APIs to bootstrap/composition code.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Architecture test forbids service-locator use outside composition boundary.
- Existing provider tests pass.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Runtime services are composable and typed without hidden global dependencies.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25b: typed service contracts & single composition root`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25C_DEPENDENCY_DAG__SCOPE___PROVIDER_LIFECYCLE.md

# G25C — Dependency DAG, Scope & Provider Lifecycle

**Milestone:** M22

## Objective

Support declarative required/provided services, explicit scopes and reversible runtime lifecycle.

## Scope

- dependency resolution
- world/instance/branch/session/request/global-safe scopes
- start/health/dispose

## Non-goals

- No hidden startup order
- No undo of world history on dispose

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25C_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Build deterministic dependency DAG with cycle diagnostics.
- Define supported scopes minimally based on actual repository needs.
- Implement activation/disposal ordering.
- Ensure lifecycle side effects have teardown handles.
- Record health/readiness and failure states.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Cycle detection.
- Dispose releases runtime effects/resources.
- Dispose leaves committed world history unchanged.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Provider lifecycle is deterministic and reversible at runtime-effect level.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25c: dependency dag, scope & provider lifecycle`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25D_RUNTIMEPROFILE_SEPARATION_FROM_WORLDPACK.md

# G25D — RuntimeProfile Separation from WorldPack

**Milestone:** M22

## Objective

Separate “what the world is” from “which providers/configuration run it”.

## Scope

- RuntimeProfile schema/version
- required capabilities/providers
- model/simulator/projection configuration
- compatibility

## Non-goals

- No provider-specific config embedded in canonical WorldPack unless it is content semantics

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25D_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Audit existing world/package configs and extract runtime-only concerns.
- Define RuntimeProfile schema and registry/reference model using existing package/version systems where possible.
- Pin active runtime revision per run/instance as appropriate.
- Support offline/deterministic profile for tests.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- WorldPack hash unchanged by runtime provider swap when content is same.
- RuntimeProfile compatibility validation.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- WorldPack and RuntimeProfile have distinct, testable responsibilities.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25d: runtimeprofile separation from worldpack`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25E_STABLE_WORLD_ABI_V1.md

# G25E — Stable World ABI v1

**Milestone:** M22

## Objective

Freeze a narrow versioned ABI between Authority/World and external runtime providers.

## Scope

- ReadOnlyWorldSnapshot
- PerceptionEnvelope
- Intent/ActionProposal
- SimulationRequest
- ProposedDelta
- ValidationResult
- CommittedEventRef
- CapabilityHealth

## Non-goals

- No ORM/session/mutable canonical handles

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Audit existing DTOs and reuse/alias instead of duplicating.
- Create ABI package/module with version policy.
- Generate/validate serialization schemas where crossing process/language boundaries.
- Add compatibility/golden fixtures.
- Document provider responsibilities and forbidden behavior.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Provider cannot mutate snapshot.
- ABI roundtrip/golden tests.
- Backward-compatible additive change test harness.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- External adapters can operate without importing internal persistence/runtime types.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25e: stable world abi v1`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25F_AGENTHARNESSPROVIDER_ADAPTATION_OF_EXISTING_POLICIES.md

# G25F — AgentHarnessProvider Adaptation of Existing Policies

**Milestone:** M22

## Objective

Wrap existing Deterministic/Rule/LLM/Human policy implementations behind the v5.1 Agent Harness ABI.

## Scope

- Perception/Fact/Memory/Skill input
- Intent/Plan/Tool/Dialogue output
- provider/model metadata

## Non-goals

- No Agent Harness owns world authority
- No forced DeepSeek dependency

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25F_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define AgentHarnessProvider contract.
- Adapt existing policies with minimal wrappers.
- Ensure provider receives filtered read-only context only.
- Record provider/model/tool versions for trajectory ledger.
- Preserve deterministic CI path.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Deterministic provider produces same intent under same context/seed.
- Forbidden mutable-state access test.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Existing agency code survives behind a stable provider seam.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25f: agentharnessprovider adaptation of existing policies`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25G_RUNTIME_CAPABILITY_CATALOG___LEGACY_REGISTRY_MERGE.md

# G25G — Runtime Capability Catalog & Legacy Registry Merge

**Milestone:** M22

## Objective

Consolidate remaining runtime provider registries into one typed catalog while keeping PackageRegistry separate.

## Scope

- provider metadata/discovery
- version/compatibility
- permissions

## Non-goals

- No universal package+runtime mega-registry

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25G_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Migrate legacy model/simulator/projection/plugin registries where semantics overlap.
- Keep domain-local registries only when they represent world content, not runtime composition.
- Provide deprecation adapters for public APIs where needed.
- Delete superseded registries.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- No duplicate provider registrations.
- Dependency resolution uses one catalog.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- One runtime provider catalog concept remains.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25g: runtime capability catalog & legacy registry merge`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25H_RUNTIMECONTROLTRANSACTION___REVERSIBLE_RUNTIME_EFFECTS.md

# G25H — RuntimeControlTransaction & Reversible Runtime Effects

**Milestone:** M22

## Objective

Model provider install/activate/deactivate/reload/rollback as runtime control operations, explicitly separate from World Commit.

## Scope

- transaction id
- before/after runtime revision
- side-effect handles
- failure rollback

## Non-goals

- No CapabilityCommit

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25H_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define runtime control transaction semantics.
- Make activation atomic from host perspective where feasible.
- Rollback partially activated dependency graph on failure.
- Record operation for later Runtime Control Ledger integration.
- Ensure world events are untouched by runtime rollback.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Activation failure leaves previous runtime usable.
- Dispose/reload does not delete world events.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Runtime changes are transactional but non-world-reality commits.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25h: runtimecontroltransaction & reversible runtime effects`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25I_RUNTIME_ARCHITECTURE_CONFORMANCE___SERVICE_LOCATOR_PERMISSION_GUARDS.md

# G25I — Runtime Architecture Conformance & Service-locator/Permission Guards

**Milestone:** M22

## Objective

Turn capability-runtime boundaries into executable architecture/security checks.

## Scope

- forbidden imports
- ORM writes
- network/file/model permissions
- catalog access

## Non-goals

- No broad monkeypatch-based policing in production

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25I_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Add static/contract tests preventing providers from direct authoritative persistence access.
- Validate declared permissions before provider activation.
- Ensure capability catalog/composition APIs are not imported from core/domain semantic modules.
- Check provider contract/version compatibility.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Malicious/reference provider direct-write attempt fails.
- Undeclared permission activation fails.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Capability Fabric cannot bypass Authority Microkernel.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25i: runtime architecture conformance & service-locator/permission guards`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G25J_M22_RUNTIME_CAPABILITY___ABI_QUALIFICATION.md

# G25J — M22 Runtime Capability / ABI Qualification

**Milestone:** M22

## Objective

Qualify provider replacement, lifecycle, RuntimeProfile and ABI compatibility without increasing core coupling.

## Scope

- swap navigation/model/simulator/reference provider where available
- reload/rollback
- deterministic profile

## Non-goals

- No M23 ledger persistence beyond temporary hooks

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G25J_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Run provider swap/reload scenarios.
- Run service-locator/permission architecture scans.
- Audit deleted legacy registries.
- Close M22 P0/P1 gaps.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- ABI contract suite + full stable regression.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- M22 PASS with one composition root/catalog and no world-history mutation by runtime lifecycle.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g25j: m22 runtime capability / abi qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: milestones/M22_QUALIFICATION.md

# M22 Qualification — Runtime Capability Fabric & Stable World ABI

## Preconditions

All Goals in M22 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M22 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M22.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M22_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- RuntimeCapability is distinct from ActorCapability.
- One typed composition root and runtime capability catalog exist.
- Provider lifecycle/dependency/scope/reload/rollback work.
- WorldPack and RuntimeProfile are separated.
- Stable World ABI exposes no mutable authority/ORM handles.
- Existing policies operate through AgentHarnessProvider adapters.
- No service-locator/global registry pattern exists in business code.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- create a local milestone checkpoint;
- continue automatically to the first Goal of the next milestone.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.


---

# FILE: goals/GOAL_G26A_SHARED_APPEND_ONLY_STREAM_INFRASTRUCTURE_FOR_TYPED_LEDGERS.md

# G26A — Shared Append-only Stream Infrastructure for Typed Ledgers

**Milestone:** M23

## Objective

Reuse event-stream storage primitives so three ledgers do not become three storage frameworks.

## Scope

- append/read/sequence/integrity/pagination/retention hooks

## Non-goals

- Do not collapse typed schemas into generic dict blob

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26A_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Extract/adapt shared stream persistence from existing event/audit code.
- Keep stream types and repository facades explicit.
- Define per-stream retention/authorization hooks.
- Preserve World Ledger stronger immutability semantics.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Ordering/integrity/concurrency tests shared.
- Typed deserialization per ledger.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Shared infrastructure, separate semantics.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26a: shared append-only stream infrastructure for typed ledgers`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G26B_WORLD_LEDGER_FACADE_OVER_EXISTING_EVENT_STORE.md

# G26B — World Ledger Facade over Existing Event Store

**Milestone:** M23

## Objective

Name/shape the existing authoritative event history as World Ledger without rewriting it.

## Scope

- CommittedEvent refs
- branch/sequence/time
- commit/adjudication/provenance refs

## Non-goals

- No duplicate copy of every world event

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26B_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Adapt existing EventStore behind WorldLedger facade/protocol only if useful.
- Keep legacy API compatibility.
- Expose stable read/query refs required by distillation/replay.
- Ensure correction/reversal remains event/branch based.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- No double append.
- Legacy replay path unchanged.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- One physical authoritative world history remains.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26b: world ledger facade over existing event store`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G26C_ACTOR_TRAJECTORY_LEDGER_WITH_PRIVACY___RETENTION_CONTROLS.md

# G26C — Actor Trajectory Ledger with Privacy / Retention Controls

**Milestone:** M23

## Objective

Record why actors made decisions while respecting private memory/context rights.

## Scope

- observation refs
- retrieved memory refs/hashes
- belief refs
- provider/model/tool
- plan/intent/adjudication/outcome
- redaction/retention

## Non-goals

- Do not permanently dump full prompts/private content by default

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26C_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define typed trajectory record.
- Store metadata/content references separately where appropriate.
- Add rights-based read authorization.
- Add retention/redaction/encryption-at-rest seam using existing security infrastructure.
- Link to world events without making trajectory authoritative truth.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Unauthorized trajectory read denied.
- Retention/redaction works without corrupting World Ledger.
- No secrets logged.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Actor explainability exists with bounded privacy exposure.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26c: actor trajectory ledger with privacy / retention controls`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G26D_RUNTIME_CONTROL_LEDGER.md

# G26D — Runtime Control Ledger

**Milestone:** M23

## Objective

Persist runtime provider/profile/model/rule activation history sufficient to explain/reproduce a run.

## Scope

- RuntimeControlTransaction
- runtime revision
- provider versions
- profile/patch
- permissions/parameters
- migration

## Non-goals

- No runtime operation rewrites World Ledger

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26D_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Persist typed runtime control records.
- Record successful and failed/rolled-back transitions appropriately.
- Link runtime revision to runs/ticks/events where needed.
- Support query “what configuration was active at world event X?”.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Activation/reload/rollback timeline query.
- Failed transaction does not become active revision.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Runtime configuration history is auditable.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26d: runtime control ledger`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G26E_CROSS_LEDGER_CORRELATION___TRACE_IDENTITY.md

# G26E — Cross-ledger Correlation & Trace Identity

**Milestone:** M23

## Objective

Allow World/Actor/Runtime ledgers to explain one outcome without merging them.

## Scope

- trace_id/run_id/world/branch/command/decision/runtime revision/commit refs

## Non-goals

- No global mutable trace state

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Standardize correlation identifiers.
- Propagate trace context through host→actor→proposal→commit→projection.
- Add join/query helpers at application/read-model layer.
- Preserve privacy filters.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- One scenario can reconstruct world event + actor decision + runtime config references.
- Missing optional actor record does not invalidate world history.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Three-ledger observability is navigable and typed.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26e: cross-ledger correlation & trace identity`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G26F_REPRODUCIBILITY_MANIFEST___RUNTIME_REVISION_PINNING.md

# G26F — Reproducibility Manifest & Runtime Revision Pinning

**Milestone:** M23

## Objective

Capture the minimal manifest needed to explain/replay deterministic outcomes under evolving providers/laws/ontology.

## Scope

- world pack/domain versions
- semantic/law/constitution versions
- runtime profile/revision
- seed
- model/provider versions
- validity assumptions

## Non-goals

- No claim that nondeterministic external LLM output is bitwise replayable unless recorded

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26F_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define reproducibility manifest schema.
- Attach manifest refs to Run and checkpoints.
- For nondeterministic providers record inputs/outputs/hashes according to policy or mark replay characteristic.
- Integrate with export/debug reports.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Deterministic run can replay from manifest.
- Missing required provider/version yields diagnostic incompatibility.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Reproducibility claims match actual provider characteristics.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26f: reproducibility manifest & runtime revision pinning`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G26G_LEDGER_INTEGRITY__QUERY__EXPORT___RETENTION_QUALIFICATION.md

# G26G — Ledger Integrity, Query, Export & Retention Qualification

**Milestone:** M23

## Objective

Provide operationally useful ledger queries/exports without weakening immutability/privacy.

## Scope

- integrity hashes/checks
- paged queries
- authorized export
- retention policies

## Non-goals

- No editable audit UI that rewrites ledger rows

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26G_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Implement integrity verification for all ledgers.
- Expose minimal read/query APIs needed by Studio/admin/debug.
- Enforce rights on actor/runtime sensitive exports.
- Document retention differences between ledgers.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Tamper/corruption detected.
- Unauthorized export denied.
- World Ledger retention never silently deletes committed history.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Ledgers are operable and policy-aware.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26g: ledger integrity, query, export & retention qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G26H_M23_TRIPLE_LEDGER_REPRODUCIBILITY_QUALIFICATION.md

# G26H — M23 Triple-ledger Reproducibility Qualification

**Milestone:** M23

## Objective

Prove one complex run can be explained across all three ledgers and replayed where deterministic.

## Scope

- cross-ledger scenario
- privacy
- runtime reload
- world commit

## Non-goals

- No M24 auto-promotion

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G26H_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Execute scenario with provider switch and actor decision.
- Trace outcome across ledgers.
- Run integrity/privacy/replay tests.
- Close M23 P0/P1 gaps.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Full ledger/integrity/rights suite.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- M23 PASS with no giant untyped audit table.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g26h: m23 triple-ledger reproducibility qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: milestones/M23_QUALIFICATION.md

# M23 Qualification — Triple Ledgers & Reproducibility

## Preconditions

All Goals in M23 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M23 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M23.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M23_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- World/Actor/Runtime ledgers remain semantically separate.
- Append-only infrastructure is shared where appropriate.
- Actor trajectory respects privacy/retention.
- Runtime control history explains active provider/profile revisions.
- Cross-ledger trace correlation works.
- Reproducibility manifests accurately describe deterministic/nondeterministic providers.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- create a local milestone checkpoint;
- continue automatically to the first Goal of the next milestone.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.


---

# FILE: goals/GOAL_G27A_RUNTIME_CAPABILITY_PROPOSAL_MODEL.md

# G27A — Runtime Capability Proposal Model

**Milestone:** M24

## Objective

Represent proposed new/updated runtime capabilities as non-active candidates with explicit provenance/risk.

## Scope

- provider/package/version
- required permissions
- expected benefit
- rollback plan
- tests/evals

## Non-goals

- Proposal is not activation

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27A_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define proposal schema/state machine.
- Link to source/creator/evidence as appropriate.
- Validate compatibility and permissions before sandbox.
- Keep ordinary agents unable to propose constitution/authority replacement.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Invalid/forbidden proposal rejected.
- Proposal has no effect before activation.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Runtime evolution begins as auditable candidate.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27a: runtime capability proposal model`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G27B_SANDBOX___SHADOW_BRANCH_EVALUATION_ENVIRONMENT.md

# G27B — Sandbox & Shadow-branch Evaluation Environment

**Milestone:** M24

## Objective

Reuse Branch/Snapshot/Experiment systems to test candidate capabilities safely.

## Scope

- branch clone
- isolated runtime profile revision
- test data/synthetic worlds
- resource limits

## Non-goals

- No candidate provider runs against production world authority by default

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27B_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Create shadow world/branch from checkpoint.
- Activate candidate only in isolated runtime composition.
- Ensure storage/network/tool permissions are sandboxed according to existing infrastructure.
- Capture all evaluation ledgers.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Shadow changes cannot alter parent.
- Provider dispose cleans runtime effects.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Candidate testing is isolated and reproducible.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27b: sandbox & shadow-branch evaluation environment`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G27C_PROMOTION_EVALUATION_GATE__INVARIANT___REGRESSION___SECURITY___COST___DETERMINISM.md

# G27C — Promotion Evaluation Gate: Invariant / Regression / Security / Cost / Determinism

**Milestone:** M24

## Objective

Turn existing M10–M17 tests into reusable promotion gates for runtime evolution.

## Scope

- core invariants
- domain/world invariants
- replay
- security/rights
- performance/cost
- determinism characteristics

## Non-goals

- No single scalar score auto-promotes critical capability

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27C_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Create evaluation manifest and runner that references existing suites.
- Support hard-fail vs advisory metrics.
- Compare candidate vs baseline profile.
- Store evidence and validity envelope.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Known-bad provider fails gate.
- Baseline provider passes.
- Evaluation results reproducible.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Promotion is evidence-driven.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27c: promotion evaluation gate: invariant / regression / security / cost / determinism`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G27D_APPROVAL___PROMOTION_POLICY.md

# G27D — Approval & Promotion Policy

**Milestone:** M24

## Objective

Define who/what can approve candidate runtime/world-structure changes by risk class.

## Scope

- automatic low-risk policy
- human/admin approval
- domain expert/source gate
- world constitution exclusions

## Non-goals

- No ordinary agent self-approval of privileged changes

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27D_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define risk tiers and approver requirements.
- Integrate rights/security/source provenance.
- Require manual/expert approval for ontology/law changes when policy says so.
- Record approval decision.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Self-approval attack rejected.
- Insufficient approver permission rejected.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Promotion authority is explicit and auditable.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27d: approval & promotion policy`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G27E_TRANSACTIONAL_ACTIVATION___ROLLBACK.md

# G27E — Transactional Activation & Rollback

**Milestone:** M24

## Objective

Promote a passed runtime capability atomically while preserving previous known-good runtime revision.

## Scope

- dependency graph activation
- runtime revision
- rollback checkpoint
- health window

## Non-goals

- Rollback cannot undo committed world events

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Prepare candidate runtime revision.
- Activate dependencies transactionally.
- Switch host at safe boundary.
- On activation failure restore previous runtime revision.
- Write Runtime Control Ledger records.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Mid-activation failure rollback.
- Committed world history unchanged by runtime rollback.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Safe activation/rollback works.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27e: transactional activation & rollback`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G27F_POST_ACTIVATION_OBSERVATION___AUTOMATIC_MANUAL_ROLLBACK_POLICY.md

# G27F — Post-activation Observation & Automatic/Manual Rollback Policy

**Milestone:** M24

## Objective

Detect regressions after promotion and safely return to previous runtime configuration.

## Scope

- health/SLO/invariant alerts
- observation window
- rollback trigger

## Non-goals

- No silent world-history rollback

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27F_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Define bounded observation period and metrics.
- Integrate existing observability.
- Implement policy-controlled runtime rollback.
- Record reason/evidence.
- Mark affected world events normally; do not erase them.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Health regression triggers configured rollback.
- World ledger remains intact.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Runtime can recover from bad promoted provider.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27f: post-activation observation & automatic/manual rollback policy`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G27G_CANDIDATE_SKILL___RULE___INSTITUTION___ONTOLOGY___LAW_PATHS.md

# G27G — Candidate→Skill / Rule / Institution / Ontology / Law Paths

**Milestone:** M24

## Objective

Connect evolutionary distillation candidates to the correct world/runtime promotion semantics without inventing generic self-modification.

## Scope

- Actor skill/capability update
- domain/world rule candidate
- institution candidate
- ontology/law candidate

## Non-goals

- No one-size-fits-all CapabilityCommit

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27G_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Map each candidate category to existing State/Ontology/Law Commit or runtime transaction.
- Reuse invariant/source/approval gates.
- Define domain-specific validation hooks where required.
- Keep candidate origin/evidence lineage.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Each category reaches correct boundary.
- Wrong-boundary attempt rejected.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- World self-growth is typed and bounded.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27g: candidate→skill / rule / institution / ontology / law paths`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G27H_CONSTITUTIONAL_ATTACK___SELF_MODIFICATION_ADVERSARIAL_QUALIFICATION.md

# G27H — Constitutional Attack & Self-modification Adversarial Qualification

**Milestone:** M24

## Objective

Prove agents/providers cannot modify core authority, branch semantics, evidence/rights contracts or immutable constitution.

## Scope

- prompt/tool/provider/package attacks
- malicious law/ontology proposals
- direct DB attempts

## Non-goals

- No unsafe exploit details beyond repository test needs

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27H_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Create adversarial test fixtures.
- Attempt provider/agent authority replacement.
- Attempt LawCommit against kernel constitution.
- Attempt branch/history rewrite and rights bypass.
- Verify diagnostics/audit.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- All constitutional attacks fail closed.
- No partial world mutation.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Core reality semantics remain non-self-modifiable by ordinary capability.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27h: constitutional attack & self-modification adversarial qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G27I_M24_BOUNDED_RUNTIME_EVOLUTION_QUALIFICATION.md

# G27I — M24 Bounded Runtime Evolution Qualification

**Milestone:** M24

## Objective

Qualify proposal→sandbox→evaluation→approval→activate→observe→rollback end-to-end.

## Scope

- one good candidate
- one bad candidate
- one forbidden candidate

## Non-goals

- No autonomous production self-rewrite

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G27I_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Run full promotion lifecycle.
- Verify three-ledger evidence.
- Audit feature flags/defaults.
- Close M24 P0/P1 gaps.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- End-to-end promotion/rollback + security regression.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- M24 PASS with bounded, reversible runtime evolution only.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g27i: m24 bounded runtime evolution qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: milestones/M24_QUALIFICATION.md

# M24 Qualification — Bounded Runtime Evolution

## Preconditions

All Goals in M24 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M24 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M24.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M24_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- Capability proposal→sandbox→evaluation→approval→activation→observation→rollback works.
- Shadow branch isolates candidate effects.
- Promotion gate reuses invariant/regression/security/cost/determinism suites.
- Runtime rollback cannot undo world history.
- Ordinary agents/providers cannot modify constitution/authority/branch/evidence-rights semantics.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- create a local milestone checkpoint;
- continue automatically to the first Goal of the next milestone.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.


---

# FILE: goals/GOAL_G28A_V5_0_PERSISTED_WORLD___EVENT___SNAPSHOT_BACKWARD_COMPATIBILITY.md

# G28A — v5.0 Persisted-world / Event / Snapshot Backward Compatibility

**Milestone:** M25

## Objective

Prove real v5.0 artifacts captured in G21A survive v5.1 runtime changes.

## Scope

- event streams
- snapshots
- world packages
- instances/branches
- DB migrations

## Non-goals

- No hand-editing golden fixtures to make them pass

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28A_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Load/migrate golden v5.0 database/artifacts.
- Replay v5.0 streams with legacy version context.
- Compare semantic hashes and critical state.
- Document any intentionally changed non-semantic metadata.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Golden replay equality.
- Migration forward repeatability.
- Failure diagnostic on unsupported artifact.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Backward compatibility report has reproducible evidence.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28a: v5.0 persisted-world / event / snapshot backward compatibility`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G28B_SCHEMA___API___SDK_COMPATIBILITY___DEPRECATION_QUALIFICATION.md

# G28B — Schema / API / SDK Compatibility & Deprecation Qualification

**Milestone:** M25

## Objective

Ensure external integrations can upgrade without hidden breaking changes.

## Scope

- OpenAPI/TS SDK
- package schemas
- Stable World ABI
- deprecation adapters

## Non-goals

- No permanent compatibility wrapper without sunset policy

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28B_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Diff public schemas against baseline.
- Classify additive/deprecated/breaking changes.
- Provide migrations/adapters where justified.
- Update SDK generation/versioning/docs.
- Remove obsolete wrappers whose sunset is complete within this program only when safe.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Old sample client/package still builds or receives documented migration path.
- ABI compatibility tests.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- No undocumented public breaking change.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28b: schema / api / sdk compatibility & deprecation qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G28C_SYNTHETIC_REFERENCE_WORLD_FULL_V5_1_REGRESSION.md

# G28C — Synthetic Reference World Full v5.1 Regression

**Milestone:** M25

## Objective

Run a complete synthetic living world through Genesis, runtime profile, agency, commits, distillation, branch/replay and product projection.

## Scope

- designer genesis
- state/ontology/law branch
- host
- distillation candidate
- provider swap
- projection

## Non-goals

- No hardcoded synthetic-world branch in core

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28C_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Instantiate through normal package/scenario/genesis path.
- Run deterministic autonomous period.
- Create/approve a safe world-scoped candidate.
- Fork branch and evolve ontology/law child-only.
- Swap runtime provider via M24 path.
- Replay and compare.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- End-to-end deterministic/reference tests.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- One world exercises the complete v5.1 stable architecture.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28c: synthetic reference world full v5.1 regression`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G28D_FAMILY___HERITAGE___CAMPAIGN_CROSS_DOMAIN_QUALIFICATION.md

# G28D — Family / Heritage / Campaign Cross-domain Qualification

**Milestone:** M25

## Objective

Prove minimal core still supports substantially different domains without domain-specific core forks.

## Scope

- synthetic/approved fixtures
- rights/evidence
- domain invariants
- projection

## Non-goals

- No fabricated real data

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28D_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Run family conflicting-claim/privacy scenario.
- Run heritage physical/surrogate/reconstruction/rights scenario.
- Run campaign resource/fog/command/co-sim scenario.
- Verify each registers only domain/world invariants/resolvers/providers.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Domain-specific invariants + replay/branch tests.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- No core conditional by domain/world name.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28d: family / heritage / campaign cross-domain qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G28E_NARRATIVE___RED_CHAMBER_SOURCE_GATED_V5_1_QUALIFICATION.md

# G28E — Narrative / Red Chamber Source-gated v5.1 Qualification

**Milestone:** M25

## Objective

Validate narrative semantics and Red Chamber integration only through approved sources, otherwise fully qualify generic path and record real-data blocker.

## Scope

- character knowledge boundaries
- canon layers
- distillation profile
- embodiment
- source gate

## Non-goals

- No model-memory canon fabrication

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28E_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Run synthetic narrative fixture unconditionally.
- If approved Red Chamber sources exist, compile/distill qualified slice; else EXTERNAL_BLOCKED only for real content.
- Verify future canon does not leak into actor perception.
- Verify user branch cannot mutate canon parent.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Source-gate/knowledge-boundary/branch tests.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Narrative path is complete independent of real-source availability.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28e: narrative / red chamber source-gated v5.1 qualification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G28F_PRODUCT_SURFACES___HOST___EXTERNAL_ADAPTER_COMPATIBILITY.md

# G28F — Product Surfaces / Host / External Adapter Compatibility

**Milestone:** M25

## Objective

Ensure Studio/Experience/Strategy/Family/Heritage and external adapters still use one server truth after consolidation.

## Scope

- web/2D
- Godot/Babylon adapter contracts if present
- digital human/text client
- admin/debug

## Non-goals

- No requirement for unavailable optional engines to be installed

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28F_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Run representative UI/API e2e.
- Verify RuntimeProfile/provider status appears through read-only diagnostics.
- Verify clients receive projection not mutable state.
- Check reconnect after provider/runtime revision changes.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Frontend build/type/e2e.
- Adapter contract tests.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- No product surface maintains second authority.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28f: product surfaces / host / external adapter compatibility`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G28G_FINAL_MINIMAL_CORE__COMPLEXITY___DEAD_CODE_REDUCTION_AUDIT.md

# G28G — Final Minimal-Core, Complexity & Dead-code Reduction Audit

**Milestone:** M25

## Objective

Prove v5.1 was implemented by consolidation rather than architecture inflation.

## Scope

- LOC/classes/protocols/registries/managers/cycles/dead code
- new abstraction justifications

## Non-goals

- Do not minify/compress code merely to reduce LOC

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28G_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Compare G21A baseline to final metrics.
- Verify one package registry + one runtime capability catalog semantics.
- List every new long-lived abstraction and what it replaced/enabled.
- Remove remaining dead compatibility code safe to delete.
- Run complexity/import/dead-code/schema duplication scans.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- No P0/P1 duplicate/dead abstraction findings.
- Architecture tests green.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Final core is conceptually smaller/cleaner and documented.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28g: final minimal-core, complexity & dead-code reduction audit`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G28H_CLEAN_ROOM_BUILD___UPGRADE___RESTORE___REPLAY_CERTIFICATION.md

# G28H — Clean-room Build / Upgrade / Restore / Replay Certification

**Milestone:** M25

## Objective

Prove a fresh operator can install v5.1, upgrade v5.0 artifacts, restore backup and replay worlds without hidden developer state.

## Scope

- clean env
- migrations
- generated SDK
- backup/restore
- offline deterministic path

## Non-goals

- No manual DB edits or local-only hacks

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28H_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Build from clean checkout/artifacts.
- Create new v5.1 world.
- Upgrade captured v5.0 DB/world.
- Restore backup into clean environment.
- Replay representative branches.
- Run SDK/sample client/package.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- Clean-room command log and hashes.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- Fresh reproducible installation and upgrade path PASS.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28h: clean-room build / upgrade / restore / replay certification`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: goals/GOAL_G28I_FINAL_V5_1_TRACEABILITY__CERTIFICATION___PROGRAM_STOP.md

# G28I — Final v5.1 Traceability, Certification & Program Stop

**Milestone:** M25

## Objective

Close every v5.1-R1 requirement with implementation/test/evidence or explicit experimental/external status and then stop.

## Scope

- final reports
- P0/P1 closure
- release readiness
- experimental status

## Non-goals

- Do not invent G29 or continue feature development

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `01_V5_1_MINIMAL_CORE_PROGRAM_ARCHITECTURE.md`
- `02_CODEX_V5_1_MASTER_PROMPT.md`
- `03_MINIMAL_CORE_CODE_CONSTITUTION.md`
- `04_V5_1_DESIGN_CONFLICT_RESOLUTIONS.md`
- `05_M0_M17_TO_V5_1_MIGRATION_MAP.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- current `STATUS.md`, `PLAN.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
- relevant existing M0–M17 reports, migrations, tests and Git history
- the immediately preceding Goal report and latest milestone report

## Preconditions / dependencies

All prior Goals in `06_V5_1_GOALS_INDEX.md`; do not skip dependency gates.

## Architecture constraints

- Preserve the single World Commit boundary and authoritative committed history.
- Prefer `KEEP/MERGE/ADAPT` over `REPLACE`; replacement requires evidence and an ADR.
- No new design noun becomes a class/service/package unless it carries irreducible behavior or eliminates duplication.
- Core/domain semantic code remains independent of FastAPI, SQLAlchemy, concrete LLM/Harness/renderer/simulator SDKs.
- Runtime provider lifecycle cannot undo committed world history.
- Existing v5.0 event/package/public compatibility must remain testable throughout the Goal.
- Keep files/classes/functions cohesive; do not solve minimality by creating God objects.

## Deliverables

- production implementation or verified deletion/consolidation corresponding to this Goal;
- focused unit/contract/property/integration/migration tests as applicable;
- updates to `reports/V5_1_TRACEABILITY_MATRIX.md`;
- updates to `reports/V5_1_CODE_MINIMALITY_LEDGER.md`;
- `reports/G28I_REPORT.md`;
- ledger/documentation updates required below.

## Implementation tasks

- Regenerate full requirement traceability.
- Run final broad regression/chaos/security/replay/migration/cross-domain suites.
- Produce required final reports and implementation status.
- Verify all stable P0/P1 gaps zero.
- Create final local Git checkpoint and stop.
- Before adding a new public abstraction, record what existing code it reuses/replaces and why direct composition is insufficient.
- Delete superseded code in the same Goal when compatibility evidence permits; otherwise add a deprecation entry with explicit owner/sunset condition.
- Keep migrations/upcasters explicit for any persisted/event/public schema change.

## Required tests and verification

- All milestone suites rerun as defined.
- Run affected Ruff/Pyright(or repository-equivalent) checks.
- Run architecture/import-boundary checks.
- Run the smallest relevant v5.0 golden regression after any stable-core/schema/event change.
- Run negative tests for privilege/authority/version failures where applicable.
- Do not require external LLM/API keys for the core acceptance path.

## Acceptance criteria

- M25 PASS; stable P0/P1=0; external/experimental items explicit; Codex stops.
- No mandatory-path TODO/FIXME/pass/NotImplemented/static fake remains.
- No new direct canonical-state mutation path exists.
- Traceability and code-minimality ledgers are current.
- Tests/assertions were not weakened to obtain PASS.

## Failure / blocker handling

- Internal correctness/architecture/test failures are `FAIL` and must be fixed before PASS.
- Real external source, credential, hardware or unavailable optional provider may be `EXTERNAL_BLOCKED` only for the narrow external slice.
- Experimental research may be `EXPERIMENTAL`; never label it stable completion.
- If a proposed refactor threatens v5.0 replay/history compatibility, stop that refactor, preserve the old path, and record a migration ADR before proceeding.

## Documentation updates

Update as applicable:

- `PLAN.md`
- `STATUS.md`
- `DECISIONS.md`
- `BLOCKERS.md`
- `KNOWN_FAILURES.md`
- `CHANGELOG.md`
- architecture/compatibility/migration docs touched by this Goal

## Git / checkpoint requirements

- Do not discard unrelated user changes.
- Do not rewrite existing history.
- Commit locally only after this Goal passes acceptance.
- Suggested message: `v5.1 g28i: final v5.1 traceability, certification & program stop`
- Do not push or deploy externally.

## Exit evidence

The Goal report must contain:

- changed/deleted files;
- before/after abstraction and LOC effects;
- architecture decisions;
- migrations/upcasters introduced;
- commands/tests/results;
- PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix;
- remaining risks;
- local commit hash.


---

# FILE: milestones/M25_QUALIFICATION.md

# M25 Qualification — v5.1 Backward Migration & Final Certification

## Preconditions

All Goals in M25 are individually PASS or have only explicitly allowed narrow EXTERNAL_BLOCKED/EXPERIMENTAL slices.

## Required reading

- `docs/spec/WANXIANG_v5_1_R1_MASTER_SPEC.md`
- `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`
- all M25 Goal reports
- latest traceability/minimality ledgers
- `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`

## Qualification procedure

1. Re-run the broadest applicable regression for all capabilities changed in M25.
2. Re-run critical Commit/Event/Replay/Branch/Persistence regression if any stable core changed.
3. Re-run architecture/import/dead-code/schema duplication checks.
4. Re-run relevant migration/backward-compatibility tests.
5. Verify no acceptance was satisfied only by static/mock/placeholder behavior.
6. Inspect code-minimality ledger for new duplicate abstractions.
7. Close internal P0/P1 defects before PASS.
8. Write `reports/M25_QUALIFICATION.md` with exact commands/results/evidence.

## PASS criteria

- v5.0 persisted worlds/events/snapshots/packages upgrade/replay deterministically.
- Public API/SDK/ABI changes are compatible or explicitly migrated/deprecated.
- Synthetic full reference world passes v5.1 end-to-end.
- Family/Heritage/Campaign/Narrative paths pass generic/source-gated qualification.
- Product surfaces/adapters still consume one server truth.
- Minimal-core final audit has zero stable P0/P1 duplication/dead-path findings.
- Clean-room build/upgrade/restore/replay passes.
- All final reports exist and stable P0/P1 gaps are zero.

## Global blockers to PASS

- direct canonical mutation bypass;
- broken v5.0 golden replay caused by this milestone;
- unversioned persisted/event semantic change;
- new duplicate authority/registry/package system;
- mandatory-path TODO/mock/fake;
- architecture tests disabled/weakened;
- P0/P1 internal gap left open.

## On PASS

- update `STATUS.md`, `PLAN.md`, `CHANGELOG.md`;
- generate all final v5.1 certification reports required by `09_FINAL_ACCEPTANCE_AND_EVIDENCE_STANDARD.md`;
- create the final local M25/v5.1 checkpoint;
- **stop the program** and report completion to the user. Do not invent or start G29/M26.

## On FAIL

Stay in the milestone, fix the failure, rerun qualification. Do not continue downstream on a broken semantic baseline.
