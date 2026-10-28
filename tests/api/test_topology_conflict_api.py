"""Conflicting source place relations reach the Player Atlas as marked data."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import Any

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app

HEADERS = {"X-Wanxiang-User": "studio"}


def test_one_click_source_reaches_atlas_with_conflicting_relations() -> None:
    client: Any = TestClient(create_app(build_reference_runtime()))
    source = {
        "source_id": "topology_conflict_source",
        "kind": "text",
        "content": (
            "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
            "Alice arrived in Garden in 1985.\n"
            "Alice visited Harbor.\n"
            "Alice walked from Garden to Harbor.\n"
            "Bob walked from Harbor to Garden.\n"
            "relationship: Alice -> Bob\nrule: visitors register\n"
        ),
        "stage": "E3",
        "rights_approved": True,
        "access": "public",
        "package_inclusion_allowed": True,
        "public_export_allowed": True,
        "external_model_processing_allowed": True,
    }
    created = client.post(
        "/studio/one-click",
        json={
            "job_id": "topology_conflict_job",
            "profile": "book",
            "semantic_provider": "local",
            "sources": [source],
        },
    )
    assert created.status_code == 201, created.text
    profile = client.post(
        "/studio/jobs/topology_conflict_job/playable-profile",
        json={"owner_id": "studio", "visibility": "public", "display_name": "Conflict World"},
    )
    assert profile.status_code == 200, profile.text
    profile_id = str(profile.json()["profile"]["profile_id"])
    detail = client.get(f"/experience/player/worlds/{profile_id}", headers=HEADERS)
    assert detail.status_code == 200, detail.text
    topology = detail.json()["world"]["visual"]["topology"]
    assert len(topology) >= 2
    assert all(item["conflicting"] is True for item in topology)
    directions = {(item["from"], item["to"]) for item in topology}
    assert ("Garden", "Harbor") in directions
    assert ("Harbor", "Garden") in directions
