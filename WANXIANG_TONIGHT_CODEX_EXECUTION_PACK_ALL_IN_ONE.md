# WANXIANG TONIGHT CODEX EXECUTION PACK — ALL IN ONE

> Convenience concatenation. The individual files remain normative for repository use.



---

# BEGIN FILE: 00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md

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


# END FILE: 00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md


---

# BEGIN FILE: 02_ENGINEERING_STANDARDS.md

# Wanxiang Engineering Standards

> Applies to all production code written under the Wanxiang Engineering Program Architecture.

---

## 1. Design priorities

In order:

1. correctness of world authority and invariants;
2. readability and explicit semantics;
3. testability and deterministic reproduction;
4. modifiability / upgradeability;
5. observability and diagnosability;
6. performance with measurements;
7. implementation convenience.

Do not trade higher priorities for lower ones without an ADR.

---

## 2. Layering rules

### Domain

Contains semantic identities, value objects, immutable command/event/delta contracts where appropriate, invariant definitions and domain-level error types.

Forbidden dependencies:
- FastAPI;
- SQLAlchemy ORM sessions/models;
- Alembic;
- React/Phaser concepts;
- network clients;
- LLM SDKs;
- global application container.

### Application

Contains use cases, command/query handlers and ports. It coordinates domain/runtime behavior but does not encode HTTP or DB details.

### Runtime

Contains validation, adjudication, commit orchestration, replay orchestration and later observe/schedule/remember hooks. It speaks through ports.

### Persistence

Implements repositories/event store/snapshot store. SQLAlchemy stays here. It must satisfy contract tests shared across adapters.

### Transport

FastAPI routes validate transport shape, authorize, call application use cases, map errors to responses, and return DTOs. No direct ORM mutations. No canonical rules in routers.

---

## 3. Naming

Use Wanxiang vocabulary consistently:

- `WorldInstance`, not generic `Game`;
- `BranchRevision`, not generic `version` when it means branch sequence;
- `ProposedWorldDelta` vs `CommittedEvent`;
- `CanonicalState` vs `Projection`;
- `Claim` vs `Fact`;
- `Observation` vs `Truth`;
- `RightsDecision`, not `is_allowed` scattered booleans when policy context matters.

Avoid:
- `Manager` without a narrow noun;
- `Utils` modules;
- `Common` dumping grounds;
- `DataService` covering unrelated contexts;
- `handle_everything` style functions.

---

## 4. File and module limits

Default production file target <= 300 lines.

If a file grows beyond 300 lines:
1. inspect for mixed responsibilities;
2. split by domain concern, protocol, adapter or use case;
3. if not split, record why in `DECISIONS.md`.

Generated files and schema snapshots are exempt but must be clearly generated.

No module may become a permanent catch-all for new Goals.

---

## 5. Function / class standards

- Keep functions focused and typed.
- Prefer pure functions for invariant checks and deterministic transforms.
- Separate command preparation, validation, resolution and commit.
- Constructors should establish valid objects, not perform hidden network/database I/O.
- Do not hide dependencies behind mutable singletons.
- Avoid inheritance-heavy frameworks for domain semantics; favor composition/protocols.
- A class should have one reason to change.

---

## 6. Domain type design

Represent important identifiers as dedicated types/value objects where practical instead of passing raw strings everywhere.

Examples:
- `WorldInstanceId`
- `BranchId`
- `EntityId`
- `EventId`
- `CommandId`
- `SnapshotId`
- `SchemaVersion`

Represent revisions and event sequence as explicit non-negative integers with validation.

Persisted contracts include schema version.

Avoid untyped nested dictionaries for canonical events/deltas. Flexible component payloads may exist, but identity, versioning, event ordering and relationship metadata remain typed.

---

## 7. Immutability and mutation ownership

Prefer immutable event records and command objects.

Do not expose internal mutable state collections to adapters/UI.

Only the Commit Authority pathway may transform canonical state.

Any convenience method named like `update_state`, `save_entity`, `set_location` must be reviewed for authority bypass. Persistence methods may persist already-authorized committed state; they do not decide legality.

---

## 8. Serialization

Serialization/deserialization is a compatibility boundary.

Rules:
- explicit schema version;
- deterministic/canonical ordering for hashes where relevant;
- no arbitrary Python object pickles for canonical durable storage;
- validation on deserialize;
- unknown/newer incompatible versions produce structured errors;
- migration/translation code is isolated and tested.

---

## 9. Persistence

Use ports to express required behavior.

SQLite is the default fast local implementation; SQL must remain PostgreSQL-compatible where the program specifies compatibility.

Transactions must respect commit atomicity.

Never make canonical correctness depend on ORM identity map side effects.

Derived current-state tables may improve query performance but must be rebuildable from snapshot + events according to the defined persistence strategy.

---

## 10. Event store requirements

A committed event should minimally be able to carry:

- event id;
- instance id;
- branch id;
- event sequence / resulting revision;
- world time when applicable;
- event type;
- schema version;
- payload/delta reference;
- causation id;
- correlation/trace id;
- command id when user/system command caused it;
- actor/controller where relevant;
- rule/resolver/runtime version metadata;
- committed timestamp (wall clock, separate from world time).

Avoid conflating wall-clock time and world time.

---

## 11. Concurrency and idempotency

Every mutation use case must answer:

- What branch revision was read?
- What revision is expected at commit?
- What happens on stale revision?
- Can request be retried safely?
- How is duplicate command detected?
- Is event append + state change atomic?

Do not add concurrency “later” after multiplayer; basic revision semantics are part of P1.

---

## 12. Errors

Create explicit error taxonomy. Suggested families:

```text
WanxiangError
  ContractError
  ValidationRejected
  PermissionDenied
  RightsDenied
  NotFound
  Conflict
    StaleRevision
    DuplicateCommandConflict
  IncompatibleVersion
  ReplayError
  CorruptEventStream
  PersistenceError
  ExternalDependencyError
  ExternalDataBlocked
```

Names may be refined, but callers must not need to parse error strings.

---

## 13. Logging and audit

Use structured logs.

Do not log:
- secrets;
- raw private memories by default;
- full untrusted source documents by default;
- biometric/private family content in generic debug logs.

Audit records for canonical commit are more durable/structured than ordinary debug logs.

---

## 14. Tests near code

When adding a public contract or invariant, add tests in the same Goal.

For every happy path, consider at least one failure path.

For state mutation, normally test:
- valid request;
- invalid request;
- duplicate request;
- stale revision;
- persistence failure behavior where practical;
- replay compatibility.

---

## 15. Property-based testing

Hypothesis is especially valuable for:
- event sequence monotonicity;
- branch isolation;
- state hash stability;
- identifier uniqueness;
- idempotency;
- random valid command sequences;
- serialization round trips.

Property tests are not a substitute for explicit scenario tests.

---

## 16. Architecture conformance

Implement import/dependency checks early. At minimum fail when:

- `packages/domain` imports FastAPI/SQLAlchemy/Alembic or an app module;
- core/runtime imports `apps/api`;
- plugin/domain packages import persistence internals/ORM session;
- projection code accesses persistence models directly;
- model provider accesses canonical persistence directly.

Architecture tests must be part of the normal quality command.

---

## 17. Code generation and API contracts

Once FastAPI/OpenAPI exists:
- API contract is explicit;
- TypeScript SDK/types should be generated or systematically synchronized;
- do not manually maintain parallel copies of large DTO schemas.

