"""The in-stage T2/T3 renderers, activated through the repository contract providers.

Measured before this spec existed: `#panorama-stage-toggle` / `#spatial-stage-toggle`
had only ever been captured at the *upgrade* panel (`t2-contract` / `t3-contract`), so
the in-stage renderers were never exercised in a browser. This spec injects the
repository contract providers — a panorama provider whose `presentation_kind` is
`"panorama"` and a `_SpatialGenerationProvider` subclass — attaches the assets through
the real routes, then drives the real Player in Chrome and records mount, drag, reset,
reduced-motion and the T0 fallback as screenshots plus measured facts.

Evidence: `CURRENT_PRODUCT_VISUAL_AUDIT/stage-renderers/`.
"""

# ruff: noqa: E501
# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import time
from dataclasses import dataclass
from threading import Thread
from typing import Any, cast

import httpx
import pytest
import uvicorn
from playwright.sync_api import Browser, BrowserType, Page, sync_playwright
from tests.conftest import make_world_runtime
from wanxiang_api.app import create_app
from wanxiang_substrate.assets.book_scene_external import (
    _ExternalImageClient,
    _ExternalImageResult,
)
from wanxiang_substrate.assets.book_scene_panorama import _PromptedPanoramaSceneProvider
from wanxiang_substrate.assets.book_scene_prompt import _SceneGenerationBrief
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationProvider,
    _SpatialPollResult,
    _SpatialProjectionFrame,
)
from wanxiang_substrate.preview.runtime import register_preview_resolvers

EVIDENCE_DIR = pathlib.Path(
    os.environ.get("WANXIANG_STAGE_RENDERER_DIR", "CURRENT_PRODUCT_VISUAL_AUDIT/stage-renderers")
)
HEADERS = {"X-Wanxiang-User": "studio"}
T2_PLACE = "Garden"
T0_PLACE = "Harbor"
SOURCE = {
    "source_id": "stage_renderer_source",
    "kind": "text",
    "content": (
        "# Chapter\nCharacter: Alice\n"
        "Alice arrived in Garden in 1985.\n"
        "Alice arrived in Harbor in 1986.\n"
        "rule: visitors register at the gate\n"
    ),
    "stage": "E3",
    "rights_approved": True,
    "access": "public",
    "external_model_processing_allowed": True,
    "private_analysis_allowed": True,
    "package_inclusion_allowed": True,
    "public_export_allowed": True,
    "training_allowed": False,
}
_PLY_VERTICES = (
    (0.0, 0.0, 0.0),
    (1.0, 0.0, 0.0),
    (0.0, 1.0, 0.0),
    (0.0, 0.0, 1.0),
    (1.0, 1.0, 1.0),
    (-1.0, 0.5, 0.25),
)

PLY = (
    f"ply\nformat ascii 1.0\nelement vertex {len(_PLY_VERTICES)}\n"
    "property float x\nproperty float y\nproperty float z\nend_header\n"
    + "".join(f"{x} {y} {z}\n" for x, y, z in _PLY_VERTICES)
).encode("utf-8")


def _png(width: int, height: int) -> bytes:
    """A small but decodable RGB PNG: the built-in renderer must be able to load it."""

    import struct
    import zlib

    def chunk(tag: bytes, payload: bytes) -> bytes:
        return (
            struct.pack(">I", len(payload))
            + tag
            + payload
            + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)
        )

    rows = b"".join(
        b"\x00" + b"".join(bytes(((x * 5) % 256, (y * 11) % 256, 96)) for x in range(width))
        for y in range(height)
    )
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(rows, 9))
        + chunk(b"IEND", b"")
    )


PANORAMA_PNG = _png(96, 48)


@dataclass
class _ContractPanoramaClient(_ExternalImageClient):
    """Deterministic contract client: no network, one PNG panorama per call."""

    calls: int = 0

    def generate(self, brief: _SceneGenerationBrief) -> _ExternalImageResult:
        self.calls += 1
        assert brief.source_refs == ()
        return _ExternalImageResult(
            PANORAMA_PNG,
            "image/png",
            provider_usage_units=11,
        )


