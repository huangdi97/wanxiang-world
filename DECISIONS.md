# Decisions ? Wanxiang Engineering Program

ADRs live in `docs/decisions/` (`NNNN-slug.md`); this file is the index.

| ADR | Title | Status |
|---|---|---|
| 0001 | Toolchain and workspace layout (M0) | accepted |
| 0002 | Architecture guard mechanism (AST-based, no bespoke framework) | accepted |
| 0003 | Domain contracts: dataclass value objects + manual versioned serialization (no Pydantic in domain) | accepted |
| 0004 | Commit atomicity: append port is the commit point; state is immutable with pure apply | accepted |
| 0005 | ComponentData carries explicit component_id (typed component identity) | accepted |
| 0006 | Event store head is the concurrency authority; event_seq (not wall clock) orders history | accepted |
| 0007 | Fork semantics: child revision = fork_revision + own event count; fork-aware authority/replay | accepted |
| 0008 | Persistence: SQLAlchemy confined to persistence package; JSON-as-text payloads for PG compatibility | accepted |
| 0009 | State-aware deterministic resolvers; synthetic micro-world resolvers live in application (not Core) | accepted |
| 0010 | API composition root (app.py) may wire persistence adapters; routes remain thin (guard exemption) | accepted |
| 0011 | Spatial substrate rides on versioned entity components (no new migration); resolvers through M1 authority | accepted |
| 0012 | Temporal substrate: world clock advanced only by commands; schedules/deadlines/recurrence as versioned components | accepted |
| 0013 | Material substrate: custody != ownership; custody != knowledge; versioned components, no migration | accepted |
| 0014 | Body/condition substrate: bounded facets, capability check blocks spatial movement, facet privacy | accepted |
| 0015 | Institution substrate: role/membership/permission/duty as versioned components; permission decisions carry provenance | accepted |
| 0016 | Population/scheduler substrate: validated StateReader cache + SQL aggregate last_event_seq; deterministic autonomous scheduler | accepted |
| 0017 | M2 milestone: integrated 72h living-world qualification test (combined synthetic world) | accepted |
| 0018 | Observation/perspective: derived read-model with rule_refs audit; sealed payload never in observations | accepted |
| 0019 | Epistemic graph: beliefs/memories as versioned components; corrections link (no silent overwrite); actor-scoped access | accepted |
| 0020 | Agency runtime: propose-only policies; order lifecycle with typed transitions | accepted |
| 0021 | Action/affordance/validator: versioned action registry + side-effect-free validator | accepted |
| 0022 | Resolution/adjudication: adjudicator registry by (action, version); seeded RNG; delta dry-run before commit | accepted |
| 0023 | Skill runtime: versioned skill registry; execution state as versioned skill.instance component | accepted |
| 0024 | Capability & learning: bounded capability (level 0..10, mastery/confidence 0..1), evidence-backed CapabilityDelta, deterministic clamped LearningPolicy | accepted |
| 0025 | Package registry: portable manifests, deterministic resolution, content hashes, default-deny executable trust, manifest schema migration | accepted |
| 0026 | Source gate: immutable sources + review stages E0..E5, rights+stage eligibility, injection default-deny, conflicting claims retained | accepted |
| 0027 | Structured compiler: safe readers, deterministic pipeline with stable hash, provenance-bound candidates, PDF/OCR/video explicitly unsupported | accepted |
| 0028 | Completion ledger: truth-label promotion graph, immutable review decisions, canon lock + override, rights gate, version diff | accepted |
| 0029 | Package install: transactional install with exact pins, portable export, explicit upgrade (fork on incompatible), v2 never mutates v1 instances | accepted |
| 0030 | World host: orchestration boundary, not a second Commit Authority; lifecycle modes gate commands | accepted |
| 0031 | Session/lease: one primary embodiment controller per actor; sessions never duplicate actor state | accepted |
| 0032 | Shadow/handoff: advice-only shadow; deterministic controller resumes on release | accepted |
| 0033 | Projection: server-composed DTOs with rights/knowledge filters and debug privilege | accepted |
| 0034 | Studio/Phaser slices: typed view models over server projections; renderers EXTERNAL_BLOCKED | accepted |
| 0035 | Persistent lifecycle: canonical host.lifecycle entity, deterministic transitions, virtual clock drivers | accepted |
| 0036 | Command queue: bounded dedup intake, serialized drain, structured statuses, backpressure | accepted |
| 0037 | Recovery: committed-events crash boundary, snapshot/event-replay fallback, resource budgets | accepted |
| 0038 | Reality bridge: normalized observations on a bus, never canonical truth | accepted |
| 0039 | Observation fusion: dedup + conflict sets, claims/proposals only, versioned policy | accepted |
| 0040 | Challenge compiler: executable specs with prerequisites/safety/rights/evidence/outcomes | accepted |
| 0041 | Director runtime: proposals only; persona changes need actor-logic review | accepted |
| 0042 | Experiment runtime: deterministic multi-seed runs, findings + validity envelope | accepted |
| 0043 | Mansion qualification: unrelated domain on the same core, no Core hacks | accepted |
| 0044 | Red Chamber slice: real data EXTERNAL_BLOCKED; Source Gate fixtures PASS | accepted |
| 0045 | Genealogy: GEDCOM subset, claims-not-truth, privacy/persona modes | accepted |
| 0046 | Heritage: IIIF/Linked Art adapters, distinct twin identities, replayable biography | accepted |
| 0047 | Co-sim: SimulationAdapter contract; adapters never own commit authority | accepted |
| 0048 | Campaign: synthetic factions/units/regions/orders with fog-of-war | accepted |
| 0049 | Liaoshen pack: real data EXTERNAL_BLOCKED; generic M8 not blocked | accepted |
| 0050 | Release qualification: stability/backup/SDK/adapters/security with labeled external checks | accepted |

