# Goal G32A Acceptance Report ? Evolution Policy Stack

## Status
PASS

## Objective
Expand the single meta-rule Lambda into layered World/Platform evolution
policies wired into the runtime, with independent World/Platform permissions.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/evolution/policy_stack.py`:
   - `WorldPolicy` ? Actor/Capability/Social/Institution/Ontology/Law/Promotion
     policies (versioned).
   - `PlatformPolicy` ? Model/Plugin/Domain/Runtime/Constitution migration
     policies (versioned).
   - `EvolutionPolicyStack` ? versioned world+platform stack with `versions()`
     (traceable) and `assert_world_cannot_mutate_platform()` (structural guard).
   - `reject_world_platform_mutation(operation)` ? any world policy attempt at a
     platform mutation is PermissionDenied (World/Platform permissions are
     independent).
   - Exported via `wanxiang_substrate.evolution` (SDK baseline +4 non-breaking).
2. `tests/unit/substrate/test_evolution_policy_stack.py` (3 tests):
   - world policy cannot mutate platform (guard + rejection);
   - world and platform policies independent;
   - policy versions traceable (world layers trace to world version).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/unit/substrate/test_evolution_policy_stack.py -q` | 3 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=13 ts=5 py=907 (+4 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| World policies (Actor/Capability/Social/Institution/Ontology/Law/Promotion) | PASS |
| Platform policies (Model/Plugin/Domain/Runtime/Constitution) | PASS |
| World/Platform permission independence | PASS (guard + rejection) |
| World policy cannot call platform mutation | PASS (tested) |
| Policy version traceable | PASS (tested) |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/evolution/policy_stack.py,
  packages/substrate/src/wanxiang_substrate/evolution/__init__.py,
  tests/unit/substrate/test_evolution_policy_stack.py, reports/G32A_REPORT.md
- modified: reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g32a: Evolution Policy Stack`