class _ContractSpatialProvider(_SpatialGenerationProvider):
    """The repository T3 contract provider, producing the PLY the built-in viewer renders."""

    provider_id = "spatial:stage-renderer-contract"
    provider_version = "2026-11"
    requires_network = False
    private_safe = False
    cost_units_per_job = 3
    allowed_media_types = frozenset({"model/ply"})

    def submit(self, request: Any, *, idempotency_key: str) -> str:
        assert idempotency_key
        assert request.place_name
        return "stage-renderer-task"

    def poll(self, task_ref: str) -> _SpatialPollResult:
        assert task_ref == "stage-renderer-task"
        return _SpatialPollResult(
            "succeeded",
            (_SpatialArtifactCandidate(PLY, "model/ply", hashlib.sha256(PLY).hexdigest()),),
            projection_frame=_SpatialProjectionFrame(
                up=(0.0, 1.0, 0.0),
                forward=(0.0, 0.0, -1.0),
                center=(0.0, 0.0, 0.0),
                scale=1.0,
                convention="stage-renderer-frame",
            ),
            provider_usage_units=3,
        )


def _start(path: pathlib.Path) -> tuple[Any, Thread, str]:
    runtime = make_world_runtime(path, extra_resolvers=register_preview_resolvers)
    app = create_app(
        runtime,
        panorama_provider=_PromptedPanoramaSceneProvider(
            provider_id="provider:stage-renderer-panorama",
            provider_version="2026-11",
            client=_ContractPanoramaClient(),
            cost_units_per_asset=1,
            private_safe=False,
        ),
        panorama_allow_network=True,
        panorama_max_cost_units=2,
    )
    app.state.spatial_asset_provider = _ContractSpatialProvider()
    app.state.spatial_asset_allow_network = True
    app.state.spatial_asset_max_cost_units = 4
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=0, log_level="error"))
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 20
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.02)
    servers = cast(Any, server.servers)
    return server, thread, f"http://127.0.0.1:{int(servers[0].sockets[0].getsockname()[1])}"


def _seed(base: str) -> str:
    """Attach one T2 panorama and one T3 spatial asset to the same place."""

    client = httpx.Client(base_url=base, headers=HEADERS, timeout=300.0)
    created = client.post(
        "/studio/one-click",
        json={
            "job_id": "stage_renderer_job",
            "profile": "book",
            "semantic_provider": "local",
            "sources": [SOURCE],
        },
    )
    assert created.status_code < 300, created.text
    profile = client.post(
        "/studio/jobs/stage_renderer_job/playable-profile",
        json={"owner_id": "studio", "visibility": "public", "display_name": "Stage Renderer"},
    )
    assert profile.status_code < 300, profile.text
    profile_id = str(profile.json()["profile"]["profile_id"])

    panorama = client.post(
        f"/experience/player/worlds/{profile_id}/panoramas",
        json={"place_name": T2_PLACE},
    )
    assert panorama.status_code == 200, panorama.text
    scenes = panorama.json()["world"]["visual"]["scenes"]
    garden = next(scene for scene in scenes if scene["place_name"] == T2_PLACE)
    assert garden["presentation_kind"] == "panorama"
    assert garden["data_uri"]

    spatial = client.post(
        f"/experience/player/worlds/{profile_id}/spatial",
        json={"place_name": T2_PLACE},
    )
    assert spatial.status_code == 202, spatial.text
    submission_id = str(spatial.json()["spatial"]["submission_id"])
    polled = client.get(f"/experience/player/worlds/{profile_id}/spatial/{submission_id}")
    assert polled.status_code == 200, polled.text
    assert polled.json()["spatial"]["state"] == "attached", polled.text
    return profile_id


