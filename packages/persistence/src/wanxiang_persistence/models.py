"""SQLAlchemy ORM models for P1 persistence.

ORM is confined to this package; domain/runtime layers access state through
ports. Schema is PostgreSQL-compatible (text PKs, integer counters, JSON-as-text
payloads); SQLite is used for local tests with foreign keys enabled.
"""

from __future__ import annotations

from sqlalchemy import (
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WorldInstanceRecord(Base):
    __tablename__ = "world_instances"

    instance_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False)
    rule_version: Mapped[int] = mapped_column(Integer, nullable=False)
    created_world_time: Mapped[int] = mapped_column(Integer, nullable=False)
    definition_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
    constitution_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
    evolution_policy_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)


class BranchRecord(Base):
    __tablename__ = "branches"

    branch_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    instance_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("world_instances.instance_id"), nullable=False, index=True
    )
    parent_branch_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    fork_revision: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fork_event_seq: Mapped[int | None] = mapped_column(Integer, nullable=True)
    fork_snapshot_ref: Mapped[str | None] = mapped_column(Text, nullable=True)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False)
    rule_version: Mapped[int] = mapped_column(Integer, nullable=False)
    snapshot_ref: Mapped[str | None] = mapped_column(Text, nullable=True)


class EventRecord(Base):
    __tablename__ = "events"
    __table_args__ = (
        UniqueConstraint("instance_id", "branch_id", "event_seq", name="uq_events_stream_seq"),
    )

    event_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    instance_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    branch_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    event_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False)
    command_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    rule_version: Mapped[int] = mapped_column(Integer, nullable=False)
    world_time: Mapped[int] = mapped_column(Integer, nullable=False)
    actor_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    causation_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    trace_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    commit_timestamp: Mapped[str | None] = mapped_column(Text, nullable=True)
    delta_json: Mapped[str] = mapped_column(Text, nullable=False)


class SnapshotRecord(Base):
    __tablename__ = "snapshots"

    snapshot_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    instance_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    branch_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    event_seq: Mapped[int] = mapped_column(Integer, nullable=False)
    schema_version: Mapped[int] = mapped_column(Integer, nullable=False)
    rule_version: Mapped[int] = mapped_column(Integer, nullable=False)
    created_world_time: Mapped[int] = mapped_column(Integer, nullable=False)
    content_ref: Mapped[str] = mapped_column(Text, nullable=False)
    state_json: Mapped[str] = mapped_column(Text, nullable=False)


class AuditTraceRecord(Base):
    __tablename__ = "audit_traces"

    trace_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    command_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    event_id: Mapped[str] = mapped_column(String(128), nullable=False)
    instance_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    branch_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    revision: Mapped[int] = mapped_column(Integer, nullable=False)
    rule_version: Mapped[int] = mapped_column(Integer, nullable=False)
    world_time: Mapped[int] = mapped_column(Integer, nullable=False)
    actor_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    commit_timestamp: Mapped[str | None] = mapped_column(Text, nullable=True)


class LineageNodeRecord(Base):
    __tablename__ = "lineage_nodes"

    node_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    kind: Mapped[str] = mapped_column(String(32), nullable=False)
    definition_ref: Mapped[str] = mapped_column(String(256), nullable=False, default="")
    inherited_history_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
    constitution_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    domain_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    runtime_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    evolution_policy: Mapped[str] = mapped_column(
        String(64), nullable=False, default="canonical_replay"
    )
    rights_ref: Mapped[str] = mapped_column(String(256), nullable=False, default="platform-default")
    provenance_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")


class LineageEdgeRecord(Base):
    __tablename__ = "lineage_edges"

    parent_node_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("lineage_nodes.node_id"), primary_key=True
    )
    child_node_id: Mapped[str] = mapped_column(
        String(128), ForeignKey("lineage_nodes.node_id"), primary_key=True
    )
    edge_kind: Mapped[str] = mapped_column(String(16), nullable=False, default="fork")
    origin_ref: Mapped[str | None] = mapped_column(String(256), nullable=True)
