"""G90H API/Studio qualification over the shared Workshop and Playable services."""

from __future__ import annotations

from typing import Any, cast

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app


def _source(source_id: str, version: str = "1") -> dict[str, object]:
    return {
        "source_id": source_id,
        "kind": "text",
        "version": version,
        "content": (
            "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
            "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
            "relationship: Alice -> Bob\nrule: visitors register\n"
        ),
        "stage": "E3",
        "owner": "fixture",
        "usage": "qualification",
        "rights_approved": True,
        "access": "private",
        "private_analysis_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": True,
        "training_allowed": False,
    }


def test_workshop_api_exposes_home_three_modes_and_playable_public_review_gate() -> None:
    client: Any = TestClient(create_app(build_reference_runtime()))

    home = client.get("/workshop")
    assert home.status_code == 200
    assert set(home.json()["creation_modes"]) == {"source", "prompt", "hybrid"}

    source = client.post(
        "/workshop/from-source",
        json={
            "workshop_id": "g90h_api_source",
            "owner_id": "alice",
            "profile": "book",
            "visibility": "private",
            "semantic_provider": "local_semantic_v1",
            "sources": [_source("g90h_api_source_record")],
        },
    )
    assert source.status_code == 201
    source_body = cast(dict[str, Any], source.json())
    assert source_body["preview"]["scoped_ref"].startswith("preview://")
    assert source_body["publishing"]["publishable"] is True
    source_profile = cast(dict[str, Any], source_body["playable_profile"])
    entered = client.post(
        f"/experience/worlds/{source_profile['profile_id']}/enter",
        headers={"X-Wanxiang-User": "alice"},
        json={"mode": "observer", "session_id": "g90h_api_source_session"},
    )
    assert entered.status_code == 200
    assert entered.json()["state_hash"]

    prompt = client.post(
        "/workshop/from-prompt",
        json={
            "workshop_id": "g90h_api_prompt",
            "owner_id": "alice",
            "visibility": "public",
            "intent": {
                "intent_id": "g90h_api_intent",
                "author_id": "alice",
                "text": "setting: river city\nactor: archivist\ngoal: preserve records",
            },
        },
    )
    assert prompt.status_code == 201
    prompt_body = cast(dict[str, Any], prompt.json())
    assert prompt_body["publishing"]["publishable"] is False
    assert "playable_profile" not in prompt_body
    for action in ("review_e5", "accept_constraints", "preview"):
        reviewed = client.post(
            "/workshop/g90h_api_prompt/review",
            json={"action": action},
        )
        assert reviewed.status_code == 200
        prompt_body = cast(dict[str, Any], reviewed.json())
    assert prompt_body["publishing"]["publishable"] is True
    assert prompt_body["publishing"]["visible_in_plaza"] is True
    prompt_profile = cast(dict[str, Any], prompt_body["playable_profile"])
    prompt_entered = client.post(
        f"/experience/worlds/{prompt_profile['profile_id']}/enter",
        headers={"X-Wanxiang-User": "alice"},
        json={"mode": "observer", "session_id": "g90h_api_prompt_session"},
    )
    assert prompt_entered.status_code == 200
    assert prompt_entered.json()["state_hash"]

    hybrid = client.post(
        "/workshop/from-hybrid",
        json={
            "workshop_id": "g90h_api_hybrid",
            "owner_id": "alice",
            "profile": "book",
            "visibility": "private",
            "semantic_provider": "local_semantic_v1",
            "intent": {
                "intent_id": "g90h_api_hybrid_intent",
                "author_id": "alice",
                "text": "setting: river city\nactor: archivist\ngoal: inspect archives",
            },
            "sources": [_source("g90h_api_hybrid_record", version="2")],
        },
    )
    assert hybrid.status_code == 201
    hybrid_body = cast(dict[str, Any], hybrid.json())
    assert hybrid_body["preview"]["scoped_ref"].startswith("preview://")
    assert hybrid_body["evidence_audit"]["all_hybrid_prompt_traces_e5"] is True
