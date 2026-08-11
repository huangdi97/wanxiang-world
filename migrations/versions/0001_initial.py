"""initial schema for P1 persistence

Revision ID: 0001_initial
Revises:
Create Date: 2026-08-12
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "world_instances",
        sa.Column("instance_id", sa.String(length=128), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("rule_version", sa.Integer(), nullable=False),
        sa.Column("created_world_time", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("instance_id"),
    )
    op.create_table(
        "branches",
        sa.Column("branch_id", sa.String(length=128), nullable=False),
        sa.Column("instance_id", sa.String(length=128), nullable=False),
        sa.Column("parent_branch_id", sa.String(length=128), nullable=True),
        sa.Column("fork_revision", sa.Integer(), nullable=True),
        sa.Column("fork_event_seq", sa.Integer(), nullable=True),
        sa.Column("fork_snapshot_ref", sa.Text(), nullable=True),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("rule_version", sa.Integer(), nullable=False),
        sa.Column("snapshot_ref", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["instance_id"], ["world_instances.instance_id"]),
        sa.PrimaryKeyConstraint("branch_id"),
    )
    op.create_index("ix_branches_instance_id", "branches", ["instance_id"])
    op.create_table(
        "events",
        sa.Column("event_id", sa.String(length=128), nullable=False),
        sa.Column("instance_id", sa.String(length=128), nullable=False),
        sa.Column("branch_id", sa.String(length=128), nullable=False),
        sa.Column("event_seq", sa.Integer(), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("command_id", sa.String(length=128), nullable=False),
        sa.Column("rule_version", sa.Integer(), nullable=False),
        sa.Column("world_time", sa.Integer(), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=True),
        sa.Column("causation_id", sa.String(length=128), nullable=True),
        sa.Column("correlation_id", sa.String(length=128), nullable=True),
        sa.Column("trace_id", sa.String(length=128), nullable=True),
        sa.Column("commit_timestamp", sa.Text(), nullable=True),
        sa.Column("delta_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("event_id"),
        sa.UniqueConstraint("command_id"),
        sa.UniqueConstraint("instance_id", "branch_id", "event_seq", name="uq_events_stream_seq"),
    )
    op.create_index("ix_events_instance_id", "events", ["instance_id"])
    op.create_index("ix_events_branch_id", "events", ["branch_id"])
    op.create_table(
        "snapshots",
        sa.Column("snapshot_id", sa.String(length=128), nullable=False),
        sa.Column("instance_id", sa.String(length=128), nullable=False),
        sa.Column("branch_id", sa.String(length=128), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("event_seq", sa.Integer(), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False),
        sa.Column("rule_version", sa.Integer(), nullable=False),
        sa.Column("created_world_time", sa.Integer(), nullable=False),
        sa.Column("content_ref", sa.Text(), nullable=False),
        sa.Column("state_json", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("snapshot_id"),
    )
    op.create_index("ix_snapshots_instance_id", "snapshots", ["instance_id"])
    op.create_index("ix_snapshots_branch_id", "snapshots", ["branch_id"])
    op.create_table(
        "audit_traces",
        sa.Column("trace_id", sa.String(length=128), nullable=False),
        sa.Column("command_id", sa.String(length=128), nullable=False),
        sa.Column("event_id", sa.String(length=128), nullable=False),
        sa.Column("instance_id", sa.String(length=128), nullable=False),
        sa.Column("branch_id", sa.String(length=128), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("rule_version", sa.Integer(), nullable=False),
        sa.Column("world_time", sa.Integer(), nullable=False),
        sa.Column("actor_id", sa.String(length=128), nullable=True),
        sa.Column("correlation_id", sa.String(length=128), nullable=True),
        sa.Column("commit_timestamp", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("trace_id"),
    )
    op.create_index("ix_audit_traces_instance_id", "audit_traces", ["instance_id"])
    op.create_index("ix_audit_traces_branch_id", "audit_traces", ["branch_id"])
    op.create_index("ix_audit_traces_command_id", "audit_traces", ["command_id"])


def downgrade() -> None:
    op.drop_table("audit_traces")
    op.drop_table("snapshots")
    op.drop_table("events")
    op.drop_table("branches")
    op.drop_table("world_instances")
