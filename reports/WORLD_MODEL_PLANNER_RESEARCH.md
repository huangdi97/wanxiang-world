# World-model / Planner Proposal Engine Research (G19E)

## Prototype
- `Planner` Port + `HeuristicPlanner` (deterministic baseline; no learned model).
- `PlannerEngine.propose/validate/rollout` — proposals never mutate canonical state; rollouts run on
  disposable simulations labeled `simulation_prediction`; impossible steps rejected by validators.

## Results
| Check | Result |
|---|---|
| Bad proposal cannot bypass invariants (rejected by validator) | PASS |
| Planner can be disabled with no core regression (flag OFF) | PASS |
| Rollout results labeled predictions/simulations | PASS |

## Decision
**KEEP_EXPERIMENTAL** — the proposal/rollout seam is sound; a learned provider and goal-scoring benchmark are
needed for promotion (EXTERNAL_BLOCKED).

## Evidence
- `uv run pytest tests/integration/test_g19e_planner.py -q` -> 3 passed.
