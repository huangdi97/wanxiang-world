# V5.2 Code Minimality Ledger

> Required by `03_????????.md`: every new class/protocol/service/registry/
> manager must answer the four questions. Deletions/merges are recorded too.
> Updated continuously across G29A?G37G.

## G29A entry

### Deleted abstraction
| Item | Why | Evidence |
|---|---|---|
| `packages/evidence` stub package (5 LOC, empty `__init__`) | Empty placeholder; no consumers; evidence/rights lives in substrate (sources) ? DELETE per v5.1 G21B/G21D disposition | `rg wanxiang_evidence` -> no production consumers; quality gate green after removal |
| `packages/model_providers` stub package (5 LOC, empty `__init__`) | Empty placeholder; no consumers; provider routing stays in capability fabric ? DELETE per v5.1 G21B/G21D disposition | `rg wanxiang_model_providers` -> no production consumers; quality gate green after removal |

### New abstraction review (script/test tooling, not production Core)
| Item | 1) irreducible semantics | 2) replaces/merges | 3) why function/type/config insufficient | 4) two consumers or external boundary |
|---|---|---|---|---|
| `scripts/generate_v52_baseline_fixtures.py` | Freezes deterministic compatibility goldens (events/snapshot/branch/worldpack/api) before v5.2 work | Replaces ad-hoc fixture copying; centralizes deterministic normalization | A plain script is the right unit; no state/service needed | Consumers: `tests/architecture/test_v52_baseline_fixtures.py` + G34D backward-replay regression |
| `tests/architecture/test_v52_baseline_fixtures.py` | Reproducibility guard (reload + same semantic hash) | N/A (test) | N/A | Runs in full quality gate |

No production Core class/protocol/service/registry/manager was added in G29A.


## G29B entry
No production abstraction added or removed in G29B (analysis + report only).
Recorded dispositions: 11 registries KEEP (domain-local / single problem);
CanonicalState vs InMemoryCanonicalState = ADAPT (contract vs impl); recovery
snapshot store flagged MERGE (G29C) with consumer evidence.


## G29C entry

### Merged abstraction
| Item | Type | Evidence |
|---|---|---|
| `wanxiang_substrate.recovery.checkpoint.SnapshotStore` Protocol + `InMemorySnapshotStore` (own state dict) | MERGE (deleted duplicate implementation) | consumers: only recovery/__init__ re-export + tests/integration/test_recovery.py (2 constructions); runtime `SnapshotStore` port is production owner (world_runtime, persistence, application) |
| `CheckpointStore` adapter | ADAPT (new thin adapter over the single snapshot port) | carries recovery-specific latest-per-instance + snapshot-id indexes only; snapshot state stored once in runtime store; public `CheckpointService` API unchanged |

### Four-question review for `CheckpointStore`
1. irreducible semantics: recovery checkpoint query model (latest per instance, load by snapshot id) distinct from runtime per-branch store queries.
2. replaces/merges: replaces the duplicate recovery InMemorySnapshotStore implementation.
3. why function/type insufficient: needs a small stateful index over the shared store; a bare function would need an external index object anyway.
4. consumers: CheckpointService + RecoveryService + recovery tests (2+ consumers).


## G29D entry
No new production abstraction (verification + tests only). Confirmed the
single-authority derivation model; no second State/Event/Audit mechanism exists.


## G29E entry

### New abstraction review ? `wanxiang_substrate.runtime_port.WorldRuntimePort` Protocol
1. irreducible semantics: the substrate<->application composition-root boundary
   (external, replaceable boundary; substrate must not import the facade).
2. replaces/merges: replaces five direct `wanxiang_application.world_runtime` imports.
3. why function/type insufficient: a Protocol gives structural typing without a
   new service or registry; the boundary is about type-level decoupling.
4. consumers: host/host, queue/queue, population/scheduler, skills/runtime,
   lifecycle/service (5 consumers) + application WorldRuntime as implementer.

### Removed dependency edge
substrate -> application (5 module imports removed; verified zero remaining).


