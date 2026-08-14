# Goal G32E Acceptance Report ? Institution Organization Rule ??

## Status
PASS

## Objective
Controlled chain from group pattern -> institution candidate -> validation ->
approval -> LawCommit (never changes Gamma without approval; LawCommits are
replayable).

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/institution_promotion.py`:
   - `InstitutionCandidate` ? rule + evidence + origin + stability_score +
     approved.
   - `InstitutionPromotionChain` ? submit/validate (counterfactual + stability
     threshold MIN_STABILITY + evidence), approve (human/policy hook,
     authorized approvers only), promote (only approved + validated -> LawCommit
     through the single CommitAuthority with kind="law").
   - Exported via `wanxiang_substrate.evolution` (SDK baseline +4 non-breaking).
2. `tests/unit/substrate/test_institution_promotion.py` (4 tests):
   - unapproved candidate does not change Gamma (event stream empty);
   - approved LawCommit is replayable (replay yields the law entity);
   - unstable candidate fails validation even if approved;
   - approval hook requires authorized approver.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_institution_promotion.py -q` | 4 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=922 (+4 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Institution candidate evidence defined | PASS |
| Counterfactual/stability tests | PASS (validate) |
| Human/policy approval hook | PASS (approve) |
| Success -> LawCommit | PASS (kind="law", single authority) |
| Unapproved candidate does not change Gamma | PASS (tested) |
| LawCommit replayable | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/institution_promotion.py,
  tests/unit/substrate/test_institution_promotion.py, reports/G32E_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/evolution/__init__.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g32e: Institution Organization Rule ??`
