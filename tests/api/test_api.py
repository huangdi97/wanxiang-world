"""GOAL_01F: FastAPI transport e2e tests (thin routes over the authoritative slice)."""

from __future__ import annotations

import pathlib
from typing import Any

import pytest
from tests.conftest import upgrade_db
from wanxiang_api.app import build_runtime, create_app


@pytest.fixture
def client(persist_db_path: pathlib.Path) -> Any:
    from fastapi.testclient import TestClient

    upgrade_db(persist_db_path)
    runtime = build_runtime(f"sqlite:///{persist_db_path.as_posix()}")
    app = create_app(runtime)
    with TestClient(app) as test_client:
        yield test_client


def _create_world(client: Any) -> dict[str, Any]:
    response = client.post("/worlds", json={"instance_id": "wld_api"})
    assert response.status_code == 201
    return response.json()


def _submit(
    client: Any, instance: str, branch: str, revision: int, **payload: object
) -> dict[str, object]:
    body = {
        "branch_id": branch,
        "expected_revision": revision,
        "action_type": payload.pop("action_type"),
        "payload": payload,
    }
    return client.post(f"/worlds/{instance}/actions", json=body).json()


def _str(value: object, name: str) -> str:
    assert isinstance(value, str), name
    return value


@pytest.mark.e2e
def test_healthz(client: Any) -> None:
    assert client.get("/healthz").json() == {"status": "ok"}


@pytest.mark.e2e
def test_create_world_and_submit_action(client: Any) -> None:
    world = _create_world(client)
    instance = _str(world["instance_id"], "instance_id")
    branch = _str(world["root_branch_id"], "root_branch_id")
    result = client.post(
        f"/worlds/{instance}/actions",
        json={
            "branch_id": branch,
            "expected_revision": 0,
            "action_type": "create_entity",
            "payload": {"entity_id": "alice", "count": 10},
            "command_id": "cmd_api_1",
        },
    ).json()
    assert result["revision"] == 1
    assert result["event"]["event_seq"] == 1
    assert result["state"]["entities"][0]["id"] == "alice"


@pytest.mark.e2e
def test_duplicate_action_is_idempotent(client: Any) -> None:
    world = _create_world(client)
    instance = _str(world["instance_id"], "instance_id")
    branch = _str(world["root_branch_id"], "root_branch_id")
    body = {
        "branch_id": branch,
        "expected_revision": 0,
        "action_type": "create_entity",
        "payload": {"entity_id": "alice", "count": 10},
        "command_id": "cmd_dup_api",
    }
    first = client.post(f"/worlds/{instance}/actions", json=body).json()
    second = client.post(f"/worlds/{instance}/actions", json=body).json()
    assert second["duplicate"] is True
    assert second["event"]["event_id"] == first["event"]["event_id"]


@pytest.mark.e2e
def test_stale_revision_returns_409(client: Any) -> None:
    world = _create_world(client)
    instance = _str(world["instance_id"], "instance_id")
    branch = _str(world["root_branch_id"], "root_branch_id")
    body = {
        "branch_id": branch,
        "expected_revision": 0,
        "action_type": "create_entity",
        "payload": {"entity_id": "alice", "count": 10},
        "command_id": "cmd_stale_api",
    }
    client.post(f"/worlds/{instance}/actions", json=body)
    response = client.post(
        f"/worlds/{instance}/actions",
        json={**body, "expected_revision": 0, "command_id": "cmd_stale2"},
    )
    assert response.status_code == 409
    assert response.json()["code"] == "stale_revision"


@pytest.mark.e2e
def test_invalid_action_returns_422(client: Any) -> None:
    world = _create_world(client)
    instance = _str(world["instance_id"], "instance_id")
    branch = _str(world["root_branch_id"], "root_branch_id")
    body = {
        "branch_id": branch,
        "expected_revision": 0,
        "action_type": "transfer_resource",
        "payload": {"source_id": "alice", "target_id": "ghost", "amount": 1},
        "command_id": "cmd_invalid_api",
    }
    response = client.post(f"/worlds/{instance}/actions", json=body)
    assert response.status_code == 422
    assert response.json()["code"] == "validation_rejected"


@pytest.mark.e2e
def test_checkpoint_replay_and_branch_flow(client: Any) -> None:
    world = _create_world(client)
    instance = _str(world["instance_id"], "instance_id")
    branch = _str(world["root_branch_id"], "root_branch_id")
    _submit(client, instance, branch, 0, action_type="create_entity", entity_id="alice", count=10)
    _submit(client, instance, branch, 1, action_type="create_entity", entity_id="bob", count=0)
    checkpoint = client.post(f"/worlds/{instance}/checkpoint", params={"branch_id": branch}).json()
    assert checkpoint["revision"] == 2
    _submit(
        client,
        instance,
        branch,
        2,
        action_type="transfer_resource",
        source_id="alice",
        target_id="bob",
        amount=3,
    )
    replay = client.post(f"/worlds/{instance}/replay", params={"branch_id": branch}).json()
    assert replay["used_snapshot"] is True
    assert replay["revision"] == 3

    branch_resp = client.post(f"/worlds/{instance}/branches", json={"parent_branch_id": branch})
    assert branch_resp.status_code == 201
    child = branch_resp.json()
    assert child["parent_branch_id"] == branch
    assert child["fork_revision"] == 3

    state = client.get(f"/worlds/{instance}/state", params={"branch_id": branch}).json()
    assert state["revision"] == 3
    events = client.get(f"/worlds/{instance}/events", params={"branch_id": branch}).json()
    assert len(events["events"]) == 3


@pytest.mark.e2e
def test_openapi_contains_world_paths(client: Any) -> None:
    response = client.get("/openapi.json")
    spec = response.json()
    paths = spec["paths"]
    assert "/worlds" in paths
    assert "/worlds/{instance_id}/actions" in paths
    assert "/worlds/{instance_id}/state" in paths
