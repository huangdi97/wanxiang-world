"""SQLAlchemy-backed snapshot store."""

from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from wanxiang_domain.hierarchy import BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, SnapshotId, WorldInstanceId
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.snapshot import StoredSnapshot
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_persistence.database import session_scope
from wanxiang_persistence.models import SnapshotRecord
from wanxiang_persistence.state_codec import state_from_primitive, state_to_primitive


class SqlAlchemySnapshotStore:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, metadata: SnapshotMetadata, state: InMemoryCanonicalState) -> SnapshotMetadata:
        record = SnapshotRecord(
            snapshot_id=metadata.snapshot_id.value,
            instance_id=metadata.instance_id.value,
            branch_id=metadata.branch_id.value,
            revision=metadata.revision.value,
            event_seq=metadata.event_seq.value,
            schema_version=metadata.schema_version.value,
            rule_version=metadata.rule_version.value,
            created_world_time=metadata.created_world_time.ticks,
            content_ref=metadata.content_ref,
            state_json=json.dumps(state_to_primitive(state), sort_keys=True),
        )
        with session_scope(self._session_factory) as session:
            session.add(record)
        return metadata

    def load(
        self, instance_id: WorldInstanceId, branch_id: BranchId, revision: BranchRevision
    ) -> StoredSnapshot | None:
        statement = select(SnapshotRecord).where(
            SnapshotRecord.instance_id == instance_id.value,
            SnapshotRecord.branch_id == branch_id.value,
            SnapshotRecord.revision == revision.value,
        )
        with session_scope(self._session_factory) as session:
            record = session.scalars(statement).first()
        return _record_to_snapshot(record) if record is not None else None

    def latest(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        at_or_before_revision: BranchRevision | None = None,
    ) -> StoredSnapshot | None:
        statement = (
            select(SnapshotRecord)
            .where(
                SnapshotRecord.instance_id == instance_id.value,
                SnapshotRecord.branch_id == branch_id.value,
            )
            .order_by(SnapshotRecord.revision.desc())
        )
        if at_or_before_revision is not None:
            statement = statement.where(SnapshotRecord.revision <= at_or_before_revision.value)
        with session_scope(self._session_factory) as session:
            record = session.scalars(statement).first()
        return _record_to_snapshot(record) if record is not None else None


def _record_to_snapshot(record: SnapshotRecord) -> StoredSnapshot:
    metadata = SnapshotMetadata(
        snapshot_id=SnapshotId(record.snapshot_id),
        instance_id=WorldInstanceId(record.instance_id),
        branch_id=BranchId(record.branch_id),
        revision=BranchRevision(record.revision),
        event_seq=EventSeq(record.event_seq),
        schema_version=SchemaVersion(record.schema_version),
        rule_version=RuntimeVersion(record.rule_version),
        created_world_time=WorldTime(record.created_world_time),
        content_ref=record.content_ref,
    )
    state = state_from_primitive(json.loads(record.state_json))
    return StoredSnapshot(metadata=metadata, state=state)
