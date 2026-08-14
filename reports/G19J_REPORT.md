# Goal G19J Acceptance Report ? Distributed World Host / Sharding Experiment & M16 Research Qualification

## Status
PASS (research; decision: REJECT promotion ? stable system stays monolithic)

## Objective
Test whether evidence justifies splitting selected hosting workloads across processes/nodes while
preserving branch ordering, ownership and replay semantics; do not distribute by default without benefit.

## Delivered
- `wanxiang_research/distributed_host.py` ? partition_for, LeaseRegistry, LeaderElection,
  OrderedChannel, PartitionCache, HostBenchmark, BenchmarkResult.
- `tests/integration/test_g19j_distributed_host.py` ? 6 tests.
- `reports/DISTRIBUTED_HOST_RESEARCH.md`, `reports/G19J_REPORT.md`,
  `reports/M16_RESEARCH_EXPANSION_QUALIFICATION.md`, `reports/M16_ACCEPTANCE.md`.
- ADR 0055 in DECISIONS.md (distribution REJECTED for promotion).

## Findings
- Single-writer leases prevent split-brain; failover preserves order + idempotency; cache invalidation
  is explicit.
- Benchmark: distribution costs ~2.2x coordination ops with no correctness benefit at current
  workload -> promotion NOT justified; modular monolith stays the stable default.

## Decision
REJECT (promotion); experiment retained behind `distributed_host` flag (OFF). Real multi-node hosting
is EXTERNAL_BLOCKED.

## Evidence
- 6 tests passed; benchmark ratio 2.2 (1/2/4 partitions); ruff/pyright clean; full M16 gate green
  (628 passed + 1 EXTERNAL_BLOCKED skip, architecture PASS).

## Final checkpoint
- commit: `g19j: distributed world host / sharding experiment & m16 research qualification`
- tag: `m16-research-expansion`
