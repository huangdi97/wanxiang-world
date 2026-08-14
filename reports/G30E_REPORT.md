# Goal G30E Acceptance Report ? ISA ?????? Commit ????

## Status
PASS

## Objective
Map ISA semantic instructions onto the existing command/proposal/delta/commit/
replay pipeline ? never a parallel command bus or a second event stream.

## Delivered
1. `packages/runtime/src/wanxiang_runtime/isa_pipeline.py`:
   - `execute_isa(op, authority, state, ...)` ? thin adapter over the existing
     machinery:
     - DECLARE/ASSERT/RETRACT/PROPOSE/COMMIT -> `reduce_isa_to_delta` then the
       SAME `CommitAuthority.commit` (single mutation boundary, one schema);
     - VALIDATE -> kernel invariant validation only (never commits);
     - FORK -> existing `fork_branch` (one history/branch model);
     - PROMOTE -> builds a `PromotionUseCase` ONLY (source_worldline_ref,
       target_world_definition_ref, candidate_ref, policy) and never commits
       the parent worldline.
   - `IsaExecutionResult` (op/delta/event/state_after/branch/promotion/validated).
   - Exported via `wanxiang_runtime.__init__` (SDK baseline +3 non-breaking).
2. `tests/unit/runtime/test_isa_pipeline.py` (5 tests):
   - DECLARE via ISA == the same business action via the old entry (identical
     semantic hash; one event; no second stream);
   - ASSERT reuses the relation transition;
   - VALIDATE runs kernel invariants without committing;
   - FORK reuses branch semantics (ancestry recorded, no event);
   - PROMOTE produces a use case and leaves the parent event stream untouched.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/runtime/test_isa_pipeline.py -q` | 5 passed |
| `uv run pytest tests/unit/runtime/ -q` | 44 passed |
| `uv run pytest tests/unit/runtime/test_isa_pipeline.py tests/unit/runtime/test_constitution_gate.py tests/unit/runtime/test_replay.py -q` | 19 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=863 (+3 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| DECLARE -> identity creation proposal | PASS |
| ASSERT/RETRACT -> fact/relation transition | PASS (via existing delta/commit) |
| PROPOSE/VALIDATE/COMMIT reuse existing pipeline | PASS |
| FORK reuses Branch | PASS (fork_branch) |
| PROMOTE only generates use case, no parent commit | PASS (tested) |
| Same business action via old + ISA entry => same semantic outcome | PASS (tested) |
| No second Event stream | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/runtime/src/wanxiang_runtime/isa_pipeline.py,
  tests/unit/runtime/test_isa_pipeline.py, reports/G30E_REPORT.md
- modified: packages/runtime/src/wanxiang_runtime/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g30e: ISA ?????? Commit ????`
