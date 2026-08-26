# G92F — Resource / Cost Budget

Date: 2026-08-26  
Status: PASS

## Delivered contract

`CostBudgetLedger` tracks calls, tokens, time, and storage independently for
world, actor, and provider `BudgetKey`s. Multi-scope admission is atomic:
every scope must fit before usage is charged. Threshold `BudgetAlert`s expose
warning/exhausted metrics. `BackpressurePolicy` distinguishes allow, defer,
and hard reject. Exhaustion recommends the next SimulationLOD level without a
partial charge; L4 exhaustion rejects explicitly.

The ledger is an admission/projection boundary only. It does not mutate World
Truth, call providers, or write through Commit Authority.

## Evidence

- `tests/unit/substrate/test_g92f_budget.py`: 2 passed, including atomic
  multi-scope usage, alerts, LOD degradation, and backpressure.
- `tests/integration/test_g92f_budget_runtime.py`: 1 passed; real SQLite
  Runtime canonical hash and event count stay unchanged during budget-driven
  LOD degradation.
- Combined focused result: 3 passed, 1 existing Hypothesis collection warning.
- Ruff check and format check: PASS.
- Pyright on changed implementation/tests: 0 errors, 0 warnings.
- `scripts/kernel_guard.py`: 0 violations.
- `scripts/architecture_check.py`: PASS.

G92F is PASS. Cost/storage Gate 28 remains pending until M89 long-run
quantification; G92G-G97J remain pending and v5.5 remains
`IN_PROGRESS / NOT_ACCEPTED`. No model training, private source upload, or
v5.6 work was performed.