Breaking API changes require version/compatibility decision.

---

## 18. Upgrade / migration discipline

Any change to persisted shape must include:
- migration;
- migration test;
- rollback/restore consideration;
- old fixture compatibility;
- update to schema/version docs.

Any change to event semantics must include replay tests against pre-change event fixtures or an explicit migration/translator.

Do not “fix” an old event by rewriting fixture history silently.

---

## 19. External adapters

Every genuine external dependency has:
- port/interface;
- production adapter when in scope;
- deterministic fake/test adapter;
- error mapping;
- timeout/retry policy where relevant;
- explicit provenance/identity in traces.

Do not create fake adapters and then claim real integration acceptance passed.

---

## 20. LLM/model providers

Core CI must not require an LLM API.

Model output is a proposal/input to typed runtime contracts, never an authority mutation.

Prompts are versioned/configured in dedicated provider/prompt modules, not scattered through business logic.

Record provider/model/prompt version and token/cost/latency when model calls are introduced.

---

## 21. Security coding rules

- no secrets in repository;
- no secrets in test snapshots;
- validate untrusted paths/URIs/files;
- parameterized SQL through ORM/query builder;
- do not `eval` untrusted package/source content;
- sanitize/segregate untrusted text supplied to models;
- least-privilege tool access;
- explicit authorization before privileged debug/global-state endpoints.

---

## 22. Documentation standards

Every non-trivial subsystem should explain:
- ownership;
- public contracts;
- invariants;
- lifecycle;
- persistence/versioning;
- failure modes;
- test strategy;
- extension points.

Avoid documentation that merely copies function signatures.

Keep `PLAN`, `STATUS`, `DECISIONS`, `BLOCKERS`, `KNOWN_FAILURES`, `CHANGELOG` current.

---

## 23. Refactoring rule

Refactoring is part of normal Goal completion when new work exposes poor cohesion.

Do not defer obvious structural problems with “TODO refactor later”.

Before creating a new abstraction, search for existing responsibility and avoid duplicate concepts.

After refactoring, replay/contract tests must remain green.

---

## 24. Review checklist

Before marking a Goal complete ask:

- Is there one authoritative mutation path?
- Did any new module bypass intended dependency direction?
- Can old persisted data still be migrated/replayed?
- Are failure modes explicit?
- Are tests asserting semantics rather than implementation details?
- Did any file become a dumping ground?
- Is a world-specific name leaking into Core?
- Can the new capability be replaced/upgraded behind a stable contract?
- Is observability sufficient to explain a failure?
- Is the code understandable without reading a large prompt/history?


# END FILE: 02_ENGINEERING_STANDARDS.md


---

# BEGIN FILE: 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md

# Wanxiang Acceptance, Testing and Evidence Standard

---

## 1. Principle

A Goal is not complete because code exists. It is complete when behavior is reproducibly demonstrated by tests and evidence.

Acceptance evidence must let a future Codex session or human reviewer answer:
- what was required;
- what changed;
- which command proved it;
- what output/result was obtained;
- what remains external;
- which commit contains the accepted state.

---

## 2. Required test classes

Each Goal declares applicability for:

- Unit
- Property
- Contract
- Integration
- Migration
- Replay/Determinism
- Architecture
- Security/Rights
- API/E2E
- Performance/Soak

`N/A` requires a short reason.

---

## 3. Mandatory quality commands

Exact commands may be adapted to repository tooling, but equivalent checks are mandatory.

Python baseline:

```text
ruff check .
ruff format --check .
pyright
pytest -q
```

Frontend when present:

```text
pnpm lint
pnpm typecheck
pnpm test
pnpm build
```

E2E when present:

```text
pnpm e2e
```

Migration checks when DB schema exists:

```text
alembic upgrade head
# fresh database + upgrade
# supported migration-from-previous-fixture test
```

No quality check may be disabled merely to finish a Goal.

---

## 4. M1 canonical acceptance scenarios

### A1 — Valid commit

Given a new synthetic world instance at branch revision 0,
when a deterministic valid command is submitted,
then it is validated/resolved,
a ProposedWorldDelta is produced,
Commit Authority commits exactly once,
branch revision advances,
a committed event is persisted,
and canonical state reflects the effect.

### A2 — Invalid command does not mutate

Given the same world,
when validation rejects a command,
then no event representing a successful state change exists,
revision does not advance for a canonical change,
and state hash is unchanged.

### A3 — Duplicate command idempotency

Submit command ID X twice.
The second attempt must not duplicate world effects or create a second equivalent committed mutation.

### A4 — Stale revision

Prepare command against revision N.
Advance branch to N+1 through another valid commit.
Attempt stale command.
It must return structured conflict/rejection and not overwrite N+1 state.

### A5 — Snapshot and replay

Commit a deterministic sequence of N actions.
Create snapshot at an intermediate revision.
Delete/rebuild derived current state.
Replay snapshot + remaining events.
Final canonical hash and semantically relevant state must equal the original final state.

### A6 — Full replay from initial baseline

For a small stream, rebuild from initial baseline + all events and compare final hash.

### A7 — Branch isolation

Fork child branch at revision K.
Commit events to child.
Parent branch event stream/state hash remains unchanged.
Child reports correct ancestry.

### A8 — Deterministic seed/version

Run the same deterministic scenario twice with same inputs/seed/runtime rule version.
Committed event semantic results and final canonical hash must match, excluding explicitly non-semantic wall-clock/audit fields.

### A9 — Corrupt stream detection

Alter/introduce invalid ordering or incompatible event fixture in a test context.
Replay must fail explicitly rather than silently produce state.

### A10 — Migration compatibility

Create data/events under a prior supported schema fixture.
Apply migrations/translators.
Replay/queries still produce the expected semantic result.

---

## 5. Architecture acceptance

At M0/M1, tests must prove forbidden imports are detected.

At least one test fixture or analyzer rule should demonstrate each critical boundary.

Example forbidden relationships:

```text
domain -> fastapi
domain -> sqlalchemy
runtime -> apps.api
projection -> sqlalchemy ORM internals
plugin/domain pack -> ORM session
model provider -> canonical repository mutation
```

---

## 6. Evidence report format

Every Goal writes `reports/goal_<id>_report.md`:

```markdown
# Goal <id> Acceptance Report

## Status
PASS | EXTERNAL_BLOCKED | FAIL

## Pre-goal state
- branch:
- commit:
- working-tree notes:

## Objective
...

## Delivered
...

## Key architecture decisions
- ADR links

## Test evidence
| Check | Command | Result | Evidence path |
|---|---|---|---|

## Acceptance criteria
| Criterion | Status | Evidence |
|---|---|---|

## Migrations / compatibility
...

## Security / rights impact
...

## Known limitations
...

## External blockers
...

## Final checkpoint
- commit:
- files changed summary:
```

No Goal report may say merely “all tests pass” without naming the relevant commands/suites.

---

## 7. Acceptance matrix

Maintain `reports/ACCEPTANCE_MATRIX.md` throughout the program, not only at G12.

Columns:

```text
Requirement ID
Source section
Owning Goal
Test/evidence
Current status
Last verified commit
Notes
```

This prevents requirements from disappearing between Goals.

---

## 8. Test fixture policy

Synthetic fixtures:
- must be explicitly named synthetic;
- must not use invented real historical/museum/family claims while implying authenticity;
- may use generic people/places/items to test runtime behavior;
- should be small enough to understand manually;
- should be stable/versioned for replay regression.

