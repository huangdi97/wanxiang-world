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
