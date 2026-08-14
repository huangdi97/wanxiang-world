"""World Lineage Graph ? first-class DAG of world definition/worldline
derivation relationships (G31B).

The graph stores derivation relationships ONLY (fork/promotion origins,
inherited history refs, constitution/domain/runtime/evolution versions,
rights/provenance). It never copies world history.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

LineageNodeKind = Literal["definition", "worldline", "derived_world"]
LineageEdgeKind = Literal["fork", "promotion"]


@dataclass(frozen=True, slots=True)
class LineageNode:
    """A node in the lineage graph (references only, no history)."""

    node_id: str
    kind: LineageNodeKind
    definition_ref: str = ""
    inherited_history_ref: str | None = None
    constitution_version: int = 1
    domain_version: int = 1
    runtime_version: int = 1
    evolution_policy: str = "canonical_replay"
    rights_ref: str = "platform-default"
    provenance: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.node_id:
            raise ContractError("lineage node id must be non-empty")
        if self.kind not in ("definition", "worldline", "derived_world"):
            raise ContractError(f"unknown lineage node kind {self.kind!r}")

    def to_primitive(self) -> dict[str, object]:
        return {
            "node_id": self.node_id,
            "kind": self.kind,
            "definition_ref": self.definition_ref,
            "inherited_history_ref": self.inherited_history_ref,
            "constitution_version": self.constitution_version,
            "domain_version": self.domain_version,
            "runtime_version": self.runtime_version,
            "evolution_policy": self.evolution_policy,
            "rights_ref": self.rights_ref,
            "provenance": list(self.provenance),
        }


@dataclass(frozen=True, slots=True)
class LineageEdge:
    """A directed derivation edge: parent -> child."""

    parent_node_id: str
    child_node_id: str
    edge_kind: LineageEdgeKind = "fork"
    origin_ref: str | None = None

    def __post_init__(self) -> None:
        if self.parent_node_id == self.child_node_id:
            raise ContractError("a lineage edge cannot point to itself")
        if self.edge_kind not in ("fork", "promotion"):
            raise ContractError(f"unknown lineage edge kind {self.edge_kind!r}")

    def to_primitive(self) -> dict[str, object]:
        return {
            "parent_node_id": self.parent_node_id,
            "child_node_id": self.child_node_id,
            "edge_kind": self.edge_kind,
            "origin_ref": self.origin_ref,
        }


class LineageGraph:
    """In-memory DAG of derivation relationships with cycle rejection."""

    def __init__(self) -> None:
        self._nodes: dict[str, LineageNode] = {}
        self._edges: dict[tuple[str, str], LineageEdge] = {}

    def add_node(self, node: LineageNode) -> None:
        if node.node_id in self._nodes:
            raise ContractError(f"lineage node {node.node_id!r} already exists")
        self._nodes[node.node_id] = node

    def get_node(self, node_id: str) -> LineageNode | None:
        return self._nodes.get(node_id)

    def require_node(self, node_id: str) -> LineageNode:
        node = self._nodes.get(node_id)
        if node is None:
            raise ContractError(f"lineage node {node_id!r} not found")
        return node

    def add_edge(self, edge: LineageEdge) -> None:
        self.require_node(edge.parent_node_id)
        self.require_node(edge.child_node_id)
        key = (edge.parent_node_id, edge.child_node_id)
        if key in self._edges:
            raise ContractError(f"lineage edge {key} already exists")
        # Cycle rejection: adding parent->child is invalid if the parent is
        # already reachable from the child (child can reach parent).
        if edge.parent_node_id in self.descendants(edge.child_node_id):
            raise ContractError(
                f"lineage cycle rejected: {edge.parent_node_id} is already a "
                f"descendant of {edge.child_node_id}"
            )
        self._edges[key] = edge

    def ancestors(self, node_id: str) -> tuple[str, ...]:
        self.require_node(node_id)
        seen: set[str] = set()
        stack = [p for (p, c) in self._edges if c == node_id]
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            stack.extend(p for (p, c) in self._edges if c == current)
        return tuple(sorted(seen))

    def descendants(self, node_id: str) -> tuple[str, ...]:
        self.require_node(node_id)
        seen: set[str] = set()
        stack = [c for (p, c) in self._edges if p == node_id]
        while stack:
            current = stack.pop()
            if current in seen:
                continue
            seen.add(current)
            stack.extend(c for (p, c) in self._edges if p == current)
        return tuple(sorted(seen))

    def common_ancestors(self, a: str, b: str) -> tuple[str, ...]:
        aa = set(self.ancestors(a))
        ab = set(self.ancestors(b))
        return tuple(sorted(aa & ab))

    def nodes(self) -> tuple[LineageNode, ...]:
        return tuple(sorted(self._nodes.values(), key=lambda n: n.node_id))

    def edges(self) -> tuple[LineageEdge, ...]:
        return tuple(
            sorted(self._edges.values(), key=lambda e: (e.parent_node_id, e.child_node_id))
        )
