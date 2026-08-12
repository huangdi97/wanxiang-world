# Wanxiang Engineering Program Architecture

> Project: 万相世界 · Wanxiang Semantic Persistent Living World OS  
> Program architecture version: EPA v1.0  
> Date: 2026-08-11  
> Normative product source: `docs/spec/WANXIANG_v5_MASTER_SPEC.md` / v5.0-R1  
> Purpose: turn the v5.0-R1 architecture into a controlled, testable, evolvable engineering execution system for Codex Desktop and human review.

---

## 0. Status and authority

This document does **not** redefine Wanxiang as a product. It defines how engineering work is decomposed, ordered, validated, checkpointed and evolved so that implementation remains faithful to the v5.0-R1 master specification.

Authority order for engineering disputes:

1. `docs/spec/WANXIANG_v5_MASTER_SPEC.md` — product semantics, architecture invariants and system intent.
2. This document — engineering program decomposition, dependency order, milestone gates and cross-cutting ownership.
3. Goal files under `goals/` — executable implementation contracts for a bounded unit of work.
4. `docs/architecture/*.md` and ADRs — implementation decisions consistent with the above.
5. Code and tests — implementation evidence, never permission to silently change the specification.

If code contradicts a higher authority, code is wrong until an explicit specification/ADR change is approved.

---

# 1. Engineering thesis

Wanxiang must not be built as a sequence of UI demos. The engineering program is organized around increasingly capable **authoritative world execution loops**.

A capability is considered real only when it is:

- represented by explicit typed contracts;
- reachable through the declared dependency direction;
- executable without a mandatory external LLM API key for core tests;
- covered by unit/contract/integration tests as applicable;
- compatible with deterministic replay where it participates in canonical state evolution;
- versioned where persisted or externally consumed;
- observable through structured audit/trace records;
- protected by rights/security checks when it handles restricted information;
- demonstrated by a vertical acceptance scenario rather than a static fixture alone.

The program optimizes for **long-term modifiability**, not short-term file count or screenshot completeness.

---

# 2. Immutable engineering invariants

These are non-negotiable unless the master specification itself changes.

## 2.1 World authority

1. `Canonical World State` has exactly one logical Commit Authority per branch execution context.
2. LLMs, humans, clients, sensors, domain plugins, rules and external simulators may submit intents, observations, actions, orders or proposed deltas; none may directly mutate authoritative state.
3. Every canonical mutation must pass the runtime chain appropriate to the action, minimally:

```text
Command / Intent / Observation
→ normalization
→ validation
→ resolution / adjudication when needed
→ Proposed WorldDelta
→ commit precondition check
→ atomic commit
→ Event Log + canonical state projection
→ audit / trace
```

4. A transport route, UI component, model provider or plugin is never a commit authority.

## 2.2 Formal object hierarchy

The only formal runtime hierarchy is:

```text
Domain Pack
→ World Pack
→ Scenario
→ World Instance
→ Branch
→ Session
→ Projection
```

Specific worlds such as Dream of the Red Chamber, Liaoshen Campaign, a family archive or a museum collection must never be hard-coded into Core.

## 2.3 Event-sourced history

1. World history is append-oriented and reconstructable.
2. Derived current-state tables/views are caches/projections, not irreplaceable truth.
3. Event identity, ordering, branch ancestry, schema version and causation/correlation metadata must be explicit.
4. Replay from a valid baseline plus ordered committed events must reproduce the same authoritative state hash under the same runtime/rule versions.
5. Historical corrections prefer correction events or new branches over silent mutation of historical rows.

## 2.4 Epistemic isolation

Canonical truth, public knowledge, group knowledge, observations, beliefs, memories, rumours/misinformation and later historical records are different concepts and may not be collapsed into one retrieval store.

## 2.5 Source gate

Real literary, historical, family, museum and reality-coupled data is not trusted merely because an LLM parsed it. Source, Claim, Evidence, review status, rights and provenance remain explicit. Unapproved or disallowed sources must not silently enter canonical compilation.

## 2.6 Projection separation

Text, React, Phaser, Godot, Babylon, digital humans, AR/VR and generated video are projections/adapters. They read filtered views and submit commands. They do not own world truth.

## 2.7 Deterministic core

