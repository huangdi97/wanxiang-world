"""Lineage & Promotion API routes (G33F): thin, permission-controlled."""

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


def _require_admin(request: Request) -> None:
    if not getattr(request.app.state, "studio_admin", False):
        raise HTTPException(status_code=403, detail="promotion requires studio admin permission")


@router.get("/promotion-candidates")
def promotion_candidates(request: Request) -> dict[str, object]:
    candidates = getattr(request.app.state, "promotion_candidates", ())
    return {"candidates": list(candidates)}


@router.post("/promotions")
def submit_promotion(payload: dict[str, object], request: Request) -> dict[str, object]:
    """Submit a promotion use case through the backend (admin-gated)."""
    _require_admin(request)
    candidate = {
        "source_worldline": payload.get("source_worldline", ""),
        "target_world_definition": payload.get("target_world_definition", ""),
        "candidate": payload.get("candidate", ""),
    }
    # The UI action only creates a promotion use case here; the pipeline (G33B)
    # + approval (G33E) run on the backend before any release.
    return {"promotion_use_case": candidate, "status": "pending_approval"}


@router.get("/compare")
def lineage_compare(node_a: str, node_b: str, request: Request) -> dict[str, object]:
    graph = _graph(request)
    try:
        aa = set(graph.ancestors(node_a))
        ab = set(graph.ancestors(node_b))
        da = set(graph.descendants(node_a))
        db = set(graph.descendants(node_b))
    except Exception as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {
        "node_a": node_a,
        "node_b": node_b,
        "common_ancestors": sorted(aa & ab),
        "only_a": sorted((aa | da) - (ab | db)),
        "only_b": sorted((ab | db) - (aa | da)),
    }