Golden fixtures are changed only when semantics intentionally change and the report explains why.

---

## 9. No mock-only acceptance

Mocks/fakes are legitimate for unit/contract tests, but a Goal that promises real internal behavior must include at least one integration path using the real implementation of that behavior.

Examples:
- persistence Goal must run against real SQLite adapter, not only mock repository;
- event store Goal must actually append/load/sequence events;
- migration Goal must actually upgrade a database fixture;
- API Goal must call application runtime, not return static JSON.

External integrations may remain fake only when the Goal explicitly scopes the real connector out or is externally blocked.

---

## 10. Failure injection

Where practical, tests should inject:
- persistence transaction failure;
- corrupted serialized payload;
- duplicate command;
- stale branch revision;
- incompatible schema;
- unavailable optional adapter.

System must fail explicitly and preserve canonical integrity.

---

## 11. Performance evidence

Early phases establish baselines rather than hard optimization targets.

Report:
- event append/replay duration for synthetic fixture;
- snapshot size/count;
- test runtime;
- later: tick latency, queue lag, model calls/cost.

A performance change must not weaken correctness/replay guarantees without an ADR.

---

## 12. Milestone M1 final evidence bundle

Before starting G02A, produce:

- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`
- `reports/ACCEPTANCE_MATRIX.md`
- deterministic scenario fixture
- replay golden hash/summary
- branch isolation evidence
- duplicate/stale command evidence
- fresh DB migration evidence
- architecture conformance evidence
- full lint/typecheck/test output paths or captured summaries
- current commit hash

Status must be PASS. External LLM/data absence is irrelevant to M1 and cannot justify skipping M1 tests.


# END FILE: 03_ACCEPTANCE_TESTING_AND_EVIDENCE.md


---

# BEGIN FILE: 04_OLD_G0_G12_TO_NEW_PROGRAM_MIGRATION.md

# Old G0–G12 → Wanxiang Engineering Program Migration Notes

## 1. Purpose

The v5 master specification's G0–G12 roadmap remains valid as a **macro implementation roadmap**. This program does not replace its product intent. It changes the execution granularity and dependency control so Codex does not implement multiple independent kernels shallowly in one oversized Goal.

---

## 2. What remains unchanged

The following are preserved:

- G0→G12 overall progression from deterministic core toward living worlds, domains, co-simulation and release qualification;
- 5 Planes / 16 Kernels;
- Domain Pack → World Pack → Scenario → World Instance → Branch → Session → Projection;
- Canonical World State / single Commit Authority;
- event sourcing / snapshot / replay / branch;
- source/evidence gate;
- rights/provenance;
- deterministic/no-LLM core;
- modular monolith first;
- synthetic domain/world fixtures before real data packs;
- Red Chamber, family, museum and Liaoshen as reference World/Domain packages, not Core.

---

## 3. Why execution is changed

The old roadmap names large capabilities. Several single Goals contain multiple independently complex kernels and standards. If sent directly as a one-shot coding task, Codex can satisfy the surface area by creating many shallow modules and interface stubs without deeply qualifying authority/replay/migration semantics.

The new program therefore distinguishes:

```text
Macro G-number / product roadmap
        ↓
Engineering Phase
        ↓
Executable Goal
        ↓
Work Packages
        ↓
Acceptance Gate
        ↓
Milestone
```

---

## 4. Mapping table

| Legacy | Original intent | New execution treatment |
|---|---|---|
| G0 | repository & engineering foundation | split into G00A repository/toolchain + G00B architecture guards |
| G1 | authoritative world kernel | split into contracts, commit, event store, replay/branch, persistence/migration, vertical qualification |
| G2 | living world substrate | split by spatial, temporal, material, body, institution, population/scheduler |
| G3 | agency/cognition/skill | split by observation, memory/belief, actor/org, action/affordance, resolver, skill, capability |
| G4 | compiler/packages/evidence | foundational evidence/rights contracts move earlier; full registry/source/compiler/review remains P4 |
| G5 | embodiment + Studio + 2D | host authority boundary comes first; embodiment/projection/UI separated |
| G6 | host/lifecycle/multiplayer | separated into lifecycle, multi-client command semantics, recovery/resource control |
| G7 | reality bridge + challenge + capability | separated into Reality Bridge, fusion, opportunity/challenge, director, experiment; capability moved with agency |
| G8 | literature / Red Chamber | treated as system qualification milestone + source-gated reference pack, not Core feature growth |
| G9 | family | split into interop, semantic family world, privacy/living archive/persona modes |
| G10 | heritage | split into IIIF, Linked Art/CIDOC, semantic twin, scenarios/simulation integration |
| G11 | co-sim/campaign/Liaoshen | split into generic simulation contract/orchestrator, synthetic campaign mechanisms, strategy experiments, source-gated Liaoshen |
| G12 | hardening/SDK/advanced projection | hardening moves throughout every milestone; final phase becomes release qualification + optional adapters |

---

## 5. Critical order corrections

### 5.1 Evidence/Rights/Version foundations move earlier

Why: Claim/Evidence/Rights/version metadata are first-class concepts used by canonical data. Waiting until the compiler phase would force schema breakage after the kernel is already persisted.

What moves early:
- foundational Claim/Evidence references;
- RightsEnvelope/decision seam;
- schema/version identifiers;
- provenance hooks.

What remains later:
- full Source Registry;
- review workflow;
- completion compiler;
- domain-specific rights policies;
- rich Studio review UI.

### 5.2 Minimal Host authority boundary before serious UI

Why: Studio/Player must learn from the beginning that API/UI are not the world authority. UI should use stable command/query/projection boundaries rather than runtime internals.

### 5.3 Co-Simulation port concept is frozen before campaign integration

The full co-simulation orchestrator remains later, but the architectural rule is frozen early: a simulator emits events/proposed deltas and never writes canonical state directly.

### 5.4 Hardening is continuous

Migration, observability, rights, security, replay compatibility and architecture conformance begin at their first relevant schema/runtime, rather than appearing for the first time in G12.

---

## 6. Goals intentionally not executed tonight

Do not implement tonight:

- G02 spatial/time/material/body/social substrate;
- G03 cognition and agent memory;
- G04 world compiler;
- G05 Studio/Phaser;
- G06 multiplayer/background host beyond M1 minimum;
- G07 reality/challenge/director;
- G08 Red Chamber;
- G09 family;
- G10 museum;
- G11 campaign/co-simulation;
- G12 advanced adapters.

This is not because they are less important. It is because all of them depend on correct event/commit/replay/version semantics.

---

## 7. What tonight must achieve instead

The batch should leave the repository in a state where the following statement is literally testable:

> A deterministic synthetic world instance can receive a structured command, validate and resolve it, commit an ordered event and canonical delta exactly once, persist the result, create a snapshot, replay to the same semantic state, fork an isolated child branch, reject stale revisions and duplicate effects, and reproduce this behavior without an LLM key.

Once this is true, later “living world” capabilities have a trustworthy substrate.

---

## 8. Resume rule after tonight

Do not tell Codex “continue G0–G12” immediately after M1.

First inspect:
- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`;
- `reports/ACCEPTANCE_MATRIX.md`;
- architecture guard output;
- file/module size report;
- migration/replay evidence;
- Git checkpoint.

Only if M1 is PASS should the next engineering contract be authored/frozen for `G02A Spatial Topology & Access`.


# END FILE: 04_OLD_G0_G12_TO_NEW_PROGRAM_MIGRATION.md


