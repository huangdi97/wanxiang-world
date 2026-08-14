# Goal G21B Acceptance Report — v5.1 Delta Traceability & Existing-code Classification

## Status
PASS

## Objective
Map every material v5.1 delta to existing code and classify the smallest required action.

## Delivered
- `reports/V5_1_TRACEABILITY_MATRIX.md` — 37 classified deltas (D01-D37): spec requirement → current owner → current evidence → action (KEEP/KEEP_AS_IS/ADAPT/MERGE/ADD/EXPERIMENTAL; REPLACE: none).
- `tests/architecture/test_v51_traceability.py` — 4 completeness checks (matrix exists; every required delta classified; no UNCLASSIFIED table row; no REPLACE without ADR). 4 passed.
- Updated `reports/V5_1_CODE_MINIMALITY_LEDGER.md`, `PLAN.md`, `STATUS.md`, `DECISIONS.md`, `CHANGELOG.md`.

## Classification summary
- KEEP/KEEP_AS_IS: source/evidence/rights gates, backward-migration paths, cross-domain qualification, product surfaces, clean-room certification.
- ADAPT: reality-calculus mapping, commit-kind envelope, version context, scoped Fact contract, GenesisSpec over existing package system, candidate/distiller semantics over existing compiler, runtime capability/ABI, triple ledgers over existing audit/event store, bounded runtime evolution orchestration.
- MERGE: runtime registries → one typed Runtime Capability Catalog (forensics in G21C/G21F first).
- ADD (new irreducible semantics): RuntimeControlTransaction, Ontology/Law candidates+commits, Runtime Capability catalog; no CapabilityCommit world kind.
- DELETE candidates: empty stub packages `wanxiang_evidence` and `wanxiang_model_providers` (5 LOC each, no live imports beyond bootstrap/false-completion scan) — resolved in G21C/G21E.
- EXPERIMENTAL: M16 research tracks (9); evolutionary distillation seam; DeepSeek Harness/Cordis optional provider only.

## Conflicts with prior M16 experiments
- Distributed/federated hosting REJECTED for promotion (ADR 0055); capability fabric absorbs only typed-contract/dependency ideas.
- DSH/Cordis optional AgentHarness provider only; core never depends on it (R9).
- Triple ledgers must not merge into the existing CompletionLedger (content/truth ledger, different concern).

## Verification
- Traceability completeness check against mother-spec headings: PASS (4/4 tests).
- No required delta left UNCLASSIFIED.
- Ruff/Pyright: new test passes ruff/pyright (verified).
- Architecture/import-boundary checks: unaffected (no production change).
- Golden replay regression: unaffected (no stable-core change).

## PASS/FAIL/EXTERNAL_BLOCKED/EXPERIMENTAL matrix
| Item | Status |
|---|---|
| Delta traceability matrix | PASS |
| Completeness check tests | PASS |
| Real-source/provider cross-domain data | EXTERNAL_BLOCKED (unchanged) |
| M16 research tracks | EXPERIMENTAL |

## Remaining risks
- Registry consolidation (D24) depends on G21C/G21F forensics; must not merge semantically distinct registries blindly.
- Commit-kind envelope must preserve v5.0 event replay (G22C/G22F guard).

## Changed files
- added: reports/V5_1_TRACEABILITY_MATRIX.md (rebuilt), tests/architecture/test_v51_traceability.py, reports/G21B_REPORT.md; updated: PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md, reports/V5_1_CODE_MINIMALITY_LEDGER.md.

## Local commit
- Message: `v5.1 g21b: v5.1 delta traceability & existing-code classification`
