"""In-memory reference composition used by CLI and socket qualification."""

from __future__ import annotations

from wanxiang_application.ports import PersistenceBundle
from wanxiang_application.synthetic_microworld import register_synthetic_resolvers
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.branch import InMemoryBranchRepository
from wanxiang_runtime.ports import InMemoryEventStore
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.snapshot import InMemorySnapshotStore
from wanxiang_substrate.preview import register_preview_resolvers


class MemoryInstances:
    """Reference instance port; canonical state remains in WorldRuntime."""

    def __init__(self) -> None:
        self._rows: dict[str, tuple[SchemaVersion, RuntimeVersion, WorldTime]] = {}

    def create(
        self,
        instance_id: WorldInstanceId,
        schema_version: SchemaVersion,
        rule_version: RuntimeVersion,
        created_world_time: WorldTime,
    ) -> None:
        self._rows[instance_id.value] = (schema_version, rule_version, created_world_time)

    def get(self, instance_id: WorldInstanceId) -> tuple[SchemaVersion, RuntimeVersion, WorldTime]:
        return self._rows[instance_id.value]


def build_reference_runtime() -> WorldRuntime:
    registry = ResolverRegistry()
    register_synthetic_resolvers(registry)
    register_preview_resolvers(registry)
    return WorldRuntime(
        PersistenceBundle(
            event_store=InMemoryEventStore(),
            snapshot_store=InMemorySnapshotStore(),
            branches=InMemoryBranchRepository(),
            instances=MemoryInstances(),
        ),
        RuntimeVersion(1),
        schema_version=SchemaVersion(1),
        resolvers=registry,
    )


__all__ = ["MemoryInstances", "build_reference_runtime"]
