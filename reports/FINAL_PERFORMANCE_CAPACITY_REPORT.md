# Final Performance / Capacity Report

## Status
PASS (mechanism) — performance and capacity baselines frozen.

## Benchmarks (scripts/benchmarks.py, profile=small_ci)
| Benchmark | Result |
|---|---|
| Commits (SQLite-bound) | 200 events, ~4.97s, ~40.2 events/s |
| Replay | 1200 events ~24ms |
| Lineage query | 400 nodes ~13ms |

## Capacity
- Large-corpus pipeline: 1000-chapter synthetic corpus parses/distills within
  memory bounds (<64 MiB estimated); incremental cache/resume (G38F/M36).
- Aggregate population benchmark: 100 actors / 1000 duties (G43F) PASS.
- 30-day + 1-year accelerated long-run summary stable with checkpoint/crash/
  recovery (G41G).

## Boundary
Real-corpus performance baselines EXTERNAL_BLOCKED (G35A); baselines are for the
platform mechanism on synthetic content.
