"""Player T2 panorama upgrades are explicit, owner-governed and non-canonical."""

# pyright: reportPrivateUsage=false

from dataclasses import dataclass
from typing import Any

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_substrate.assets.book_scene_external import (
    _ExternalImageClient,
    _ExternalImageResult,
)
from wanxiang_substrate.assets.book_scene_panorama import _PromptedPanoramaSceneProvider
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief


@dataclass
class _PanoramaClient(_ExternalImageClient):
    calls: int = 0

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        self.calls += 1
        assert brief.source_refs == ()
        return _ExternalImageResult(
            b"\x89PNG\r\n\x1a\nplayer-panorama",
            "image/png",
            provider_usage_units=470000,
        )


def _source() -> dict[str, object]:
    return {
        "source_id": "panorama_book",
        "kind": "text",
        "content": (
            "# Chapter\n"
            "Character: Alice\n"
            "Alice arrived in Garden in 1985.\n"
            "Alice arrived in Harbor in 1986.\n"
        ),
        "stage": "E3",
        "rights_approved": True,
        "access": "public",
        "external_model_processing_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": True,
    }


def test_t2_panorama_is_explicit_owner_upgrade_and_cached_for_player() -> None:
    provider_client = _PanoramaClient()
    provider = _PromptedPanoramaSceneProvider(
        provider_id="provider:panorama-api",
        provider_version="2026-10",
        client=provider_client,
        cost_units_per_asset=3,
        private_safe=False,
    )
    app = create_app(
        build_reference_runtime(),
        panorama_provider=provider,
        panorama_allow_network=True,
        panorama_max_cost_units=3,
    )
    client: Any = TestClient(app)
    created = client.post(
        "/studio/one-click",
        json={"job_id": "panorama_job", "profile": "book", "sources": [_source()]},
    )
    assert created.status_code == 201
    assert provider_client.calls == 0

    profile = client.post(
        "/studio/jobs/panorama_job/playable-profile",
        json={
            "owner_id": "studio",
            "visibility": "public",
            "display_name": "Panorama World",
        },
    )
    assert profile.status_code == 200
    profile_id = str(profile.json()["profile"]["profile_id"])
    endpoint = f"/experience/player/worlds/{profile_id}/panoramas"

    denied_status = client.get(endpoint, headers={"X-Wanxiang-User": "visitor"})
    assert denied_status.status_code == 403
    capability = client.get(endpoint, headers={"X-Wanxiang-User": "studio"})
    assert capability.status_code == 200
    assert capability.json()["generation"]["available"] is True
    assert capability.json()["generation"]["cost_units"] == 3
    assert capability.json()["generation"]["budget_reserved"] == 0
    assert capability.json()["generation"]["budget_remaining"] == 3
    assert capability.json()["ready_places"] == []

    denied = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "visitor"},
        json={"place_name": "Garden"},
    )
    assert denied.status_code == 403
    assert provider_client.calls == 0

    first = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "studio"},
        json={"place_name": "Garden"},
    )
    assert first.status_code == 200
    assert first.json()["tier"] == "T2"
    assert first.json()["provider_calls"] == 1
    assert first.json()["cost_units"] == 3
    assert first.json()["provider_usage_units"] == 470000
    after_capability = client.get(endpoint, headers={"X-Wanxiang-User": "studio"})
    assert after_capability.status_code == 200
    assert after_capability.json()["ready_places"] == ["Garden"]
    assert after_capability.json()["generation"]["available"] is False
    assert after_capability.json()["generation"]["reason"] == "budget_insufficient"
    assert after_capability.json()["generation"]["budget_reserved"] == 3
    assert after_capability.json()["generation"]["budget_remaining"] == 0
    assert first.json()["budget"]["reserved"] == 3
    assert first.json()["budget"]["remaining"] == 0

    blocked_second_place = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "studio"},
        json={"place_name": "Harbor"},
    )
    assert blocked_second_place.status_code == 409
    assert blocked_second_place.json()["detail"] == "budget_insufficient"
    assert provider_client.calls == 1

    scenes = first.json()["world"]["visual"]["scenes"]
    garden = next(scene for scene in scenes if scene["place_name"] == "Garden")
    assert garden["presentation_kind"] == "panorama"
    assert garden["projection_only"] is True
    assert provider_client.calls == 1

    second = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "studio"},
        json={"place_name": "Garden"},
    )
    assert second.status_code == 200
    assert second.json()["provider_calls"] == 0
    assert second.json()["cache_hits"] == 1
    assert second.json()["cost_units"] == 0
    assert second.json()["provider_usage_units"] == 0
    assert provider_client.calls == 1

    visitor_world = client.get(
        f"/experience/player/worlds/{profile_id}",
        headers={"X-Wanxiang-User": "visitor"},
    )
    assert visitor_world.status_code == 200
    public_scene = next(
        scene
        for scene in visitor_world.json()["world"]["visual"]["scenes"]
        if scene["place_name"] == "Garden"
    )
    assert public_scene["presentation_kind"] == "panorama"
    assert public_scene["projection_only"] is True