## Decision log (inline quick notes)

- 2026-08-11: Repository begins as a fresh `git init` on `main`; the batch control
  documents shipped in the workspace are committed as the initial baseline, then
  Goal checkpoints follow the `goal <id>: ...` convention.
| 0051 | G13E: ReplayEngine checks event_seq and revision independently; child branches pass start_seq=1 (branch-local seq restarts, revision continues from fork); snapshot continuation uses baseline.revision+1 | accepted |
| 0052 | G14D: restore_and_replay validates snapshot baselines against event history (semantic hash + versions); invalid/unreadable snapshots fall back to authoritative replay with snapshot_rejected observable | accepted |
| 0053 | G14H: CoSimOrchestrator checkpoint includes the orchestrator clock so restore+continue realigns barriers; mismatched checkpoints are explicit errors | accepted |
| 0054 | G17F: package resolver honors explicit root_version pins (seed before traversal); yank blocks new installs but preserves metadata | accepted |
| 0055 | G19J: distributed hosting REJECTED for promotion - final v5.0-R1 version freeze and release-readiness bundle approved as LOCAL checkpoint (tag m17-final-certification); release version tag (proposed v5.0-R1-rc1) and any push/deploy require explicit user authorization | accepted | - benchmark shows 2.2x coordination overhead with zero correctness gain; modular monolith remains stable default; partition/lease/channel seam stays behind `distributed_host` flag (OFF) | accepted |
| 0056 | G21A: v5.1 program pack (master spec + goal/milestone contracts) committed as part of the baseline checkpoint for single-commit reproducibility; no production code change in the freeze Goal | accepted |
| 0057 | G21B: v5.1 deltas classified per matrix; stub packages evidence/model_providers flagged as DELETE candidates pending call-site evidence (G21C/G21E); triple ledgers must remain distinct from CompletionLedger | accepted |
| 0058 | G21C: exactly one commit path confirmed; duplicate recovery SnapshotStore flagged MERGE (runtime port is production owner); CompletionLedger stays separate from triple-ledger streams; domain registries (action/adjudicator/resolver/skill) stay domain-local, Runtime Capability Catalog (G25G) covers runtime providers only | accepted |
| 0059 | G21D: dependency topology pinned acyclic; substrate->application inversion documented as P2 with planned WorldRuntimePort fix (no production change in this Goal) | accepted |
| 0060 | G29A: v5.2 baseline freeze approach ? verify-then-freeze (quality gate re-run, pre-existing failures fixed: BOM ruff panic D1, v51_metrics pyright D2, corrupted guard scripts D3/D4); golden fixtures frozen under tests/fixtures/v5_2_baseline/ with deterministic normalization (fixed commit ids/timestamps); empty stub packages evidence/model_providers deleted (zero call sites); 140 md BOMs left untouched (cosmetic); v5.1 stash@{0} NOT restored (tree is intended start state) | accepted |
| 0061 | G29B: actual disposition verified with call sites ? registries all domain-local/single-problem (KEEP); CanonicalState contract vs InMemoryCanonicalState impl = ADAPT not duplicate; recovery snapshot store = the only MERGE candidate (G29C); zero world-specific Core leakage; no REPLACE without ADR | accepted |
| 0062 | G29C: recovery checkpoint snapshot store merged into the single runtime SnapshotStore port ? CheckpointStore adapter keeps recovery indexes (latest-per-instance, snapshot-id) on top of the one snapshot state store; InMemorySnapshotStore kept as deprecated alias; recovery SnapshotStore Protocol removed (no consumers) | accepted |
| 0063 | G29D: derivation model verified and pinned by tests ? committed events are the only authority; snapshots are cache; audit_traces is a reference view (no delta column); StateReader cache is discardable; apps/api forbidden from ORM writes | accepted |
| 0064 | G29E dependency-direction ADR: domain -> runtime -> application/persistence -> substrate -> apps/api; Kernel (domain+runtime) never depends on Runtime/Forge/Web/ORM; World content never enters Kernel; substrate->application inversion resolved via consumer-owned WorldRuntimePort (current_state/submit_command/events) | accepted |
| 0065 | G29F: no production fake/placeholder exists; deterministic reference simulators (FakeSimulator/FakeSensorAdapter) are KEEP (real behavior, co-sim/reality M8); static-success paths pinned (environment.close, digital_human.interrupt); distributed_host research flag marked REJECTED (ADR 0055) and isolated OFF | accepted |
| 0066 | G29G: minimality is a continuous metric ? v52_minimality_budget.py (reuses v5.1 scanners) pins counts + hard invariants (0 cycles, 1 commit path); M27-M34 incremental budgets are allowances with justification, not absolute LOC caps | accepted |
| 0067 | G29H/M26: full gate regression found+fixed 2 FAILs (WorldRuntimePort param name for pyright protocol match; SnapshotStore deprecated alias restored + SDK baseline regenerated); M26=PASS ? v5.2 semantic work (M27) can start | accepted |
| 0068 | G30A: Reality Root is vocabulary + documentation over existing contracts (REALITY_ROOT_SEMANTICS + RealityRootContract Protocol), no new engine/store; five primitives tested; no domain rules in the module | accepted |
| 0069 | G30B: ConstitutionManifest = immutable roots vs mutable law layers; ROOT_CONSTITUTION immutable with no self-amendment; legacy v5 pack compat manifest; world_definition_ref records constitution binding (direct World Definition field in G31A) | accepted |
| 0070 | G30C: constitution enforcement lives in the kernel INVARIANTS tuple (additive, always-run, cannot be overridden); platform identities protected (sys_ prefix + explicit ids); ConstitutionViolation typed error; no new engine | accepted |
| 0071 | G30D: World Semantic ISA = 8 typed instructions (WorldIsaOp) reducing data ops to existing deltas; control ops map to existing use cases; no parallel bus; ISA_VERSION 1 with explicit unknown-version failure | accepted |
| 0072 | G30E: execute_isa is a thin adapter over CommitAuthority/fork_branch/validation (no parallel bus, no second stream); PROMOTE emits PromotionUseCase only, never commits parent | accepted |
| 0073 | G30F: one CommitAuthority supports state/ontology/law kinds (CommitRequest.kind + delta_schema_version, audit-recorded); capability changes are RuntimeControlTransactions in the Runtime Control Ledger, never World Commits; invalid kind rejected atomically | accepted |
| 0074 | G30G: FactScopePolicy partitions write authority (canonical=commit authority only, actor=actor-owned); scope-only elevation to canonical rejected; canonical promotion requires Commit; projection filters ledger.fact by scope/rights | accepted |
| 0075 | G30H: VersionContext (constitution/semantic/law/domain/runtime) is history metadata resolved via an immutable revision log with legacy fallback; snapshots freeze the context; never part of semantic hash (replay deterministic) | accepted |
| 0076 | G30I/M27: full gate PASS (714+1); mutation-path search confirms single CommitAuthority path; resolution dry-run is pure; M27=PASS ? v5.2 lineage work (M28) can start | accepted |
| 0077 | G31A: WorldDefinition read-only versioned; Branch fork == Worldline fork (reuses BranchAncestry, no second history object); InstanceIdentity records definition/genesis/constitution/runtime refs | accepted |
| 0078 | G31B: LineageGraph is a thin DAG store (node/edge + ancestor/descendant queries, cycle rejection); stores derivation refs only, never history | accepted |
| 0079 | G31C: lineage persisted via minimal lineage_nodes/edges (migration 0003, downgrade-safe); branch lineage derived from existing branches table (no second system); Event history never copied | accepted |
| 0080 | G31D: WorldHypervisor composes WorldHost/HostRegistry (no second host); explicit instance/worldline routing + per-instance budget/profile; wrong-route commands rejected | accepted |
| 0081 | G31E: interworld presence = OriginIdentity + PresenceRef with explicit translation/sync policies; no implicit write-back; identity conflicts rejected unless mapped | accepted |
| 0082 | G31F: hybrid genesis = semantic compatibility analysis (constitution/identity/ontology/law/rights/history) producing candidate or rejection; never fakes Git merge; never rewrites parent histories | accepted |
| 0083 | G31G: lineage exposed via GET-only API (ancestors/descendants/promotion-origin), OpenAPI-regenerated SDK contract (13 routes), Studio read-only projection; UI never holds authority | accepted |
| 0084 | G31H/M28: full gate PASS (747+1); lineage model moved to domain to keep persistence->substrate direction clean; migration head 0003 constants updated; M28=PASS ? M29 evolution work can start | accepted |
| 0085 | G32A: EvolutionPolicyStack = versioned World/Platform policies; world policy can never mutate platform (structural guard + explicit rejection) | accepted |
| 0086 | G32B: multi-scale evolution scheduler = modular cadence activation (linear growth, no full scans); deterministic per seed/cadence; thin layer over population runtime | accepted |
| 0087 | G32C: capability and persona evolve through separate channels; skill gain never rewrites persona (explicit PersonaDelta only); trajectory provenance recorded per change | accepted |
| 0088 | G32D: social pattern distillation is windowed + threshold-gated; candidates never write Canon; provenance = window refs + origin | accepted |
| 0089 | G32E: institution promotion = controlled chain (evidence -> validate -> approve -> LawCommit); unapproved candidates never change Gamma; LawCommits replayable | accepted |
| 0090 | G32F: ontology/law candidates validated against constitution mutable layers + policy (no escalation); branch-local evolution never pollutes parent | accepted |
| 0091 | G32G: telemetry is opt-in; trajectories require explicit rights + retention; unauthorized data never enters the cross-world dataset; revocation supported | accepted |
| 0092 | G32H/M29: full gate PASS (774+1); synthetic society habit->norm->institution chain is controlled (validate/approve -> LawCommit); platform power isolated; M29=PASS ? M30 promotion work can start | accepted |
| 0093 | G33A: abstraction ladder L0-L8 with per-level evidence/stability/cross-scenario/approval; one step at a time; L7/L8 explicit approval; policy versioned | accepted |
| 0094 | M35-M42 program start (2026-08-15): G38A independent audit verified M34 NOT complete (v5.2 M30-M34 pending: G33B-G37G + gates); remediation = complete v5.2 M30-M34 before M35 Kernel v1 freeze; kernel freeze policy per 01_KERNEL_FREEZE_POLICY.md | accepted |
| 0095 | G33B: WorldlinePromotionPipeline = distill -> review -> assemble new WorldDefinition id -> lineage edge; parent definition/source worldline never mutated; derived world re-instantiable | accepted |
| 0096 | G33C: PromotionControlLedger append-only + replayable; withdraw only changes installability/registry status; source history never deleted (parent replay unchanged) | accepted |
| 0097 | G33D: CrossWorldDistiller reads only authorized telemetry (opt-in/rights), excludes trajectories, preserves anonymized world origins; candidates never activate without explicit approval | accepted |
| 0098 | G33E: PlatformFeedbackLab = shadow/sandbox gate (benchmark/invariant/security/cost/determinism) -> platform-only approval -> versioned release; rollback is status-only (events never rewritten) | accepted |
| 0099 | G33F: promotion/lineage API + Studio views are thin and admin-gated (403 without permission); UI actions route through backend authority; OpenAPI regenerated (16 routes) | accepted |
| 0100 | G33G/M30: full gate PASS (798+1); worlds beget worlds + experience -> platform candidates with no direct write; M30=PASS ? M31 compatibility convergence can start | accepted |
| 0101 | G34A: final Kernel/Runtime/Forge/Experiences responsibility boundaries documented + conformance test (Kernel import isolation, no new God Engine) | accepted |
| 0102 | G34B: WorldPack schema v5.2 migration — optional constitution/genesis/evolution/lineage refs; canonical includes refs only when set (legacy hashes preserved); migrate_to_v52 + wxpack migrate | accepted |
| 0103 | G34C: migration 0004 persists world definition/constitution/evolution metadata + lineage kind index; downgrade-safe; backup/restore path verified (event count/hash unchanged) | accepted |
| 0104 | G34D: old Event/Snapshot/Branch backward replay proven against M26 golden samples (hashes match, no data-clearing); new v5.2 fields default via legacy adapter | accepted |
| 0105 | G34E: constitution endpoint + TS SDK client added; lineage/promotion endpoints kept; old world/branch endpoints preserved (no breaking removal); OpenAPI regenerated (17 routes) | accepted |
| 0106 | G34F: performance regression verified — commit SQLite-bound (~29 ev/s), replay 1200 ev ~35ms, lineage 400-node ~23ms; no unexplained degradation; benchmark extended with lineage | accepted |
| 0107 | G34G/M31: full gate PASS (819+1); migration head 0004; backward-compat report generated; M31=PASS — M32 Red Chamber Source Gate can start (real source EXTERNAL_BLOCKED until a legal edition is available) | accepted |
| 0108 | G35A: real《红楼梦》full-text source EXTERNAL_BLOCKED (no legal/traceable edition in env; read-only + no network/rights verification); no model-memory canon; registration mechanism verified with synthetic fixture | accepted |
| 0109 | G35B: chapter/segment source locators — read-only segmentation with stable offsets/chapter ids; claims back-link to exact source slices; mechanism verified on synthetic corpus (real text EXTERNAL_BLOCKED) | accepted |
| 0110 | G35C: identity/alias distillation = pure IdentityDistiller (caller-supplied mention/alias rules) + evidence-backed AliasClaim (G35B locators) + human/rule IdentityReviewGate; candidates never Canon until approved; converts to G04B ClaimCandidate so no second claim abstraction; same-name different-identity never merged | accepted |
| 0111 | G35D: place/object/organization + topology distillation = EntityDistiller (pure, caller-supplied rules) + EntityConnection (source-bound edges) + EntityReviewGate; completion_notes are strings never evidence (space completion never impersonates source); shared evidence_ok extracted (identity gate ADAPTED, no behavior change); unresolved connection targets -> Completion | accepted |
| 0112 | G35E: canon compilation = ScenarioPoint + CanonCompiler (pure; segment-before/at/after classification) -> CompiledCanon with Past/Character/Future buckets; runtime_view = Past+Character only; FutureCanon visible only via control_plane_view (world never sees future); per-character canon via character_canon(key) | accepted |