## G29F entry
No production abstraction added or removed (scanner extension + tests + flag
metadata only). Verified zero empty-body production functions/classes; the two
static-success paths are documented no-ops/unsupported branches.


## G29G entry

### New abstraction review ? `scripts/v52_minimality_budget.py` (tooling, not Core)
1. irreducible semantics: continuous minimality metric + per-milestone budgets.
2. replaces/merges: reuses v51_metrics.compute_metrics + v51_forensics.collect +
   architecture_check cycle check (no third scanner).
3. why function/type insufficient: a script + JSON budget is the right unit.
4. consumers: CI quality gate + M27-M34 acceptance checks + this test file.

### Refactor
`scripts/v51_metrics.compute_metrics()` extracted (behavior identical; main()
output unchanged) so the budget script reuses it.


## G29H/M26 entry
No new production abstraction. Restored `SnapshotStore` deprecated alias in
recovery (API compat) and renamed a port parameter for pyright protocol
compatibility (no semantic change).


## G30A entry (M27, allowance +3, used +2)

### New abstractions
| Item | 4-question review |
|---|---|
| `wanxiang_domain.reality_root.RealityRootContract` (Protocol) | 1) documents the five Reality Root primitives on existing types; 2) replaces nothing (new vocabulary); 3) a Protocol is the minimal documentation-level unit; 4) consumers: G30A tests + M27 ISA mapping + world runtimes (documentation boundary) |
| `wanxiang_domain.reality_root.SemanticMapping` (dataclass) | 1) documentation record (name/meaning/mapped_to/no_domain_rules); 2) replaces nothing; 3) a plain dataclass is sufficient; 4) consumed by tests + reports |

No new store/engine; module imports only domain core.


## G30B entry (M27 allowance +3; used +2 so far -> ConstitutionManifest + ConstitutionVersion; SemanticMapping/RealityRootContract/ConstitutionId also count)