Core world execution, invariants, replay, branch isolation, basic scheduling and deterministic policies must be testable without an LLM key. Optional model providers sit behind ports.

## 2.8 Modular monolith first

Logical kernels are boundaries, not automatic microservices. Until there is measured need for isolation/scaling, keep a modular monolith with explicit ports/adapters and strict dependency rules.

---

# 3. Program terminology

## 3.1 Macro Phase

A broad capability era containing multiple engineering Goals. A phase is not directly handed to Codex as one task.

## 3.2 Goal

The largest unit that may be handed to Codex as a bounded execution contract. A Goal must have a single dominant engineering objective and a verifiable acceptance gate.

## 3.3 Work Package

A sub-unit inside a Goal used to sequence implementation. Work packages are not independent completion claims.

## 3.4 Gate

A set of reproducible tests/checks that must pass before the Goal may be marked PASS and the next dependent Goal may begin.

## 3.5 Milestone

A system-level capability checkpoint reached by multiple Goals. Milestones run broader regression and architecture audits.

## 3.6 Checkpoint

A local Git commit/tag plus evidence report that permits deterministic resumption and rollback.

---

# 4. Goal sizing rules

A Goal is too large and MUST be split when two or more of the following are true:

- it introduces more than one major kernel boundary;
- it introduces both a new persistent data model and a large UI surface;
- it introduces both a third-party standard adapter and a new runtime subsystem;
- it requires unrelated acceptance scenarios;
- it spans multiple independent failure domains;
- it cannot be described with one dominant Objective sentence;
- its expected implementation would create pressure for generic manager/service/util files;
- it requires touching most packages in the repository;
- it cannot be fully verified with a bounded regression command set.

A Goal may be substantial, but it must remain **deep rather than broad**.

---

# 5. Macro program architecture

The legacy G0–G12 roadmap is retained as a product-aligned macro roadmap, but execution is decomposed into smaller goals.

## Phase P0 — Engineering Constitution and Reproducibility

Legacy mapping: G0.

Purpose:
- create the repository, toolchain and architecture enforcement system;
- freeze dependency direction and contribution rules;
- establish ledgers, ADRs, test taxonomy and evidence format;
- ensure future Codex runs cannot silently weaken quality gates.

Expected execution goals:
- G00A Repository & Toolchain Foundation
- G00B Architecture Guards & Engineering Constitution

Milestone M0: **Reproducible Engineering Base**.

## Phase P1 — Authoritative World Foundation

Legacy mapping: G1 plus foundational parts of G4/G12.

Purpose:
- define stable domain primitives;
- implement canonical Commit Authority;
- implement event sequencing, idempotency and append semantics;
- implement snapshot/replay/branch;
- establish persistence ports/adapters, migrations and trace contracts.

Expected goals:
- G01A Core Semantic Contracts
- G01B Commit Authority & Invariants
- G01C Event Store & Concurrency Semantics
- G01D Snapshot, Replay, Branch & Determinism
- G01E Persistence, Migration & Recovery Foundation
- G01F Minimal World Environment / API Boundary

Milestone M1: **Authoritative World Exists**.

## Phase P2 — Living World Substrate

Legacy mapping: G2.

Expected goals:
- G02A Spatial Topology & Access
- G02B Temporal System & Schedules
- G02C Material, Container, Custody & Information Payload
- G02D Body / Condition Constraints
- G02E Institution / Authority / Duty / Norm
- G02F Population Resolution & Autonomous Scheduler

Milestone M2: **Deterministic Living World Exists**.

## Phase P3 — Agency, Cognition and Action Runtime

Legacy mapping: G3 plus part of G7.

Expected goals:
- G03A Observation & Perspective Isolation
- G03B Belief / Memory / Temporal Epistemic Graph
- G03C Actor & Organization Runtime
- G03D Action / Affordance / Validator
- G03E Resolver / Adjudication & Deterministic Policies
- G03F Skill Runtime
- G03G Capability & Learning

Milestone M3: **Bounded Agents Can Live Inside the World**.

## Phase P4 — World Definition, Evidence and Packages

Legacy mapping: G4.

Note: fundamental Evidence/Rights/Version contracts are introduced earlier in P1; P4 delivers the complete authoring/compiler system.

