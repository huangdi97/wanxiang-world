# Goal G16I Acceptance Report — Performance, Capacity, Cost & Resource-budget Qualification

## Status
PASS

## Objective
Measure and document operating envelopes for commits, replay, hosting, actor scheduling, projections, batch experiments and package operations.

## Delivered
- `scripts/benchmarks.py` — repeatable benchmark suite (commits, replay) with environment capture.
- `tests/integration/test_g16i_performance.py` — 3 tests.
- `reports/PERFORMANCE_CAPACITY_COST.md`, `reports/performance_benchmarks.json`, `reports/G16I_REPORT.md`.

## Findings
- Measured envelope: ~44 commits/s (SQLite durability), 16ms replay of 1200 events, 90-day run ~36s.
- Bottleneck identified (per-commit fsync) with an evidence-based next step (batch/PostgreSQL), not speculation.
- Resource budgets enforced and violations explicit.

## Evidence
- 3 tests passed; ruff/pyright clean.

## Remaining limitations
- No internet/MMO-scale claims; numbers are environment-measured. Cloud/PostgreSQL benchmarking EXTERNAL_BLOCKED.

## Final checkpoint
- commit: `g16i: performance, capacity, cost & resource-budget qualification`
