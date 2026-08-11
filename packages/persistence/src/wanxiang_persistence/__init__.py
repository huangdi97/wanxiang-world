"""Wanxiang persistence: durable adapters for event/snapshot/branch/instance."""

from wanxiang_persistence.audit_repository import AuditTraceRepository
from wanxiang_persistence.branch_repository import SqlAlchemyBranchRepository
from wanxiang_persistence.database import create_engine_for, session_scope
from wanxiang_persistence.event_store import SqlAlchemyEventStore
from wanxiang_persistence.instance_repository import WorldInstanceRepository
from wanxiang_persistence.models import Base
from wanxiang_persistence.snapshot_store import SqlAlchemySnapshotStore
from wanxiang_persistence.state_codec import state_from_primitive, state_to_primitive

__version__ = "0.1.0"

__all__ = [
    "AuditTraceRepository",
    "Base",
    "SqlAlchemyBranchRepository",
    "SqlAlchemyEventStore",
    "SqlAlchemySnapshotStore",
    "WorldInstanceRepository",
    "create_engine_for",
    "session_scope",
    "state_from_primitive",
    "state_to_primitive",
]
