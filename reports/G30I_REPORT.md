# Goal G30I Acceptance Report ? M27 Root Constitution ISA ????

## Status
PASS

## Objective
Prove the new M27 semantics (Reality Root / Constitution / ISA / Fact Scope /
version context) did not create a second kernel and the old authority path
remains the only mutation path.

## Delivered
1. Ran the full M27 gate (`milestones/M27_QUALIFICATION.md`):
   - full quality suite -> 714 passed + 1 EXTERNAL_BLOCKED skip (live
     PostgreSQL); ruff/format/pyright/architecture PASS.
2. Architecture + mutation-path search:
   - `commit_paths` = 1 (forensics);
   - event-store `append(` call sites: exactly one production path
     (`CommitAuthority.commit` -> `EventAppendPort.append`); the in-memory
     port implementation is the only other appearance;
   - state `.apply(` call sites: `state.apply_delta` (authority path) and
     `ReplayEngine.replay` (rebuild) are the canonical uses;
     `resolution/service._validate_delta` is a PURE dry-run on a copy (no
     mutation, result discarded); `LearningPolicy.apply` operates on
     capability/learner state (runtime control), never canonical world state;
   - no route/provider/UI writes canonical tables (architecture guard +
     G29D evidence).
3. Generated `reports/M27_QUALIFICATION.md` (commit range, gate results,
   acceptance matrix, perf/complexity, blockers, next-milestone prerequisites).

## Gate fixes
- Full regression surfaced 3 pre-existing quality nits in the M27 tests:
  B017 blind `pytest.raises(Exception)` (constitution + constitution-gate
  tests) and one unformatted blank-line pair in errors.py ? all fixed; the
  budget test anchor updated (ports 23 -> 24 after RealityRootContract).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run python scripts/quality.py` | ruff/format/pyright PASS; pytest 714 passed + 1 skip; architecture PASS |
| `uv run python scripts/v51_forensics.py` | commit_paths 1; registries 10; services 15; engines 2; ports 24; stores 16; 0 oversized |
| `uv run python scripts/v52_minimality_budget.py` | hard_ok=True (0 cycles, 1 commit path) |
| mutation-path grep | only authority path appends events; resolution dry-run is pure |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| M27 gate executed | PASS |
| All commits still enter a single authority | PASS (commit_paths 1 + grep) |
| Old replay still PASS | PASS (golden hash unchanged; 714 tests) |
| No second state/event/branch/commit system | PASS |
| Architecture + mutation-path search | PASS |
| root/constitution/ISA acceptance report | PASS (M27_QUALIFICATION.md) |
| Report + ledgers updated | PASS |

## Changed files
- modified: tests/architecture/test_v52_minimality_budget.py,
  tests/unit/domain/test_constitution.py,
  tests/unit/runtime/test_constitution_gate.py,
  packages/domain/src/wanxiang_domain/errors.py,
  reports/V5_1_DUPLICATE_FORENSICS.md, reports/V5_2_MINIMALITY_BUDGET.md,
  reports/v52_minimality_budget.json, PLAN.md, STATUS.md, DECISIONS.md,
  CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md
- added: reports/G30I_REPORT.md, reports/M27_QUALIFICATION.md

## Local commit
- Message: `g30i: M27 Root Constitution ISA ????`