Expected goals:
- G04A Package / Schema / Dependency Registry
- G04B Source Registry & Source Gate
- G04C Structured Compiler MVP (UTF-8 text/Markdown + JSON/YAML only)
- G04D Completion Ledger / Review Workflow
- G04E Package Install / Export / Migration Compatibility

Milestone M4: **Worlds Can Be Authored, Reviewed, Installed and Instantiated**.

## Phase P5 — Host, Human Control and Projection

Legacy mapping: G5 + G6.

Expected goals:
- G05A Minimal World Host Authority Boundary
- G05B Session & Embodiment Lease
- G05C Shadow/Human Policy & Control Handoff
- G05D Projection API & Perspective/Rights Filters
- G05E Studio Debug Vertical Slice
- G05F Phaser 2D Player Vertical Slice
- G06A Persistent Lifecycle / Pause / Advance / Background
- G06B Command Queue / Idempotent Multi-client Semantics
- G06C Crash Recovery / Checkpoint / Resource Budget

Milestone M5: **Human Can Enter a Persistent World Without Becoming the Authority**.

## Phase P6 — Reality, Opportunities, Director and Experiments

Legacy mapping: G7 + missing/under-owned parts of Kernel 14.

Expected goals:
- G07A PhysicalObservation / Reality Bridge
- G07B Observation Fusion & Validation
- G07C Opportunity / Challenge / Event Compiler
- G07D Director Runtime
- G07E Experiment Runtime / Multi-run / ValidityEnvelope

Milestone M6: **World Can Be Safely Coupled to External Context and Controlled Experiments**.

## Phase P7 — Domain Generality Qualification

Legacy mapping: G8, G9, G10.

Expected goals are domain validation projects, not Core rewrites:
- G08A Synthetic Mansion Living-world Qualification
- G08B Red Chamber Source-gated Reference Slice
- G09A GEDCOM/GEDZIP Interop
- G09B Family Semantic World & Conflicting Claims
- G09C Family Privacy / Living Archive / Digital Persona Modes
- G10A IIIF Ingest
- G10B Linked Art/CIDOC Interop
- G10C Heritage Object Semantic Twin
- G10D Museum / Object Biography / Reconstruction Scenarios

Milestone M7: **Multiple Unrelated Domains Prove Core Generality**.

## Phase P8 — Co-Simulation and Strategy

Legacy mapping: G11.

Expected goals:
- G11A SimulationAdapter Contract & Fake Simulator
- G11B Multi-rate/Event-driven Co-Sim Orchestrator
- G11C Synthetic Campaign Domain
- G11D Command / Logistics / Movement / Fog-of-war
- G11E Batch Experiment & Strategy Evaluation
- G11F Liaoshen Source-gated Reference Pack

Milestone M8: **Mechanistic External Models Can Participate Without Owning Canonical State**.

## Phase P9 — Release Qualification and Advanced Adapters

Legacy mapping: G12, but hardening is continuous and not deferred to this phase.

Expected goals:
- G12A 30-day / 1000+ tick stability qualification
- G12B Backup / restore / migration qualification
- G12C Package SDK + OpenAPI/TS SDK
- G12D Gymnasium/PettingZoo
- G12E Godot/Babylon projection contracts
- G12F Asset Foundry seam
- G12G Digital Human / XR gateway contracts
- G12H Deployment / security / private installation qualification

Milestone M9: **Release-qualified Wanxiang Platform Foundation**.

---

# 6. Dependency DAG

The program is not a simple chain. The primary dependency structure is:

