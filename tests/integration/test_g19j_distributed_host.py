"""G19J: distributed world host / sharding experiment & M16 research qualification.

- No split-brain canonical commits (single-writer lease per partition).
- Failover preserves event order and idempotency (duplicate delivery harmless).
- Benchmark quantifies coordination overhead vs modular-monolith baseline:
  marginal benefit => REJECT promotion; stable system stays monolithic.
- Research flag off => no core regression.
"""

from __future__ import annotations

from wanxiang_research.distributed_host import (
    HostBenchmark,
    LeaderElection,
    LeaseRegistry,
    OrderedChannel,
    PartitionCache,
    partition_for,
)
from wanxiang_research.flags import DEFAULT_FLAGS


def test_partitioning_deterministic_by_instance_branch() -> None:
    first = partition_for("inst_1", "branch_a", node_count=4)
    second = partition_for("inst_1", "branch_a", node_count=4)
    assert first == second
    assert first.instance_id == "inst_1"
    assert first.branch_id == "branch_a"
    # Same world/branch always maps to the same node count bucket.
    assert partition_for("inst_1", "branch_a", node_count=4).partition_id == first.partition_id


def test_no_split_brain_canonical_commits() -> None:
    registry = LeaseRegistry(lease_ticks=5)
    election = LeaderElection(("node_a", "node_b", "node_c"), registry)
    assert election.elect("p0") == "node_a"
    # Another node cannot acquire while the lease is live.
    assert registry.acquire("p0", "node_b") is False
    assert registry.holder("p0") == "node_a"
    holders = dict(registry.live_holders())
    assert len([n for n in holders.values() if n == "node_a"]) == 1
    # No partition ever has more than one live holder.
    assert len(set(holders.values())) == len(holders)


def test_failover_preserves_order_and_idempotency() -> None:
    registry = LeaseRegistry(lease_ticks=5)
    channel = OrderedChannel()
    election = LeaderElection(("node_a", "node_b"), registry)
    partition = "p0"
    assert election.elect(partition) == "node_a"
    assert channel.deliver(partition, "cmd_1") is True
    assert channel.deliver(partition, "cmd_2") is True
    # node_a fails: lease expires.
    for _ in range(5):
        registry.advance()
    assert registry.holder(partition) is None
    # node_b becomes leader after failover.
    failover = LeaderElection(("node_b",), registry)
    assert failover.elect(partition) == "node_b"
    # Duplicate delivery of an already-applied command is idempotent.
    assert channel.deliver(partition, "cmd_2") is False
    assert channel.deliver(partition, "cmd_3") is True
    assert channel.order(partition) == ("cmd_1", "cmd_2", "cmd_3")


def test_cache_invalidation_on_leader_change() -> None:
    cache = PartitionCache()
    cache.put("p0", version=1, value="world_v1")
    assert cache.get("p0", version=1) == "world_v1"
    assert cache.get("p0", version=2) is None
    cache.invalidate("p0")
    assert cache.get("p0", version=1) is None
    cache.put("p0", version=2, value="world_v2")
    assert cache.get("p0", version=2) == "world_v2"


def test_benchmark_shows_distributed_overhead() -> None:
    result = HostBenchmark().run(commands=100, partitions=1)
    assert result.split_brain == 0
    assert result.lost_events == 0
    assert result.monolith_ops == 100
    # Coordination (leader check + ordered delivery + renewal) costs extra ops.
    assert result.overhead_ratio > 1.0
    # More partitions do not remove the per-partition coordination cost.
    multi = HostBenchmark().run(commands=100, partitions=4)
    assert multi.overhead_ratio > 1.0
    # Evidence: distribution adds coordination overhead with no correctness gain
    # here, so promotion to stable defaults is NOT justified (REJECT).


def test_flag_off_no_core_regression() -> None:
    assert DEFAULT_FLAGS.is_enabled("distributed_host") is False
    from wanxiang_substrate.compiler.compiler import StructuredCompiler
    from wanxiang_substrate.sources.fixture import approved_source

    assert StructuredCompiler().compile("stable_2", {"src": approved_source()}).ok
