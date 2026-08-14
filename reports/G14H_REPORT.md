# Goal G14H Acceptance Report — SimulationAdapter & External-system Byzantine Behavior Qualification

## Status
PASS (one orchestrator checkpoint gap found and fixed)

## Objective
Prove external simulators/sensors can be slow, inconsistent or malicious without owning world truth.

## Findings
- External bad output cannot mutate canonical state directly (proposals only).
- Invalid proposals rejected/audited; conflicts arbitrated deterministically.
- Timeouts fail fast without host deadlock.
- **Fixed (P1)**: CoSimOrchestrator checkpoint omitted the orchestrator clock, breaking restore+continue;
  the clock is now part of the checkpoint and restore realigns barriers.
- Checkpoint mismatches (wrong length/payload) detected explicitly.
- Byzantine observations rejected or retained as conflicts.

## Delivered
- `tests/integration/test_g14h_byzantine.py` — 5 tests.
- Core fix: `packages/substrate/src/wanxiang_substrate/cosim/orchestrator.py`.
- `reports/EXTERNAL_SIMULATOR_ADVERSARIAL.md`, `reports/G14H_REPORT.md`.

## Evidence
- `uv run pytest tests/integration/test_g14h_byzantine.py -q` -> 5 passed; co-sim/reality regression 17 passed.

## Remaining limitations
- Real external providers/hardware remain EXTERNAL_BLOCKED; deterministic byzantine adapters cover the boundary.

## Final checkpoint
- commit: `g14h: simulationadapter & external-system byzantine behavior qualification`