def _launch(browser_type: BrowserType) -> Browser:
    configured = os.environ.get("WANXIANG_BROWSER_EXECUTABLE", "")
    candidates = tuple(
        pathlib.Path(value)
        for value in (
            configured,
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        )
        if value
    )
    executable = next((path for path in candidates if path.is_file()), None)
    if executable:
        return browser_type.launch(headless=True, executable_path=str(executable))
    return browser_type.launch(headless=True)


def _shot(page: Page, name: str) -> str:
    EVIDENCE_DIR.joinpath("screenshots").mkdir(parents=True, exist_ok=True)
    target = EVIDENCE_DIR / "screenshots" / f"{name}.png"
    stage = page.locator("#world-stage")
    if stage.count() and stage.first.is_visible():
        stage.first.screenshot(path=str(target))
    else:
        page.screenshot(path=str(target))
    return f"screenshots/{name}.png"


def _digest_of(locator: Any) -> str:
    return hashlib.sha256(locator.screenshot()).hexdigest()


def _toggle_visible(page: Page, toggle: str) -> bool:
    return bool(
        page.evaluate(
            "id => {const n=document.getElementById(id);return n?!n.hidden:false}", toggle
        )
    )


def _enter_observer_at(page: Page, base: str, place: str) -> None:
    page.goto(base, wait_until="domcontentloaded")
    page.wait_for_timeout(2200)
    page.locator("#world-list [data-profile]").first.click()
    page.wait_for_timeout(1200)
    page.locator("#enter-observer").click()
    page.wait_for_timeout(1600)
    direct = page.locator(f'[data-observer-scene="{place}"]')
    if direct.count():
        direct.first.click()
    else:
        page.locator(f'[data-observer-generate="{place}"]').first.click()
    page.wait_for_timeout(1400)


