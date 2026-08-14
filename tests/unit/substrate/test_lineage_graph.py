"""G31B: World Lineage Graph data model."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.lineage import LineageEdge, LineageGraph, LineageNode


def _node(node_id: str, kind: str = "worldline") -> LineageNode:
    return LineageNode(
        node_id=node_id,
        kind=kind,  # type: ignore[arg-type]
        definition_ref=f"def:{node_id}",
        constitution_version=1,
        domain_version=1,
        runtime_version=1,
        evolution_policy="canonical_replay",
        provenance=("ref://origin",),
    )


@pytest.mark.unit
def test_tree_fixture_queries() -> None:
    graph = LineageGraph()
    for nid in ("root", "a", "b", "a1", "a2"):
        graph.add_node(_node(nid))
    graph.add_edge(LineageEdge("root", "a", edge_kind="fork"))
    graph.add_edge(LineageEdge("root", "b", edge_kind="fork"))
    graph.add_edge(LineageEdge("a", "a1", edge_kind="fork"))
    graph.add_edge(LineageEdge("a", "a2", edge_kind="promotion", origin_ref="cand_1"))
    assert graph.ancestors("a1") == ("a", "root")
    assert graph.descendants("root") == ("a", "a1", "a2", "b")
    assert graph.common_ancestors("a1", "b") == ("root",)
    assert graph.common_ancestors("a1", "a2") == ("a", "root")


@pytest.mark.unit
def test_dag_fixture_queries() -> None:
    graph = LineageGraph()
    for nid in ("root", "x", "y", "z", "w"):
        graph.add_node(_node(nid))
    graph.add_edge(LineageEdge("root", "x"))
    graph.add_edge(LineageEdge("root", "y"))
    graph.add_edge(LineageEdge("x", "z"))
    graph.add_edge(LineageEdge("y", "z"))  # diamond: z has two parents
    graph.add_edge(LineageEdge("z", "w"))
    assert graph.ancestors("w") == ("root", "x", "y", "z")
    assert graph.common_ancestors("x", "y") == ("root",)
    assert graph.common_ancestors("z", "w") == ("root", "x", "y")


@pytest.mark.unit
def test_cycle_insertion_is_rejected() -> None:
    graph = LineageGraph()
    for nid in ("a", "b", "c"):
        graph.add_node(_node(nid))
    graph.add_edge(LineageEdge("a", "b"))
    graph.add_edge(LineageEdge("b", "c"))
    with pytest.raises(ContractError):
        graph.add_edge(LineageEdge("c", "a"))  # would close the cycle
    # self-edge rejected too
    with pytest.raises(ContractError):
        graph.add_edge(LineageEdge("a", "a"))


@pytest.mark.unit
def test_duplicate_node_and_edge_rejected() -> None:
    graph = LineageGraph()
    graph.add_node(_node("a"))
    with pytest.raises(ContractError):
        graph.add_node(_node("a"))
    graph.add_node(_node("b"))
    graph.add_edge(LineageEdge("a", "b"))
    with pytest.raises(ContractError):
        graph.add_edge(LineageEdge("a", "b"))


@pytest.mark.unit
def test_node_carries_versions_rights_provenance() -> None:
    node = LineageNode(
        node_id="wd_derived",
        kind="derived_world",
        definition_ref="pack://derived@1.0.0",
        inherited_history_ref="wl_parent:5",
        constitution_version=2,
        domain_version=3,
        runtime_version=2,
        evolution_policy="living_open",
        rights_ref="rights:cc0",
        provenance=("ref://source", "ref://review"),
    )
    prim = node.to_primitive()
    assert prim["inherited_history_ref"] == "wl_parent:5"
    assert prim["constitution_version"] == 2
    assert prim["evolution_policy"] == "living_open"
    assert prim["rights_ref"] == "rights:cc0"
    assert prim["provenance"] == ["ref://source", "ref://review"]
