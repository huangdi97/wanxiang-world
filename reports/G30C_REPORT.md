# Goal G30C Acceptance Report ? Constitution ???????

## Status
PASS

## Objective
Make Constitution constraints executable in the pre-commit validation path, with
kernel invariants taking priority over any domain/world override.

## Delivered
1. Wired Constitution checks into the existing Invariant Registry
   (`wanxiang_runtime.invariants`):
   - `PLATFORM_PROTECTED_ENTITY_PREFIX = "sys_"` +
     `PLATFORM_PROTECTED_ENTITY_IDS` (`sys_reality_root`,
     `sys_commit_boundary`, `sys_commit_authority`, `sys_constitution`).
   - `check_no_mutation_of_protected_entities` ? world deltas cannot
     create/update/delete platform identities (commit boundary / Reality Root /
     constitution / authority).
   - `check_no_relation_to_protected_entities` ? world deltas cannot relate
     platform identities to world content.
   - Both added to the `INVARIANTS` tuple, which `apply_delta` runs before any
     change is produced ? so a violation raises with NO state mutation.
   - Because these are kernel invariants, they always run and cannot be removed
     or overridden by any world/delta (kernel priority).
2. `ConstitutionViolation(ValidationRejected)` added to
   `wanxiang_domain.errors` (typed failure, exported in domain __init__).
3. `tests/unit/runtime/test_constitution_gate.py` (7 tests):
   - protected identities are platform-scoped;
   - cannot create `sys_commit_authority` / `sys_reality_root` (no mutation);
   - relation to a protected entity rejected (kernel reference check fires
     first ? kernel priority proven by order);
   - a committing world delta targeting the boundary is rejected with an empty
     event stream and unchanged revision;
   - kernel invariants cannot be overridden (duplicate entity still rejected);
   - normal world deltas are NOT blocked by the constitution.

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/runtime/test_constitution_gate.py -q` | 7 passed |
| `uv run pytest tests/unit/runtime tests/unit/domain tests/integration/test_m1_acceptance.py tests/unit/application -q` | 90 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Constitution check wired into Invariant Registry | PASS |
| Kernel invariant priority over Domain/World override | PASS (INVARIANTS always run; tested) |
| Ordinary LawCommit cannot modify Reality Root | PASS (protected identities, tested) |
| World policy cannot elevate itself to platform authority | PASS (sys_commit_authority blocked, tested) |
| Violation => rejected with no state mutation | PASS (tested) |
| No new Commit Boundary bypass | PASS (1 commit path unchanged) |
| Report + ledgers updated | PASS |

## Changed files
- modified: packages/runtime/src/wanxiang_runtime/invariants.py,
  packages/domain/src/wanxiang_domain/errors.py,
  packages/domain/src/wanxiang_domain/__init__.py,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md
- added: tests/unit/runtime/test_constitution_gate.py, reports/G30C_REPORT.md

## Local commit
- Message: `g30c: Constitution ???????`
