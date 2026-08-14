"""Lineage API routes: read-only lineage queries (G31G)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Request
from wanxiang_substrate.lineage import LineageGraph

router = APIRouter(prefix="/lineage", tags=["lineage"])


def _graph(request: Request) -> LineageGraph:
    graph = getattr(request.app.state, "lineage_graph", None)
    if graph is None:
        graph = LineageGraph()
        request.app.state.lineage_graph = graph
    return graph


@router.get("/nodes/{node_id}/ancestors")
def ancestors(node_id: str, request: Request) -> dict[str, object]:
    try:
        return {"node_id": node_id, "ancestors": list(_graph(request).ancestors(node_id))}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/nodes/{node_id}/descendants")
def descendants(node_id: str, request: Request) -> dict[str, object]:
    try:
        return {"node_id": node_id, "descendants": list(_graph(request).descendants(node_id))}
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/nodes/{node_id}/promotion-origin")
def promotion_origin(node_id: str, request: Request) -> dict[str, object]:
    graph = _graph(request)
    origin = None
    for edge in graph.edges():
        if edge.child_node_id == node_id and edge.edge_kind == "promotion":
            origin = edge.origin_ref
            break
    if graph.get_node(node_id) is None:
        raise HTTPException(status_code=404, detail=f"lineage node {node_id!r} not found")
    return {"node_id": node_id, "promotion_origin": origin}