---

# BEGIN FILE: 01_CODEX_TONIGHT_MASTER_PROMPT.md

# Codex Tonight Master Execution Prompt — Wanxiang P0 + P1

> This is the executable controller for the first long engineering batch.  
> Scope: Engineering Constitution + Authoritative World Foundation only.  
> Stop condition: M1 Authoritative World Acceptance PASS, or a genuine unrecoverable external environment blocker that prevents even deterministic local engineering work.

---

## COPY THE BLOCK BELOW INTO CODEX DESKTOP

Read the repository and all required program documents before changing production code.

Normative reading order:

1. `docs/spec/WANXIANG_v5_MASTER_SPEC.md`
2. `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md`
3. `02_ENGINEERING_STANDARDS.md`
4. `03_ACCEPTANCE_TESTING_AND_EVIDENCE.md`
5. `AGENTS.md` if present
6. `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `BLOCKERS.md`, `KNOWN_FAILURES.md`, `CHANGELOG.md`
7. all Goal files listed below
8. current repository tree, git status, git log, existing tests and configuration

Do not infer product requirements from old chat history. The v5 master spec is the product Source of Truth. The Engineering Program Architecture controls implementation order and acceptance.

### Objective for this execution batch

Build and verify the engineering foundation and the authoritative deterministic world kernel up through Milestone M1. The result must be a maintainable foundation on which Living World Substrate can safely be built later.

### Execute these Goals continuously and in order

1. `goals/GOAL_00A_REPOSITORY_FOUNDATION.md`
2. `goals/GOAL_00B_ARCHITECTURE_GUARDS.md`
3. `goals/GOAL_01A_CORE_CONTRACTS.md`
4. `goals/GOAL_01B_COMMIT_AUTHORITY.md`
5. `goals/GOAL_01C_EVENT_STORE.md`
6. `goals/GOAL_01D_REPLAY_BRANCH.md`
7. `goals/GOAL_01E_PERSISTENCE_MIGRATION.md`
8. `goals/GOAL_01F_MINIMAL_WORLD_VERTICAL_SLICE.md`

Do **not** begin G02 living substrate, cognition, Studio, Phaser, real Red Chamber, family, museum, campaign, Reality Bridge or Co-Simulation after finishing this batch. Stop after the M1 acceptance report and checkpoint are complete.

### Non-negotiable runtime invariants

- LLMs, clients, rules, humans, sensors and simulators never directly mutate Canonical World State.
- All required canonical changes flow through validation/resolution as applicable and Commit Authority.
- Canonical history is event-sourced and replayable.
- Snapshot is an optimization/baseline, not a substitute for event history.
- Branch writes never mutate parent branch history.
- Duplicate command retry cannot duplicate world effects.
- Stale branch revision cannot silently overwrite later state.
- Domain/World/Scenario/Instance/Branch/Session/Projection terminology must not be collapsed.
- Specific worlds are never hard-coded into Core.
- Core tests must run without an LLM key.
- No TODO, placeholder, NotImplemented, static JSON response or mock-only path may be used to claim completion.

### Engineering behavior

For routine technical decisions, choose the simplest maintainable option consistent with the documents and record non-trivial decisions in `DECISIONS.md` or an ADR. Do not interrupt for ordinary library/layout choices.

If the repository is empty or incomplete, initialize it according to Goal 00A. If equivalent mature tooling already exists, preserve it when it satisfies the contracts; do not rewrite merely for preference.

Maintain a modular monolith. Do not introduce microservices, distributed queues, Kafka/NATS/Redis or Kubernetes in this batch.

### Code quality

Enforce the engineering standards, including:
- small cohesive modules;
- default production file target <= 300 lines;
- no growing generic manager/service/utils dumping grounds;
- domain layer independent of FastAPI/SQLAlchemy/LLM SDKs;
- explicit ports at persistence/external boundaries;
- typed public APIs;
- explicit error taxonomy;
- no hidden global mutable singleton;
- constructors without hidden I/O;
- no business logic in transport routes;
- no direct ORM mutation from runtime/domain/plugin callers;
- migrations for persisted schema changes;
- schema/version metadata for persisted/external contracts;
- structured logs/audit with secrets/private payload protection.

If existing code violates these constraints and lies on the path required by this batch, refactor it as part of the relevant Goal rather than layering new code on top of poor structure.

### Goal execution protocol

For each Goal:

1. read the entire Goal file and dependencies;
2. inspect existing implementation and tests;
3. update `PLAN.md` / `STATUS.md` to mark the Goal ACTIVE;
4. write/adjust tests early enough to drive invariant behavior;
5. implement the smallest complete architecture that satisfies Scope;
6. run Goal-specific tests frequently;
7. run lint/typecheck/architecture/migration checks as applicable;
8. fix internal failures; do not skip/delete tests to proceed;
9. inspect changed files for poor cohesion, duplication, dead code, generic dumping grounds and architecture leakage;
10. refactor before acceptance when needed;
11. run the Goal acceptance commands;
12. write `reports/goal_<id>_report.md` with concrete evidence;
13. update `STATUS`, `PLAN`, `DECISIONS`, `BLOCKERS`, `KNOWN_FAILURES`, `CHANGELOG`;
14. create a local final checkpoint commit `goal <id>: <summary>` only after PASS;
15. automatically continue to the next Goal.

Do not push to a remote and do not deploy production.

### Blocker handling

Treat failing tests, type errors, architecture violations, migration errors, missing internal modules and resolvable ambiguities as internal engineering problems. Resolve them; do not ask the user.

Only mark `EXTERNAL_BLOCKED` for genuine external dependencies (private data, permissions, credentials, unavailable external systems/hardware) after the internal interface/fake/test path is complete. This P0/P1 batch should require no external data or LLM key, so external blocking should be rare.

### M1 final qualification

After Goal 01F, run a dedicated M1 system acceptance using a clearly synthetic micro-world. It must prove the entire authoritative path, not isolated mocks:

```text
instantiate deterministic synthetic world
→ submit valid command
→ validate
→ resolve
→ produce ProposedWorldDelta
→ atomic Commit Authority
→ ordered event persisted
→ branch revision advanced
→ query canonical state
→ create snapshot
→ commit more events
→ discard/rebuild derived current state
→ restore snapshot + replay remaining events
→ compare final canonical semantic hash
→ fork child branch
→ commit child-only mutation
→ prove parent unchanged
→ retry duplicate command
→ prove no duplicate effect
→ submit stale-revision command
→ prove structured conflict and no mutation
```

Also test at least one rejected invalid command and one corrupt/incompatible replay fixture.

Run the complete quality suite on the final tree.

Create:
- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`
- updated `reports/ACCEPTANCE_MATRIX.md`
- `docs/IMPLEMENTATION_STATUS.md` section for M0/M1

M1 is PASS only if deterministic acceptance succeeds without an LLM key and no required test is skipped.

### Final stop

When M1 PASS is complete:
- update `STATUS.md` to show M0 and M1 PASS;
- ensure working tree is clean except intentionally documented artifacts;
- create final local checkpoint commit if required by the Goal/report sequence;
- summarize implemented capabilities, key ADRs, tests, limitations and the next dependency (`G02A Spatial Topology & Access`);
- STOP. Do not autonomously start the next phase.


# END FILE: 01_CODEX_TONIGHT_MASTER_PROMPT.md


---

# BEGIN FILE: goals/GOAL_00A_REPOSITORY_FOUNDATION.md

