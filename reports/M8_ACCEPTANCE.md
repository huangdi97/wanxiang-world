# M8 Acceptance ? Mechanistic External Models Can Participate Without Owning Canonical State

## Verdict
PASS

## Scope
P8 (G11A?G11F) delivered on top of verified M1-M7. The mandatory scenario ran
over real internal paths (fake simulators, orchestrator, campaign, batch
experiments).

## Mandatory scenario (tests/integration/test_m8_qualification.py)
1. Two deterministic fake simulators (rates 2 and 5) run 10 synchronization
   barriers; each advances only on its own rate boundaries (supply 20, weather
   4 over 20 ticks).
2. Adapters only emit events/proposed deltas; never commit.
3. Conflicting simulator proposals are adjudicated explicitly (deterministic
   winner "supply", rejected list).
4. Campaign: organization order with delay moves a unit; supply flow raises
   resources; movement to a region with no route fails (deviation); fog-of-war
   hides the red faction's eastern region from blue.
5. Batch experiment across 2 variants x 3 seeds produces a 6-run matrix,
   deterministic across reruns, with distributions and a Finding carrying
   assumptions + ValidityEnvelope.

## Required proofs
| Proof | Status | Evidence |
|---|---|---|
| SimulationAdapter full contract incl. checkpoint/restore/assumptions/validity | PASS | adapter tests |
| Adapters receive slices/snapshots; only emit events/proposed deltas | PASS | emit tests + vertical |
| Multi-rate ordering deterministic and restartable | PASS | orchestrator determinism + restore tests |
| Conflicting proposals adjudicated explicitly | PASS | arbitration tests |
| Campaign logistics/position/resource invariants hold | PASS | campaign tests + vertical |
| Faction observations/beliefs respect fog-of-war | PASS | knows() tests |
| Batch results are distributions with verification/validity metadata | PASS | experiment distribution/envelope |
| Liaoshen real pack EXTERNAL_BLOCKED; generic M8 not blocked | PASS | template + M8 PASS |

## Required regression
| Gate | Status | Evidence |
|---|---|---|
| M1-M7 milestone gates | PASS | full suite |
| Architecture conformance | PASS | scripts/architecture_check.py |
| Persistence/migration/replay compatibility | PASS | full suite |
| Rights/projection leakage | PASS | full suite |
| No-LLM deterministic profile | PASS | full suite |
| Lint/typecheck | PASS | ruff + pyright clean |
| TODO/placeholder + secret scan | PASS | architecture guard |

## Evidence summary
- `uv run python scripts/quality.py` -> All quality checks passed (372 tests).
- Checkpoint commit: `m8: qualify milestone`
- Milestone tag: `m8-cosimulation-strategy`