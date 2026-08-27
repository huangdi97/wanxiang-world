# V5.2 Minimality Budget (G29G)

Code minimality is a continuous acceptance metric. No arbitrary absolute
LOC cap: per-milestone *incremental* allowances on new abstractions (each
with mandatory justification in `V5_2_CODE_MINIMALITY_LEDGER.md`) plus
hard invariants that must hold at every milestone.

## Current snapshot — M93 / v5.5 G96A

| Metric | Count |
|---|---|
| Production files | 567 |
| Production LOC | 64323 |
| Public classes | 1215 |
| Public functions | 521 |
| Registries | 17 |
| Managers | 0 |
| Services | 25 |
| Engines | 5 |
| Ports | 43 |
| Stores | 31 |
| State/schema models | 39 |
| Import cycles | 0 |
| Commit paths | 1 |
| Oversized modules (>300 lines) | 0 |

Hard invariants hold: **True** (0 cycles, 1 commit path).

## Historical incremental budgets M26-M93

| Milestone | New-abstraction allowance | Note | Hard constraints |
|---|---|---|---|
| M26 | 0 | Baseline freeze + convergence; no net new abstractions (dedupe only). | 0 cycles; 1 commit path; no second Event/Branch/Registry/State |
| M27 | 3 | Reality Root / Constitution / ISA are thin semantic layers over existing contracts; allow minimal value types + ISA verbs mapped to the existing pipeline. | no RealityRootEngine/SemanticISAEngine god objects; no second commit pipeline |
| M28 | 4 | Worldline / Lineage Graph / Hypervisor; lineage must reuse branch history semantics. | no second branch system; no WorldLineageManager god object |
| M29 | 3 | Evolution Policy Stack as configuration over one runtime; scheduler + distillations are functions. | no third runtime for canon modes; no per-distiller pipeline |
| M30 | 3 | Promotion pipeline + cross-world distillation reuse Candidate/Invariant machinery. | no World Merge as git-merge; no auto platform promotion |
| M31 | 2 | Compatibility migrations + thin API extensions only. | migrations have rollback/compat; no new API namespace copy |
| M32 | 1 | Red Chamber content (World/Domain/Experience) must NOT add Core abstractions. | no Core special-casing for red_chamber; no model-memory Canon |
| M33 | 1 | Red Chamber instance runtime; reuse Living World substrate. | no second Runtime; no Core hack for RC-001 |
| M34 | 0 | Final acceptance: verification + evidence only; no new abstractions. | working tree clean or explained; no failed-test skips |
| M51 | 5 | Source->LivingWorld Forge baseline: unified Job/JobCheckpoint/JobStore/JobService + typed job errors; reuses single commit path (jobs never mutate canon). | 1 commit path; no second source registry; jobs propose only |
| M52 | 12 | Source Registry & Adapter Foundation: convergence fields, blob refs, SourceAdapter ABI + AdapterRegistry, book/structured/asset adapters, ingestion security gate. All adapters propose only; single SourceRegistry. | 1 commit path; single source registry; no fake extraction |
| M53 | 8 | Parse/Segment/Stable Locator: ParsedDocument IR, StructureParser, segment model + format locators, incremental cache, parse checkpoint, diagnostics API. All propose only; single locator/source-registry. | 1 commit path; single source registry; no fake extraction |
| M54 | 14 | Distillation & Candidate Fabric: unified CandidateEnvelope, distiller DAG + registry, reference passes (identity/event/relation/character/object), candidate clustering. Candidates propose only; no Canon. | 1 commit path; no Canon from candidates; no second envelope |
| M55 | 8 | Evidence/Rights/Review/Completion core: evidence bindings, conflict ledger, rights gate, review ledger, E0-E5 completion + planner, review API routes. All decisions append-only/reversible; no Canon promotion. | 1 commit path; no last-write-wins; no auto canon |
| M56 | 9 | Domain Matching & WorldDraft: domain capability registry + recommender + resolver, WorldDraft v1 + store, coverage, scenario mining, genesis draft. Drafts are compile intermediates, never runtime state. | 1 commit path; no second runtime state; no per-world domain fork |
| M57 | 10 | World compiler/package/preview: revision-pinned compiler boundary, formal package manifest wrapper, deterministic rebuild plan, and an isolated preview scope over the existing runtime port. | 1 commit path; no second runtime state; preview never mutates published registry |
| M58 | 8 | Studio/API/CLI surfaces reuse one AuthoringService, existing JobStore, review ledger, and package/preview boundaries. | one backend for API and CLI; no transport-owned state; no second commit path |
| M59 | 8 | Cross-source reference E2E hardening: bounded chunks, hashes, resume/idempotency and security evidence over the existing Forge path. | single source registry; no source bytes in Git; resume is idempotent |
| M60 | 10 | Semantic world views add typed candidate projections for identity, events, relations, knowledge, topology and object continuity. | semantic views remain Forge data; no E0 promotion; deterministic no-API path |
| M61 | 8 | Source-family alignment and fusion preserve provenance, dissent, rights decisions and incremental recomputation. | no last-write-wins; source identity stays explicit; rights gate is scope-aware |
| M62 | 8 | Multimodal and external-source additions are ports/capability descriptors only; missing providers remain typed failures. | connectors propose only; no network in reference path; OCR_REQUIRED is explicit |
| M63 | 8 | Domain fingerprint/composition and gap packs remain draft-scoped and reuse the single capability registry. | no per-world domain fork; gap packs are proposals; no OS sandbox claim |
| M64 | 8 | Completion and consistency add constraint-backed evidence views without changing the canonical completion boundary. | E1-E5 cannot enter E0 implicitly; unknowns stay explicit; no auto canon |
| M65 | 10 | Scenario/genesis authoring adds bounded Forge engines and immutable candidate snapshots; runtime activation reuses existing ports. | engines are Forge-scoped; snapshot is not runtime state; activation uses existing Commit Authority |
| M66 | 8 | Worldness validation is a bounded simulation/repair proposal loop over WorldDraft and never writes Canonical World State. | repair is candidate-only; bounded simulation; single commit path |
| M67 | 8 | Authoring orchestration composes existing stages, providers and job checkpoints without a transport-owned pipeline. | provider routing is proposal-only; checkpoint is metadata; no second orchestrator |
| M68 | 6 | Review inbox/impact policy reuses the append-only review ledger and keeps defer/unknown outside Canon. | review is not commit authority; decisions append-only; unknown is not E0 |
| M69 | 6 | One-click profiles are a facade over the unified authoring service, package validator, preview registry and existing runtime. | API and CLI share one service; publish updates Forge job metadata only; incomplete packages remain blocked |
| M70 | 0 | Production hardening is evidence, compatibility, documentation and delivery work; no new Kernel authority or runtime state is allowed. | no new authority; no source/private artifact publication; stop after final certification |
| M71 | 5 | Real-book semantic distillation adds a bounded provider port and typed progress without allowing providers to mutate Canon. | private bytes remain outside Git; provider output is candidate-only; zero coverage is typed |
| M72 | 4 | Rights and schema diagnostics make the Source -> Candidate boundary explicit while preserving the existing SourceRegistry. | rights gates remain independent; no source rewriting; no hidden provider fallback |
| M73 | 4 | CLI/API/Studio lifecycle additions reuse AuthoringService and expose the same typed state transitions. | one authoring backend; transport owns no state; no second commit path |
| M74 | 4 | Worldness dimensions carry measurements and evidence, with bounded repair proposals over the draft only. | worldness cannot commit canon; no hardcoded coverage; failure evidence is retained |
| M75 | 5 | Living Instance evaluation proves commit/replay and branch isolation through the existing Commit Authority runtime port. | only Commit Authority mutates canon; replay must match; parent branch remains unchanged |
| M76 | 3 | Browser Studio and random-socket smoke evidence complete the product surface without introducing a separate runtime. | same API use cases; socket allocation is bounded; no browser-only success path |
| M77 | 0 | Real private-source acceptance and regression evidence only. | same source bytes; all required evidence present; NOT_ACCEPTED remains honest |
| M78 | 0 | Final feature-branch delivery and Actions verification only. | no v5.5; no model training; stop after delivery |
| M88 | 25 | PressureProfile, Opportunity lifecycle, Director modes, canon attractor, intervention, Quest projection and deterministic benchmark records reuse the existing reality/runtime branch ports. | one runtime and branch system; Director/Quest/intervention remain proposal or projection only; no pressure-specific Kernel types |
| M89 | 39 | Long-horizon scheduler, detached background execution, cursor-only checkpoint/recovery, reference compaction, SimulationLOD, cost budget, and qualification value objects reuse the existing runtime. | one runtime/event store/branch system; scheduler/LOD/budget/compaction remain proposal or reference-only; no giant manager and no world-specific Kernel types |
| M90 | 2 | Thirty-day actor/relationship/organization qualification compares typed projection snapshots over the existing Commit Authority and replay path; no new runtime state is introduced. | same source and package bytes; append-only canonical history and replay equality; all three projection planes change without projection commits |
| M91 | 15 | Pattern observations, repeated-pattern detection, and the bounded habit/norm/institution/culture-ontology candidate layers consume immutable derived views over committed history without creating a second history. | derived cache only; event refs and rebuild determinism; no automatic Candidate or canonical mutation |
| M92 | 24 | World laboratory evidence contracts add a sanitized RunArtifact, versioned experiment metadata, isolated fork/intervention evidence, bounded batch worldlines, provider assignment and trajectory/validation reports over the existing runtime and Commit Authority. | one runtime/event store/branch system; artifacts contain refs and hashes, never private source bytes; provider output remains proposal-only; unknown validation is not pass |
| M93 | 30 | Physical/visual provider ABI records, deterministic reference adapters, perspective/privacy projections, external capability status, and reconciliation evidence reuse the existing read and proposal boundaries. | one runtime/event store/branch system; provider output remains proposal or projection only; no external engine or GPU dependency is claimed without evidence |

Every new abstraction must answer the four questions in
`reports/V5_2_CODE_MINIMALITY_LEDGER.md`; otherwise it is not added.
