"""G31G: Lineage API contract tests (read-only, no authority in UI)."""

from __future__ import annotations

import json
import pathlib
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient
from wanxiang_api.app import create_app
from wanxiang_substrate.lineage import LineageEdge, LineageGraph, LineageNode

ROOT = pathlib.Path(__file__).resolve().parents[2]


def _graph() -> LineageGraph:
    graph = LineageGraph()
    graph.add_node(LineageNode(node_id="wd_root", kind="definition"))
    graph.add_node(LineageNode(node_id="wl_child", kind="worldline"))
    graph.add_node(LineageNode(node_id="wd_derived", kind="derived_world"))
    graph.add_edge(LineageEdge("wd_root", "wl_child", edge_kind="fork"))
    graph.add_edge(
        LineageEdge("wl_child", "wd_derived", edge_kind="promotion", origin_ref="cand_001")
    )
    return graph


@pytest.mark.e2e
def test_lineage_api_queries() -> None:
    app = create_app(lineage_graph=_graph())
    client: Any = TestClient(app)
    with client:
        ancestors = cast(
            dict[str, object],
            client.get("/lineage/nodes/wl_child/ancestors").json(),
        )
        assert ancestors["ancestors"] == ["wd_root"]
        descendants = cast(
            dict[str, object],
            client.get("/lineage/nodes/wd_root/descendants").json(),
        )
        assert descendants["descendants"] == ["wd_derived", "wl_child"]  # sorted
        origin = cast(
            dict[str, object],
            client.get("/lineage/nodes/wd_derived/promotion-origin").json(),
        )
        assert origin["promotion_origin"] == "cand_001"
        assert client.get("/lineage/nodes/missing/ancestors").status_code == 404


@pytest.mark.e2e
def test_lineage_api_is_read_only() -> None:
    """Lineage QUERY endpoints are GET-only; the promotion ACTION is admin-gated POST."""
    contract = json.loads(
        (ROOT / "packages/sdk_ts/src/openapi-contract.json").read_text(encoding="utf-8")
    )
    lineage_paths = {
        path: item for path, item in contract["paths"].items() if path.startswith("/lineage")
    }
    assert lineage_paths
    for path, item in lineage_paths.items():
        if path == "/lineage/promotions":
            assert set(item) == {"post"}, f"promotion action must be POST: {path}"
        else:
            assert set(item) == {"get"}, f"lineage query route must be GET-only: {path}"
