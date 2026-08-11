"""Ports the application layer needs from persistence/adapters."""

from __future__ import annotations

from typing import Protocol

from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.audit import AuditRecord
from wanxiang_runtime.branch import BranchRepository
from wanxiang_runtime.ports import EventStore
from wanxiang_runtime.snapshot import SnapshotStore


class WorldInstanceStore(Protocol):
    def create(
        self,
        instance_id: WorldInstanceId,
        schema_version: SchemaVersion,
        rule_version: RuntimeVersion,
        created_world_time: WorldTime,
    ) -> None: ...

    def get(
        self, instance_id: WorldInstanceId
    ) -> tuple[SchemaVersion, RuntimeVersion, WorldTime]: ...


class AuditSink(Protocol):
    def record(self, audit: AuditRecord) -> None: ...


class PersistenceBundle:
    """Bundled persistence ports injected into the application runtime."""

    def __init__(
        self,
        event_store: EventStore,
        snapshot_store: SnapshotStore,
        branches: BranchRepository,
        instances: WorldInstanceStore,
        audit: AuditSink | None = None,
    ) -> None:
        self.event_store = event_store
        self.snapshot_store = snapshot_store
        self.branches = branches
        self.instances = instances
        self.audit = audit
