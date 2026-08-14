# V5.2 Code Disposition ? Actual Inventory (G29B)

Generated: 2026-08-14 (G29B)
Status: PASS
Method: deterministic AST scanners (`scripts/v51_forensics.py`,
`scripts/v51_dependency_graph.py`, `scripts/architecture_check.py`,
`scripts/v51_metrics.py`) + `rg` call-site evidence over packages/apps.
Every DELETE/MERGE disposition below carries consumer evidence; nothing was
classified by name alone.

## 1. Inventory summary (actual, post-G29A)

| Area | Count | Notes |
|---|---|---|
| Physical packages | 8 | application, domain, observability, persistence, research, runtime, sdk_ts, substrate |
| Apps | 1 | apps/api (FastAPI composition root) |
| Production .py files | 263 | 21,822 LOC; 524 classes; 186 functions |
| Migrations | 2 | 0001_initial, 0002_add_event_seq_index (head 0002) |
| Tests | 164 tracked files | 655 pytest passing + 1 EXTERNAL_BLOCKED skip |
| Scripts | 29 | tooling/quality/forensics/ops |
| Commit paths | 1 | packages/runtime/src/wanxiang_runtime/authority.py `commit` |

## 2. Package/app disposition

| Unit | Disposition | Rationale (evidence) |
|---|---|---|
| packages/domain | KEEP | Pure semantic contracts; no framework imports (guard-enforced); world-agnostic |
| packages/runtime | KEEP/ADAPT | Single CommitAuthority + ReplayEngine + branch/snapshot ports; will gain thin v5.2 adapters only |
| packages/application | KEEP/ADAPT | Orchestration facade; PersistenceBundle/WorldInstanceStore/AuditSink all consumed by apps/api + world_runtime/state_reader |
| packages/persistence | KEEP/ADAPT | SqlAlchemyEventStore + SqlAlchemySnapshotStore consumed by apps/api and runtime ports |
| packages/substrate | KEEP/ADAPT | Modular monolith substrate; largest package (188 files) but 0 oversized modules; registries are domain-local |
| packages/observability | KEEP | telemetry; consumed by apps/api + substrate |
| packages/research | EXPERIMENTAL | 9 research tracks behind OFF flags; distributed host REJECTED for promotion (ADR 0055) |
| packages/sdk_ts | KEEP | TS SDK; OpenAPI contract drift-tested |
| apps/api | KEEP/ADAPT | composition root; 10 routes / 10 operations |
| packages/evidence | DELETED (G29A) | empty stub, zero consumers (`rg wanxiang_evidence` -> none) |
| packages/model_providers | DELETED (G29A) | empty stub, zero consumers (`rg wanxiang_model_providers` -> none) |

## 3. Duplicate-abstraction findings (call-site verified)

### 3.1 Registries (11 total; 10 classes + RegistryLifecycle)
| Registry | Consumers | Disposition |
|---|---|---|
| packages/substrate/packages/registry.py PackageRegistry + InMemoryPackageRegistry | packages/__init__, lifecycle.py, install.py | KEEP ? package manifest registry (single package ecosystem) |
| packages/substrate/actions/registry.py ActionRegistry | actions runtime | KEEP ? domain-local |
| packages/substrate/resolution/registry.py AdjudicatorRegistry | resolution runtime | KEEP ? domain-local |
| packages/substrate/skills/registry.py SkillRegistry | skills runtime | KEEP ? domain-local |
| packages/substrate/sources/registry.py SourceRegistry | sources runtime | KEEP ? domain-local |
| packages/runtime/resolver.py ResolverRegistry | runtime | KEEP ? command validator registry |
| packages/substrate/host/host.py HostRegistry | host runtime | KEEP ? host registry |
| packages/research/results.py ExperimentRegistry | research (EXPERIMENTAL) | KEEP ? research only |
| packages/research/distributed_host.py LeaseRegistry | research (EXPERIMENTAL, flag OFF) | KEEP ? research only |
| packages/substrate/packages/lifecycle.py RegistryLifecycle | lifecycle | KEEP ? lifecycle helper, not a registry store |

No two registries serve the same problem; no MERGE required. The v5.2 rule "Package
Registry + Provider Registry are two different problems" is already satisfied.

