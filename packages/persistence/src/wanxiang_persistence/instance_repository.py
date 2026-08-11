"""World instance metadata repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from wanxiang_domain.errors import NotFound
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

from wanxiang_persistence.database import session_scope
from wanxiang_persistence.models import WorldInstanceRecord


class WorldInstanceRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def create(
        self,
        instance_id: WorldInstanceId,
        schema_version: SchemaVersion,
        rule_version: RuntimeVersion,
        created_world_time: WorldTime,
    ) -> None:
        record = WorldInstanceRecord(
            instance_id=instance_id.value,
            schema_version=schema_version.value,
            rule_version=rule_version.value,
            created_world_time=created_world_time.ticks,
        )
        with session_scope(self._session_factory) as session:
            session.add(record)

    def get(self, instance_id: WorldInstanceId) -> tuple[SchemaVersion, RuntimeVersion, WorldTime]:
        statement = select(WorldInstanceRecord).where(
            WorldInstanceRecord.instance_id == instance_id.value
        )
        with session_scope(self._session_factory) as session:
            record = session.scalars(statement).first()
        if record is None:
            raise NotFound(f"world instance {instance_id.value} not found")
        return (
            SchemaVersion(record.schema_version),
            RuntimeVersion(record.rule_version),
            WorldTime(record.created_world_time),
        )