```text
G00A Repository Foundation
  └─> G00B Architecture Guards
       ├─> G01A Core Contracts
       │    ├─> G01B Commit Authority
       │    │    └─> G01C Event Store
       │    │         └─> G01D Snapshot/Replay/Branch
       │    │              └─> G01E Persistence/Migration
       │    │                   └─> G01F Minimal World API
       │    │
       │    └─> foundational Evidence/Rights/Version contracts
       │
       └─> continuous cross-cutting gates

G01F
 └─> G02A/B/C/D/E
       └─> G02F Autonomous Scheduler
            └─> G03A Observation
                 ├─> G03B Cognition
                 ├─> G03C Actor/Org
                 └─> G03D Action/Affordance
                      └─> G03E Resolver
                           └─> G03F Skill
                                └─> G03G Capability

G01A + G01E
 └─> G04A Package Registry
      └─> G04B Source Gate
           └─> G04C Compiler
                └─> G04D Review/Completion
                     └─> G04E Package install/export

G02F + G03E + G04E
 └─> G05A Host Boundary
      ├─> G05B/C Embodiment
      ├─> G05D Projection
      └─> G06A/B/C Persistence lifecycle & multiplayer

G03G + G05A
 ├─> G07A/B Reality Bridge
 ├─> G07C Opportunity/Challenge
 ├─> G07D Director
 └─> G07E Experiment

M5/M6 complete
 ├─> G08 Literature qualification
 ├─> G09 Family qualification
 └─> G10 Heritage qualification

G01D + G05A + G07E
 └─> G11A/B Co-Simulation
      └─> Campaign qualification

M7 + M8
 └─> G12 Release Qualification
```

No Goal may import from a future phase to satisfy current acceptance.

---

# 7. Cross-cutting responsibility matrix

Cross-cutting capabilities must have an introduction point and remain mandatory thereafter.

| Concern | Introduced by | Mandatory thereafter | Minimum enforcement |
|---|---|---|---|
| Typed public contracts | G00A/G01A | all goals | typecheck + contract tests |
| Dependency direction | G00B | all goals | architecture import tests |
| Schema version | G00A/G01A | all persisted/external contracts | schema field + compatibility tests |
| Event provenance | G01B | all canonical changes | event metadata + audit assertions |
| Determinism | G01B/G01D | all deterministic runtime paths | same-input same-hash tests |
| Migration | G01E | every schema change | up migration + compatibility test |
| Rights | G01A foundation | every query/projection/source path | allow/deny tests |
| Source provenance | G01A/G04B | every real compiled claim | evidence link tests |
| Observability | G01B | all runtime/host/model operations | structured trace identifiers |
| Security | G00A | all adapters and uploads | validation + secret scanning + least privilege |
| Model routing/cost | first model provider | every model call | provider metadata + cost/latency counters |
| Backup/recovery | G06C | every release milestone | restore/replay acceptance |
| Performance baseline | M1 | every milestone | regression metrics, not premature optimization |
| Documentation ledger | G00A | every Goal | PLAN/STATUS/DECISIONS/etc. updated |

A Goal cannot declare PASS by saying a cross-cutting concern is “handled elsewhere” if its own changes participate in that concern.

---

# 8. Architecture boundaries and physical package map

The exact physical tree may be adjusted through ADRs, but dependency direction is frozen.

Recommended initial map:

```text
apps/
  api/                    # transport only
  web/                    # studio/player shell later

packages/
  domain/                 # pure semantic types/value objects/invariants
  application/            # use cases and orchestration ports
  runtime/                # validate/resolve/commit/replay coordination
  persistence/            # repositories/event store/snapshot adapters
  evidence/               # source/evidence/rights core contracts and policies
  packages_registry/      # package manifests/dependency resolution later
  compiler/               # authoring/compilation later
  substrate/              # living-world substrate later
  cognition/              # epistemic runtime later
  agency/                 # actor/action/skill runtime later
  projections/            # filtered DTO/gateways later
  reality_bridge/         # physical observations later
  challenges/             # opportunity/challenge/capability later
  cosim/                  # simulation adapters later
  model_providers/        # deterministic/optional LLM providers
  sdk_ts/                 # generated client later
```

Allowed dependency direction in early phases:

```text
domain
↑
evidence contracts (must not depend on persistence/web)
↑
application ports/use-cases
↑
runtime orchestration
↑
persistence/adapters and transport
```

Important clarifications:

- `domain` MUST NOT import FastAPI, SQLAlchemy, Alembic, React concepts, network clients or model SDKs.
- `runtime` MUST NOT import `apps/api`.
- `persistence` may implement ports defined above it; higher layers may not import SQLAlchemy models directly.
- `apps/api` maps transport DTOs to application commands/queries and does not contain business rules.
- future domain/world packages cannot obtain ORM sessions or write canonical tables directly.

---

