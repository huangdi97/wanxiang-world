"""G88H API/Studio shared playable product path."""

from __future__ import annotations

from typing import Any, cast

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app


def _source() -> dict[str, object]:
    return {
        "source_id": "api_playable_source",
        "kind": "text",
        "content": (
            "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
            "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
            "relationship: Alice -> Bob\nrule: visitors register\n"
        ),
        "stage": "E3",
        "rights_approved": True,
        "access": "private",
        "private_analysis_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": False,
        "training_allowed": False,
    }


def test_api_and_studio_share_playable_backend() -> None:
    app = create_app(build_reference_runtime())
    client: Any = TestClient(app)
    job_id = "job_api_playable"
    one_click = client.post(
        "/studio/one-click",
        json={"job_id": job_id, "profile": "book", "sources": [_source()]},
    )
    assert one_click.status_code == 201
    profile_response = client.post(
        f"/studio/jobs/{job_id}/playable-profile",
        json={"owner_id": "alice", "visibility": "public", "display_name": "API World"},
    )
    assert profile_response.status_code == 200
    profile = cast(dict[str, Any], profile_response.json()["profile"])
    profile_id = str(profile["profile_id"])
    character = client.post(
        "/experience/characters",
        headers={"X-Wanxiang-User": "alice"},
        json={
            "display_name": "Alice",
            "character_id": "ent_alice",
            "compatible_profile_ids": [profile_id],
        },
    )
    assert character.status_code == 201
    entered = client.post(
        f"/experience/worlds/{profile_id}/enter",
        headers={"X-Wanxiang-User": "alice"},
        json={"mode": "embodiment", "session_id": "session_api", "character_id": "ent_alice"},
    )
    assert entered.status_code == 200
    instance = cast(dict[str, Any], entered.json()["instance"])
    instance_id = str(instance["instance_id"])
    action = client.post(
        f"/experience/instances/{instance_id}/action",
        headers={"X-Wanxiang-User": "alice"},
        json={"text": "set status to awake"},
    )
    assert action.status_code == 200
    action_body = cast(dict[str, Any], action.json())
    assert action_body["proposal"]["status"] == "proposed"
    assert action_body["diff"]["no_change"] is False
    assert action_body["event_id"]
    left = client.post(
        f"/experience/instances/{instance_id}/leave",
        headers={"X-Wanxiang-User": "alice"},
    )
    assert left.status_code == 200
    continued = client.post(
        f"/experience/instances/{instance_id}/continue",
        headers={"X-Wanxiang-User": "alice"},
    )
    assert continued.status_code == 200
    assert continued.json()["instance"]["instance_id"] == instance_id
    plaza = client.get("/experience/plaza", headers={"X-Wanxiang-User": "alice"})
    assert plaza.status_code == 200
    assert plaza.json()["continue"]["instance_id"] == instance_id
    ui = client.get("/studio/ui")
    assert ui.status_code == 200
    assert "World Plaza" in ui.text
    assert "enterPlayable" in ui.text
    assert "freeAction" in ui.text
    denied = client.get(f"/experience/instances/{instance_id}", headers={"X-Wanxiang-User": "bob"})
    assert denied.status_code == 404
