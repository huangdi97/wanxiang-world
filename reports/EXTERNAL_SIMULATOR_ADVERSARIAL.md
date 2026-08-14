# External Simulator Adversarial Qualification (G14H)

## Scenarios
| Byzantine behavior | Handling | Result |
|---|---|---|
| Adapter emits proposed deltas | never auto-committed; canonical state untouched (proposals only) | PASS |
| Conflicting proposals | deterministic arbitration; conflict marked; rejected set explicit | PASS |
| Adapter violates declared rate | AdapterContractError (rejected before commit) | PASS |
| Adapter crash/timeout during advance | fail fast (no host deadlock); healthy orchestrator continues | PASS |
| Checkpoint mismatch (wrong length / wrong payload) | OrchestrationError / AdapterContractError (detected) | PASS |
| Orchestrator restore+continue | clock persisted in checkpoint; barriers realign (fixed in this Goal) | PASS |
| Invalid observation (negative tick, confidence, wrong unit) | rejected at the boundary (WanxiangError family) | PASS |
| Conflicting observations from one source | retained as a conflict set (never silently resolved) | PASS |

## Fix (P1)
`CoSimOrchestrator.checkpoint()` did not persist the orchestrator clock (`_now`), so `restore()` + continue
could "step backwards" or mis-step barriers. The checkpoint now includes the clock and restore realigns it.

## Design
- Simulation boundary is a Port/Adapter; external output is proposal/observation only, never committed directly.
- Fail closed on unverifiable proposals; timeouts fail fast; checkpoint mismatches are explicit.

## Evidence
- `uv run pytest tests/integration/test_g14h_byzantine.py -q` -> 5 passed.
- Co-sim + reality regression (17 tests) PASS.