# 9. Event/Commit consistency contract

This contract is mandatory before M1.

## 9.1 Command identity

Every externally submitted command/action that can lead to a canonical mutation must carry or receive:

- `command_id` / idempotency key;
- instance id;
- branch id;
- actor/controller identity when relevant;
- expected branch revision when optimistic concurrency applies;
- causation id;
- correlation/trace id.

## 9.2 Commit transaction

A successful commit must atomically establish:

1. accepted adjudication/result;
2. ordered committed event(s);
3. canonical delta application or rebuildable projection update;
4. new branch revision;
5. audit trace.

No partial state is allowed where current state changed but the corresponding event was not committed, or vice versa.

## 9.3 Idempotency

Retrying the same `command_id` must not duplicate canonical effects. The system should return/recover the prior result or a deterministic duplicate outcome.

## 9.4 Optimistic concurrency

If a command was prepared against revision N and branch has advanced incompatibly, commit must fail with a structured conflict rather than overwrite later state.

## 9.5 Replay

Replay must use committed event ordering and declared versions. Replay is not “reading a serialized final state”.

## 9.6 Branching

A branch has explicit ancestry:

```text
parent_branch_id
fork_event_seq / fork_revision
fork_snapshot_ref when applicable
```

Writes to a child never mutate the parent event stream.

---

# 10. Versioning and migration policy

Versioning is not deferred to release hardening.

Every persisted/external contract must identify its schema version.

At minimum track:

- DB schema migration revision;
- event schema version;
- snapshot schema version;
- package schema version;
- runtime version/build id in acceptance evidence;
- rule/domain package version where a committed outcome depends on it;
- model/prompt/provider version when a model participates in a non-deterministic proposal.

Compatibility tests must include old fixtures. A migration that makes old event logs unreplayable is a breaking defect unless an explicit migration/translation strategy is part of the change.

World instances must pin their package/domain versions and may not silently “float” to a newer package release.

---

# 11. Testing architecture

Testing is part of implementation, not a final step.

## 11.1 Unit tests

Target pure invariants, value objects, validation, deterministic resolvers and serialization rules.

## 11.2 Property tests

Use Hypothesis for invariants such as:

- unique identifiers;
- monotonic revision/time constraints;
- illegal transfer cannot create duplicated ownership;
- branch operations preserve parent state;
- replay hash remains stable for generated valid action sequences.

## 11.3 Contract tests

Required for:

- persistence ports;
- event store adapters;
- source/model/simulator adapters later;
- API DTO/OpenAPI compatibility;
- package plugin boundaries.

## 11.4 Integration tests

Exercise real SQLite persistence and migrations; where feasible also provide PostgreSQL-compatible CI/service tests without making PostgreSQL mandatory for the fastest local test loop.

## 11.5 E2E tests

E2E starts when an actual transport/UI exists. E2E must verify authoritative behavior, not only HTTP 200 or pixels.

## 11.6 Replay/golden tests

Canonical deterministic fixtures have stable expected hashes/summary artifacts. A legitimate schema/runtime change updates them only with documented rationale.

## 11.7 Architecture tests

Automated tests fail on forbidden imports/dependencies.

## 11.8 Mutation/negative-path thinking

Acceptance must include rejected commands, permission denial, stale revisions, duplicate command ids, corrupt events/snapshots, migration failure paths and recovery behavior.

---

# 12. Code quality and maintainability standard

## 12.1 Readability

- prefer explicit domain terms from the master specification;
- avoid ambiguous names such as `data`, `thing`, `manager`, `helper`, `utils`, `process_all`;
- functions should reveal intent through names and types;
- public abstractions require concise docstrings describing invariants/ownership, not narrating syntax;
- comments explain why or constraints, not what obvious code does.

## 12.2 File/module size

- default target: <= 300 lines per production file;
- exceeding 300 lines requires splitting unless cohesion would become worse; any justified exception is recorded in `DECISIONS.md`;
- no continuously growing `manager.py`, `service.py`, `utils.py`, `models.py` dumping grounds;
- a module should have one bounded responsibility.

## 12.3 Function/class discipline

- prefer small composable functions;
- avoid god objects coordinating unrelated kernels;
- constructors must not perform hidden I/O;
- explicit dependencies over service locators/global mutable singletons;
- domain types should make illegal states difficult to represent.

