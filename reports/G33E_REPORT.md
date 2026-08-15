# Goal G33E Acceptance Report ? ???? Sandbox Benchmark Approval

## Status
PASS

## Objective
Validate cross-world candidates via a shadow/sandbox run (benchmark / ablation /
invariant / security / cost / determinism), with an approval policy and versioned
Domain/Runtime release; world instances never approve platform upgrades;
rollback never rewrites past world events.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/platform_feedback.py`:
   - `SandboxReport` (benchmark metrics + invariants/security/cost/determinism +
     approved).
   - `VersionedRelease` (kind domain/runtime, name, version, status).
   - `PlatformFeedbackLab` ? run_sandbox (shadow run), approve (only
     platform_reviewer/platform_policy; world instance rejected), release
     (versioned after approval), rollback (status change only).
   - Exported via `wanxiang_substrate.evolution` (SDK baseline +4 non-breaking).
2. `tests/unit/substrate/test_platform_feedback.py` (3 tests):
   - world instance does not own platform approval;
   - sandbox gate blocks approval/release on failure;
   - versioned release + rollback do not rewrite world events (golden hash
     7d17aba7... unchanged).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_platform_feedback.py -q` | 3 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=947 (+4 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Shadow/sandbox run | PASS |
| Benchmark/ablation/invariant/security/cost/determinism | PASS |
| Approval policy | PASS (platform-only; world instance rejected) |
| Versioned Domain/Runtime release after approval | PASS |
| World instance does not own platform approval | PASS (tested) |
| Rollback doesn't rewrite past world events | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/platform_feedback.py,
  tests/unit/substrate/test_platform_feedback.py, reports/G33E_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/evolution/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g33e: ???? Sandbox Benchmark Approval`
