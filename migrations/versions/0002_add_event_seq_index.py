"""add ordered stream index on events

Revision ID: 0002_add_event_seq_index
Revises: 0001_initial
Create Date: 2026-08-12
"""

from __future__ import annotations

from alembic import op

revision = "0002_add_event_seq_index"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        "ix_events_stream_ordered",
        "events",
        ["instance_id", "branch_id", "event_seq"],
    )


def downgrade() -> None:
    op.drop_index("ix_events_stream_ordered", table_name="events")
