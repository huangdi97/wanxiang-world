"""add lineage nodes and edges

Revision ID: 0003_add_lineage
Revises: 0002_add_event_seq_index
Create Date: 2026-08-15
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0003_add_lineage"
down_revision = "0002_add_event_seq_index"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "lineage_nodes",
        sa.Column("node_id", sa.String(length=128), nullable=False),
        sa.Column("kind", sa.String(length=32), nullable=False),
        sa.Column("definition_ref", sa.String(length=256), nullable=False, server_default=""),
        sa.Column("inherited_history_ref", sa.String(length=256), nullable=True),
        sa.Column("constitution_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("domain_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("runtime_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column(
            "evolution_policy",
            sa.String(length=64),
            nullable=False,
            server_default="canonical_replay",
        ),
        sa.Column(
            "rights_ref", sa.String(length=256), nullable=False, server_default="platform-default"
        ),
        sa.Column("provenance_json", sa.Text(), nullable=False, server_default="[]"),
        sa.PrimaryKeyConstraint("node_id"),
    )
    op.create_table(
        "lineage_edges",
        sa.Column("parent_node_id", sa.String(length=128), nullable=False),
        sa.Column("child_node_id", sa.String(length=128), nullable=False),
        sa.Column("edge_kind", sa.String(length=16), nullable=False, server_default="fork"),
        sa.Column("origin_ref", sa.String(length=256), nullable=True),
        sa.ForeignKeyConstraint(["parent_node_id"], ["lineage_nodes.node_id"]),
        sa.ForeignKeyConstraint(["child_node_id"], ["lineage_nodes.node_id"]),
        sa.PrimaryKeyConstraint("parent_node_id", "child_node_id"),
    )
    op.create_index("ix_lineage_edges_child", "lineage_edges", ["child_node_id"])


def downgrade() -> None:
    op.drop_index("ix_lineage_edges_child", table_name="lineage_edges")
    op.drop_table("lineage_edges")
    op.drop_table("lineage_nodes")
