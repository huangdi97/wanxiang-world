# G97D — Parallel Worldline Certification

Date: 2026-08-27  
Status: PASS

## Scope

G97D closes the separate Gate 41 requirement for at least four parallel
worldlines. It is a bounded engineering/laboratory qualification over a
synthetic, private, rights-approved text source with `training_allowed=false`.
It is not the original 2026-08-25 323,815-character private book; that
real-book acceptance remains `NOT_ACCEPTED` because its rights-approved
diagnostic still produced zero candidates and zero coverage.

## Product-chain evidence

`tests/integration/test_g97d_parallel_worldline_certification.py` creates one
immutable source-created `WorldPackage` and executes four isolated runs through
the same product path:

`SourceRecord → OneClickAuthoring(profile=book) → WorldPackage → Preview →
PlayableService → Living Instance → SQLite WorldRuntime → multi-provider
proposal → Commit Authority → Snapshot → Replay → WorldRunArtifact → Comparator`.

The package is authored once and read by every worker. Four separate SQLite
databases are initialized before execution to keep the known Alembic/SQLite
initialization hazard outside the concurrency measurement; the product-chain
workers then run concurrently through a real `ThreadPoolExecutor` with
`max_parallelism=4`. No worker shares canonical state, event store, branch, or
playable store with another worker.

## Measured parallel qualification

| Measure | Result |
|---|---:|
| Completed registry runs | 4 |
| Seed policy | 2 seeds (9704, 9705) × 2 explicit policies |
| Provider policy variants | forward: Alice→alpha, Bob→beta; reverse: Alice→beta, Bob→alpha |
| Providers per worldline | 2 deterministic private-safe reference providers |
| Worker parallelism | configured 4; 4 distinct worker thread IDs reached the shared barrier |
| Initial-state hash cardinality | 1 across all 4 runs |
| Final-state hash cardinality | ≥2, reflecting retained seed/policy differences |
| Provider proposals | 2 proposal-only invocations per run |
| Provider-side event effect | none; event stream unchanged before Commit Authority action |
| RunArtifact completeness | package/scenario/constitution/runtime/provider/seed/control/commit/snapshot/branch/trajectory/validation/metric/privacy refs present per run |
| Artifact integrity | 4/4 content hashes verify |
| Replay evidence | 4/4 SQLite runs replay to the committed semantic hash |
| Comparator | aligned and qualified; 4 worldlines, all Actor/Relation/Institution/Macro/Cost planes, nonzero differences retained |
| Export privacy | provider input uses `payload_redacted`; source payload absent from serialized evidence |

The batch checkpoint ended with all four run IDs completed and no failed rows.
The registry result rows carry worldline, artifact, checkpoint, seed,
parameter, and metric references. Each artifact is immutable and hash
verifiable; its commit and snapshot references point to the corresponding
isolated SQLite stream. The later action is submitted through
`PlayableService` and the existing Commit Authority, not through a provider or
the comparator.

## Evidence boundaries

The provider runner returned proposals only and the canonical event stream was
unchanged until the normal action submission. The comparator reports aligned
numeric trajectory differences; it does not select a winner, infer a causal
effect, or write world state. The four runs demonstrate deterministic,
auditable parallel execution and policy/seed-sensitive divergence within this
fixture only. They do not establish scientific validity, population validity,
universal emergence, or live-world predictive power.

No original source text was modified, uploaded, exported, or used as a hidden
test fixture. No Candidate was hand-filled, no compiler/worldness gate was
disabled, no coverage was hardcoded, no internal helper was used as a product
shortcut, and no model was trained.

## Quality evidence

- G97D plus G95D/G95E/G95F unit and product-chain regression: `13 passed, 1 warning`.
- Full quality: `1449 passed, 1 skipped, 2 warnings` in 422.71s (7:02).
- The one skip is the documented PostgreSQL `EXTERNAL_BLOCKED` profile because
  `WANXIANG_POSTGRES_TEST_URL` is not configured.
- Ruff check and format check: PASS.
- Full Pyright: `0 errors, 0 warnings`.
- `scripts/architecture_check.py`: PASS.
- `scripts/kernel_guard.py`: 0 violations.
- `git diff --check`: PASS.

G97D is PASS for the parallel World Lab scope. Gate 41 is now ACCEPTED. The
original real-book `NOT_ACCEPTED` boundary, the remaining release gates, and
the prohibition on v5.6/model-training work remain in force.