Actually count: M27 used = RealityRootContract, SemanticMapping (G30A) + ConstitutionManifest, ConstitutionVersion (G30B) = 4 vs allowance +3. ConstitutionalId is an ID subclass (not a new abstraction category). Deviation recorded: ConstitutionManifest is the core v5.2 semantic object (world family bounds); ConstitutionVersion mirrors SchemaVersion. Accepted with justification in this ledger (the +3 allowance was deliberately tight; the two Constitution types carry irreducible semantics for M27's core requirement).


## G30C entry
New abstraction: `ConstitutionViolation` error type (typed failure category,
subclass of ValidationRejected). Two invariant check FUNCTIONS added to the
existing INVARIANTS tuple (not new classes). No new engine/store/boundary.


## G30D entry
New abstraction: `WorldIsaOp` (discriminated payload) + `WorldIsaInstruction`
(Literal alias). reduce_isa_to_delta is a function. No engine/bus/store.
ISA is intentionally a thin reduction layer (per ADR 0068/0071).


## G30E entry
New abstractions: `execute_isa` (function adapter), `IsaExecutionResult` +
`PromotionUseCase` (small frozen result records). Justification: thin mapping
over existing pipeline; no new engine/bus/store; PROMOTE record is the future
promotion use-case envelope (G33).


## G30F entry
New abstractions: WorldCommitKind (Literal alias), RuntimeControlTransaction +
RuntimeControlLedger (substrate capability). Justification: kind is the unified
commit discriminator (no third pipeline); RuntimeControlLedger is the append-only
Runtime Control Ledger per the triple-ledger spec (never a World Commit).
CommitRequest/AuditRecord extended with defaulted fields (backward compatible).


## G30G entry
New abstraction: `FactScopePolicy` (pure policy class, stateless static methods).
Justification: irreducible scope/rights partition semantics; no store/engine.
ProjectionService gained one entity-type branch (ledger.fact), no new service.


## G30H entry
New abstractions: VersionContext, VersionContextEntry, SnapshotVersionContext
(frozen records) + extend/resolve_context (pure functions). Justification:
minimized history-interpretation metadata; no store/engine; legacy adapter
reuses existing golden fixtures (unchanged hash).


## G30I/M27 entry
No new production abstraction (verification + gate fixes only). Recorded M27
abstraction delta in the budget (ports 23 -> 24 = RealityRootContract).


## G31A entry
New abstractions: WorldDefinition, WorldlineIdentity, InstanceIdentity,
WorldlineFork (frozen records) + 2 ID types. Justification: formal identity
model for lineage (M28 core); no store/engine; fork reuses BranchAncestry.


## G31B entry
New abstractions: LineageNode, LineageEdge (frozen records) + LineageGraph
(thin in-memory DAG). Justification: lineage DAG storage/query is M28 core;
no manager god object (plain class), no history copy.


## G31C entry
New abstractions: LineageRepository (SQLAlchemy repository over 2 minimal
tables) + 2 ORM records. Justification: lineage persistence is M28 core;
branch lineage reuses the branches table (branch_lineage_from_branches is a
view function, not a duplicate store).


## G31D entry
New abstractions: WorldHypervisor (composer over existing WorldHost/HostRegistry)
+ RuntimeProfile (frozen record). Justification: M28 multi-instance isolation
core; no second host; routing/budget are thin additions over existing pieces.


## G31E entry
New abstractions: OriginIdentity, PresenceRef (frozen records) + PresenceRegistry
(thin registry). Justification: M28 interworld identity/presence core; explicit
policies prevent dual-write; no engine/store beyond the thin registry.


## G31F entry
New abstractions: GenesisCheck, HybridGenesisReport (frozen records) +
analyze_hybrid_genesis (pure function). Justification: M28 hybrid-genesis
safety core; pure analysis, no merge engine, no parent mutation.


## G31G entry
New abstractions: lineage_routes router (3 GET endpoints) + Studio read-only
projection method. Justification: M28 lineage exposure; routes are thin
transports over the shared LineageGraph; no new store/engine.


## G31H/M28 entry
Moved LineageNode/LineageEdge/LineageGraph to `wanxiang_domain.lineage`
(substrate graph.py = thin re-export) to keep persistence->domain direction;
no new abstraction in this Goal (fixture generator + tests only).


## G32A entry
New abstractions: WorldPolicy, PlatformPolicy, EvolutionPolicyStack (frozen
records) + reject_world_platform_mutation (function). Justification: M29
evolution policy core; policies are config, not a new runtime.


## G32B entry
New abstractions: EvolutionCadence (frozen record) + EvolutionScheduler (thin
class). Justification: M29 multi-scale scheduling core; deterministic modular
activation; no engine/registry.


## G32C entry
New abstractions: PersonaDelta, TrajectoryEntry, ActorEvolutionState (frozen
records) + ActorEvolutionTracker (thin stateful class). Justification: M29
actor evolution separation core; reuses CapabilityDelta.


## G32D entry
New abstractions: BehaviorRecord, CandidateEnvelope (frozen records) +
SocialPatternDistiller (thin class). Justification: M29 distillation core;
candidate-only output (never Canon).


## G32E entry
New abstractions: InstitutionCandidate (frozen record) + InstitutionPromotionChain
(thin chain over CommitAuthority). Justification: M29 institution promotion
core; reuse single authority for LawCommits.


## G32F entry
New abstractions: OntologyCandidate, LawCandidate (frozen records) +
OntologyLawEvolution (stateless validator). Justification: M29 ontology/law
evolution core; pure validation, no engine.


## G32G entry
New abstractions: TelemetryEnvelope (frozen record) + TelemetryPolicy (stateless)
+ CrossWorldDataset (thin store). Justification: M29 telemetry/privacy core;
opt-in + revocable; no sensitive collection by default.


## G32H/M29 entry
No new production abstraction (verification + synthetic-society test only).
M29 abstraction delta recorded in the budget (evolution package).


## G33A entry
New abstractions: LevelRequirement, PromotionEvidence (frozen records) +
PromotionPolicy (versioned table) + validate_promotion (function). Justification:
M30 promotion ladder core; pure validation.


## G33B entry
New abstractions: GenesisSnapshot, PromotionReview (frozen records) +
WorldlinePromotionPipeline (thin chain over WorldDefinition/LineageGraph).
Justification: M30 derived-world promotion core; parent never mutated; reuses
domain WorldDefinition + lineage graph.


## G33C entry
New abstractions: PromotionRecord (frozen record) + PromotionControlLedger
(append-only). Justification: M30 promotion auditability/revocation core;
withdrawal is a status change, never a history deletion.


## G33D entry
New abstractions: CrossWorldCandidate (frozen record) + CrossWorldDistiller
(thin class over CrossWorldDataset). Justification: M30 cross-world
distillation core; authorization + anonymization + no auto-activation.


## G33E entry
New abstractions: SandboxReport, VersionedRelease (frozen records) +
PlatformFeedbackLab (thin chain). Justification: M30 platform-feedback
sandbox/approval core; platform-only approval; rollback never rewrites events.


## G33F entry
New abstractions: promotion_routes router (3 endpoints) + Studio read-only
methods + admin-gated promote. Justification: M30 promotion/lineage surface;
thin transports over existing graph/ladder/pipeline; no new store/engine.


## G33G/M30 entry
No new production abstraction (verification + e2e test only). M30 abstraction
delta recorded in the budget (promotion package).


## G34A entry
No new production abstraction (doc + conformance test only). Pinned the
engine-named set (no God Engines).


## G34B entry
No new abstraction class; extended PackageManifest with 4 optional fields and
the existing packages/migration.py with v2->v3 + migrate_to_v52 (functions).
Justification: M31 WorldPack schema migration core; legacy hashes preserved.


## G34C entry
No new abstraction class (3 ORM columns + migration only). Justification: M31
persistence compatibility core; metadata columns nullable -> no data migration
of existing rows.


## G34D entry
No new abstraction (verification tests only).


## G34E entry
New abstractions: constitution_routes router (1 GET endpoint) + TS SDK
constitution client (types + helpers). Justification: M31 API/SDK
compatibility; thin read-only surface; old endpoints untouched.


## G34F entry
No new production abstraction (benchmark extension + tests only). Performance
bounds recorded; no critical-path degradation.


## G34G/M31 entry
No new production abstraction (verification + rate-limiter reset helper).
M31 abstraction delta recorded in the budget.


## G35A entry
No new production abstraction (registration test only). Real source is
EXTERNAL_BLOCKED; mechanism verified with an explicitly-labeled synthetic fixture.


## G35B entry
New abstraction: SourceLocator (frozen record) + 3 pure functions. Justification:
M32 source-locator mechanism; read-only; no engine/store.
## G35C entry
New abstractions: AliasClaim, IdentityCandidate, IdentityReviewDecision (frozen
records) + IdentityDistiller (pure) + IdentityReviewGate (thin) + identity_to_claim
(function). Justification: M32 identity/alias distillation core; reuses G35B
SourceLocator + G04B ClaimCandidate/EvidenceLink/SourceGate (no second claim
model / registry / engine); candidates never Canon until human/rule review.
## G35D entry
New abstractions: EntityMention, EntityConnection, EntityCandidate,
EntityReviewDecision, DistilledEntities (frozen records) + EntityDistiller
(pure) + EntityReviewGate (thin) + evidence_ok (function) + AUTHORIZED_REVIEWERS
(moved from identity.py). Justification: M32 place/object/organization +
topology distillation core; reuses G35B locators + G35C review semantics via
the shared evidence_ok (IdentityReviewGate ADAPTED, behavior unchanged; no
second evidence rule set); completion_notes never evidence; no registry/engine.
## G35E entry
New abstractions: ScenarioPoint, CanonClaim, CompiledCanon (frozen records) +
CanonCompiler (pure) + scenario_at (function). Justification: M32 canon
compilation core; reuses G35B locators; runtime/control-plane view split keeps
FutureCanon from leaking to the world; no registry/engine/store.
## G35F entry
New abstractions: narrative domain pack (actions/components/resolver/query
modules). Justification: M32 generic household/historical-China domain core;
FORBIDDEN RedChamberCore; missing actions defined in the Domain Pack, never in
Core reference actions; reuses institution (access/duty), material (letter
payload) and agency (authority resolver pattern); no new registry/engine.
## G35G entry
New abstractions: CharacterFact, RelationClaim, KnowledgeBoundary, CharacterCanon
(frozen records) + CharacterDistiller (pure). Justification: M32 runnable
per-character model core; reuses G35B locators + G35E ScenarioPoint/temporal
classification (imported, not duplicated); knowledge boundary prevents private
fact leaks; future facts control-plane only; no registry/engine/store.
## G35H entry
New abstractions: CompletionRecord, CompletionDecision (frozen records) +
CompletionReviewLedger (append-only) + CompletionStudio (read-only queries) +
apply_batch_review (function) + CLI script. Justification: M32 completion
review core; extends (does not replace) G04D CompletionLedger truth taxonomy;
E0-E5 stage semantics with terminal E4/E5; can_enter_canon default false;
reuses AUTHORIZED_REVIEWERS from sources.evidence; no second registry/engine.
## G35I entry
New abstractions: GenesisSpec, WorldPackSignature, AssembledWorldPack (frozen
records) + WorldPackAssembler (pure) + literary_constitution /
sign_world_pack / verify_world_pack (functions). Justification: M32 world-pack
assembly core; reuses G34B PackageManifest v5.2 refs, G31A WorldDefinition,
G30B ConstitutionManifest, G35B/G35E locators+scenario; no new registry/engine;
instantiation dry-run only (no authority writes); core packages stay free of
Red Chamber hardcode.

## M32 entry
No new production abstraction (qualification gate + reports only).
## G36A entry
New abstractions: RC001Profile, InitialSnapshot, RC001Instance (frozen records)
+ instantiate_rc001 / record_lineage_root / resolve_rc001_profile / genesis_delta
(functions). Justification: M33 RC-001 instantiation core; reuses G35I assembler,
G31A InstanceIdentity, CommitAuthority, snapshot hashing, LineageGraph; no new
registry/engine; single commit path.
## G36B entry
New abstractions: MovementProfile (frozen record) + travel_time (function).
Justification: M33 spatial movement-time core; reuses G02A spatial graph/query;
no new registry/engine/store.
## G36C entry
New abstractions: NPCProfile, Activity (frozen records) + daily_schedule /
resolve_population / resolve_population_result (functions). Justification: M33
NPC schedule/population policy core; composes institution/narrative/body
resolvers; no new registry/engine/store.
## G36D entry
New abstractions: ACTION_READ_AND_REMEMBER + resolve_read_and_remember (function).
Justification: M33 read->memory continuity core; reuses material resolve_read +
epistemic memory components; no new registry/engine/store.
## G36E entry
New abstractions: PerceptionEnvelope, PropagatedMessage (frozen records) +
perceive / propagate_message / rumour_distortion / propagatable_claims
(functions). Justification: M33 perception/propagation core; reuses G03B memory
model + G35E runtime view; no new registry/engine/store.
## G36F entry
New abstractions: EmbodimentState, ControlHandoffEvent (frozen records) +
EmbodimentController (thin) + major_decision (function). Justification: M33
embodiment/handoff core; composes G05B LeaseService + G05C ShadowPolicy; no new
registry/engine/store.
## G36G entry
New abstractions: StrategyConfig, BaselineComparison, SoftAttractor, CanonLocks
(frozen records/immutable set) + strategy_for / compare_to_baseline (functions).
Justification: M33 three-strategy policy core; reuses G04D CanonLocked; no new
registry/engine/store.
## G36H entry
New abstractions: ExperienceStudio (read-only queries) + ExperienceViews (frozen
record). Justification: M33 Studio surface; composes existing queries (spatial,
actions, canon runtime view, completion studio, baseline compare); no write
path, no UI authority.
## M33 entry
No new production abstraction (qualification gate + reports only). M33
abstraction deltas recorded in the rc001/spatial/session/material/epistemic
entries above.
## G37A entry
New abstractions: DayEvent, SevenDayResult (frozen records) + SevenDayReferenceRun
(thin) + optional_llm_run (function). Justification: M34 seven-day reference
run core; deterministic; LLM run separated; no new registry/engine/store.
## G37B entry
New abstractions: WorldlineRun, WorldlineComparison (frozen records) +
run_worldlines / compare_worldlines / verify_parent_hash (functions).
Justification: M34 three-worldline comparison core; deterministic; no new
registry/engine/store.
## G37C entry
New abstractions: LongHorizonPromotion (frozen record) + accelerate /
distill_stable / promote_long_horizon (functions). Justification: M34
long-horizon promotion core; reuses G33B pipeline + G33A ladder; no new
registry/engine/store.
## G37D entry
New abstractions: ChaosCheck, ChaosReport (frozen records) + chaos check
functions. Justification: M34 chaos core; reuses runtime snapshot/state
round-trip + CommitAuthority + G36F embodiment; no new registry/engine/store.
## G37E entry
No new production abstraction (verification + audit only). Minimality metrics
captured in v52_minimality_budget.json; per-abstraction justifications recorded
throughout G29A..G37D; no safely-removable compatibility shim identified.

## G37F entry
No new production abstraction (regression + traceability evidence only).

## G37G entry
No new production abstraction (final certification + tag only).
## G38B entry
New abstractions: KernelAbiManifest (frozen record) + abi_manifest / abi_golden /
verify_abi_golden (functions). Justification: M35 kernel v1 ABI freeze core;
deterministic golden; no registry/engine.

## G38C entry
New abstraction: scripts/kernel_guard.py (tooling, not Core). Justification:
M35 kernel change guard (domain names / direct mutation / ABI drift).

## G38D/G38E/G38F/G38G entries
G38D/G38E: no new production abstraction (audits). G38F: CorpusPipeline +
CorpusProfile + generate_synthetic_corpus (mechanism; reuses G35B/G35C).
G38G: no new production abstraction (baselines + benchmark).
## G39 entry
New abstractions: canon_graph package (SceneCandidate, CharacterGraph, SourceGraph,
TimelineGraph, CanonGraph, CoverageReport, FullCorpusPipeline). Justification: M36
full-corpus -> canon-graph composition; reuses G35B/G35C/G38F; no new
registry/engine/store.
## G45 entry
New abstractions: ReleaseFreeze, ReleaseBundle, ReleaseGates, FinalCertification
(frozen records) + freeze_sdk / build_release_bundle / certify_release
(functions). Justification: M42 production release gate core; certification
refused when any gate is red; no new registry/engine/store.

## M51 entry (G54E)
New abstractions: jobs package (Job, JobCheckpoint, JobStore, JobService,
JobError taxonomy). Justification: unified Source->LivingWorld Import/Authoring
job with idempotent create + checkpoint/resume; reuses WanxiangError + single
commit path (jobs never mutate canon); no second registry/engine/store.
Count impact: service_classes 15->16, store_classes 19, py symbols 1176->1190.

## M52 entry (G55A-G55G)
New abstractions: source convergence fields (no new types), BlobRef +
SourceBlobStore, SourceAdapter/ReferenceTextAdapter/AdapterRegistry/
SourceInspection/IngestResult, BookAdapter, StructuredAdapter, AssetAdapter +
GenericAsset, IngestSecurityGate + security errors, Chapter. Justification:
M52 Source Registry & Adapter Foundation; single SourceRegistry, single ObjectStore
port (G16D), adapters propose only. Count impact: registries 11->12, ports 24->25,
py 1190->1231.
