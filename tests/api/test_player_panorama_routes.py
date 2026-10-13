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
        return _ExternalImageResult(b"\x89PNG\r\n\x1a\nplayer-panorama", "image/png")


def _source() -> dict[str, object]:
    return {
        "source_id": "panorama_book",
        "kind": "text",
        "content": "# Chapter\nCharacter: Alice\nAlice arrived in Garden in 1985.\n",
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
    scenes = first.json()["world"]["visual"]["scenes"]
    garden = next(scene for scene in scenes if scene["place_name"] == "Garden")
    assert garden["presentation_kind"] == "panorama"
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
