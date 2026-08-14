# Strategy / Experiment Workbench Qualification (G18D)

## Service (`wanxiang_api.strategy_workbench_service`)
| Operation | Behavior |
|---|---|
| run | deterministic CoSim batch; result links to config_hash (seed/versions), runtime/schema versions, branch ancestry; marked counterfactual |
| arbitrate | surfaces conflicting simulator proposals with winner + rejected set |

## Results
| Check | Result |
|---|---|
| Same experiment config/seed reproduces a deterministic result | PASS |
| Result links to package/runtime versions and branch ancestry | PASS |
| Invalid simulator proposal is visible as rejected/contract-error, never hidden | PASS |
| Counterfactual results are never presented as historical fact (counterfactual=True) | PASS |

## Evidence
- `uv run pytest tests/integration/test_g18d_strategy_workbench.py -q` -> 3 passed.
- Exploratory simulation is distinct from evidence-backed historical mode (counterfactual label).
