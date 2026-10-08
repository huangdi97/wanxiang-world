"""M95 product-chain evidence tests; no scripted result counts as human UX."""

from __future__ import annotations

import json
from typing import Any, cast

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app


def _source() -> dict[str, object]:
    return {
        "source_id": "m95_evidence_source",
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


def _client() -> Any:
    return TestClient(create_app(build_reference_runtime()))


def test_action_evidence_links_commit_path_and_redacts_input() -> None:
    client: Any = _client()
    assert (
        client.post(
            "/studio/one-click",
            json={"job_id": "m95_evidence_job", "profile": "book", "sources": [_source()]},
        ).status_code
        == 201
    )
    profile_response = client.post(
        "/studio/jobs/m95_evidence_job/playable-profile",
        json={"owner_id": "player-a", "visibility": "public", "display_name": "Evidence World"},
    )
    profile = cast(dict[str, Any], profile_response.json()["profile"])
    profile_id = str(profile["profile_id"])
    character = client.post(
        "/experience/characters",
        headers={"X-Wanxiang-User": "player-a"},
        json={
            "display_name": "Alice",
            "character_id": "ent_alice",
            "compatible_profile_ids": [profile_id],
        },
    )
    assert character.status_code == 201
    entered = client.post(
        f"/experience/worlds/{profile_id}/enter",
        headers={"X-Wanxiang-User": "player-a"},
        json={"mode": "embodiment", "session_id": "m95_session", "character_id": "ent_alice"},
    )
    instance_id = str(entered.json()["instance"]["instance_id"])
    action_text = "set status to awake"
    action = client.post(
        f"/experience/instances/{instance_id}/action",
        headers={"X-Wanxiang-User": "player-a"},
        json={"text": action_text},
    )
    assert action.status_code == 200
    body = cast(dict[str, Any], action.json())
    evidence = cast(dict[str, Any], body["evidence"])
    assert evidence["stages"] == [
        "input",
        "proposal",
        "validate_resolve",
        "commit_authority",
        "state_diff",
        "projection",
    ]
    assert evidence["proposal_status"] == "proposed"
    assert evidence["event_id"] == body["event_id"]
    assert evidence["state_diff_event_id"] == body["diff"]["event_id"]
    assert evidence["after_revision"] == body["revision"]
    assert evidence["before_state_hash"] != evidence["after_state_hash"]
    assert action_text not in json.dumps(evidence, ensure_ascii=False)
    assert "source_path" not in evidence
    assert "source_digest" not in evidence
    assert evidence["redactions"] == [
        "raw_input",
        "proposal_payload",
        "session_id",
        "actor_id",
        "source_path",
        "source_digest",
    ]


def test_product_route_keeps_leave_continue_identity_after_commit() -> None:
    client: Any = _client()
    assert (
        client.post(
            "/studio/one-click",
            json={"job_id": "m95_continuity_job", "profile": "book", "sources": [_source()]},
        ).status_code
        == 201
    )
    profile = cast(
        dict[str, Any],
        client.post(
            "/studio/jobs/m95_continuity_job/playable-profile",
            json={"owner_id": "player-b", "visibility": "public"},
        ).json()["profile"],
    )
    profile_id = str(profile["profile_id"])
    assert (
        client.post(
            "/experience/characters",
            headers={"X-Wanxiang-User": "player-b"},
            json={
                "display_name": "Alice",
                "character_id": "ent_alice",
                "compatible_profile_ids": [profile_id],
            },
        ).status_code
        == 201
    )
    entered = client.post(
        f"/experience/worlds/{profile_id}/enter",
        headers={"X-Wanxiang-User": "player-b"},
        json={"mode": "embodiment", "session_id": "m95_b_session", "character_id": "ent_alice"},
    )
    instance_id = str(entered.json()["instance"]["instance_id"])
    action = client.post(
        f"/experience/instances/{instance_id}/action",
        headers={"X-Wanxiang-User": "player-b"},
        json={"text": "set status to awake"},
    )
    committed_hash = action.json()["state_hash"]
    assert (
        client.post(
            f"/experience/instances/{instance_id}/leave", headers={"X-Wanxiang-User": "player-b"}
        ).json()["status"]
        == "left"
    )
    continued = client.post(
        f"/experience/instances/{instance_id}/continue", headers={"X-Wanxiang-User": "player-b"}
    )
    assert continued.status_code == 200
    assert continued.json()["instance"]["instance_id"] == instance_id
    assert continued.json()["state_hash"] == committed_hash