@dataclass
class _UncertainPanoramaClient(_ExternalImageClient):
    calls: int = 0

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        _ = brief
        self.calls += 1
        raise RuntimeError("provider response lost after submission")


def test_t2_panorama_blocks_automatic_retry_after_unresolved_paid_attempt() -> None:
    provider_client = _UncertainPanoramaClient()
    provider = _PromptedPanoramaSceneProvider(
        provider_id="provider:uncertain-panorama",
        provider_version="2026-10",
        client=provider_client,
        cost_units_per_asset=3,
        private_safe=False,
    )
    app = create_app(
        build_reference_runtime(),
        panorama_provider=provider,
        panorama_allow_network=True,
        panorama_max_cost_units=6,
    )
    client: Any = TestClient(app)
    created = client.post(
        "/studio/one-click",
        json={"job_id": "panorama_uncertain", "profile": "book", "sources": [_source()]},
    )
    assert created.status_code == 201
    profile = client.post(
        "/studio/jobs/panorama_uncertain/playable-profile",
        json={
            "owner_id": "studio",
            "visibility": "public",
            "display_name": "Uncertain Panorama World",
        },
    )
    assert profile.status_code == 200
    profile_id = str(profile.json()["profile"]["profile_id"])
    endpoint = f"/experience/player/worlds/{profile_id}/panoramas"

    first = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "studio"},
        json={"place_name": "Garden"},
    )
    assert first.status_code == 409
    assert provider_client.calls == 1

    retry = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "studio"},
        json={"place_name": "Garden"},
    )
    assert retry.status_code == 409
    assert retry.json()["detail"] == (
        "panorama generation outcome is unresolved; automatic retry is blocked"
    )
    assert provider_client.calls == 1

    capability = client.get(endpoint, headers={"X-Wanxiang-User": "studio"})
    assert capability.status_code == 200
    assert capability.json()["generation"]["budget_reserved"] == 3
    assert capability.json()["generation"]["budget_remaining"] == 3


class _IdempotentPanoramaProvider(_PromptedPanoramaSceneProvider):
    generation_is_idempotent = True


@dataclass
class _RetryablePanoramaClient(_ExternalImageClient):
    calls: int = 0

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        _ = brief
        self.calls += 1
        if self.calls == 1:
            raise RuntimeError("response lost after idempotent submission")
        return _ExternalImageResult(
            b"\x89PNG\r\n\x1a\nresumed-panorama",
            "image/png",
            provider_usage_units=470000,
        )


def test_t2_idempotent_provider_can_resume_existing_reservation_without_rebilling() -> None:
    provider_client = _RetryablePanoramaClient()
    provider = _IdempotentPanoramaProvider(
        provider_id="provider:idempotent-panorama",
        provider_version="2026-10",
        client=provider_client,
        cost_units_per_asset=3,
        private_safe=False,
    )
    app = create_app(
        build_reference_runtime(),
        panorama_provider=provider,
        panorama_allow_network=True,
        panorama_max_cost_units=3,
    )
    client: Any = TestClient(app)
    created = client.post(
        "/studio/one-click",
        json={"job_id": "panorama_resume", "profile": "book", "sources": [_source()]},
    )
    assert created.status_code == 201
    profile = client.post(
        "/studio/jobs/panorama_resume/playable-profile",
        json={
            "owner_id": "studio",
            "visibility": "public",
            "display_name": "Resume Panorama World",
        },
    )
    assert profile.status_code == 200
    profile_id = str(profile.json()["profile"]["profile_id"])
    endpoint = f"/experience/player/worlds/{profile_id}/panoramas"

    first = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "studio"},
        json={"place_name": "Garden"},
    )
    assert first.status_code == 409
    assert provider_client.calls == 1

    held = client.get(endpoint, headers={"X-Wanxiang-User": "studio"})
    assert held.status_code == 200
    assert held.json()["generation"]["reason"] == "budget_insufficient"
    assert held.json()["generation"]["budget_reserved"] == 3
    assert held.json()["generation"]["budget_remaining"] == 0

    resumed = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "studio"},
        json={"place_name": "Garden"},
    )
    assert resumed.status_code == 200
    assert resumed.json()["provider_calls"] == 1
    assert resumed.json()["cost_units"] == 3
    assert resumed.json()["budget"]["reserved"] == 3
    assert resumed.json()["budget"]["remaining"] == 0
    assert provider_client.calls == 2

    cached = client.post(
        endpoint,
        headers={"X-Wanxiang-User": "studio"},
        json={"place_name": "Garden"},
    )
    assert cached.status_code == 200
    assert cached.json()["provider_calls"] == 0
    assert cached.json()["cache_hits"] == 1
    assert provider_client.calls == 2
