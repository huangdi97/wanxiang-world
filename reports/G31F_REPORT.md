# Goal G31F Acceptance Report ? Hybrid Genesis ??????????

## Status
PASS

## Objective
First version of pre-merge semantic checks that REJECT unsafe merges instead of
faking a Git merge; output a MergePlan Candidate or a Rejection; never
auto-resolve arbitrary conflicts.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/lineage/hybrid_genesis.py`:
   - `GenesisCheck` (name/ok/detail), `HybridGenesisReport`
     (left_ref/right_ref/verdict/checks + failing_checks()).
   - `analyze_hybrid_genesis(left, right)` ? six checks:
     constitution compatibility (legacy v5 compatible), identity (distinct
     definitions, no silent id collision), ontology (shared schema version),
     law (same package lineage or explicit policy required), rights (same
     genesis provenance), history (both parents append-only; analysis never
     rewrites parent history).
   - Verdict = candidate (all checks ok) or rejected (with failing checks).
   - Exported via `wanxiang_substrate.lineage` (SDK baseline +4 non-breaking).
2. `tests/unit/substrate/test_hybrid_genesis.py` (5 tests):
   - incompatible constitution rejected;
   - legacy constitution compatible;
   - rights conflict rejected;
   - compatible worlds -> merge-plan candidate;
   - analysis never rewrites parent histories (content hashes unchanged).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_hybrid_genesis.py -q` | 5 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=903 (+4 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Constitution compatibility | PASS |
| Identity/Ontology/Law/Rights/History policy checks | PASS |
| MergePlan Candidate or Rejection output | PASS |
| No auto-resolve of arbitrary conflicts | PASS (rejection on any failing check) |
| Incompatible constitution rejected | PASS (tested) |
| Rights conflict rejected | PASS (tested) |
| Parent histories not rewritten | PASS (tested) |
| No fake Git merge | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/lineage/hybrid_genesis.py,
  tests/unit/substrate/test_hybrid_genesis.py, reports/G31F_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/lineage/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g31f: Hybrid Genesis ??????????`
