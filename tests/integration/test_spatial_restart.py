"""A persisted attached T3 ticket rehydrates when a restarted app opens the world."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib
from typing import Any, cast

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_substrate.assets.book_spatial_types import _SpatialGenerationTicket
from wanxiang_substrate.playable.local_store import LocalJsonPlayableStore
from wanxiang_substrate.spatial import plan_book_scene_assets

HEADERS = {"X-Wanxiang-User": "studio"}


def _glb(payload: bytes = b"restart-spatial") -> bytes:
    total = 12 + len(payload)
    return b"glTF" + (2).to_bytes(4, "little") + total.to_bytes(4, "little") + payload


def _source() -> dict[str, object]:
    return {
        "source_id": "spatial_restart_source",
        "kind": "text",
        "content": "# Chapter\nCharacter: Alice\nAlice arrived in Garden in 1985.\n",
        "stage": "E3",
        "rights_approved": True,
        "access": "public",
        "external_model_processing_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": True,
    }


def _seed(client: Any) -> str:
    created = client.post(
        "/studio/one-click",
        json={
            "job_id": "spatial_restart_job",
            "profile": "book",
            "sources": [_source()],
        },
    )
    assert created.status_code == 201, created.text
    profile = client.post(
        "/studio/jobs/spatial_restart_job/playable-profile",
        json={"owner_id": "studio", "visibility": "public", "display_name": "Restart Spatial"},
    )
    assert profile.status_code == 200, profile.text
    return str(profile.json()["profile"]["profile_id"])


def test_restored_spatial_ticket_reattaches_on_world_open(
    tmp_path: pathlib.Path,
    monkeypatch: Any,
) -> None:
    monkeypatch.setenv("WANXIANG_VISUAL_CACHE_DIR", str(tmp_path / "visual-cache"))
    store_path = tmp_path / "player.json"
    first: Any = TestClient(
        create_app(
            build_reference_runtime(),
            playable_store=LocalJsonPlayableStore(store_path),
        )
    )
    profile_id = _seed(first)
    playable = first.app.state.playable
    package = playable.packages[profile_id]
    plan = plan_book_scene_assets(package)
    scene_key = plan.scene_requests[0].stable_key
    ref = first.app.state.spatial_asset_objects.put(
        _glb(b"spatial-bytes"),
        content_type="model/gltf-binary",
        rights="public",
    )
    first.app.state.spatial_asset_jobs.put(
        _SpatialGenerationTicket(
            submission_id="submission_restart",
            scene_key=scene_key,
            provider_id="provider:spatial-fixture",
            provider_version="1.0",
            provider_task_ref="task_restart",
            state="attached",
            reserved_cost_units=0,
            delivery_rights="public",
            scope_key=profile_id,
            asset_refs=(ref,),
        )
    )

    second: Any = TestClient(
        create_app(
            build_reference_runtime(),
            playable_store=LocalJsonPlayableStore(store_path),
        )
    )
    service = second.app.state.playable
    assert service.spatial_assets(profile_id, viewer_id="studio") == {}

    opened = second.get(f"/experience/player/worlds/{profile_id}", headers=HEADERS)
    assert opened.status_code == 200, opened.text
    assets = cast(
        dict[str, tuple[object, ...]],
        service.spatial_assets(profile_id, viewer_id="studio"),
    )
    assert assets[scene_key] == (ref,)
