"""Lineage repository over SQLite/PostgreSQL (G31C).

Persists the world-definition/worldline lineage graph with the minimal new
tables (`lineage_nodes`, `lineage_edges`). Branch forks are NOT duplicated:
they already live in the `branches` table (parent_branch_id / fork_revision /
fork_event_seq); `branch_lineage_from_branches` derives branch-level lineage
from that existing table on demand.
"""

from __future__ import annotations

import json

from sqlalchemy import select
from sqlalchemy.orm import Session, sessionmaker
from wanxiang_domain.lineage import LineageEdge, LineageGraph, LineageNode

from wanxiang_persistence.database import session_scope
from wanxiang_persistence.models import LineageEdgeRecord, LineageNodeRecord


def _node_to_record(node: LineageNode) -> LineageNodeRecord:
    return LineageNodeRecord(
        node_id=node.node_id,
        kind=node.kind,
        definition_ref=node.definition_ref,
        inherited_history_ref=node.inherited_history_ref,
        constitution_version=node.constitution_version,
        domain_version=node.domain_version,
        runtime_version=node.runtime_version,
        evolution_policy=node.evolution_policy,
        rights_ref=node.rights_ref,
        provenance_json=json.dumps(list(node.provenance), sort_keys=True),
    )


def _record_to_node(record: LineageNodeRecord) -> LineageNode:
    return LineageNode(
        node_id=record.node_id,
        kind=record.kind,  # type: ignore[arg-type]
        definition_ref=record.definition_ref,
        inherited_history_ref=record.inherited_history_ref,
        constitution_version=record.constitution_version,
        domain_version=record.domain_version,
        runtime_version=record.runtime_version,
        evolution_policy=record.evolution_policy,
        rights_ref=record.rights_ref,
        provenance=tuple(json.loads(record.provenance_json or "[]")),
    )


def _edge_to_record(edge: LineageEdge) -> LineageEdgeRecord:
    return LineageEdgeRecord(
        parent_node_id=edge.parent_node_id,
        child_node_id=edge.child_node_id,
        edge_kind=edge.edge_kind,
        origin_ref=edge.origin_ref,
    )


def _record_to_edge(record: LineageEdgeRecord) -> LineageEdge:
    return LineageEdge(
        parent_node_id=record.parent_node_id,
        child_node_id=record.child_node_id,
        edge_kind=record.edge_kind,  # type: ignore[arg-type]
        origin_ref=record.origin_ref,
    )


class LineageRepository:
    """SQLAlchemy repository for the lineage graph."""

    def __init__(self, session_factory: sessionmaker[Session]) -> None:
        self._session_factory = session_factory

    def save_node(self, node: LineageNode) -> None:
        with session_scope(self._session_factory) as session:
            session.merge(_node_to_record(node))

    def save_edge(self, edge: LineageEdge) -> None:
        with session_scope(self._session_factory) as session:
            session.merge(_edge_to_record(edge))

    def load_graph(self) -> LineageGraph:
        graph = LineageGraph()
        with session_scope(self._session_factory) as session:
            for record in session.scalars(
                select(LineageNodeRecord).order_by(LineageNodeRecord.node_id)
            ):
                graph.add_node(_record_to_node(record))
            for record in session.scalars(
                select(LineageEdgeRecord).order_by(
                    LineageEdgeRecord.parent_node_id, LineageEdgeRecord.child_node_id
                )
            ):
                graph.add_edge(_record_to_edge(record))
        return graph


def branch_lineage_from_branches(branches: tuple[object, ...], graph: LineageGraph) -> LineageGraph:
    """Derive branch-fork lineage edges from the EXISTING branches table.

    Each branch with a parent_branch_id yields a fork edge in the graph; no
    history is copied and no second branch system is created.
    """
    for branch in branches:
        ancestry = getattr(branch, "ancestry", None)
        parent = getattr(ancestry, "parent_branch_id", None) if ancestry is not None else None
        if parent is None:
            continue
        child_id = getattr(branch, "branch_id", None)
        if child_id is None:
            continue
        try:
            graph.add_edge(
                LineageEdge(
                    parent_node_id=parent.value,
                    child_node_id=child_id.value,
                    edge_kind="fork",
                    origin_ref=f"branch://{getattr(branch, 'instance_id', '')}/{child_id.value}",
                )
            )
        except Exception:
            # Duplicate/cycle derivations from the table are ignored (data model
            # guarantees cycle-free branch history by construction).
            continue
    return graph
