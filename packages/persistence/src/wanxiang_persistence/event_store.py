"""SQLAlchemy-backed event store implementing the runtime EventStore contract."""

from __future__ import annotations

import json

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from wanxiang_domain.errors import (
    Conflict,
    CorruptEventStream,
    DuplicateCommandConflict,
    PersistenceError,
    WanxiangError,
)
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.hierarchy import EventSeq
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.serialization_history import event_from_primitive, event_to_primitive

from wanxiang_persistence.database import session_scope
from wanxiang_persistence.models import EventRecord


class SqlAlchemyEventStore:
    """Durable event store with strict ordering, idempotency and integrity."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self.session_factory = session_factory

    def append(self, event: CommittedEvent) -> None:
        if self.command_result_event(event.command_id) is not None:
            raise DuplicateCommandConflict(f"command {event.command_id.value} already committed")
        current = self.last_event_seq(event.instance_id, event.branch_id)
        if event.event_seq.value != current.value + 1:
            raise Conflict(
                "out-of-order append: expected seq "
                f"{current.value + 1}, got {event.event_seq.value}"
            )
        record = EventRecord(
            event_id=event.event_id.value,
            instance_id=event.instance_id.value,
            branch_id=event.branch_id.value,
            event_seq=event.event_seq.value,
            revision=event.revision.value,
            schema_version=event.schema_version.value,
            command_id=event.command_id.value,
            rule_version=event.rule_version.value,
            world_time=event.world_time.ticks,
            actor_id=event.actor_id.value if event.actor_id else None,
            causation_id=event.causation_id.value if event.causation_id else None,
            correlation_id=event.correlation_id.value if event.correlation_id else None,
            trace_id=event.trace_id.value if event.trace_id else None,
            commit_timestamp=(
                event.commit_timestamp.utc.isoformat() if event.commit_timestamp else None
            ),
            delta_json=json.dumps(event_to_primitive(event), sort_keys=True),
        )
        try:
            with session_scope(self.session_factory) as session:
                session.add(record)
        except IntegrityError as exc:
            raise _map_integrity_error(exc, event) from exc

    def load(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        *,
        from_seq: int | None = None,
        to_seq: int | None = None,
    ) -> tuple[CommittedEvent, ...]:
        statement = (
            select(EventRecord)
            .where(
                EventRecord.instance_id == instance_id.value,
                EventRecord.branch_id == branch_id.value,
            )
            .order_by(EventRecord.event_seq)
        )
        if from_seq is not None:
            statement = statement.where(EventRecord.event_seq >= from_seq)
        if to_seq is not None:
            statement = statement.where(EventRecord.event_seq <= to_seq)
        with session_scope(self.session_factory) as session:
            records = session.scalars(statement).all()
        return tuple(_record_to_event(record) for record in records)

    def last_event_seq(self, instance_id: WorldInstanceId, branch_id: BranchId) -> EventSeq:
        statement = select(func.max(EventRecord.event_seq)).where(
            EventRecord.instance_id == instance_id.value,
            EventRecord.branch_id == branch_id.value,
        )
        with session_scope(self.session_factory) as session:
            max_seq = session.scalar(statement)
        return EventSeq(max_seq) if max_seq is not None else EventSeq(0)

    def command_result_event(self, command_id: CommandId) -> CommittedEvent | None:
        statement = select(EventRecord).where(EventRecord.command_id == command_id.value)
        with session_scope(self.session_factory) as session:
            record = session.scalars(statement).first()
        return _record_to_event(record) if record is not None else None

    def has_command(self, command_id: CommandId) -> bool:
        return self.command_result_event(command_id) is not None

    def integrity_check(self, instance_id: WorldInstanceId, branch_id: BranchId) -> None:
        events = self.load(instance_id, branch_id)
        expected = 1
        seen: set[str] = set()
        for event in events:
            if event.event_seq.value != expected:
                raise CorruptEventStream(
                    f"expected event seq {expected}, got {event.event_seq.value}"
                )
            if event.event_id.value in seen:
                raise CorruptEventStream(f"duplicate event id {event.event_id.value}")
            seen.add(event.event_id.value)
            expected += 1


def _record_to_event(record: EventRecord) -> CommittedEvent:
    payload = json.loads(record.delta_json)
    return event_from_primitive(payload)


def _map_integrity_error(exc: IntegrityError, event: CommittedEvent) -> WanxiangError:
    message = str(exc.orig)
    if "command_id" in message or "uq_events" in message and "command" in message.lower():
        return DuplicateCommandConflict(f"command {event.command_id.value} already committed")
    if "uq_events_stream_seq" in message or "events.instance_id" in message:
        return Conflict(f"out-of-order/duplicate append for seq {event.event_seq.value}")
    return PersistenceError(f"database constraint violation: {message}")