### 3.2 State models (18)
| Finding | Disposition |
|---|---|
| domain/state.py CanonicalState (contract) vs runtime/state.py InMemoryCanonicalState (impl, 48 consumers) | ADAPT/KEEP ? intentional port/implementation split, not a duplicate |
| runtime/snapshot.py StoredSnapshot | KEEP ? runtime snapshot store entry |
| substrate/recovery/checkpoint.py SnapshotStore + InMemorySnapshotStore | MERGE (G29C) ? duplicate of runtime SnapshotStore port; only 2 internal consumers (recovery/__init__, recovery/recovery.py) |
| substrate projection/spatial/capability/session/lifecycle model states | KEEP ? distinct domain state types, no semantic overlap |
| error/exception "State" classes (InvalidMaterialState, UnauthorizedProjection, CorruptSnapshot, NoSnapshot, InvalidSpatialState) | KEEP ? exception types, not state stores |

### 3.3 Event stores / stores (16)
| Finding | Disposition |
|---|---|
| runtime/ports.py EventStore (port) + InMemoryEventStore (48 consumers) | KEEP ? core port |
| persistence/event_store.py SqlAlchemyEventStore | ADAPT ? SQL transport of the same port, consumed by apps/api |
| persistence/snapshot_store.py SqlAlchemySnapshotStore | ADAPT ? SQL transport of the runtime SnapshotStore port |
| substrate/assets/storage.py ObjectStore + LocalObjectStore | KEEP ? asset storage, single pair |
| substrate/ledger/ledger.py CompletionLedger | KEEP ? completion ledger, distinct from triple ledgers (DECISIONS 0057/0058) |
| research MemoryStore / SensorStream / SyntheticSensorStream | EXPERIMENTAL ? research only |

### 3.4 Services (15)
- 8 substrate services (Lifecycle/Perspective/Projection/Checkpoint/Recovery/Adjudication/Session/Lease) ? each has a distinct bounded role; no two overlap (verified by module locality).
- 7 apps/api product facades (Studio/Strategy/ExperiencePlayer/FamilyPortal/HeritageWorkbench/Learn/OperatorConsole) ? thin projections over the same substrate services; KEEP (product surface).

### 3.5 Engines (3)
- runtime ReplayEngine ? core replay; KEEP.
- research PlannerEngine ? EXPERIMENTAL; KEEP behind flag.
- persistence create_engine_for ? SQLAlchemy engine factory (function); KEEP.
- v5.2 hard rule: no new RealityRootEngine/SemanticISAEngine/WorldlineEngine/EvolutionManager god objects. Existing set already minimal.

### 3.6 Ports (23)
- All 23 ports have at least one consumer or are part of a documented external
  boundary (DB, LLM/harness, simulator, sensor, renderer, asset storage, search).
  No unused port found by `rg` over packages/apps.

## 4. World-specific leakage into Core
`rg -ni "red_chamber|???|mansion|liaoshen|genealogy|heritage|rc-001" packages/domain/src packages/runtime/src`
-> zero hits. Core (domain + runtime) is world-agnostic. Red Chamber content must
live in World/Domain/Experience content (reference_worlds / packages), never Core.

## 5. DELETE / MERGE candidates (with migration strategy)
| Candidate | Type | Consumers today | Migration strategy | When |
|---|---|---|---|---|
| packages/evidence, packages/model_providers | DELETE | none | removed with full regression (G29A) | done |
| substrate/recovery/checkpoint.py SnapshotStore + InMemorySnapshotStore | MERGE | recovery/__init__.py, recovery/recovery.py (2 internal) | point recovery module at the runtime SnapshotStore port; delete the duplicate class pair; keep CheckpointService/RecoveryService behavior | G29C |

Everything else is KEEP/ADAPT. No REPLACE dispositions are warranted without an ADR.

## 6. Dead-code check
- No production module with zero `wanxiang_*` import consumers found among the
  scanned packages (all package `__init__` exports are re-exported and used).
- `packages/research` tracks are EXPERIMENTAL but referenced by tests + flags.
- No TODO/FIXME/placeholder in production paths (see G29F for the full sweep).

## 7. Conclusion
The repository is already close to the v5.2 "one of each" target: one commit path,
one event semantics, one branch model, one package registry, one snapshot port
(after the single G29C merge), domain-local registries only, no world-specific Core
leakage. G29B found exactly one actionable duplicate (recovery snapshot store) and
two already-deleted stubs.