# GOAL 00A — Repository & Toolchain Foundation

## Objective

Create a reproducible monorepo engineering base for Wanxiang with Python/TypeScript tooling, CI-ready quality commands, ledgers, documentation structure, deterministic test configuration and local developer startup. This Goal establishes no fake business functionality.

## Scope

- repository/workspace structure;
- Python 3.12 toolchain using `uv` unless an equivalent mature setup already exists;
- TypeScript/pnpm workspace foundation for future web/sdk code, without building product UI;
- pytest, Hypothesis, Ruff, Pyright;
- ESLint/TypeScript strict/Vitest baseline where TS workspace is initialized;
- Docker Compose baseline if compatible with environment, but local tests must not require Docker;
- configuration and `.env.example`;
- structured logging foundation;
- project ledgers and ADR structure;
- common scripts/Makefile/task runner equivalents for quality commands;
- Git hygiene and secret exclusions.

## Non-goals

- no world domain model beyond minimal smoke-test placeholder package importability;
- no FastAPI business endpoints;
- no database schema beyond tooling bootstrap if absolutely necessary;
- no React/Phaser UI;
- no LLM integration;
- no real world packs;
- no microservices/distributed messaging.

## Required reading

- v5 master spec: engineering architecture, recommended tech stack, code quality, immutable principles;
- `00_WANXIANG_ENGINEERING_PROGRAM_ARCHITECTURE.md`;
- `02_ENGINEERING_STANDARDS.md`;
- `03_ACCEPTANCE_TESTING_AND_EVIDENCE.md`;
- current git/repository state.

## Architecture constraints

- modular monolith;
- future `domain` must be framework-independent;
- local deterministic test loop must not require API keys or Docker;
- tooling/config should work from repository root;
- no production source file should be created merely as an empty placeholder to make a directory exist.

## Deliverables

Expected or equivalent structure:

```text
AGENTS.md
README.md
PLAN.md
STATUS.md
DECISIONS.md
BLOCKERS.md
KNOWN_FAILURES.md
CHANGELOG.md
pyproject.toml
pnpm-workspace.yaml
.env.example
apps/
packages/
docs/spec/
docs/architecture/
docs/decisions/
docs/runbook/
tests/
reports/
scripts/
```

Add `docs/runbook/DEVELOPMENT.md` with exact bootstrap and quality commands.

## Implementation tasks

1. Inventory repository and preserve useful existing setup.
2. Establish workspace/package names that align with Program Architecture.
3. Configure Python package discovery without circular editable-install hacks.
4. Configure Ruff and Pyright with meaningful strictness.
5. Configure pytest and Hypothesis profiles suitable for deterministic CI.
6. Configure TS strict baseline and root commands if TS is initialized.
7. Add repository-root quality command(s) that can run all applicable checks.
8. Add `.gitignore`, `.env.example`, and secret-safe configuration loading convention.
9. Add structured logging setup location and tests for configuration redaction if implemented now.
10. Create ledgers with initial program status; do not fill them with speculative tasks beyond current program.
11. Add ADR template.
12. Add acceptance report template.
13. Ensure source/test package naming is unambiguous and importable from clean environment.
14. Add CI workflow if repository policy permits; otherwise add CI-ready scripts and document why workflow is deferred.
15. Verify fresh environment bootstrap from documented commands as far as current environment permits.

## Tests

- test package imports;
- test root configuration loads with no secrets;
- test deterministic test seed/profile behavior where configured;
- run Ruff/Pyright/pytest;
- run TS lint/typecheck/test baseline if TS initialized;
- optional CI config validation.

## Acceptance criteria

PASS only if:
- documented root bootstrap works;
- Python quality checks pass;
- TS baseline checks pass if included;
- no API key needed;
- repository contains required ledgers/docs;
- no business placeholder is being counted as implemented functionality;
- quality commands have stable names used by later Goal files;
- `reports/goal_00A_report.md` contains commands and results.

## Failure / blocker handling

Fix internal setup failures. Do not mark missing optional external services as blockers. If Docker is unavailable locally, deterministic non-Docker tests must still pass and Docker validation may be documented separately.

## Documentation updates

- README getting started;
- development runbook;
- PLAN/STATUS/CHANGELOG;
- DECISIONS for tool substitutions.

## Git / checkpoint requirements

Create final local commit only after acceptance:

`goal 00A: establish reproducible engineering foundation`


# END FILE: goals/GOAL_00A_REPOSITORY_FOUNDATION.md


---

# BEGIN FILE: goals/GOAL_00B_ARCHITECTURE_GUARDS.md

# GOAL 00B — Architecture Guards & Engineering Constitution

## Objective

Convert Wanxiang architectural rules into automated repository constraints so future Goals cannot silently create framework leakage, authority bypass or maintainability decay.

## Scope

- import/dependency conformance tests;
- code-structure quality checks;
- prohibited dependency rules;
- file-size reporting/guard policy;
- generic dumping-ground detection policy/review script where practical;
- test taxonomy folders/markers;
- acceptance matrix bootstrap;
- contribution/AGENTS instructions for Codex.

## Non-goals

- do not implement canonical world behavior;
- do not invent a complex custom static-analysis framework;
- do not enforce arbitrary complexity numbers that create busywork;
- no microservice boundaries.

## Required reading

Program Architecture and Engineering Standards in full.

## Architecture constraints

The guard mechanism itself must be simple, local and maintainable. Prefer existing import-linter rules or small tests/scripts over a bespoke compiler.

## Deliverables

1. automated checks preventing critical forbidden imports;
2. documented dependency diagram;
3. `docs/architecture/MODULE_BOUNDARIES.md`;
4. `reports/ACCEPTANCE_MATRIX.md` initialized with M0/M1 requirements;
5. `AGENTS.md` updated with non-negotiable coding/authority rules;
6. normal quality command includes architecture conformance.

## Implementation tasks

1. Define current physical packages and legal dependency direction.
2. Add tests/rules that fail if `domain` imports FastAPI/SQLAlchemy/Alembic/app modules.
3. Add rules preventing runtime/core from importing transport apps.
4. Add future-facing guards/comments for plugins/model providers not accessing persistence internals directly.
5. Implement a simple production file-size report. Default target <=300 lines; report/explain exceptions rather than blindly failing generated files.
6. Add import-cycle detection through tooling or test.
7. Add repository search/check preventing committed secrets and clearly dangerous placeholder markers in required production paths, while not banning legitimate words in docs/tests.
8. Define test markers/folders: unit, property, contract, integration, architecture, migration, e2e.
9. Add acceptance evidence schema/template validation if practical.
10. Add a deliberate small test fixture proving the architecture guard actually fails on a forbidden dependency, or test the rule implementation directly.

## Tests

- architecture rule positive tests;
- architecture rule deliberate negative fixture;
- import cycle check;
- file-size report execution;
- full quality suite.

## Acceptance criteria

- critical layer violations are machine-detectable;
- quality command fails on a controlled forbidden-import fixture/test case;
- architecture docs match actual package tree;
- no large custom framework was added merely for policy enforcement;
- M0 acceptance matrix entries have evidence;
- M0 can be declared PASS after 00A+00B.

## Failure / blocker handling

Architecture conflicts in existing code are internal issues: refactor or document an explicit ADR only when the master architecture permits it.

## Documentation updates

- AGENTS;
- MODULE_BOUNDARIES;
- DECISIONS;
- acceptance matrix;
- M0 acceptance report.

