# Worldline Comparison Qualification (G15F)

## Scenario
Shared history (letter fixture) -> fork at a chosen revision -> three worldlines:
- Baseline: no intervention.
- Intervention 1: deliver the letter to the recipient.
- Intervention 2: deliver then read.

## Results
| Criterion | Result |
|---|---|
| Branch ancestry explicit (child.parent == parent) | PASS |
| Parent history unchanged after all worldlines | PASS |
| Baseline identical to parent (no intervention) | PASS |
| Interventions diverge causally (custody moved) | PASS |
| Each worldline independently replayable to its hash | PASS |
| Semantic diff highlights causal differences | PASS |
| Historical read consistent with fork revision (time-travel/read-only) | PASS |

## Semantics
Counterfactuals are simulations, not claims about real history; parent history is never mutated to
create an alternative worldline.

## Evidence
- `uv run pytest tests/integration/test_g15f_worldlines.py -q` -> 1 passed.
