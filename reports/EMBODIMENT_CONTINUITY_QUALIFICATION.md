# Embodiment Continuity Qualification (G15D)

## Scenario (day 1 -> exit -> advance -> re-entry)
| Step | Behavior | Result |
|---|---|---|
| Human takes over the mayor (embodiment lease) | LeaseService.acquire -> one primary controller | PASS |
| Human command | normal committed action through Commit Authority (temporal.advance) | PASS |
| Shadow advice while human controls | ShadowPolicy records advice with sequence | PASS |
| Conflicting takeover | second session -> LeaseConflict (one controller) | PASS |
| Human exits | lease released; primary_controller None | PASS |
| World advances after exit | AutonomousScheduler commits more events; revision grows | PASS |
| Control handoff | ControlHandoff hand_back -> resume (autonomous continues) | PASS |
| Re-entry | new lease; projection reflects the authoritative current state (not stale) | PASS |

## Worldness criterion
Control-handoff continuity: human control, exit, autonomous continuation, and re-entry are coherent;
sessions are ephemeral while the world instance/branch persists independently.

## Evidence
- `uv run pytest tests/integration/test_g15d_embodiment.py -q` -> 1 passed.
- Human actions remain normal committed actions (no bypass of Commit Authority or actor constraints).
