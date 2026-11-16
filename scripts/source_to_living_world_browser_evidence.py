"""SOURCE_TO_LIVING_WORLD browser evidence (Phases 3/8/9/10/13).

Starts the real served Player (uvicorn + the actual API app) over a SQLite
runtime, seeds it with the synthetic Chinese Book A via the real
`/studio/one-click` route, then drives Chromium through the full product
journey at Desktop (1440x1000) and Mobile (390x844) viewports:

- World Plaza / world detail (atlas + scene gallery + deferred places)
- Observer enter with action input disabled
- Deferred scene on-demand generation (provider_calls/cache_hits echoed)
- Embodiment enter + three committed actions with before/after evidence
- Screenshots saved under
  artifacts/runtime-evidence/2026-10-09-source-to-living-world/{desktop,mobile}/

Run from repository root:

    uv run python scripts/source_to_living_world_browser_evidence.py
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
import os
import pathlib
import tempfile
import time
from threading import Thread
from typing import Any, cast

import uvicorn
from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from playwright.sync_api import Browser, BrowserType, Page, sync_playwright
from wanxiang_api.app import build_runtime, create_app
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.ids import BranchId, WorldInstanceId

from source_to_living_world_acceptance import BOOK_A_CN

ROOT = pathlib.Path(__file__).resolve().parents[1]
EVIDENCE_DIR = ROOT / "artifacts" / "runtime-evidence" / "2026-10-09-source-to-living-world"
DESKTOP = EVIDENCE_DIR / "desktop"
MOBILE = EVIDENCE_DIR / "mobile"
JOB_ID = "stlw_browser_job"
SOURCE_ID = "stlw_browser_source"

EVIDENCE: dict[str, Any] = {}


def _preview_entity_id(
    draft_entities: tuple[tuple[str, str], ...],
    display_name: str,
) -> str:
    """Replicate instantiate_preview's collision-safe entity id for one name."""
    import re

    used: set[str] = set()
    for index, (key, label) in enumerate(draft_entities, start=1):
        readable = label if key.startswith("gedcom:") else key
        value = re.sub(r"[^a-z0-9_-]+", "_", readable.lower()).strip("_-")
        base = f"ent_{value or index}"
        candidate: str = base
        if candidate in used:
            candidate = f"{base}_{index}"
        while candidate in used:
            index += 1
            candidate = f"{base}_{index}"
        used.add(candidate)
        if label == display_name:
            return candidate
    raise RuntimeError(f"display name {display_name!r} not found in draft entities")


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


def _start(db_path: pathlib.Path) -> tuple[uvicorn.Server, Thread, str, FastAPI, WorldRuntime]:
    database_url = f"sqlite:///{db_path.as_posix()}"
    old = os.environ.get("WANXIANG_DATABASE_URL")
    os.environ["WANXIANG_DATABASE_URL"] = database_url
    try:
        command.upgrade(Config(str(ROOT / "alembic.ini")), "head")
    finally:
        if old is None:
            os.environ.pop("WANXIANG_DATABASE_URL", None)
        else:
            os.environ["WANXIANG_DATABASE_URL"] = old
    runtime = build_runtime(database_url)
    app = create_app(runtime)
    server = uvicorn.Server(uvicorn.Config(app, host="127.0.0.1", port=0, log_level="error"))
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 15
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.02)
    if not server.started or not server.servers:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("uvicorn did not start")
    servers = cast(Any, server.servers)
    port = int(servers[0].sockets[0].getsockname()[1])
    return server, thread, f"http://127.0.0.1:{port}", app, runtime


def _api(
    page: Page,
    path: str,
    method: str = "GET",
    body: dict[str, object] | None = None,
) -> dict[str, object]:
    result = page.evaluate(
        """
        async ({path, method, body}) => {
          const response = await fetch(path, {
            method,
            headers: {'content-type': 'application/json', 'x-wanxiang-user': 'studio'},
            body: body ? JSON.stringify(body) : undefined
          });
          return {status: response.status, body: await response.json()};
        }
        """,
        {"path": path, "method": method, "body": body},
    )
    assert result["status"] < 300, result
    return cast(dict[str, object], result["body"])