## Git / checkpoint requirements

`goal 00B: enforce architecture and quality boundaries`


# END FILE: goals/GOAL_00B_ARCHITECTURE_GUARDS.md


---

# BEGIN FILE: goals/GOAL_01A_CORE_CONTRACTS.md

# GOAL 01A — Core Semantic Contracts

## Objective

Define a minimal, durable, framework-independent set of typed semantic contracts required by the authoritative world kernel, including identity, versioning, commands, events, deltas, snapshots, branches, claims/evidence/rights foundations and structured errors.

## Scope

Core contracts only. They must be rich enough for G01B–G01F but must not pre-build later Living World Substrate, cognition, skills or domain packages.

At minimum evaluate/define:
- WorldInstance identity;
- Branch identity/revision/ancestry metadata;
- Entity / Component / Relation minimal identity contracts;
- Command/ActionIntent base envelope sufficient for deterministic micro-world;
- ProposedWorldDelta;
- CommittedEvent envelope;
- CanonicalState representation boundary;
- Snapshot metadata;
- Run metadata if needed for determinism;
- Claim/Evidence references as foundational first-class concepts;
- RightsEnvelope/decision foundation sufficient to avoid redesign later;
- schema/runtime version identifiers;
- structured error taxonomy.

## Non-goals

- no spatial/body/schedule model;
- no Temporal Epistemic Graph;
- no complete Rights product policy;
- no Source Registry compiler;
- no World Package implementation;
- no SQLAlchemy models in domain;
- no HTTP routes required.

## Required reading

- master spec sections on first-class objects, canonical state, world hierarchy, rights/provenance, versioning;
- Program Architecture event/commit/version contracts;
- Engineering Standards.

## Architecture constraints

- framework-independent;
- serialized forms are explicit and versioned;
- avoid one universal `dict[str, Any]` event/delta model;
- support extension without adding real-world-specific core enums;
- distinguish world time from wall-clock commit time;
- distinguish Proposal from CommittedEvent.

## Deliverables

- typed domain modules organized by responsibility;
- error hierarchy;
- serialization contracts/version metadata;
- domain contract tests;
- architecture doc explaining ownership and extension points.

## Implementation tasks

1. Define strong ID/value types where useful without excessive ceremony.
2. Define branch revision/event sequence semantics explicitly.
3. Define command envelope including idempotency/causation/correlation fields as needed.
4. Define `ProposedWorldDelta` in a way that can be validated/applied but does not permit arbitrary hidden mutation.
5. Define immutable committed event envelope.
6. Define canonical state read model boundary and semantic hashing strategy inputs; avoid hashing non-semantic wall-clock/debug fields.
7. Define snapshot metadata and version fields.
8. Define foundational Claim/Evidence reference contracts; a source is not automatically a fact.
9. Define foundational RightsEnvelope/decision hooks while keeping full policy later.
10. Define schema version and incompatible-version errors.
11. Write serialization round-trip tests.
12. Write property tests for valid IDs/revisions and rejected invalid values.
13. Ensure domain has zero forbidden framework imports.
14. Document decisions where multiple representations were plausible.

## Tests

- construction/validation tests;
- serialization round trip;
- invalid revision/version cases;
- semantic hash stability for equivalent deterministic canonical state;
- typecheck and architecture tests.

## Acceptance criteria

- later Commit/EventStore can be implemented without changing fundamental names/ownership;
- no SQLAlchemy/FastAPI imports in domain;
- Proposal and Commit records are distinct;
- branch/event sequence version semantics documented;
- rights/evidence foundations exist early enough to prevent later schema breakage;
- tests pass without external services.

## Failure / blocker handling

Resolve ambiguity using master semantics and record ADR. Do not overbuild generic metamodels to cover every future domain.

## Documentation updates

- `docs/architecture/CORE_CONTRACTS.md`;
- DECISIONS;
- acceptance matrix;
- goal report.

## Git / checkpoint requirements

`goal 01A: define authoritative world core contracts`


# END FILE: goals/GOAL_01A_CORE_CONTRACTS.md


---

# BEGIN FILE: goals/GOAL_01B_COMMIT_AUTHORITY.md

# GOAL 01B — Commit Authority & Core Invariants

## Objective

Implement the only authoritative mutation pathway for the initial kernel: accept validated/resolved proposals, enforce commit preconditions/invariants, apply canonical deltas, produce committed events/audit metadata and expose deterministic results without depending on web/database/LLM frameworks.

## Scope

- Commit Authority service/use case;
- initial invariant framework;
- pure delta application;
- commit result contract;
- validation/resolution seam for deterministic micro-world;
- structured audit/trace metadata;
- in-memory adapters acceptable for unit-level execution, with persistence supplied later.

## Non-goals

- no full Action Validator from G03D;
- no domain-specific physics/social rules;
- no multiplayer queue;
- no SQL persistence requirement in this Goal;
- no LLM.

## Required reading

Master spec Canonical State Kernel, World Reality Bus, standard runtime loop, core invariants.

## Architecture constraints

- mutation cannot occur outside Commit Authority public path;
- commit inputs include expected branch revision where required;
- apply operation deterministic;
- rejected proposal cannot partially mutate state;
- audit/trace data is emitted separately from domain state where appropriate.

## Deliverables

- Commit Authority implementation;
- invariant registry/composition mechanism kept simple;
- deterministic minimal resolver/proposal test support;
- typed commit result/errors;
- tests for success/rejection/atomicity semantics.

## Implementation tasks

1. Implement read-only canonical state input and pure delta application semantics.
2. Add minimum invariants needed for P1: entity existence/reference integrity as applicable, revision monotonicity, duplicate identity prevention, branch identity matching, schema compatibility.
3. Implement expected-revision precondition.
4. Keep resolution separate from commit: Commit Authority does not invent outcomes.
5. Produce committed event candidate/record through an event append port; if event store final implementation is next Goal, define the port now.
6. Guarantee state/event atomicity at the abstraction contract; in-memory implementation must model all-or-nothing behavior.
7. Add structured audit trace fields.
8. Add tests that attempt direct illegal update through exposed APIs and confirm no such public mutation path exists.
9. Add tests for proposal validation rejection preserving state hash.
10. Add deterministic successful commit test.

## Tests

- valid commit;
- invalid proposal/no mutation;
- wrong instance/branch;
- stale revision;
- duplicate entity/reference violation where supported;
- transaction/port failure leaves canonical state unchanged in the tested adapter;
- deterministic result hash.

## Acceptance criteria

- exactly one logical production mutation path exists for canonical P1 state;
- stale revision is a typed conflict;
- failed commit does not advance revision or state;
- committed result has event/audit identity;
- no transport/ORM/model dependency leaks into domain/runtime core;
- full quality suite green.

## Failure / blocker handling

Any need to bypass Commit Authority is an architecture defect, not a shortcut. Refactor instead.

## Documentation updates

- `docs/architecture/COMMIT_AUTHORITY.md`;
- core runtime sequence diagram;
- goal report/acceptance matrix.

## Git / checkpoint requirements

`goal 01B: implement canonical commit authority`


# END FILE: goals/GOAL_01B_COMMIT_AUTHORITY.md


---

# BEGIN FILE: goals/GOAL_01C_EVENT_STORE.md

# GOAL 01C — Event Store, Ordering, Idempotency & Concurrency Semantics

## Objective

