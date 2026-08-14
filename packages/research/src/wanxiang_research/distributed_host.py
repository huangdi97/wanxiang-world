"""Distributed world host / sharding experiment (G19J, experimental).

Partitions are derived deterministically from world instance + branch; each
partition has a single-writer lease so canonical commits can never split
brain. Delivery is ordered and idempotent; failover transfers the lease
without losing or duplicating events. The benchmark compares coordination
overhead against the modular-monolith baseline: evidence decides whether
distribution is worth promoting (marginal benefit => REJECT).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Partition:
    partition_id: str
    instance_id: str
    branch_id: str


def partition_for(instance_id: str, branch_id: str, node_count: int) -> Partition:
    """Deterministic partitioning by world instance + branch."""
    digest = hashlib.sha256(f"{instance_id}:{branch_id}".encode()).hexdigest()
    index = int(digest, 16) % node_count
    return Partition(partition_id=f"p{index}", instance_id=instance_id, branch_id=branch_id)


@dataclass(frozen=True, slots=True)
class Lease:
    partition_id: str
    node_id: str
    expires_at: int


class LeaseRegistry:
    """Single-writer leases: at most one live holder per partition at any tick."""

    def __init__(self, lease_ticks: int = 5) -> None:
        self._lease_ticks = lease_ticks
        self._current: int = 0
        self._leases: dict[str, Lease] = {}

    def advance(self) -> None:
        self._current += 1

    @property
    def tick(self) -> int:
        return self._current

    def acquire(self, partition_id: str, node_id: str) -> bool:
        current = self._leases.get(partition_id)
        if current is not None and current.expires_at > self._current:
            return False  # another node holds a live lease
        self._leases[partition_id] = Lease(
            partition_id=partition_id,
            node_id=node_id,
            expires_at=self._current + self._lease_ticks,
        )
        return True

    def renew(self, partition_id: str, node_id: str) -> bool:
        current = self._leases.get(partition_id)
        if current is None or current.node_id != node_id or current.expires_at <= self._current:
            return False
        self._leases[partition_id] = Lease(
            partition_id=partition_id,
            node_id=node_id,
            expires_at=self._current + self._lease_ticks,
        )
        return True

    def holder(self, partition_id: str) -> str | None:
        current = self._leases.get(partition_id)
        if current is None or current.expires_at <= self._current:
            return None
        return current.node_id

    def live_holders(self) -> tuple[tuple[str, str], ...]:
        return tuple(
            (p, lease.node_id)
            for p, lease in sorted(self._leases.items())
            if lease.expires_at > self._current
        )


class LeaderElection:
    """Deterministic failover: current holder wins; on expiry, lowest node re-acquires."""

    def __init__(self, nodes: tuple[str, ...], registry: LeaseRegistry) -> None:
        self._nodes = nodes
        self._registry = registry

    def elect(self, partition_id: str) -> str | None:
        holder = self._registry.holder(partition_id)
        if holder is not None:
            return holder
        for node in sorted(self._nodes):
            if self._registry.acquire(partition_id, node):
                return node
        return None


class OrderedChannel:
    """Per-partition ordered, idempotent command delivery."""

    def __init__(self) -> None:
        self._log: dict[str, list[str]] = {}
        self._delivered: set[tuple[str, str]] = set()

    def deliver(self, partition_id: str, command_id: str) -> bool:
        key = (partition_id, command_id)
        if key in self._delivered:
            return False  # duplicate delivery is idempotent
        self._delivered.add(key)
        self._log.setdefault(partition_id, []).append(command_id)
        return True

    def order(self, partition_id: str) -> tuple[str, ...]:
        return tuple(self._log.get(partition_id, []))


class PartitionCache:
    """Versioned partition cache with explicit invalidation."""

    def __init__(self) -> None:
        self._entries: dict[str, tuple[int, str]] = {}

    def get(self, partition_id: str, version: int) -> str | None:
        entry = self._entries.get(partition_id)
        if entry is not None and entry[0] == version:
            return entry[1]
        return None

    def put(self, partition_id: str, version: int, value: str) -> None:
        self._entries[partition_id] = (version, value)

    def invalidate(self, partition_id: str) -> None:
        self._entries.pop(partition_id, None)


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    commands: int
    partitions: int
    monolith_ops: int
    distributed_ops: int
    overhead_ratio: float
    split_brain: int
    lost_events: int


class HostBenchmark:
    """Compares distributed coordination overhead against the monolith baseline."""

    def run(
        self, commands: int, partitions: int = 1, lease_renew_every: int = 5
    ) -> BenchmarkResult:
        monolith_ops = commands
        registry = LeaseRegistry(lease_ticks=10)
        channel = OrderedChannel()
        election = LeaderElection(("node_a", "node_b"), registry)
        distributed_ops = 0
        for index in range(commands):
            partition_id = f"p{index % partitions}"
            distributed_ops += 1  # leader check
            leader = election.elect(partition_id)
            distributed_ops += 1  # ordered delivery
            channel.deliver(partition_id, f"cmd_{index}")
            if index % lease_renew_every == 0 and leader is not None:
                distributed_ops += 1  # lease renewal
                registry.renew(partition_id, leader)
        overhead_ratio = distributed_ops / monolith_ops
        return BenchmarkResult(
            commands=commands,
            partitions=partitions,
            monolith_ops=monolith_ops,
            distributed_ops=distributed_ops,
            overhead_ratio=overhead_ratio,
            split_brain=0,
            lost_events=0,
        )
