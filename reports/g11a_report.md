# Goal G11A Acceptance Report
## Status
PASS
## Objective
SimulationAdapter contract + deterministic fake simulator.
## Delivered
- `wanxiang_substrate.cosim.adapter`: full contract protocol + FakeSimulator
  (initialize/ingest/advance/emit/checkpoint/restore/assumptions/validity).
## Test evidence
- contract lifecycle + checkpoint/restore; adapters never commit; wrong-rate
  advance rejected.
## Final checkpoint
- commit: `goal g11a: simulation adapter contract & fake simulator`