## 12.4 Dependency inversion

External databases, queues, clocks, UUID generation, model providers, filesystem/object storage and external simulators are accessed through ports where they affect testability or determinism.

Do not create an interface for every trivial function; create ports at true external/change boundaries.

## 12.5 Error model

Errors must be structured and typed sufficiently for callers/tests to distinguish:

- validation rejection;
- rights/permission denial;
- stale revision/concurrency conflict;
- duplicate/idempotent request;
- not found;
- incompatible schema/version;
- corrupted persistence/replay;
- external dependency unavailable;
- external-data blocked.

Do not use broad `except Exception: pass` or convert all domain failures to HTTP 500.

## 12.6 Upgradeability

- never read/write internal JSON blobs from many unrelated modules;
- centralize serialization/version translation by bounded context;
- add migrations when persisted shape changes;
- keep adapters replaceable;
- do not encode product-specific worlds into core enums/if-statements;
- new Domain/World Packs should extend through registry/plugin contracts rather than edits to core conditionals.

## 12.7 Type discipline

- Python public APIs fully typed;
- Pyright strict enough to catch unsafe optional/union use;
- TypeScript strict;
- avoid `Any` as an escape hatch in core contracts;
- DTO and schema duplication across Python/TS should be generated through OpenAPI/schema tooling when the API exists.

---

# 13. Observability contract

Starting at P1, runtime operations must produce structured trace/audit metadata.

Minimum identifiers when applicable:

```text
trace_id
correlation_id
command_id
instance_id
branch_id
run_id
session_id
actor_id
event_id
event_seq
snapshot_id
rule/resolver id + version
model/provider id + version
```

Logs must not contain secrets or unfiltered private memory/content by default.

Important runtime metrics introduced progressively:

- commit success/failure/conflict rate;
- replay consistency failures;
- snapshot creation/restore time;
- tick/advance latency later;
- actor/model call counts later;
- token/cost/latency later;
- command queue lag later;
- API error rate later.

Observability must diagnose authority and causality, not merely print messages.

---

# 14. Security / rights baseline

From the first external input:

- secrets are never committed or logged;
- untrusted source content cannot become executable instructions to Codex/runtime/model tools;
- source text and system instructions are separated;
- file/URI inputs are validated before processing;
- rights/privacy decisions are made by explicit policy objects, not only UI badges;
- audit logs are protected from ordinary mutation/deletion paths;
- model/tool permissions are least-privilege;
- real/private data is not included in synthetic fixtures.

---

# 15. Definition of Ready for a Goal

Codex must not start a Goal unless:

1. Required reading exists or is explicitly marked not applicable.
2. Dependencies are PASS.
3. Objective is singular and clear.
4. Scope and Non-goals are explicit.
5. Architecture constraints are stated.
6. Deliverables are concrete.
7. Acceptance criteria are machine-verifiable where possible.
8. External blockers are separated from internal implementation work.
9. No unresolved P0 contradiction exists with the master spec.

---

# 16. Definition of Done for every Goal

A Goal is PASS only when all applicable items are complete:

1. implementation finished;
2. no TODO/placeholder/NotImplemented in required runtime paths;
3. new/changed code has appropriate unit/contract/integration tests;
4. negative-path tests exist;
5. lint passes;
6. typecheck passes;
7. migrations apply cleanly when schema changed;
8. old supported fixtures/replay cases remain compatible;
9. build passes;
10. relevant E2E passes;
11. architecture conformance passes;
12. acceptance commands and evidence recorded;
13. documentation and ledgers updated;
14. known limitations are explicit and not disguised as success;
15. local commit created only after Gate PASS;
16. no automatic remote push/deploy unless specifically authorized.

Status values:

- `PASS`
- `EXTERNAL_BLOCKED` — only for genuinely external data/credentials/hardware/approval after the internal port/fallback/test work is complete.
- `FAIL`

`PARTIAL` is allowed during work but not as a Goal completion state.

---

# 17. Blocker taxonomy

## Internal blocker

Examples:
- failing test;
- architecture cycle;
- migration bug;
- design ambiguity resolvable from normative docs;
- environment setup under repository control.

