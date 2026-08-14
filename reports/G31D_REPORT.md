# Goal G31D Acceptance Report ? World Hypervisor ?????

## Status
PASS

## Objective
Multi-instance / worldline / runtime-profile isolation on the existing World
Host ? no second host.

## Delivered
1. `packages/substrate/src/wanxiang_substrate/host/hypervisor.py`:
   - `RuntimeProfile` ? name + ResourceBudget + evolution_policy bound per
     instance.
   - `WorldHypervisor` ? composes the existing WorldHost/HostRegistry (reused,
     no second host): `bind(host, profile)`, `profile(instance)`,
     `host(instance)`, `submit(instance, command)`, `statuses()`, `shutdown()`.
   - Routing: every CommandEnvelope carries instance_id (+ branch_id as the
     worldline view); `submit` verifies `command.instance_id == route target`
     before forwarding; per-instance BudgetTracker enforces the bound budget.
2. `tests/integration/test_hypervisor.py` (3 tests):
   - two instances with the same local entity id ("alice") keep isolated state
     (count 10 vs 5);
   - interleaved commands route to the correct instance (x/y isolation) and a
     wrong-route command is rejected;
   - profile + per-instance budget binding (BudgetExceeded after 2 commands).

## Verification (commands + results)
| Command | Result |
|---|---|
| `uv run pytest tests/integration/test_hypervisor.py -q` | 3 passed |
| `uv run pytest tests/integration/test_g14e_host_multiplayer.py tests/integration/test_hypervisor.py -q` | 7 passed |
| `uv run python scripts/architecture_check.py` | Architecture conformance: PASS |
| `uv run python scripts/sdk_baseline.py` | routes=10 ts=5 py=894 (+2 non-breaking) |
| `uv run ruff check` / `ruff format --check` / `pyright` (changed files) | PASS / PASS / 0 errors |

## PASS/FAIL/EXTERNAL_BLOCKED matrix
| Item | Status |
|---|---|
| Reuse Host lifecycle | PASS (WorldHost/HostRegistry reused) |
| Instance/worldline routing + resource budget + runtime profile binding | PASS |
| Commands carry explicit world/instance/worldline | PASS (envelope + route verification) |
| Two instances same-ID entities don't pollute | PASS (tested) |
| Concurrent commands route correctly | PASS (tested) |
| No second host | PASS |
| Report + ledgers updated | PASS |

## Changed files
- added: packages/substrate/src/wanxiang_substrate/host/hypervisor.py,
  tests/integration/test_hypervisor.py, reports/G31D_REPORT.md
- modified: reports/sdk_api_baseline.json, reports/SDK_API_BASELINE.md,
  PLAN.md, STATUS.md, DECISIONS.md, CHANGELOG.md,
  reports/V5_2_FINAL_ACCEPTANCE_MATRIX.md, reports/V5_2_CODE_MINIMALITY_LEDGER.md

## Local commit
- Message: `g31d: World Hypervisor ?????`
