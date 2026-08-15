"""G34E: API/SDK client compatibility (constitution endpoint + old clients intact)."""

from __future__ import annotations

import json
import pathlib
from typing import Any, cast

import pytest
from fastapi.testclient import TestClient
from wanxiang_api.app import create_app

ROOT = pathlib.Path(__file__).resolve().parents[2]


@pytest.mark.e2e
def test_constitution_endpoint_returns_manifest() -> None:
    app = create_app()
    client: Any = TestClient(app)
    with client:
        resp = client.get("/constitutions/con_platform_root")
        assert resp.status_code == 200
        body = cast(dict[str, Any], resp.json())
        assert body["constitution_id"] == "con_platform_root"
        assert body["name"]
        assert "root_constraints" in body
        assert client.get("/constitutions/missing").status_code == 404


@pytest.mark.e2e
def test_openapi_includes_constitution_and_keeps_old_endpoints() -> None:
    contract = json.loads(
        (ROOT / "packages/sdk_ts/src/openapi-contract.json").read_text(encoding="utf-8")
    )
    paths = set(contract["paths"])
    # New v5.2 resource present.
    assert "/constitutions/{constitution_id}" in paths
    assert "/lineage/promotions" in paths
    # Old world/branch endpoints preserved (no breaking removal).
    for old in (
        "/worlds",
        "/worlds/{instance_id}",
        "/worlds/{instance_id}/state",
        "/worlds/{instance_id}/events",
        "/worlds/{instance_id}/actions",
        "/worlds/{instance_id}/branches",
        "/worlds/{instance_id}/branches/compare",
        "/worlds/{instance_id}/checkpoint",
        "/worlds/{instance_id}/replay",
        "/healthz",
    ):
        assert old in paths, f"old endpoint removed: {old}"


@pytest.mark.e2e
def test_old_client_smoke_world_actions_still_work(persist_db_path: pathlib.Path) -> None:
    """Old world/branch clients keep working (no breaking change)."""
    from typing import cast as _cast

    from tests.conftest import upgrade_db
    from wanxiang_api.app import build_runtime
    from wanxiang_api.routes import reset_action_rate_limiter

    upgrade_db(persist_db_path)
    reset_action_rate_limiter()  # isolate this test from shared rate-limit state
    app = create_app(build_runtime(f"sqlite:///{persist_db_path.as_posix()}"))
    client: Any = TestClient(app)
    with client:
        world = _cast(dict[str, Any], client.post("/worlds", json={}).json())
        instance = world["instance_id"]
        branch = world["root_branch_id"]
        action = _cast(
            dict[str, Any],
            client.post(
                f"/worlds/{instance}/actions",
                json={
                    "branch_id": branch,
                    "expected_revision": 0,
                    "action_type": "create_entity",
                    "payload": {"entity_id": "ent_g34e", "count": 1},
                },
            ).json(),
        )
        assert action["event"] is not None
        state = _cast(
            dict[str, Any],
            client.get(f"/worlds/{instance}/state", params={"branch_id": branch}).json(),
        )
        entities = _cast(list[dict[str, Any]], state["state"]["entities"])
        assert any(str(e.get("id")) == "ent_g34e" for e in entities)