Implement the durable event-stream abstraction and a real local adapter with explicit ordering, branch revisions, idempotent command semantics and optimistic concurrency behavior required by later replay/host/multiplayer features.

## Scope

- EventStore port;
- append/load stream operations;
- ordered sequence/revision;
- command-id idempotency tracking as appropriate;
- optimistic concurrency / expected revision;
- in-memory implementation for fast tests;
- SQLite implementation may begin here or be completed in 01E, but at least one real persistence integration path must exist by M1;
- transaction semantics compatible with Commit Authority.

## Non-goals

- Kafka/event broker;
- distributed consensus;
- multi-region replication;
- event streaming UI;
- multiplayer transport.

## Required reading

Program Architecture Event/Commit consistency contract and master event-sourcing principles.

## Architecture constraints

- append-only committed history;
- event sequence strictly ordered per branch;
- duplicate command retry cannot create duplicate effect;
- stale expected revision is rejected;
- no silent event rewrite;
- wall-clock commit timestamp does not determine canonical ordering.

## Deliverables

- EventStore port and adapters;
- contract test suite reusable by adapters;
- idempotency/concurrency tests;
- stream integrity checks;
- documentation.

## Implementation tasks

1. Finalize event stream key: instance + branch.
2. Define revision/event sequence initial/empty semantics.
3. Implement atomic append with expected revision.
4. Implement load from sequence/revision.
5. Implement command idempotency semantics and retrieval of prior result/event references where appropriate.
6. Ensure event IDs unique.
7. Detect out-of-order/corrupt event stream in tests.
8. Build reusable EventStore contract tests.
9. Run contract tests against in-memory adapter.
10. Run against real SQLite adapter now if available; otherwise ensure 01E completes it before M1.
11. Add failure-injection path for append/transaction error.
12. Document future PostgreSQL compatibility assumptions without adding distributed infrastructure.

## Tests

- sequential appends;
- expected revision success/failure;
- concurrent simulated writers against same revision;
- duplicate command ID;
- load ranges/order;
- corrupt sequence detection;
- adapter contract parity;
- transaction failure no partial append.

## Acceptance criteria

- stream ordering independent of wall-clock;
- duplicate command cannot duplicate committed semantic effect;
- stale writer loses with explicit conflict;
- contract tests reusable;
- no event is silently overwritten;
- real persistence path is planned/partially present and M1 dependency explicit.

## Failure / blocker handling

SQLite locking nuances are engineering issues; keep semantics deterministic and document adapter limitations. Do not replace required optimistic concurrency with last-write-wins.

## Documentation updates

- `docs/architecture/EVENT_STORE.md`;
- DECISIONS for revision semantics;
- goal report.

## Git / checkpoint requirements

`goal 01C: implement ordered event store semantics`


# END FILE: goals/GOAL_01C_EVENT_STORE.md


---

# BEGIN FILE: goals/GOAL_01D_REPLAY_BRANCH.md

# GOAL 01D — Snapshot, Replay, Branch & Determinism

## Objective

Make Wanxiang history operational: create/restore snapshots, replay committed event streams to canonical state, fork isolated branches, compare semantic state and verify deterministic reconstruction.

## Scope

- snapshot contract/store port;
- snapshot creation at revision;
- replay engine;
- branch ancestry and fork;
- branch isolation;
- canonical semantic hash;
- replay integrity/version checks;
- basic branch diff sufficient for M1 diagnostics.

## Non-goals

- rich Studio time-travel UI;
- distributed snapshots;
- long-world performance optimization;
- narrative canon comparison;
- full experiment runtime.

## Required reading

Master spec Event/Branch/Temporal Kernel, world Git, replay/determinism requirements.

## Architecture constraints

- snapshot is a checkpoint, not replacement for history;
- replay uses ordered committed events;
- parent history immutable from child;
- semantic hash excludes nondeterministic audit fields;
- incompatible/corrupt history fails explicitly.

## Deliverables

- ReplayEngine;
- snapshot store abstraction + local implementations as appropriate;
- branch repository/model;
- branch creation use case;
- semantic hash utility narrowly scoped to canonical state;
- deterministic golden fixture tests.

## Implementation tasks

1. Define snapshot content vs metadata and schema version.
2. Create snapshot at a known branch revision.
3. Restore state from snapshot.
4. Replay subsequent events through the same trusted delta/event application semantics; do not invent a second mutation model.
5. Support replay from initial baseline for small fixture.
6. Define and calculate canonical semantic hash deterministically.
7. Implement branch fork at valid revision/snapshot.
8. Verify child reads ancestry/baseline then receives independent child commits.
9. Implement minimal state/event diff useful for tests/reports.
10. Add corrupt/missing/incompatible event failure tests.
11. Add property tests with generated deterministic command/event sequences where feasible.
12. Create stable synthetic golden replay fixture.

## Tests

- snapshot round trip;
- replay from snapshot;
- full replay from baseline;
- final hash equality;
- child branch isolation;
- parent unchanged;
- invalid fork revision;
- corrupt event order;
- incompatible schema;
- deterministic same-seed scenario.

## Acceptance criteria

- derived current state can be discarded and rebuilt for fixture;
- replay final semantic hash equals original;
- child mutations do not affect parent;
- corrupt history is not silently accepted;
- golden fixture committed and documented;
- no alternate hidden state-update pathway used during replay.

## Failure / blocker handling

If existing persistence design prevents reconstructability, change persistence design now; do not defer to G12.

## Documentation updates

- `docs/architecture/REPLAY_BRANCHING.md`;
- golden fixture notes;
- goal report.

## Git / checkpoint requirements

`goal 01D: add replay snapshots and isolated branches`


# END FILE: goals/GOAL_01D_REPLAY_BRANCH.md


---

# BEGIN FILE: goals/GOAL_01E_PERSISTENCE_MIGRATION.md

# GOAL 01E — Persistence, Schema Migration & Recovery Foundation

## Objective

Provide a real local durable persistence implementation for M1 with SQLAlchemy 2/Alembic, clean repository ports, transactional commit compatibility, migration tests and a foundation that remains PostgreSQL-compatible without coupling higher layers to ORM models.

## Scope

Persist the P1 concepts only:
- world instance metadata needed for M1;
- branch metadata/revision;
- events;
- snapshots;
- idempotency/command records if design requires;
- minimal canonical projection/current state if chosen, explicitly rebuildable;
- audit metadata needed for M1.

## Non-goals

- full tables for spatial/body/memory/family/heritage;
- pgvector;
- graph database;
- Redis/NATS/Kafka;
- S3/object storage unless required for snapshots and justified;
- production HA.

## Required reading

Master persistence layering, database boundary, Program Architecture version/migration policy.

## Architecture constraints

- ORM confined to persistence package;
- domain/runtime access through ports;
- SQLite local tests;
- schema designed to be PostgreSQL-compatible;
- migration revision mandatory;
- canonical commit transaction all-or-nothing;
- rebuildability documented.

## Deliverables

- SQLAlchemy mappings;
- repositories/event/snapshot store adapters;
- Alembic initial migrations;
- integration tests using fresh SQLite database;
- migration fixture test;
- recovery/rebuild test;
- persistence architecture documentation.

## Implementation tasks

