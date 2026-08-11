"""Audit trace repository (durable structured audit)."""

from __future__ import annotations

from sqlalchemy.orm import Session, sessionmaker
from wanxiang_runtime.audit import AuditRecord

from wanxiang_persistence.database import session_scope
from wanxiang_persistence.models import AuditTraceRecord


class AuditTraceRepository:
    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def record(self, audit: AuditRecord) -> None:
        row = AuditTraceRecord(
            trace_id=audit.trace_id.value,
            command_id=audit.command_id.value,
            event_id=audit.event_id.value,
            instance_id=audit.instance_id.value,
            branch_id=audit.branch_id.value,
            revision=audit.revision.value,
            rule_version=audit.rule_version.value,
            world_time=audit.world_time.ticks,
            actor_id=audit.actor_id.value if audit.actor_id else None,
            correlation_id=audit.correlation_id.value if audit.correlation_id else None,
            commit_timestamp=(
                audit.commit_timestamp.utc.isoformat() if audit.commit_timestamp else None
            ),
        )
        with session_scope(self._session_factory) as session:
            session.add(row)
