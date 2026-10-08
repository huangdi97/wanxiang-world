"""R7 operational/readiness projections.

These records are observability only. They summarize runtime evidence and never
become canonical world truth, a migration decision, or a commit precondition.
Secret-bearing fields are intentionally absent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

MigrationStatus = Literal["idle", "planned", "shadow_replay", "blocked", "complete"]
ComponentStatus = Literal["ready", "degraded", "blocked", "unknown"]


@dataclass(frozen=True, slots=True)
class R7OpsView:
    """Non-canonical operational snapshot for one worldline."""

    world_id: str
    worldline_id: str
    revision: int
    runtime_lock_hash: str
    reality_profile_ref: str
    world_profile_ref: str
    provider_graph_hash: str
    proposal_count: int = 0
    commit_count: int = 0
    reject_count: int = 0
    history_append_latency_ms: float = 0.0
    replay_duration_ms: float = 0.0
    actor_calls: int = 0
    model_calls: int = 0
    execution_jobs: int = 0
    token_count: int = 0
    cost_microunits: int = 0
    resource_units: int = 0
    migration_status: MigrationStatus = "idle"
    outbox_pending: int = 0
    outbox_retries: int = 0

    def __post_init__(self) -> None:
        for name in (
            "world_id",
            "worldline_id",
            "runtime_lock_hash",
            "reality_profile_ref",
            "world_profile_ref",
            "provider_graph_hash",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        counters = (
            self.revision,
            self.proposal_count,
            self.commit_count,
            self.reject_count,
            self.actor_calls,
            self.model_calls,
            self.execution_jobs,
            self.token_count,
            self.cost_microunits,
            self.resource_units,
            self.outbox_pending,
            self.outbox_retries,
        )
        if any(value < 0 for value in counters):
            raise ValueError("operational counters must be non-negative")
        if self.history_append_latency_ms < 0 or self.replay_duration_ms < 0:
            raise ValueError("operational latencies must be non-negative")

    def to_dict(self) -> dict[str, object]:
        return {
            "world_id": self.world_id,
            "worldline_id": self.worldline_id,
            "revision": self.revision,
            "runtime_lock_hash": self.runtime_lock_hash,
            "reality_profile_ref": self.reality_profile_ref,
            "world_profile_ref": self.world_profile_ref,
            "provider_graph_hash": self.provider_graph_hash,
            "proposal_count": self.proposal_count,
            "commit_count": self.commit_count,
            "reject_count": self.reject_count,
            "history_append_latency_ms": self.history_append_latency_ms,
            "replay_duration_ms": self.replay_duration_ms,
            "actor_calls": self.actor_calls,
            "model_calls": self.model_calls,
            "execution_jobs": self.execution_jobs,
            "token_count": self.token_count,
            "cost_microunits": self.cost_microunits,
            "resource_units": self.resource_units,
            "migration_status": self.migration_status,
            "outbox_pending": self.outbox_pending,
            "outbox_retries": self.outbox_retries,
            "canonical": False,
        }


@dataclass(frozen=True, slots=True)
class R7ReadinessView:
    """Operational readiness; explicitly not a statement about world truth."""

    ready: bool
    world_host: ComponentStatus
    providers: ComponentStatus
    migration: ComponentStatus
    blockers: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if any(not blocker.strip() for blocker in self.blockers):
            raise ValueError("readiness blockers must be non-empty strings")
        expected = (
            self.world_host == "ready"
            and self.providers == "ready"
            and self.migration == "ready"
            and not self.blockers
        )
        if self.ready != expected:
            raise ValueError("ready must equal the component/blocker projection")

    def to_dict(self) -> dict[str, object]:
        return {
            "ready": self.ready,
            "world_host": self.world_host,
            "providers": self.providers,
            "migration": self.migration,
            "blockers": list(self.blockers),
            "canonical": False,
        }


def r7_readiness(
    *,
    world_host: ComponentStatus,
    providers: ComponentStatus,
    migration: ComponentStatus,
    blockers: tuple[str, ...] = (),
) -> R7ReadinessView:
    """Build a deterministic readiness projection from operational inputs."""
    ready = world_host == "ready" and providers == "ready" and migration == "ready" and not blockers
    return R7ReadinessView(ready, world_host, providers, migration, blockers)


__all__ = [
    "ComponentStatus",
    "MigrationStatus",
    "R7OpsView",
    "R7ReadinessView",
    "r7_readiness",
]