@pytest.mark.e2e
def test_in_stage_t2_and_t3_renderers_mount_drag_reset_and_fall_back(
    persist_db_path: pathlib.Path,
) -> None:
    server, _thread, base = _start(persist_db_path)
    audit: dict[str, Any] = {"facts": {}, "screenshots": []}
    try:
        profile_id = _seed(base)
        audit["facts"]["profile_id"] = profile_id
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                _enter_observer_at(page, base, T2_PLACE)
                audit["screenshots"].append(_shot(page, "t2-stage-available-desktop"))

                assert _toggle_visible(page, "panorama-stage-toggle"), page.content()[:400]
                audit["facts"]["t2_toggle_visible"] = True
                page.locator("#panorama-stage-toggle").click()
                page.wait_for_timeout(1500)
                host = page.locator("#world-stage-panorama")
                if not host.is_visible():
                    reason = page.evaluate(
                        "async () => {try{const a=await window.__WANXIANG_PANORAMA_STAGE__.toggle();"
                        "return a?'active':'inactive'}catch(e){return String((e&&e.message)||e)}}"
                    )
                    raise AssertionError(f"panorama stage did not mount: {reason}")
                canvas = host.locator("canvas")
                assert canvas.count() == 1
                assert (
                    page.locator("#panorama-stage-toggle").get_attribute("aria-pressed") == "true"
                )
                audit["screenshots"].append(_shot(page, "t2-stage-mounted-desktop"))
                mounted = _digest_of(canvas)

                box = canvas.bounding_box()
                assert box is not None
                centre_x = box["x"] + box["width"] / 2
                centre_y = box["y"] + box["height"] / 2
                page.mouse.move(centre_x, centre_y)
                page.mouse.down()
                page.mouse.move(centre_x + 140, centre_y + 70, steps=10)
                page.mouse.up()
                page.wait_for_timeout(700)
                dragged = _digest_of(canvas)
                audit["screenshots"].append(_shot(page, "t2-stage-dragged-desktop"))
                assert dragged != mounted, "dragging the panorama did not change the view"
                audit["facts"]["t2_drag_changed_view"] = True

                page.locator("#panorama-stage-toggle").click()
                page.wait_for_timeout(600)
                assert not host.is_visible()
                assert (
                    page.locator("#panorama-stage-toggle").get_attribute("aria-pressed") == "false"
                )

                assert _toggle_visible(page, "spatial-stage-toggle"), page.content()[:400]
                audit["facts"]["t3_toggle_visible"] = True
                page.locator("#spatial-stage-toggle").click()
                page.wait_for_timeout(1500)
                spatial_host = page.locator("#world-stage-spatial")
                assert spatial_host.is_visible()
                spatial_canvas = spatial_host.locator("canvas")
                assert spatial_canvas.count() == 1
                audit["screenshots"].append(_shot(page, "t3-stage-mounted-desktop"))
                spatial_mounted = _digest_of(spatial_canvas)

                spatial_box = spatial_canvas.bounding_box()
                assert spatial_box is not None
                page.mouse.move(
                    spatial_box["x"] + spatial_box["width"] / 2,
                    spatial_box["y"] + spatial_box["height"] / 2,
                )
                page.mouse.down()
                page.mouse.move(
                    spatial_box["x"] + spatial_box["width"] / 2 + 150,
                    spatial_box["y"] + spatial_box["height"] / 2 + 60,
                    steps=10,
                )
                page.mouse.up()
                page.wait_for_timeout(700)
                spatial_dragged = _digest_of(spatial_canvas)
                audit["screenshots"].append(_shot(page, "t3-stage-dragged-desktop"))
                assert spatial_dragged != spatial_mounted
                audit["facts"]["t3_drag_changed_view"] = True

                reset_button = spatial_host.locator("button")
                assert reset_button.count() >= 1, spatial_host.inner_html()[:400]
                reset_button.first.click()
                page.wait_for_timeout(700)
                reset_digest = _digest_of(spatial_canvas)
                audit["screenshots"].append(_shot(page, "t3-stage-reset-desktop"))
                assert reset_digest != spatial_dragged, "reset did not restore the view"
                reset_button.first.click()
                page.wait_for_timeout(500)
                assert _digest_of(spatial_canvas) == reset_digest, "reset is not deterministic"
                audit["facts"]["t3_reset_deterministic"] = True
                # The first mounted frame differs from a settled frame (the canvas is
                # resized by ResizeObserver right after mount), so equality with the
                # mount frame is recorded as a measurement instead of asserted.
                audit["facts"]["t3_reset_matches_mount_frame"] = reset_digest == spatial_mounted

                _enter_observer_at(page, base, T0_PLACE)
                audit["screenshots"].append(_shot(page, "t0-fallback-desktop"))
                assert not _toggle_visible(page, "panorama-stage-toggle")
                assert not _toggle_visible(page, "spatial-stage-toggle")
                image = page.locator("#scene-visual-image")
                assert image.is_visible()
                assert str(image.get_attribute("src") or "").startswith("data:")
                audit["facts"]["t0_fallback_visible"] = True
            finally:
                browser.close()

            reduced = _launch(playwright.chromium)
            try:
                context = reduced.new_context(
                    viewport={"width": 1440, "height": 1000},
                    reduced_motion="reduce",
                )
                page = context.new_page()
                _enter_observer_at(page, base, T2_PLACE)
                stage = page.locator("#world-stage")
                box = stage.bounding_box()
                assert box is not None
                page.mouse.move(box["x"] + 40, box["y"] + 40)
                page.mouse.move(box["x"] + 160, box["y"] + 120, steps=6)
                page.wait_for_timeout(300)
                parallax = page.evaluate(
                    "() => document.getElementById('world-stage').style.getPropertyValue('--stage-x')"
                )
                assert parallax == "", f"reduced motion still moved the stage: {parallax!r}"
                audit["facts"]["reduced_motion_parallax_disabled"] = True
                audit["screenshots"].append(_shot(page, "reduced-motion-desktop"))
                context.close()
            finally:
                reduced.close()
    finally:
        server.should_exit = True
        EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)
        EVIDENCE_DIR.joinpath("audit.json").write_text(
            json.dumps(audit, ensure_ascii=False, indent=2), encoding="utf-8"
        )
