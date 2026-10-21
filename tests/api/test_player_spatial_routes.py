"""T3 Player API exposes only governed async capability and supports restart rehydration."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
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
    _SpatialProjectionFrame,
)
from wanxiang_substrate.playable.factory import profile_from_world_package
from wanxiang_substrate.spatial import plan_book_scene_assets


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
            projection_frame=_SpatialProjectionFrame(
                up=(0.0, 1.0, 0.0),
                forward=(0.0, 0.0, -1.0),
                center=(1.0, 2.0, 3.0),
                scale=0.5,
                convention="api-test-frame",
            ),
            provider_usage_units=6,
        )


class _CancelableSpatialProvider(_FakeSpatialProvider):
    supports_cancel = True

    def __init__(self) -> None:
        super().__init__()
        self.cancellations: list[tuple[str, str]] = []

    def cancel(self, task_ref: str, *, request_id: str) -> None:
        self.cancellations.append((task_ref, request_id))


class _SubmitUnavailableSpatialProvider(_FakeSpatialProvider):
    def submit(self, request: _SourceSceneRequest, *, idempotency_key: str) -> str:
        _ = request, idempotency_key
        raise RuntimeError("provider transport unavailable")


class _PollUnavailableSpatialProvider(_FakeSpatialProvider):
    def poll(self, task_ref: str) -> _SpatialPollResult:
        _ = task_ref
        raise RuntimeError("artifact URL temporarily unavailable")


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


def test_t3_capability_fails_closed_for_negative_provider_cost() -> None:
    provider = _FakeSpatialProvider()
    provider.cost_units_per_job = -1
    _, client, profile_id = _world(
        spatial_provider=provider,
        spatial_allow_network=True,
        spatial_max_cost_units=7,
    )
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"
    response = client.get(endpoint, headers={"X-Wanxiang-User": "studio"})

    assert response.status_code == 200
    assert response.json()["generation"] == {
        "available": False,
        "reason": "budget_insufficient",
        "cost_units": 0,
        "budget_total": 7,
        "budget_reserved": 0,
        "budget_remaining": 7,
    }


def test_t3_submit_transport_failure_is_retryable_without_fabricating_terminal_state() -> None:
    provider = _SubmitUnavailableSpatialProvider()
    app, client, profile_id = _world(
        spatial_provider=provider,
        spatial_allow_network=True,
        spatial_max_cost_units=7,
    )
    owner = {"X-Wanxiang-User": "studio"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"

    response = client.post(endpoint, headers=owner, json={"place_name": "Garden"})

    assert response.status_code == 503
    assert response.json()["detail"] == "spatial provider temporarily unavailable"
    tickets = app.state.spatial_asset_jobs.list_scope(profile_id)
    assert len(tickets) == 1
    assert tickets[0].state == "submission_ambiguous"


def test_t3_poll_transport_failure_is_retryable_and_keeps_submitted_ticket() -> None:
    provider = _PollUnavailableSpatialProvider()
    app, client, profile_id = _world(
        spatial_provider=provider,
        spatial_allow_network=True,
        spatial_max_cost_units=7,
    )
    owner = {"X-Wanxiang-User": "studio"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"
    submitted = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    submission_id = str(submitted.json()["spatial"]["submission_id"])

    response = client.get(f"{endpoint}/{submission_id}", headers=owner)

    assert response.status_code == 503
    assert response.json()["detail"] == "spatial provider temporarily unavailable"
    ticket = app.state.spatial_asset_jobs.get(submission_id)
    assert ticket is not None
    assert ticket.state == "submitted"


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
        "budget_total": 0,
        "budget_reserved": 0,
        "budget_remaining": 0,
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
        "available": False,
        "reason": "budget_insufficient",
        "cost_units": 7,
        "budget_total": 7,
        "budget_reserved": 7,
        "budget_remaining": 0,
    }
    serialized_jobs = json.dumps(jobs, sort_keys=True)
    assert "provider_task_ref" not in serialized_jobs
    assert "provider_request_ref" not in serialized_jobs
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
    assert body["spatial"]["provider_usage_units"] == 6
    assert body["spatial"]["asset_count"] == 1
    assert body["spatial"]["media_types"] == ["model/gltf-binary"]
    serialized_spatial = json.dumps(body["spatial"], sort_keys=True)
    assert "provider_task_ref" not in serialized_spatial
    assert "provider_request_ref" not in serialized_spatial
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
    spatial_scene = next(scene for scene in scenes if scene.get("spatial", {}).get("ready") is True)
    assert spatial_scene["spatial"]["projection_frame"]["convention"] == "api-test-frame"
    assert spatial_scene["spatial"]["projection_frame"]["scale"] == 0.5

    app.state.playable._spatial_asset_refs.clear()
    app.state.playable._spatial_projection_frames.clear()
    restored_list = client.get(endpoint, headers=owner)
    assert restored_list.status_code == 200
    assert restored_list.json()["rehydrated_attachments"] == 1
    restored_world = client.get(
        f"/experience/player/worlds/{profile_id}",
        headers=owner,
    )
    restored_scenes = restored_world.json()["world"]["visual"]["scenes"]
    restored_scene = next(
        scene for scene in restored_scenes if scene.get("spatial", {}).get("ready") is True
    )
    assert restored_scene["spatial"]["projection_frame"]["convention"] == "api-test-frame"
    assert provider.polls == ["provider-secret-task-ref"]

    app.state.playable._spatial_asset_refs.clear()
    app.state.playable._spatial_projection_frames.clear()
    restored = client.get(f"{endpoint}/{submission_id}", headers=owner)
    assert restored.status_code == 200
    assert restored.json()["spatial"]["state"] == "attached"
    restored_scenes = restored.json()["world"]["visual"]["scenes"]
    assert any(scene.get("spatial", {}).get("ready") is True for scene in restored_scenes)
    assert provider.polls == ["provider-secret-task-ref"]


def test_public_visitor_rehydrates_attached_t3_scene_without_owner_warmup() -> None:
    app, client, profile_id = _world()
    owner = {"X-Wanxiang-User": "studio"}
    visitor = {"X-Wanxiang-User": "visitor"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"
    provider = _FakeSpatialProvider()
    app.state.spatial_asset_provider = provider
    app.state.spatial_asset_allow_network = True
    app.state.spatial_asset_max_cost_units = 7

    submitted = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    submission_id = str(submitted.json()["spatial"]["submission_id"])
    attached = client.get(f"{endpoint}/{submission_id}", headers=owner)
    assert attached.status_code == 200

    app.state.playable._spatial_asset_refs.clear()
    visitor_asset = client.get(
        f"/experience/player/worlds/{profile_id}/spatial-assets/0",
        params={"place_name": "Garden"},
        headers=visitor,
    )
    assert visitor_asset.status_code == 200
    restored_world = client.get(
        f"/experience/player/worlds/{profile_id}",
        headers=visitor,
    )
    assert restored_world.status_code == 200
    scenes = restored_world.json()["world"]["visual"]["scenes"]
    assert any(scene.get("spatial", {}).get("ready") is True for scene in scenes)

    assert visitor_asset.content.startswith(b"glTF")
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

    app.state.playable._spatial_asset_refs.clear()
    visitor_asset_after_restart = client.get(
        f"/experience/player/worlds/{profile_id}/spatial-assets/0",
        params={"place_name": "Garden"},
        headers={"X-Wanxiang-User": "visitor"},
    )
    assert visitor_asset_after_restart.status_code == 404
    visitor_world = client.get(
        f"/experience/player/worlds/{profile_id}",
        headers={"X-Wanxiang-User": "visitor"},
    )
    assert visitor_world.status_code == 200
    assert visitor_world.json()["world"]["visual"] is None


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


def test_t3_restart_rehydrates_verified_asset_without_provider_recall() -> None:
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
    submission_id = str(submitted.json()["spatial"]["submission_id"])
    ticket = app.state.spatial_asset_jobs.get(submission_id)
    assert ticket is not None

    coordinator = app.state.spatial_asset_jobs
    payload = _glb(b"verified-before-crash")
    ref = app.state.spatial_asset_objects.put(
        payload,
        content_type="model/gltf-binary",
        rights=ticket.delivery_rights,
    )
    coordinator.put(
        replace(
            ticket,
            state="verified",
            asset_refs=(ref,),
            provider_usage_units=6,
        )
    )
    app.state.playable._spatial_asset_refs.clear()
    app.state.playable._spatial_projection_frames.clear()
    provider.polls.clear()

    listed = client.get(endpoint, headers=owner)

    assert listed.status_code == 200
    assert listed.json()["rehydrated_attachments"] == 1
    assert listed.json()["unavailable_attachments"] == 0
    restored = app.state.spatial_asset_jobs.get(submission_id)
    assert restored is not None
    assert restored.state == "attached"
    assert provider.polls == []
    scenes = client.get(
        f"/experience/player/worlds/{profile_id}",
        headers=owner,
    ).json()["world"]["visual"]["scenes"]
    assert any(scene.get("spatial", {}).get("ready") is True for scene in scenes)


def test_t3_restart_does_not_rehydrate_missing_spatial_blob() -> None:
    app, client, profile_id = _world()
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

    ticket = app.state.spatial_asset_jobs.get(submission_id)
    assert ticket is not None and ticket.asset_refs
    app.state.spatial_asset_objects.delete(ticket.asset_refs[0])
    app.state.playable._spatial_asset_refs.clear()

    listed = client.get(endpoint, headers=owner)
    assert listed.status_code == 200
    assert listed.json()["rehydrated_attachments"] == 0
    assert listed.json()["unavailable_attachments"] == 1

    world = client.get(f"/experience/player/worlds/{profile_id}", headers=owner)
    scenes = world.json()["world"]["visual"]["scenes"]
    assert not any(scene.get("spatial", {}).get("ready") is True for scene in scenes)

    recovered = client.get(f"{endpoint}/{submission_id}", headers=owner)
    assert recovered.status_code == 409
    assert recovered.json()["detail"] == "verified spatial asset storage is unavailable"


def test_t3_poll_route_revalidates_persisted_asset_rights_before_player_attach() -> None:
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
    submission_id = str(submitted.json()["spatial"]["submission_id"])
    ticket = app.state.spatial_asset_jobs.get(submission_id)
    assert ticket is not None
    package = app.state.playable.packages[profile_id]
    package.draft.compiler_metadata["visual_asset_rights_v1"] = "source-gated"

    payload = _glb(b"tampered-rights")
    valid_ref = app.state.spatial_asset_objects.put(
        payload,
        content_type="model/gltf-binary",
        rights="source-gated",
    )
    tampered_ref = replace(valid_ref, rights="public")
    app.state.spatial_asset_jobs.put(
        replace(
            ticket,
            state="verified",
            delivery_rights="public",
            asset_refs=(tampered_ref,),
        )
    )

    response = client.get(f"{endpoint}/{submission_id}", headers=owner)

    assert response.status_code == 409
    assert "current source rights" in response.json()["detail"]
    assert app.state.playable.spatial_assets(profile_id, viewer_id="studio") == {}


def test_t3_read_rehydrate_rejects_ticket_and_asset_rights_upgrade() -> None:
    app, client, profile_id = _world()
    owner = {"X-Wanxiang-User": "studio"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"
    payload = _glb(b"rehydrate-rights")
    ref = app.state.spatial_asset_objects.put(
        payload,
        content_type="model/gltf-binary",
        rights="public",
    )
    package = app.state.playable.packages[profile_id]
    package.draft.compiler_metadata["visual_asset_rights_v1"] = "source-gated"
    plan = plan_book_scene_assets(package)
    scene_key = plan.scene_requests[0].stable_key
    from wanxiang_substrate.spatial import SpatialGenerationTicket

    app.state.spatial_asset_jobs.put(
        SpatialGenerationTicket(
            submission_id="tampered-rehydrate",
            scene_key=scene_key,
            provider_id="spatial:tampered",
            provider_version="1",
            provider_task_ref="task",
            state="attached",
            reserved_cost_units=0,
            delivery_rights="public",
            scope_key=profile_id,
            asset_refs=(ref,),
        )
    )
    app.state.playable._spatial_asset_refs.clear()

    listed = client.get(endpoint, headers=owner)

    assert listed.status_code == 200
    assert listed.json()["rehydrated_attachments"] == 0
    assert listed.json()["unavailable_attachments"] == 1
    assert app.state.playable.spatial_assets(profile_id, viewer_id="studio") == {}
    assert package.draft.compiler_metadata["visual_asset_rights_v1"] == "source-gated"


def test_t3_terminal_task_can_be_explicitly_retried_with_new_budget_reservation() -> None:
    provider = _FakeSpatialProvider()
    app, client, profile_id = _world(
        spatial_provider=provider,
        spatial_allow_network=True,
        spatial_max_cost_units=14,
    )
    owner = {"X-Wanxiang-User": "studio"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"

    first_response = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    first_id = str(first_response.json()["spatial"]["submission_id"])
    first = app.state.spatial_asset_jobs.get(first_id)
    assert first is not None
    app.state.spatial_asset_jobs.put(
        replace(first, state="failed", reason="provider_task_terminal")
    )

    retried = client.post(
        endpoint,
        headers=owner,
        json={"place_name": "Garden", "retry_terminal": True},
    )

    assert retried.status_code == 202
    retry_view = retried.json()["spatial"]
    assert retry_view["attempt"] == 1
    assert retry_view["submission_id"] != first_id
    assert len(provider.submissions) == 2
    listed = client.get(endpoint, headers=owner).json()
    assert [item["attempt"] for item in listed["spatial_jobs"]] == [0, 1]
    assert listed["generation"]["budget_reserved"] == 14
    assert listed["generation"]["budget_remaining"] == 0


def test_t3_ambiguous_submission_cannot_be_explicitly_retried() -> None:
    provider = _SubmitUnavailableSpatialProvider()
    _, client, profile_id = _world(
        spatial_provider=provider,
        spatial_allow_network=True,
        spatial_max_cost_units=14,
    )
    owner = {"X-Wanxiang-User": "studio"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"
    assert client.post(endpoint, headers=owner, json={"place_name": "Garden"}).status_code == 503

    retried = client.post(
        endpoint,
        headers=owner,
        json={"place_name": "Garden", "retry_terminal": True},
    )

    assert retried.status_code == 409
    assert "cannot be retried safely" in retried.json()["detail"]


def test_t3_cancel_is_owner_only_and_waits_for_provider_terminal_truth() -> None:
    provider = _CancelableSpatialProvider()
    app, client, profile_id = _world(
        spatial_provider=provider,
        spatial_allow_network=True,
        spatial_max_cost_units=7,
    )
    owner = {"X-Wanxiang-User": "studio"}
    visitor = {"X-Wanxiang-User": "visitor"}
    endpoint = f"/experience/player/worlds/{profile_id}/spatial"

    submitted = client.post(endpoint, headers=owner, json={"place_name": "Garden"})
    assert submitted.status_code == 202
    submission_id = str(submitted.json()["spatial"]["submission_id"])
    cancel_url = f"{endpoint}/{submission_id}/cancel"

    denied = client.post(cancel_url, headers=visitor)
    assert denied.status_code == 403

    cancelled = client.post(cancel_url, headers=owner)
    assert cancelled.status_code == 202
    projected = cancelled.json()["spatial"]
    assert projected["state"] == "submitted"
    assert projected["cancellation_requested"] is True
    request_id = hashlib.sha256(f"{submission_id}:cancel-v1".encode()).hexdigest()[:32]
    assert provider.cancellations == [("provider-secret-task-ref", request_id)]

    listed = client.get(endpoint, headers=owner).json()
    assert listed["cancellation_supported"] is True
    assert listed["spatial_jobs"][0]["cancellation_requested"] is True
    ticket = app.state.spatial_asset_jobs.get(submission_id)
    assert ticket is not None
    assert ticket.state == "submitted"
