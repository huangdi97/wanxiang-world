"""add world metadata (definition/constitution/evolution) + lineage kind index

Revision ID: 0004_add_world_metadata
Revises: 0003_add_lineage
Create Date: 2026-08-15
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0004_add_world_metadata"
down_revision = "0003_add_lineage"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "world_instances",
        sa.Column("definition_ref", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "world_instances",
        sa.Column("constitution_ref", sa.String(length=256), nullable=True),
    )
    op.add_column(
        "world_instances",
        sa.Column("evolution_policy_ref", sa.String(length=64), nullable=True),
    )
    op.create_index("ix_lineage_nodes_kind", "lineage_nodes", ["kind"])


def downgrade() -> None:
    op.drop_index("ix_lineage_nodes_kind", table_name="lineage_nodes")
    op.drop_column("world_instances", "evolution_policy_ref")
    op.drop_column("world_instances", "constitution_ref")
    op.drop_column("world_instances", "definition_ref")
