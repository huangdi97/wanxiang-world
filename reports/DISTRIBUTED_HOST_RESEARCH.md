# Distributed World Host / Sharding Experiment Research (G19J)

## Prototype
- `partition_for(instance, branch, node_count)` ? deterministic sharding by world instance + branch.
- `LeaseRegistry` + `LeaderElection` ? single-writer lease per partition (no split-brain); deterministic
  failover on lease expiry.
- `OrderedChannel` ? per-partition ordered, idempotent delivery (duplicate command retries never
  duplicate effects).
- `PartitionCache` ? versioned cache with explicit invalidation on leader/world change.
- `HostBenchmark` ? quantifies coordination overhead vs the modular-monolith baseline.

## Results
| Check | Result |
|---|---|
| No split-brain canonical commits (single live holder per partition) | PASS |
| Failover preserves event order and idempotency | PASS |
| Cache invalidation on leader/world change | PASS |
| Deterministic partitioning by instance/branch | PASS |
| Benchmark: monolith 100 ops vs distributed 220 ops (ratio 2.2) @ 1/2/4 partitions | PASS (evidence) |
| Flag OFF -> no core regression | PASS |

## Decision
**REJECT (promotion to stable defaults).** Distribution adds ~2.2x coordination overhead with zero
correctness gain at the current workload scale; no split-brain/ordering defect was found that
distribution would fix. The modular monolith remains the stable default. The partition/lease/channel
seam stays behind the `distributed_host` flag (OFF) for future workload evidence. Real multi-process/
multi-node hosting is EXTERNAL_BLOCKED (single-process deterministic model used).

## Evidence
- `uv run pytest tests/integration/test_g19j_distributed_host.py -q` -> 6 passed.
- Benchmark (commands=100): partitions=1/2/4 -> distributed_ops=220, overhead_ratio=2.2, split_brain=0, lost_events=0.
- ruff/pyright clean; full M16 gate: 628 pytest + 1 EXTERNAL_BLOCKED skip, architecture PASS.
