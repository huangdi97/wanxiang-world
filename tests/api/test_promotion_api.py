"""G33F: Lineage & Promotion API/Studio minimal surface."""

from __future__ import annotations

import json
import pathlib
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient
from wanxiang_api.app import create_app
from wanxiang_api.studio_service import StudioRequiresAdmin, StudioService
from wanxiang_substrate.lineage import LineageEdge, LineageGraph, LineageNode

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _graph() -> LineageGraph:
    graph = LineageGraph()
    graph.add_node(LineageNode(node_id="wd_parent", kind="definition"))
    graph.add_node(LineageNode(node_id="wl_rc", kind="worldline"))
    graph.add_node(LineageNode(node_id="wd_derived", kind="derived_world"))
    graph.add_edge(LineageEdge("wd_parent", "wl_rc", edge_kind="fork"))
    graph.add_edge(LineageEdge("wl_rc", "wd_derived", edge_kind="promotion"))
    return graph


@pytest.mark.e2e
def test_unauthorized_promote_is_rejected() -> None:
    app = create_app(lineage_graph=_graph())
    client: Any = TestClient(app)
    with client:
        resp = client.post(
            "/lineage/promotions",
            json={
                "source_worldline": "wl_rc",
                "target_world_definition": "wd_derived",
                "candidate": "cand_1",
            },
        )
        assert resp.status_code == 403  # no admin permission


@pytest.mark.e2e
def test_admin_promote_goes_through_backend_authority() -> None:
    app = create_app(lineage_graph=_graph())
    app.state.studio_admin = True
    client: Any = TestClient(app)
    with client:
        resp = client.post(
            "/lineage/promotions",
            json={
                "source_worldline": "wl_rc",
                "target_world_definition": "wd_derived",
                "candidate": "cand_1",
            },
        )
        assert resp.status_code == 200
        body = cast(dict[str, Any], resp.json())
        assert body["status"] == "pending_approval"
        assert body["promotion_use_case"]["candidate"] == "cand_1"


@pytest.mark.e2e
def test_lineage_compare_endpoint() -> None:
    app = create_app(lineage_graph=_graph())
    client: Any = TestClient(app)
    with client:
        resp = client.get("/lineage/compare", params={"node_a": "wd_derived", "node_b": "wl_rc"})
        assert resp.status_code == 200
        body = cast(dict[str, Any], resp.json())
        assert set(body["common_ancestors"]) == {"wd_parent"}


@pytest.mark.unit
def test_studio_ui_action_routes_through_backend_authority() -> None:
    studio = StudioService(cast(Any, None), admin=False)
    with pytest.raises(StudioRequiresAdmin):
        studio.promote("wl_rc", "wd_derived", "cand_1")
    admin_studio = StudioService(cast(Any, None), admin=True)
    result = admin_studio.promote("wl_rc", "wd_derived", "cand_1")
    assert result["status"] == "pending_approval"
    # Studio lineage diff is a read-only projection.
    diff = admin_studio.lineage_compare(_graph(), "wd_derived", "wl_rc")
    common = diff["common_ancestors"]
    assert isinstance(common, list)
    assert common == ["wd_parent"]


@pytest.mark.e2e
def test_sdk_contract_includes_promotion_routes() -> None:
    contract = json.loads(
        (ROOT / "packages/sdk_ts/src/openapi-contract.json").read_text(encoding="utf-8")
    )
    paths = set(contract["paths"])
    assert "/lineage/promotions" in paths
    assert "/lineage/promotion-candidates" in paths
    assert "/lineage/compare" in paths
