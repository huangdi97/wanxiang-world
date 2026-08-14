# Goal G32D Acceptance Report ? Relation Group Social Pattern Distillation

## Status
PASS

## Objective
Distill relation/group/norm candidates from repeated behavior history ? never
directly into Canon ? with windowed detection, CandidateEnvelope +
origin/provenance, and a policy-controlled stability threshold.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/distillation.py`:
   - `BehaviorRecord` (behavior/actor/window), `CandidateEnvelope`
     (candidate_id, pattern_type, key, observed_count, windows_seen, threshold,
     origin_ref, provenance; `meets_threshold`).
   - `SocialPatternDistiller` ? windowed pattern detection (one count per
     window), policy-controlled threshold filtering; candidates only when the
     stability threshold is met; provenance = sorted window refs.
   - Exported via `wanxiang_substrate.evolution` (SDK baseline +4 non-breaking).
2. `tests/unit/substrate/test_distillation.py` (4 tests):
   - single behavior cannot upgrade (no candidate below threshold);
   - multi-window stable pattern forms a candidate (with provenance);
   - threshold is policy-controlled;
   - candidates are envelopes, never canon (no truth label).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_distillation.py -q` | 4 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=918 (+4 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Reuse evolutionary distillation (candidate flow) | PASS |
| Windowed pattern detection | PASS |
| CandidateEnvelope + origin/provenance | PASS |
| Stability threshold controlled by policy | PASS (tested) |
| Single behavior cannot upgrade | PASS (tested) |
| Multi-window stable pattern -> candidate | PASS (tested) |
| Never writes Canon directly | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/distillation.py,
  tests/unit/substrate/test_distillation.py, reports/G32D_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/evolution/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g32d: Relation Group Social Pattern Distillation`
