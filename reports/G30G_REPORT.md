# Goal G30G Acceptance Report ? Fact Scope ? Authority Partition

## Status
PASS

## Objective
Unify Fact semantics while keeping canonical/public/org/actor/hypothesis/
reconstruction write-permission isolation; forbid scope-only elevation of
beliefs to canonical; require Commit for canonical promotion; filter
projection/perception by scope and rights.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/ledger/fact_scope.py`:
   - `FactScope` (canonical/public/org/actor/hypothesis/reconstruction) +
     `FACT_SCOPES` + `FACT_SCOPE_WRITERS` (canonical is exclusive to
     `commit_authority`; actor is actor-owned; hypothesis/reconstruction are
     researcher-owned).
   - `FactScopePolicy`:
     - `assert_write_allowed(scope, writer)` -> PermissionDenied on mismatch;
     - `assert_canonical_promotion_requires_commit(current, target, via_commit)`
       -> any cross-scope change without Commit is rejected; canonical
       promotion specifically requires Commit (scope-only edits rejected);
     - `can_view(scope, viewer)` -> projection/perception filter (canonical +
       public visible; org only to org viewers; actor only to the owner via
       projection; hypothesis/reconstruction only to researchers; system/admin
       override).
   - Exported via `wanxiang_substrate.ledger` (SDK baseline +4 non-breaking).
2. `ProjectionService` now filters `ledger.fact` entities by scope + rights:
   actor-owned facts are hidden from other actors, org facts hidden from
   outsiders, hypothesis/reconstruction hidden from ordinary actors (admin
   override preserved). Existing projection behavior unchanged for other types.
3. `tests/unit/substrate/test_fact_scope.py` (5 tests):
   - canonical exclusive to commit authority; actor scope not writable by
     authority; commit authority can write the other scopes;
   - scope-only elevation to canonical rejected; canonical promotion via Commit
     allowed at policy layer;
   - any scope change without Commit rejected; same-scope edit fine;
   - actor belief does not leak canonical/other-actor/org/hypothesis facts;
   - cross-role peeking fails (org hidden from outsider; admin sees all).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_fact_scope.py -q` | 5 passed |
| `uv run pytest tests/unit/substrate tests/integration/test_g14g_auth_privacy.py tests/integration/test_g15d_embodiment.py -q` | 69 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=870 (+4 non-breaking) |
| `uv run python scripts/v52_minimality_budget.py` | hard_ok=True (0 cycles, 1 commit path) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Fact schema + scope policy | PASS (FactScopePolicy over the shared Fact schema) |
| Scope-only elevation to canonical forbidden | PASS (tested) |
| Canonical promotion requires Commit | PASS (tested) |
| Projection/Perception filtered by scope + rights | PASS (ProjectionService integration + tests) |
| Actor belief does not leak canonical | PASS (tested) |
| Cross-role peeking fails | PASS (tested) |
| No new Commit Boundary bypass | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/ledger/fact_scope.py,
  tests/unit/substrate/test_fact_scope.py, reports/G30G_REPORT.md
- modified: packages/substrate/src/wanxiang_substrate/ledger/__init__.py,
  packages/substrate/src/wanxiang_substrate/projection/service.py,
  reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  reports/v52_minimality_budget.json, PLAN.md, STATUS.md, DECISIONS.md,
  CHANGELOG.md, reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md,
  reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g30g: Fact Scope ? Authority Partition`
