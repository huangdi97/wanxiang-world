"""SQLAlchemy-backed branch repository."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from wanxiang_domain.errors import NotFound
from wanxiang_domain.hierarchy import BranchAncestry, BranchMetadata, BranchRevision, EventSeq
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion

from wanxiang_persistence.database import session_scope
from wanxiang_persistence.models import BranchRecord


class SqlAlchemyBranchRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save(self, metadata: BranchMetadata) -> None:
        record = BranchRecord(
            branch_id=metadata.branch_id.value,
            instance_id=metadata.instance_id.value,
            parent_branch_id=(
                metadata.ancestry.parent_branch_id.value
                if metadata.ancestry.parent_branch_id
                else None
            ),
            fork_revision=(
                metadata.ancestry.fork_revision.value if metadata.ancestry.fork_revision else None
            ),
            fork_event_seq=(
                metadata.ancestry.fork_event_seq.value if metadata.ancestry.fork_event_seq else None
            ),
            fork_snapshot_ref=metadata.ancestry.fork_snapshot_ref,
            schema_version=metadata.schema_version.value,
            rule_version=metadata.rule_version.value,
            snapshot_ref=metadata.snapshot_ref,
        )
        with session_scope(self._session_factory) as session:
            session.add(record)

    def get(self, branch_id: BranchId) -> BranchMetadata:
        statement = select(BranchRecord).where(BranchRecord.branch_id == branch_id.value)
        with session_scope(self._session_factory) as session:
            record = session.scalars(statement).first()
        if record is None:
            raise NotFound(f"branch {branch_id.value} not found")
        return _record_to_metadata(record)

    def list(self, instance_id: WorldInstanceId) -> tuple[BranchMetadata, ...]:
        statement = (
            select(BranchRecord)
            .where(BranchRecord.instance_id == instance_id.value)
            .order_by(BranchRecord.branch_id)
        )
        with session_scope(self._session_factory) as session:
            records = session.scalars(statement).all()
        return tuple(_record_to_metadata(record) for record in records)


def _record_to_metadata(record: BranchRecord) -> BranchMetadata:
    parent = record.parent_branch_id
    ancestry = BranchAncestry(
        parent_branch_id=BranchId(parent) if parent else None,
        fork_revision=BranchRevision(record.fork_revision)
        if record.fork_revision is not None
        else None,
        fork_event_seq=EventSeq(record.fork_event_seq)
        if record.fork_event_seq is not None
        else None,
        fork_snapshot_ref=record.fork_snapshot_ref,
    )
    return BranchMetadata(
        branch_id=BranchId(record.branch_id),
        instance_id=WorldInstanceId(record.instance_id),
        ancestry=ancestry,
        schema_version=SchemaVersion(record.schema_version),
        rule_version=RuntimeVersion(record.rule_version),
        snapshot_ref=record.snapshot_ref,
    )