1. Map P1 persistence objects without leaking ORM to domain.
2. Define unique/index constraints for instance/branch/event seq/event id/command id.
3. Implement transactional append/commit semantics.
4. Ensure foreign keys/integrity are enabled in SQLite tests.
5. Create Alembic migrations from explicit model decisions, not auto-generated noise without review.
6. Test fresh database upgrade to head.
7. Create at least one previous-schema fixture or migration simulation sufficient to prove migration harness works; if this is initial revision, create a controlled pre-head fixture rather than claiming migration strategy tested with only empty DB.
8. Test persistence adapter contracts.
9. Test destroy/recreate application process/store object and reload durable world.
10. Test rebuild derived/current projection from snapshot/events.
11. Document backup/restore boundary for later G06C without implementing full production backup tooling.
12. Run SQL against PostgreSQL compatibility assumptions where feasible; record SQLite-specific limitations.

## Tests

- fresh Alembic upgrade;
- constraints/index behavior;
- duplicate event/command rejection;
- transaction rollback;
- persistence across process/store recreation;
- snapshot/event replay from DB;
- migration harness;
- full adapter contract tests.

## Acceptance criteria

- M1 works with actual SQLite persistence, not only in-memory mocks;
- no ORM types escape into domain/runtime public API;
- migrations are reproducible;
- failed transaction does not create state/event mismatch;
- durable replay passes;
- schema/version documented.

## Failure / blocker handling

Do not bypass migrations by deleting the DB in tests that are specifically intended to test upgrade compatibility.

## Documentation updates

- `docs/architecture/PERSISTENCE.md`;
- development DB commands;
- migration policy docs;
- goal report.

## Git / checkpoint requirements

`goal 01E: add durable persistence and migration foundation`


# END FILE: goals/GOAL_01E_PERSISTENCE_MIGRATION.md


---

# BEGIN FILE: goals/GOAL_01F_MINIMAL_WORLD_VERTICAL_SLICE.md

# GOAL 01F — Minimal Authoritative World Vertical Slice & M1 Qualification

## Objective

Integrate P0/P1 components into a small but real deterministic synthetic world execution path and prove Milestone M1 end-to-end. This is the first proof that Wanxiang has an authoritative replayable world kernel rather than only contracts and repositories.

## Scope

Build a tiny generic synthetic micro-world with no real literary/historical content. It only needs enough entities/components/actions to test canonical mutation semantics.

Implement minimal application/API/environment boundaries needed to exercise:
- create/instantiate synthetic World Instance;
- get canonical state/snapshot;
- submit deterministic structured command/action;
- validate minimal preconditions;
- deterministic resolve;
- ProposedWorldDelta;
- Commit Authority;
- event query;
- checkpoint;
- replay;
- branch;
- minimal branch diff;
- deterministic environment API functions needed for M1 tests.

A small FastAPI transport is allowed/expected if the repository stack is ready, but M1 must also be testable directly through application/runtime APIs. HTTP is not the authority.

## Non-goals

- no React UI;
- no Phaser;
- no LLM;
- no Living World spatial substrate beyond a trivial generic component/action used to test mutation;
- no cognition/memory;
- no Source Compiler;
- no Red Chamber/family/museum/campaign names or facts;
- no multiplayer websocket.

## Required reading

All prior Goals, M1 scenarios in Acceptance Standard, master API/world environment concepts.

## Architecture constraints

- API routes thin;
- application use cases own orchestration entry points;
- runtime owns validate/resolve/commit semantics;
- persistence behind ports;
- synthetic domain behavior clearly marked fixture/demo and not encoded as core-world-specific branching logic;
- same authoritative path used by direct application tests and HTTP tests.

## Deliverables

- deterministic synthetic micro-world fixture/package-like test data clearly marked synthetic;
- application use cases;
- minimal API endpoints or equivalent environment facade;
- M1 integration tests;
- final M1 acceptance report and matrix;
- implementation status docs.

## Implementation tasks

1. Define a generic synthetic scenario small enough to understand manually, e.g. two entities and a deterministic transferable token/resource or status update. Do not prematurely implement full item/spatial substrate.
2. Instantiate world with explicit instance/branch/revision/schema/runtime metadata.
3. Implement minimal command validator using typed contracts.
4. Implement deterministic resolver that produces ProposedWorldDelta; keep it fixture/domain-side enough not to hard-code future product domains into Core.
5. Execute through Commit Authority and durable EventStore.
6. Provide query for canonical state/event stream/snapshot metadata.
7. Provide checkpoint and replay use case.
8. Provide branch creation and child command.
9. Add duplicate command handling at the application boundary.
10. Add stale revision handling.
11. Add a minimal `WorldEnvironment` facade consistent with future `create/reset/observe/legal_actions/step/checkpoint/restore/branch/metrics/close`, implementing only the subset honestly supported now and clearly marking unsupported methods by interface scope rather than fake success. Prefer not exposing methods until implemented if the language/API design allows.
12. If FastAPI endpoints are added, generate explicit schemas and map domain errors to structured HTTP errors.
13. Add OpenAPI smoke/contract tests if API exists.
14. Run M1 A1–A10 acceptance scenarios.
15. Run full repository quality suite.
16. Inspect for files >300 lines, import cycles, duplicate schemas, broad `Any`, dead code and route business logic; refactor before final PASS.
17. Generate `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`.
18. Update `reports/ACCEPTANCE_MATRIX.md`, `docs/IMPLEMENTATION_STATUS.md`, PLAN/STATUS/etc.

## Tests

Mandatory M1 tests:
- valid commit;
- invalid command no mutation;
- duplicate command idempotency;
- stale revision conflict;
- durable event ordering;
- snapshot + remaining replay;
- full replay;
- branch isolation;
- deterministic semantic hash;
- corrupt/incompatible replay failure;
- fresh DB migration;
- persistence reload;
- architecture conformance;
- API contract/E2E if API exists.

## Acceptance criteria

M1 PASS requires all of the following:

1. No LLM/API key.
2. World instance can be created with real application/runtime/persistence code.
3. A valid deterministic command changes canonical state exactly once through Commit Authority.
4. An invalid command does not mutate state.
5. Duplicate command cannot duplicate effect.
6. Stale revision is explicitly rejected.
7. Event order is durable.
8. Snapshot + replay reconstructs same semantic hash.
9. Full baseline replay works for fixture.
10. Child branch mutation leaves parent unchanged.
11. Corrupt/incompatible stream fails explicitly.
12. SQLite durable persistence and migrations pass.
13. No required production path contains TODO/placeholder/NotImplemented/mock-only completion.
14. Architecture guards pass.
15. Ruff/format/typecheck/pytest and applicable TS/build checks pass.
16. Final acceptance evidence names commands, tests and commit.
17. Working tree is clean or only contains explicitly documented generated acceptance artifacts before final checkpoint.

## Failure / blocker handling

There should be no real external data blocker. Fix all internal failures. If an optional environment tool (Docker/PostgreSQL) is unavailable, M1 still must pass with the defined local deterministic path; document optional validation separately.

## Documentation updates

- `reports/M1_AUTHORITATIVE_WORLD_ACCEPTANCE.md`;
- `reports/ACCEPTANCE_MATRIX.md`;
- `docs/IMPLEMENTATION_STATUS.md`;
- world runtime foundation guide;
- PLAN/STATUS/DECISIONS/BLOCKERS/KNOWN_FAILURES/CHANGELOG.

## Git / checkpoint requirements

Create Goal checkpoint:

`goal 01F: qualify authoritative world milestone`

After all M1 evidence is complete, optionally create local annotated tag:

`m1-authoritative-world`

Do not push.


# END FILE: goals/GOAL_01F_MINIMAL_WORLD_VERTICAL_SLICE.md