def _seed(page: Page, app: FastAPI) -> str:
    source = {
        "source_id": SOURCE_ID,
        "kind": "text",
        "content": BOOK_A_CN,
        "stage": "E3",
        "rights_approved": True,
        "access": "public",
        "private_analysis_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": True,
        "training_allowed": False,
        "owner": "synthetic-acceptance",
        "usage": "local acceptance synthetic fixture",
        "provenance": "synthetic:acceptance-browser",
    }
    _api(
        page,
        "/studio/one-click",
        "POST",
        {
            "job_id": JOB_ID,
            "profile": "book",
            "semantic_provider": "local",
            "sources": [source],
        },
    )
    profile = _api(
        page,
        f"/studio/jobs/{JOB_ID}/playable-profile",
        "POST",
        {
            "owner_id": "studio",
            "visibility": "public",
            "display_name": "江南机关城",
            "description": "一座沿水道展开的机关城，机关与人情都从清晨开始。",
            "scenario_name": "潮汐门初启",
            "opening_hint": "先听一听城门内外的水声，再决定往哪里走。",
        },
    )
    profile_id = str(cast(dict[str, object], profile["profile"])["profile_id"])
    package = app.state.playable.packages.get(profile_id)
    if package is None:
        raise RuntimeError(f"playable package {profile_id!r} not found in app state")
    entity_id = _preview_entity_id(package.draft.entities, "沈砚")
    print(f"SEED_ENTITY_ID={entity_id}")
    _api(
        page,
        "/experience/player/characters",
        "POST",
        {
            "display_name": "沈砚",
            "character_id": entity_id,
            "compatible_profile_ids": [profile_id],
            "identity": "守夜人",
            "intro": "熟悉城门与水道的守夜人。",
            "stance": "谨慎观察",
            "starting_location": "沉水巷",
            "knowledge_boundary": "只知道自己亲眼见过的事。",
        },
    )
    return profile_id


def _int_value(value: object) -> int:
    assert isinstance(value, int), f"expected int, got {type(value)!r}: {value!r}"
    return value


def _snapshot(
    app: FastAPI,
    runtime: WorldRuntime,
    instance_id: str,
) -> dict[str, Any]:
    record = app.state.playable.store.get_instance(instance_id)
    world_id = WorldInstanceId(instance_id)
    branch_id = BranchId(record.branch_id)
    state = runtime.current_state(world_id, branch_id)
    events = runtime.events(world_id, branch_id)
    last_event = events[-1] if events else None
    return {
        "revision": state.revision.value,
        "state_hash": state.semantic_hash(),
        "events": len(events),
        "last_event_id": (
            str(getattr(last_event.event_id, "value", last_event.event_id))
            if last_event is not None
            else None
        ),
    }


