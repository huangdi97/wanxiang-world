# Multi-simulator Federation & Co-Simulation Research (G19H)

## Prototype
- `SimulatorAdapter` Port + `TickSimulator` (fast/coarse) and `PreciseSimulator` (slow/precise)
  deterministic fake simulators with declared `ValidityEnvelope`.
- `FederationScheduler` ? multi-rate time coordination (advances only simulators whose due time is
  reached; causality preserved by time-ordered emission) with reproducible checkpoint/restore and a
  deterministic coordination-step benchmark.
- `ConflictResolver` ? conflicts resolved EXPLICITLY by declared model precedence; no precedence means
  UNRESOLVED (never implicit fastest-wins). `FederationCoordinator` emits a `CommitProposal` (data,
  never committed to canonical state); proposal is ready only when no conflict is unresolved.
- Partial simulator failure is isolated: failed simulator is recorded and the others continue.

## Results
| Check | Result |
|---|---|
| Checkpoint/restore reproducible (stable digest) | PASS |
| Conflicts resolved explicitly before commit; no implicit winner | PASS |
| Failed simulator does not corrupt others/world | PASS |
| Multi-rate coordination deterministic (7 steps for tick+precise @ 3.0) | PASS |
| Validity envelopes/assumptions persist with every delta | PASS |
| Flag OFF -> no core regression | PASS |

## Decision
**KEEP_EXPERIMENTAL** ? deterministic federation seam proven; real heterogeneous simulators/FMI
integrations are EXTERNAL_BLOCKED. Promotion requires federation determinism + explicit-conflict
parity on real adapters.

## Evidence
- `uv run pytest tests/integration/test_g19h_sim_federation.py -q` -> 7 passed.
- ruff/pyright clean; architecture PASS at the M16 gate.
