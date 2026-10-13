"""T3 Player API exposes only governed async capability and supports restart rehydration."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import json
from typing import Any

import pytest
from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_substrate.assets.book_scene_plan import _SourceSceneRequest
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationProvider,
    _SpatialPollResult,
)
from wanxiang_substrate.playable.factory import profile_from_world_package


def _glb(payload: bytes = b"api-spatial") -> bytes:
    total = 12 + len(payload)
    return b"glTF" + (2).to_bytes(4, "little") + total.to_bytes(4, "little") + payload


class _FakeSpatialProvider(_SpatialGenerationProvider):
    provider_id = "spatial:api-test"
    provider_version = "2026-10"
    requires_network = True
    private_safe = False
    cost_units_per_job = 7
    allowed_media_types = frozenset({"model/gltf-binary"})

    def __init__(self) -> None:
        self.submissions: list[tuple[str, str]] = []
        self.polls: list[str] = []

    def submit(self, request: _SourceSceneRequest, *, idempotency_key: str) -> str:
        self.submissions.append((request.place_name, idempotency_key))
        return "provider-secret-task-ref"

    def poll(self, task_ref: str) -> _SpatialPollResult:
        self.polls.append(task_ref)
        content = _glb()
        return _SpatialPollResult(
            "succeeded",
            (
                _SpatialArtifactCandidate(
                    content,
                    "model/gltf-binary",
                    hashlib.sha256(content).hexdigest(),
                ),
            ),
        )


def _source() -> dict[str, object]:
    return {
        "source_id": "spatial_api_book",
        "kind": "text",
        "content": "# Chapter\nCharacter: Alice\nAlice arrived in Garden in 1985.\n",
        "stage": "E3",
        "rights_approved": True,
        "access": "public",
        "external_model_processing_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": True,
    }


def _world(
    *,
    spatial_provider: _SpatialGenerationProvider | None = None,
    spatial_allow_network: bool = False,
    spatial_max_cost_units: int = 0,
) -> tuple[Any, Any, str]:
    app = create_app(
        build_reference_runtime(),
        spatial_provider=spatial_provider,
        spatial_allow_network=spatial_allow_network,
        spatial_max_cost_units=spatial_max_cost_units,
    )
    client: Any = TestClient(app)
    created = client.post(
        "/studio/one-click",
        json={"job_id": "spatial_api_job", "profile": "book", "sources": [_source()]},
    )
    assert created.status_code == 201
    profile = client.post(
        "/studio/jobs/spatial_api_job/playable-profile",
        json={
            "owner_id": "studio",
            "visibility": "public",
            "display_name": "Spatial API World",
        },
    )
    assert profile.status_code == 200
    return app, client, str(profile.json()["profile"]["profile_id"])


def test_t3_player_api_is_owner_only_idempotent_and_rehydrates_attachment() -> None:
    app, client, profile_id = _world()
    owner = {"X-Wanxiang-User": "studio"}
    visitor = {"X-Wanxiang-User": "visitor"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"

    unavailable = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    assert unavailable.status_code == 503
    initial_status = client.get(endpoint, headers=owner)
    assert initial_status.status_code == 200
    assert initial_status.json()["generation"] == {
        "available": False,
        "reason": "provider_not_configured",
        "cost_units": 0,
    }

    provider = _FakeSpatialProvider()
    app.state.spatial_asset_provider = provider
    app.state.spatial_asset_allow_network = True
    app.state.spatial_asset_max_cost_units = 7

    submitted = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    assert submitted.status_code == 202
    spatial = submitted.json()["spatial"]
    submission_id = str(spatial["submission_id"])
    assert spatial["state"] == "submitted"
    assert spatial["reserved_cost_units"] == 7
    assert len(provider.submissions) == 1

    listed = client.get(endpoint, headers=owner)
    assert listed.status_code == 200
    jobs = listed.json()["spatial_jobs"]
    assert len(jobs) == 1
    assert jobs[0]["submission_id"] == submission_id
    assert jobs[0]["state"] == "submitted"
    assert jobs[0]["place_name"] == "Garden"
    assert "scene_key" not in jobs[0]
    assert listed.json()["generation"] == {
        "available": True,
        "reason": "",
        "cost_units": 7,
        "provider": {"id": "spatial:api-test", "version": "2026-10"},
    }
    serialized_jobs = json.dumps(jobs, sort_keys=True)
    assert "provider_task_ref" not in serialized_jobs
    assert "provider-secret-task-ref" not in serialized_jobs
    assert "asset_id" not in serialized_jobs
    assert "content_hash" not in serialized_jobs

    denied_list = client.get(endpoint, headers=visitor)
    assert denied_list.status_code == 403

    duplicate = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    assert duplicate.status_code == 202
    assert duplicate.json()["spatial"]["submission_id"] == submission_id
    assert len(provider.submissions) == 1

    denied = client.post(endpoint, headers=visitor, json={"place_name": "Garden"})
    assert denied.status_code == 403
    assert len(provider.submissions) == 1

    polled = client.get(f"{endpoint}/{submission_id}", headers=owner)
    assert polled.status_code == 200
    body = polled.json()
    assert body["spatial"]["state"] == "attached"
    assert body["spatial"]["asset_count"] == 1
    assert body["spatial"]["media_types"] == ["model/gltf-binary"]
    serialized_spatial = json.dumps(body["spatial"], sort_keys=True)
    assert "provider_task_ref" not in serialized_spatial
    assert "provider-secret-task-ref" not in serialized_spatial
    assert "asset_id" not in serialized_spatial
    assert "content_hash" not in serialized_spatial
    assert provider.polls == ["provider-secret-task-ref"]

    asset = client.get(
        f"/experience/player/worlds/{profile_id}/spatial-assets/0",
        params={"place_name": "Garden"},
        headers=owner,
    )
    assert asset.status_code == 200
    assert asset.content.startswith(b"glTF")
    assert asset.headers["content-type"] == "model/gltf-binary"
    assert asset.headers["x-content-type-options"] == "nosniff"
    assert asset.headers["cache-control"] == "private, no-store"

    scenes = body["world"]["visual"]["scenes"]
    assert any(scene.get("spatial", {}).get("ready") is True for scene in scenes)

    app.state.playable._spatial_asset_refs.clear()
    restored = client.get(f"{endpoint}/{submission_id}", headers=owner)
    assert restored.status_code == 200
    assert restored.json()["spatial"]["state"] == "attached"
    restored_scenes = restored.json()["world"]["visual"]["scenes"]
    assert any(scene.get("spatial", {}).get("ready") is True for scene in restored_scenes)
    assert provider.polls == ["provider-secret-task-ref"]


def test_t3_source_gated_spatial_asset_is_not_delivered_to_public_visitor() -> None:
    app = create_app(build_reference_runtime())
    client: Any = TestClient(app)
    source = _source()
    source["public_export_allowed"] = False
    created = client.post(
        "/studio/one-click",
        json={"job_id": "spatial_private_asset", "profile": "book", "sources": [source]},
    )
    assert created.status_code == 201
    profile = client.post(
        "/studio/jobs/spatial_private_asset/playable-profile",
        json={
            "owner_id": "studio",
            "visibility": "public",
            "display_name": "Source-gated Spatial World",
        },
    )
    profile_id = str(profile.json()["profile"]["profile_id"])
    provider = _FakeSpatialProvider()
    app.state.spatial_asset_provider = provider
    app.state.spatial_asset_allow_network = True
    app.state.spatial_asset_max_cost_units = 7
    owner = {"X-Wanxiang-User": "studio"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"

    submitted = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    submission_id = str(submitted.json()["spatial"]["submission_id"])
    attached = client.get(f"{endpoint}/{submission_id}", headers=owner)
    assert attached.status_code == 200

    owner_asset = client.get(
        f"/experience/player/worlds/{profile_id}/spatial-assets/0",
        params={"place_name": "Garden"},
        headers=owner,
    )
    visitor_asset = client.get(
        f"/experience/player/worlds/{profile_id}/spatial-assets/0",
        params={"place_name": "Garden"},
        headers={"X-Wanxiang-User": "visitor"},
    )

    assert owner_asset.status_code == 200
    assert visitor_asset.status_code == 404


def test_t3_poll_ticket_cannot_be_reused_against_another_world() -> None:
    app, client, profile_id = _world()
    provider = _FakeSpatialProvider()
    app.state.spatial_asset_provider = provider
    app.state.spatial_asset_allow_network = True
    app.state.spatial_asset_max_cost_units = 7
    owner = {"X-Wanxiang-User": "studio"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"
    submitted = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    submission_id = str(submitted.json()["spatial"]["submission_id"])

    unrelated = client.post(
        "/studio/one-click",
        json={
            "job_id": "spatial_other_job",
            "profile": "book",
            "sources": [
                {
                    **_source(),
                    "source_id": "spatial_other_book",
                    "content": "# Chapter\nCharacter: Bob\nBob arrived in Harbor in 1986.\n",
                }
            ],
        },
    )
    assert unrelated.status_code == 201
    other_profile = client.post(
        "/studio/jobs/spatial_other_job/playable-profile",
        json={"owner_id": "studio", "visibility": "public", "display_name": "Other"},
    )
    other_id = str(other_profile.json()["profile"]["profile_id"])

    denied = client.get(
        f"/experience/player/worlds/{other_id}/spatial/{submission_id}",
        headers=owner,
    )
    assert denied.status_code == 404
    assert provider.polls == []


def test_t3_same_source_in_two_worlds_gets_distinct_world_scoped_ticket() -> None:
    app, client, first_id = _world()
    provider = _FakeSpatialProvider()
    app.state.spatial_asset_provider = provider
    app.state.spatial_asset_allow_network = True
    app.state.spatial_asset_max_cost_units = 7
    owner = {"X-Wanxiang-User": "studio"}

    package = app.state.playable.packages[first_id]
    second_profile = profile_from_world_package(
        package,
        profile_id=f"{first_id}:copy",
        owner_id="studio",
        visibility="public",
        display_name="Spatial API World Copy",
    )
    app.state.playable.register_profile(second_profile, package)
    second_id = second_profile.profile_id
    assert second_id != first_id

    first = client.post(
        f"/experience/player/worlds/{first_id}/spatial",
        headers=owner,
        json={"place_name": "Garden"},
    )
    second = client.post(
        f"/experience/player/worlds/{second_id}/spatial",
        headers=owner,
        json={"place_name": "Garden"},
    )

    assert first.status_code == second.status_code == 202
    first_ticket = str(first.json()["spatial"]["submission_id"])
    second_ticket = str(second.json()["spatial"]["submission_id"])
    assert first_ticket != second_ticket
    assert len(provider.submissions) == 2

    cross_poll = client.get(
        f"/experience/player/worlds/{second_id}/spatial/{first_ticket}",
        headers=owner,
    )
    assert cross_poll.status_code == 404
    assert provider.polls == []


def test_t3_provider_can_be_injected_through_application_factory() -> None:
    provider = _FakeSpatialProvider()
    app, client, profile_id = _world(
        spatial_provider=provider,
        spatial_allow_network=True,
        spatial_max_cost_units=7,
    )
    owner = {"X-Wanxiang-User": "studio"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"

    submitted = client.post(endpoint, headers=owner, json={"place_name": "Garden"})

    assert submitted.status_code == 202
    assert submitted.json()["spatial"]["reserved_cost_units"] == 7
    assert len(provider.submissions) == 1
    assert app.state.spatial_asset_provider is provider


def test_t3_application_factory_fails_closed_for_invalid_network_or_budget_config() -> None:
    with pytest.raises(ValueError, match="spatial_allow_network"):
        create_app(build_reference_runtime(), spatial_allow_network=True)
    with pytest.raises(ValueError, match="spatial_max_cost_units"):
        create_app(build_reference_runtime(), spatial_max_cost_units=-1)