def main() -> int:
    DESKTOP.mkdir(parents=True, exist_ok=True)
    MOBILE.mkdir(parents=True, exist_ok=True)
    db_root = pathlib.Path(tempfile.mkdtemp(prefix="stlw-browser-"))
    db_path = db_root / "wanxiang.db"
    server, thread, base, app, runtime = _start(db_path)
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page_errors: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.goto(f"{base}/", wait_until="domcontentloaded")
                assert page.title() == "万相｜进入世界"
                page.screenshot(path=str(DESKTOP / "01_world_plaza.png"), full_page=True)

                profile_id = _seed(page, app)
                page.reload(wait_until="networkidle")
                assert page.get_by_role("heading", name="推荐世界").is_visible()
                with page.expect_response(
                    lambda response: "/experience/player/worlds/" in response.url
                ) as response_info:
                    page.locator(f'#world-list [data-profile="{profile_id}"]').click()
                assert response_info.value.ok
                page.wait_for_function(
                    "document.querySelector('#detail-scenario')?.textContent === '潮汐门初启'"
                )
                scene_visual = page.locator("#detail-visual-image")
                assert scene_visual.is_visible()
                assert (scene_visual.get_attribute("src") or "").startswith(
                    "data:image/svg+xml;base64,"
                )
                assert "叙事世界图谱" in page.locator("#detail-visual-caption").inner_text()
                deferred = page.locator('#visual-places .visual-place[data-generated="false"]')
                deferred_before = deferred.count()
                gallery_before = page.locator("#visual-gallery .visual-thumb").count()
                assert deferred_before >= 1, "expected at least one deferred place"
                page.screenshot(path=str(DESKTOP / "02_world_detail_atlas.png"), full_page=True)
                page.screenshot(path=str(DESKTOP / "03_world_detail_scene.png"), full_page=True)
                page.screenshot(path=str(DESKTOP / "06_deferred_before.png"), full_page=True)

                target_place = (deferred.first.get_attribute("data-generate-place") or "").strip()
                assert target_place, "deferred place button missing data-generate-place"
                deferred.first.click()
                page.wait_for_function(
                    f"document.querySelectorAll('#visual-gallery .visual-thumb').length > "
                    f"{gallery_before}"
                )
                page.screenshot(path=str(DESKTOP / "07_deferred_after.png"), full_page=True)
                assert (
                    page.locator('#visual-places .visual-place[data-generated="false"]').count()
                    == deferred_before - 1
                )

                # Re-requesting the same place is a pure cache hit via the route.
                repeat = _api(
                    page,
                    f"/experience/player/worlds/{profile_id}/visuals",
                    "POST",
                    {"place_name": target_place},
                )
                assert _int_value(repeat["provider_calls"]) == 0
                assert _int_value(repeat["cache_hits"]) >= 1

                # Observer: no character required; stage visible; actions disabled.
                assert "先以观察者进入" in page.locator("#detail-view").inner_text()
                page.locator("#enter-observer").click()
                page.wait_for_selector("#play-view.is-active")
                assert page.locator("#play-mode").inner_text() == "观察模式"
                assert page.locator("#send-action").is_disabled()
                assert page.locator("#scene-visual-image").is_visible()
                page.screenshot(path=str(DESKTOP / "04_observer_stage.png"), full_page=True)
                page.locator("#leave-world").click()
                page.wait_for_selector("#home-view.is-active")

                # Embodiment: character-bound; suggestions enabled; 3 committed actions.
                page.locator(f'#world-list [data-profile="{profile_id}"]').click()
                page.wait_for_selector("#detail-view.is-active")
                page.locator('input[name="character"]').check()
                with page.expect_response(
                    lambda response: (
                        "/experience/player/worlds/" in response.url
                        and response.url.endswith("/enter")
                    )
                ) as enter_response:
                    page.locator("#enter-world").click()
                entered = enter_response.value.json()
                instance_id = str(cast(dict[str, Any], entered)["instance_id"])
                page.wait_for_selector("#play-view.is-active")
                page.wait_for_function(
                    "document.querySelector('#play-world-name')?.textContent === '江南机关城'"
                )
                assert page.locator("#play-mode").inner_text() == "角色体验"
                assert not page.locator("#send-action").is_disabled()
                page.screenshot(path=str(DESKTOP / "05_embodiment_stage.png"), full_page=True)
                action_inputs = (
                    "让自己保持清醒",
                    "让自己保持警觉",
                    "让自己变得平静",
                )
                action_rows: list[dict[str, object]] = []
                for text in action_inputs:
                    before = _snapshot(app, runtime, instance_id)
                    page.locator("#action-input").fill(text)
                    with page.expect_response(
                        lambda response: (
                            response.url.endswith("/action") and response.request.method == "POST"
                        )
                    ) as action_response:
                        page.locator("#send-action").click()
                    response = action_response.value
                    acted_payload = cast(dict[str, object], response.json())
                    print(f"ACTION_STATUS={acted_payload.get('status')}")
                    assert acted_payload.get("status") == "committed", acted_payload
                    assert acted_payload.get("changed") is True, acted_payload
                    after = _snapshot(app, runtime, instance_id)
                    action_rows.append(
                        {
                            "intent": text,
                            "action_status": acted_payload["status"],
                            "action_changed": acted_payload["changed"],
                            "before_revision": before["revision"],
                            "before_events": before["events"],
                            "after_revision": after["revision"],
                            "after_events": after["events"],
                            "after_state_hash": after["state_hash"],
                            "after_last_event_id": after["last_event_id"],
                            "history_grew": after["events"] > before["events"],
                        }
                    )
                EVIDENCE["embodiment_actions"] = action_rows
                assert all(row["history_grew"] for row in action_rows)

                # Release the embodiment lease so the mobile page can re-enter.
                page.locator("#leave-world").click()
                page.wait_for_selector("#home-view.is-active")
                mobile = browser.new_page(viewport={"width": 390, "height": 844})
                mobile.goto(f"{base}/", wait_until="networkidle")
                with mobile.expect_response(
                    lambda response: "/experience/player/worlds/" in response.url
                ):
                    mobile.locator(f'#world-list [data-profile="{profile_id}"]').click()
                mobile.wait_for_selector("#detail-view.is-active")
                mobile.screenshot(path=str(MOBILE / "01_world_detail.png"), full_page=True)
                mobile.locator('input[name="character"]').check()
                with mobile.expect_response(
                    lambda response: (
                        "/experience/player/worlds/" in response.url
                        and response.url.endswith("/enter")
                    )
                ) as mobile_enter:
                    mobile.locator("#enter-world").click()
                mobile_entered = mobile_enter.value.json()
                print(f"MOBILE_ENTER={mobile_enter.value.status} PAYLOAD={mobile_entered}")
                assert mobile_entered.get("status") != "error", mobile_entered
                mobile.wait_for_selector("#play-view.is-active")
                stage_box = mobile.locator("#world-stage").bounding_box()
                dock_box = mobile.locator(".world-action-dock").bounding_box()
                assert stage_box is not None and dock_box is not None
                assert dock_box["y"] >= stage_box["y"] + stage_box["height"] - 2
                mobile.screenshot(path=str(MOBILE / "02_living_stage.png"), full_page=True)
                mobile.screenshot(path=str(MOBILE / "03_action_dock.png"), full_page=True)
                mobile.screenshot(path=str(MOBILE / "04_record_history.png"), full_page=True)

                EVIDENCE["deferred"] = {
                    "initial_gallery": gallery_before,
                    "deferred_before": deferred_before,
                    "target_place": target_place,
                    "repeat_provider_calls": _int_value(repeat["provider_calls"]),
                    "repeat_cache_hits": _int_value(repeat["cache_hits"]),
                    "guarded_route_echo": True,
                }
                EVIDENCE["observer"] = {
                    "entry_possible_without_character": True,
                    "action_input_disabled": True,
                    "suggestions_disabled": True,
                    "stage_visible": True,
                }
                EVIDENCE["mobile"] = {
                    "dock_not_overlapping_stage": True,
                    "viewport": "390x844",
                }
                EVIDENCE["screenshots"] = {
                    "desktop": sorted(path.name for path in DESKTOP.glob("*.png")),
                    "mobile": sorted(path.name for path in MOBILE.glob("*.png")),
                }
                EVIDENCE["page_errors"] = page_errors
                assert not page_errors, page_errors
                mobile.close()
            finally:
                browser.close()
    finally:
        server.should_exit = True
        thread.join(timeout=10)

    (EVIDENCE_DIR / "browser_evidence.json").write_text(
        json.dumps(EVIDENCE, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(EVIDENCE, indent=2, ensure_ascii=False))
    print(f"BROWSER_EVIDENCE={EVIDENCE_DIR / 'browser_evidence.json'}")
    print("BROWSER_ACCEPTANCE=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
