# Goal G21C Acceptance Report — Duplicate Abstraction, Registry, State & Manager Forensics

## Status
PASS

## Objective
Find architectural duplication that would make v5.1 additive rather than consolidating.

## Delivered
- `scripts/v51_forensics.py` — deterministic AST scan (registries, state models, stores, services/managers, engines, ports, oversized modules, commit paths); writes `reports/V5_1_DUPLICATE_FORENSICS.md`.
- `reports/V5_1_DUPLICATE_FORENSICS.md` — scan inventory + disposition analysis for every candidate.
- `tests/architecture/test_v51_forensics.py` — 3 acceptance checks (deterministic scan; exactly one commit path; dispositions recorded). 3 passed.
- Updated traceability matrix, code-minimality ledger, PLAN/STATUS/CHANGELOG/DECISIONS.

## Key findings
- Commit paths: exactly 1 (`CommitAuthority.commit`); capability resolver `_apply_delta` only produces ProposedWorldDelta. No hidden second authority path (confirms reports/CANONICAL_MUTATION_PATHS.md).
- Registries (10): all domain-specific (package/source/skill/action/adjudicator/resolver/host) — KEEP_AS_IS; research registries EXPERIMENTAL. One typed Runtime Capability Catalog deferred to G25G for runtime providers only.
- Strong MERGE candidate: duplicate `SnapshotStore`/`InMemorySnapshotStore` in `wanxiang_runtime.snapshot` vs `wanxiang_substrate.recovery.checkpoint`. Runtime one is the production port (SqlAlchemy impl); recovery CheckpointService should consume it (G21F/G21G). Risk: medium.
- Stores: EventStore port/impl KEEP; CompletionLedger KEEP (content truth, must NOT merge into triple-ledger streams per R8); research stores EXPERIMENTAL.
- Services (15): all small/cohesive; no god objects; apps/api services are thin per-surface route services.
- Engines (2): ReplayEngine KEEP; PlannerEngine (research) EXPERIMENTAL.
- Ports (23): all justified replaceable/external boundaries; only duplicated port is the recovery SnapshotStore.
- Schema duplicates: none — one generated OpenAPI contract + drift test (SCHEMA_DRIFT_AUDIT.md).
- Oversized modules: 0 (>300 LOC).
- Placeholder scan: no TODO/FIXME/NotImplemented/pass in production; `return NotImplemented` in packages/model.py is the comparison-protocol sentinel (legitimate).

## No deletion performed (per Goal non-goal)
All dispositions are documented; deletions/merges execute in G21E/G21F/G21G with call-site evidence.

## Verification
- Architecture scan deterministic (test compares two runs).
- Direct canonical mutation search green: 1 commit path.
- Ruff/Pyright on new files: PASS (verified).
- Golden replay regression: unaffected (no production change).

## PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix
| Item | Status |
|---|---|
| Duplicate forensics + dispositions | PASS |
| Single authority path verified | PASS |
| SnapshotStore consolidation | MERGE candidate (G21F/G21G) |
| M16 research registries/stores | EXPERIMENTAL |

## Remaining risks
- SnapshotStore merge must preserve recovery semantics (corrupt-snapshot validation, latest-by-instance) when adapting to the runtime port.
- Registry unification (G25G) must not collapse domain registries with different value types/lifecycles.

## Changed files
- added: scripts/v51_forensics.py, reports/V5_1_DUPLICATE_FORENSICS.md, tests/architecture/test_v51_forensics.py, reports/G21C_REPORT.md; updated: PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md, reports/V5_1_TRACEABILITY_MATRIX.md, reports/V5_1_CODE_MINIMALITY_LEDGER.md.

## Local commit
- Message: `v5.1 g21c: duplicate abstraction, registry, state & manager forensics`
