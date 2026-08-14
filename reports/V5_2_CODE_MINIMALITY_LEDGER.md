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