Codex must resolve these and continue. Do not ask the user for routine engineering choices.

## External blocker

Examples:
- private family data not provided;
- rights approval not obtained;
- real museum API unavailable;
- LLM key unavailable for optional provider acceptance;
- physical sensor/hardware absent.

Codex must:
1. implement the interface/port;
2. implement deterministic/fake fixture where valid;
3. test the internal path;
4. write `BLOCKERS.md` entry;
5. mark only the affected real-world acceptance `EXTERNAL_BLOCKED`;
6. continue independent work.

---

# 18. Git and checkpoint protocol

Each executable Goal:

1. starts from a known clean/recorded working tree;
2. records pre-goal commit hash in its report;
3. does not rewrite unrelated history;
4. makes focused commits if needed, with one final Goal checkpoint commit;
5. uses message `goal <id>: <summary>` for the final checkpoint;
6. updates `CHANGELOG.md` and status ledgers;
7. does not push or deploy without explicit instruction.

Milestones may receive local annotated tags such as:

```text
m0-engineering-base
m1-authoritative-world
```

only when all milestone gates pass.

---

# 19. Milestone gates

## M0 — Reproducible Engineering Base

Must prove:
- fresh clone/install commands documented;
- Python/TS toolchain reproducible;
- tests/lint/typecheck build pipelines work;
- architecture import guards fail intentionally on a fixture violation;
- ledgers/ADRs/evidence format exist.

## M1 — Authoritative World Exists

Must prove with deterministic synthetic micro-world:

```text
create instance
→ submit valid command
→ validate
→ resolve
→ commit
→ inspect event log
→ checkpoint
→ destroy derived/current state
→ replay
→ canonical hash identical
→ branch from checkpoint
→ mutate child
→ parent unchanged
→ duplicate command does not duplicate effect
→ stale revision is rejected
```

No LLM key.

## M2 — Deterministic Living World Exists

Must additionally prove spatial/time/material/social continuity and autonomous scheduling.

Later milestones extend this pattern rather than replacing it with screenshots.

---

# 20. Tonight execution boundary

The recommended long-running first batch is deliberately limited to **P0 + P1 / M0 + M1**.

It is large enough to establish a serious codebase, but intentionally does not start Living World Substrate, cognition, Studio UI, Red Chamber, family, museum or campaign implementation.

Reason: every later subsystem depends on the correctness of authoritative state, events, replay, branch, versioning and persistence. Pushing farther before M1 qualification magnifies rework risk.

Tonight batch files:

- `01_CODEX_TONIGHT_MASTER_PROMPT.md`
- `02_ENGINEERING_STANDARDS.md`
- `03_ACCEPTANCE_TESTING_AND_EVIDENCE.md`
- `goals/GOAL_00A_REPOSITORY_FOUNDATION.md`
- `goals/GOAL_00B_ARCHITECTURE_GUARDS.md`
- `goals/GOAL_01A_CORE_CONTRACTS.md`
- `goals/GOAL_01B_COMMIT_AUTHORITY.md`
- `goals/GOAL_01C_EVENT_STORE.md`
- `goals/GOAL_01D_REPLAY_BRANCH.md`
- `goals/GOAL_01E_PERSISTENCE_MIGRATION.md`
- `goals/GOAL_01F_MINIMAL_WORLD_VERTICAL_SLICE.md`

Only after the final M1 acceptance report is PASS should the program move to G02A.

---

# 21. Program architecture change policy

This document is meant to evolve, but changes are controlled.

A change requires an ADR when it modifies:
- dependency direction;
- canonical authority semantics;
- event ordering/branching semantics;
- persisted contract/schema compatibility;
- package trust model;
- formal hierarchy names;
- Goal dependency ordering;
- cross-cutting ownership.

Minor wording, examples and non-normative guidance may change without an ADR.

No Codex task may silently change this program architecture merely to make implementation easier.

---

# 22. Final program rule

The program values a smaller amount of real, replayable, evolvable world infrastructure over a larger amount of shallow feature code.

At every checkpoint ask:

> If UI, LLM and derived tables were removed, could the authoritative world behavior still be reconstructed, explained, migrated and tested?

If the answer is no, the foundation is not complete.
