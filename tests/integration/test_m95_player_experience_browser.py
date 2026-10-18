"""M95 automated Player Experience smoke; human acceptance remains separate."""

from __future__ import annotations

import os
import pathlib
import time
from threading import Thread
from typing import Any, cast

import pytest
import uvicorn
from playwright.sync_api import Browser, BrowserType, Page, sync_playwright
from tests.conftest import make_world_runtime
from wanxiang_api.app import create_app
from wanxiang_substrate.preview.runtime import register_preview_resolvers


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


def _start(path: pathlib.Path) -> tuple[uvicorn.Server, Thread, str]:
    runtime = make_world_runtime(path, extra_resolvers=register_preview_resolvers)
    server = uvicorn.Server(
        uvicorn.Config(create_app(runtime), host="127.0.0.1", port=0, log_level="error")
    )
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
    return server, thread, f"http://127.0.0.1:{port}"


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


def _seed(page: Page) -> str:
    source = {
        "source_id": "m95_browser_source",
        "kind": "text",
        "content": (
            "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
            "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
            "Alice 来到江南城。\nAlice 来到机关桥。\n"
            "Alice 来到潮汐港。\nAlice 来到望月亭。\nAlice 来到青石巷。\n"
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
    _api(
        page,
        "/studio/one-click",
        "POST",
        {
            "job_id": "m95_browser_job",
            "profile": "book",
            "semantic_provider": "local",
            "sources": [source],
        },
    )
    profile = _api(
        page,
        "/studio/jobs/m95_browser_job/playable-profile",
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
    _api(
        page,
        "/experience/player/characters",
        "POST",
        {
            "display_name": "沈砚",
            "character_id": "ent_alice",
            "compatible_profile_ids": [profile_id],
            "identity": "守夜人",
            "intro": "熟悉城门与水道的守夜人。",
            "stance": "谨慎观察",
            "starting_location": "沉水巷",
            "knowledge_boundary": "只知道自己亲眼见过的事。",
        },
    )
    return profile_id


@pytest.mark.e2e
def test_chinese_player_journey_over_sqlite_runtime(persist_db_path: pathlib.Path) -> None:
    server, thread, base = _start(persist_db_path)
    review = pathlib.Path(".impeccable/review")
    review.mkdir(parents=True, exist_ok=True)
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page_errors: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.goto(f"{base}/", wait_until="domcontentloaded")
                assert page.title() == "万相｜进入世界"
                assert page.locator("html").get_attribute("lang") == "zh-CN"
                assert page.evaluate("window.__PLAYER_I18N__?.locale") == "zh-CN"
                assert (
                    page.evaluate("window.__PLAYER_I18N__?.strings?.hero_title")
                    == "创造世界，进入世界，让世界继续发生。"
                )

                builtin_ply = (
                    b"ply\n"
                    b"format ascii 1.0\n"
                    b"element vertex 4\n"
                    b"property float x\n"
                    b"property float y\n"
                    b"property float z\n"
                    b"property uchar red\n"
                    b"property uchar green\n"
                    b"property uchar blue\n"
                    b"end_header\n"
                    b"-1 -1 0 255 96 80\n"
                    b"1 -1 0 80 220 180\n"
                    b"-1 1 0 90 150 255\n"
                    b"1 1 0 245 230 120\n"
                )
                page.route(
                    "**/spatial-assets/0**",
                    lambda route: route.fulfill(
                        status=200,
                        content_type="model/ply",
                        body=builtin_ply,
                    ),
                )
                page.evaluate(
                    """() => {
                      window.__WANXIANG_SPATIAL_STAGE__.sync(
                        {
                          place_name: "内置 PLY 空间",
                          spatial: {
                            ready: true,
                            asset_count: 1,
                            media_types: ["model/ply"]
                          }
                        },
                        "profile-builtin-ply",
                        {"x-wanxiang-user": "studio"}
                      );
                    }"""
                )
                assert (
                    page.evaluate("document.querySelector('#spatial-stage-toggle').hidden") is False
                )
                page.evaluate("document.querySelector('#play-view').classList.add('is-active')")
                assert page.evaluate("window.__WANXIANG_SPATIAL_STAGE__.toggle()") is True
                builtin_canvas = page.locator("#world-stage-spatial canvas")
                assert builtin_canvas.is_visible()
                canvas_box = builtin_canvas.bounding_box()
                assert canvas_box is not None
                assert canvas_box["width"] > 100 and canvas_box["height"] > 100
                assert builtin_canvas.get_attribute("aria-label") == "内置 PLY 空间"
                assert (
                    builtin_canvas.get_attribute("aria-describedby")
                    == "spatial-stage-controls-hint"
                )
                stage_copy = page.locator("#world-stage-spatial").inner_text()
                assert "4 个空间点" in stage_copy
                assert "拖动旋转" in stage_copy
                reset_view = page.get_by_role("button", name="复位视角")
                assert reset_view.is_visible()
                builtin_canvas.press("ArrowRight")
                reset_view.press("Enter")
                assert builtin_canvas.evaluate("node => document.activeElement === node") is True
                assert page.evaluate("window.__WANXIANG_SPATIAL_STAGE__.deactivate()") is False
                assert page.locator("#world-stage-spatial").is_hidden()
                page.evaluate("document.querySelector('#play-view').classList.remove('is-active')")
                page.unroute("**/spatial-assets/0**")

                page.route(
                    "**/spatial-assets/0**",
                    lambda route: route.fulfill(
                        status=200,
                        content_type="model/gltf-binary",
                        body=b"glTF-test",
                    ),
                )
                page.evaluate(
                    """() => {
                      window.__WANXIANG_SPATIAL_RENDERER__ = {
                        supports: types => types.includes("model/gltf-binary"),
                        mount: async ({container, loadAsset}) => {
                          const asset = await loadAsset(0);
                          container.dataset.loaded = asset.mediaType;
                          return () => { container.dataset.cleaned = "true"; };
                        }
                      };
                      window.__WANXIANG_SPATIAL_STAGE__.sync(
                        {
                          place_name: "Test Place",
                          spatial: {
                            ready: true,
                            asset_count: 1,
                            media_types: ["model/gltf-binary"]
                          }
                        },
                        "profile-test",
                        {"x-wanxiang-user": "studio"}
                      );
                    }"""
                )
                assert (
                    page.evaluate("document.querySelector('#spatial-stage-toggle').hidden") is False
                )
                assert page.evaluate("window.__WANXIANG_SPATIAL_STAGE__.toggle()") is True
                assert (
                    page.evaluate("document.querySelector('#world-stage-spatial').hidden") is False
                )
                assert (
                    page.evaluate("document.querySelector('#world-stage-spatial').dataset.loaded")
                    == "model/gltf-binary"
                )
                assert page.evaluate("window.__WANXIANG_SPATIAL_STAGE__.toggle()") is False
                assert (
                    page.evaluate("document.querySelector('#world-stage-spatial').hidden") is True
                )
                assert (
                    page.evaluate("document.querySelector('#world-stage-spatial').dataset.cleaned")
                    == "true"
                )
                page.evaluate(
                    """() => {
                      window.__WANXIANG_SPATIAL_RENDERER__ = {
                        supports: () => { throw new Error("supports-failure"); },
                        mount: async () => null
                      };
                      window.__WANXIANG_SPATIAL_STAGE__.sync(
                        {
                          place_name: "Broken",
                          spatial: {
                            ready: true,
                            asset_count: 1,
                            media_types: ["model/gltf-binary"]
                          }
                        },
                        "profile-test",
                        {}
                      );
                    }"""
                )
                assert (
                    page.evaluate("document.querySelector('#spatial-stage-toggle').hidden") is True
                )
                page.evaluate(
                    """() => {
                      window.__WANXIANG_SPATIAL_RENDERER__ = {
                        supports: () => true,
                        mount: async () => () => {
                          throw new Error("cleanup-failure");
                        }
                      };
                      window.__WANXIANG_SPATIAL_STAGE__.sync(
                        {
                          place_name: "Cleanup",
                          spatial: {
                            ready: true,
                            asset_count: 1,
                            media_types: ["model/gltf-binary"]
                          }
                        },
                        "profile-test",
                        {}
                      );
                    }"""
                )
                assert page.evaluate("window.__WANXIANG_SPATIAL_STAGE__.toggle()") is True
                assert page.evaluate("window.__WANXIANG_SPATIAL_STAGE__.deactivate()") is False
                page.unroute("**/spatial-assets/0**")
                assert page.get_by_role(
                    "heading", name="创造世界，进入世界，让世界继续发生。"
                ).is_visible()
                profile_id = _seed(page)
                page.reload(wait_until="networkidle")
                body_copy = page.locator("body").inner_text()
                for heading in ("推荐世界", "我的世界", "最近经历", "我的角色"):
                    assert page.get_by_role("heading", name=heading).is_visible()
                for forbidden in (
                    "WorldPackage",
                    "Candidate",
                    "Commit",
                    "RuntimeProfile",
                    "raw JSON",
                    "World Plaza",
                    "My Worlds",
                    "My Characters",
                    "Enter world",
                    "Create world",
                    "enterPlayable",
                    "state_hash",
                    "event_id",
                    "branch_id",
                    "profile_id",
                    profile_id,
                ):
                    assert forbidden not in body_copy
                assert page.locator(".skip-link").count() == 1
                assert page.locator("#world-search").get_attribute("aria-label")
                detail = _api(page, f"/experience/player/worlds/{profile_id}")
                assert len(cast(list[object], detail["characters"])) == 1, detail
                page.screenshot(path=str(review / "desktop.png"), full_page=True)
                with page.expect_response(
                    lambda response: "/experience/player/worlds/" in response.url
                ) as response_info:
                    page.locator(f'#world-list [data-profile="{profile_id}"]').click()
                detail_response = response_info.value
                assert detail_response.ok
                detail_body = cast(dict[str, object], detail_response.json())
                assert len(cast(list[object], detail_body["characters"])) == 1, detail_body
                page.wait_for_function(
                    "document.querySelector('#detail-scenario')?.textContent === '潮汐门初启'"
                )
                assert page.locator("#detail-mode").text_content() == "角色体验"
                detail_visual = page.locator("#detail-visual-image")
                assert detail_visual.is_visible()
                assert (detail_visual.get_attribute("src") or "").startswith(
                    "data:image/svg+xml;base64,"
                )
                assert page.locator("#visual-gallery-wrap").is_visible()
                assert page.locator("#visual-gallery .visual-thumb").count() >= 2
                assert page.locator("#panorama-upgrade-panel").is_hidden()
                assert "叙事世界图谱" in page.locator("#detail-visual-caption").inner_text()
                entrances = page.locator("#atlas-entrances [data-atlas-place]")
                assert entrances.count() >= 3
                assert page.locator("#atlas-entrances").is_visible()
                ready_entrance = (
                    page.locator("#atlas-entrances [data-atlas-place]")
                    .filter(has=page.locator("small", has_text="已有场景"))
                    .first
                )
                assert ready_entrance.count() == 1
                entrance_name = ready_entrance.get_attribute("data-atlas-place")
                assert entrance_name
                ready_entrance.click()
                assert entrance_name in page.locator("#detail-visual-caption").inner_text()
                assert page.locator("#atlas-entrances").is_hidden()
                page.locator('#visual-gallery [data-visual-index="0"]').click()
                assert page.locator("#atlas-entrances").is_visible()
                place_buttons = page.locator("#visual-places .visual-place")
                assert place_buttons.count() >= 5
                assert page.locator("#visual-place-count").is_visible()
                place_search = page.locator("#visual-place-search")
                place_search.fill("机关桥")
                assert place_buttons.count() == 1
                place_search.fill("")
                assert place_buttons.count() >= 5
                ready_place = page.locator("#visual-places [data-focus-place]").first
                ready_name = ready_place.get_attribute("data-focus-place")
                assert ready_name
                ready_place.click()
                assert ready_place.get_attribute("aria-pressed") == "true"
                assert ready_name in page.locator("#detail-visual-caption").inner_text()
                assert page.locator("#panorama-upgrade-panel").is_visible()
                assert (
                    "未配置可用的全景生成器" in page.locator("#panorama-upgrade-copy").inner_text()
                )
                assert page.locator("#panorama-upgrade-submit").is_hidden()
                assert "原文证据" in page.locator("#detail-visual-caption").inner_text()
                assert "插画投影" in page.locator("#detail-visual-caption").inner_text()
                assert page.locator("#spatial-upgrade-panel").is_visible()
                assert "未配置空间生成器" in page.locator("#spatial-upgrade-copy").inner_text()
                assert page.locator("#spatial-submit").is_hidden()
                assert page.locator("#spatial-refresh").is_hidden()
                page.locator('#visual-gallery [data-visual-index="0"]').click()
                assert "叙事世界图谱" in page.locator("#detail-visual-caption").inner_text()
                deferred_places = page.locator(
                    '#visual-places .visual-place[data-generated="false"]'
                )
                assert deferred_places.count() >= 1
                before_gallery_count = page.locator("#visual-gallery .visual-thumb").count()
                before_deferred_count = deferred_places.count()
                deferred_name = deferred_places.first.get_attribute("data-generate-place")
                assert deferred_name
                deferred_places.first.click()
                page.wait_for_function(
                    f"document.querySelectorAll('#visual-gallery .visual-thumb').length > "
                    f"{before_gallery_count}"
                )
                assert page.locator(
                    '#visual-places .visual-place[data-generated="false"]'
                ).count() == (before_deferred_count - 1)
                assert deferred_name in page.locator("#detail-visual-caption").inner_text()
                assert (
                    page.locator(
                        f'#visual-places [data-focus-place="{deferred_name}"]'
                    ).get_attribute("aria-pressed")
                    == "true"
                )
                assert not page_errors, page_errors
                assert page.locator('input[name="character"]').count() == 1, page.locator(
                    "#detail-view"
                ).inner_html()
                assert "以此角色进入" in page.locator("#detail-view").inner_text()
                assert "先以观察者进入" in page.locator("#detail-view").inner_text()
                fallback_copy = page.evaluate(
                    """sceneReadyStatus(
                        {
                          fallback_from_provider:'provider:test@1',
                          fallback_reason:'provider_failure'
                        },
                        '机关桥'
                    )"""
                )
                assert "已使用离线保底场景" in fallback_copy
                assert "高阶视觉生成失败" in fallback_copy
                page.locator("#enter-observer").click()
                page.wait_for_selector("#play-view.is-active")
                assert page.locator("#play-mode").inner_text() == "观察模式"
                assert page.locator("#fork-worldline").is_hidden()
                assert page.locator("#send-action").is_disabled()
                assert page.locator("#scene-visual-image").is_visible()
                assert page.locator("#relation-list").inner_text().count("Alice") == 0
                page.locator("#worldline-toggle").click()
                page.wait_for_selector("#worldline-panel:not([hidden])")
                assert page.locator("#worldline-list li").count() == 1
                assert page.locator("#worldline-list [data-switch-worldline]").count() == 0
                assert page.locator("#worldline-list [data-compare-worldline]").count() == 0
                page.keyboard.press("Escape")
                assert page.locator("#worldline-panel").is_hidden()
                focus = page.locator("#stage-focus-toggle")
                focus.click()
                assert focus.get_attribute("aria-pressed") == "true"
                assert page.locator(".world-stage-hud").is_hidden()
                assert page.locator("#scene-visual-image").is_visible()
                focus.click()
                assert focus.get_attribute("aria-pressed") == "false"
                assert page.locator(".world-stage-hud").is_visible()
                assert page.locator("#observer-scene-explorer").is_visible()
                before_location = page.locator("#play-location").inner_text()
                deferred_stage_button = page.locator(
                    "#observer-scene-list [data-observer-generate]"
                ).first
                assert deferred_stage_button.count() == 1
                deferred_stage_name = deferred_stage_button.get_attribute("data-observer-generate")
                assert deferred_stage_name
                deferred_stage_button.click()
                generated_stage_button = page.locator(
                    f'#observer-scene-list [data-observer-scene="{deferred_stage_name}"]'
                )
                generated_stage_button.wait_for(state="visible")
                assert deferred_stage_name in page.locator("#scene-visual-caption").inner_text()
                assert "非此刻位置" in page.locator("#scene-visual-caption").inner_text()
                assert "原文证据" in page.locator("#scene-visual-caption").inner_text()
                assert (
                    "视觉生成器 procedural-svg@1.1.0"
                    in page.locator("#scene-visual-caption").inner_text()
                )
                assert "插画投影" in page.locator("#scene-visual-caption").inner_text()
                assert page.locator("#play-location").inner_text() == before_location
                assert page.locator("#send-action").is_disabled()
                scene_button = page.locator(
                    '#observer-scene-list [data-observer-scene]:not([data-observer-scene=""])'
                ).last
                preview_place = scene_button.get_attribute("data-observer-scene")
                assert preview_place
                scene_button.click()
                assert preview_place in page.locator("#scene-visual-caption").inner_text()
                assert "非此刻位置" in page.locator("#scene-visual-caption").inner_text()
                assert page.locator("#play-location").inner_text() == before_location
                assert page.locator("#send-action").is_disabled()
                page.locator('#observer-scene-list [data-observer-scene=""]').click()
                assert page.locator("#play-location").inner_text() == before_location
                page.locator("#world-stage").screenshot(
                    path=str(review / "observer-stage-desktop.png")
                )
                page.locator("#leave-world").click()
                page.wait_for_selector("#home-view.is-active")
                page.locator(f'#world-list [data-profile="{profile_id}"]').click()
                page.wait_for_selector("#detail-view.is-active")
                page.locator('input[name="character"]').check()
                page.locator("#enter-world").click()
                page.wait_for_selector("#play-view.is-active")
                page.wait_for_function(
                    "document.querySelector('#play-world-name')?.textContent === '江南机关城'"
                )
                scene_visual = page.locator("#scene-visual-image")
                assert scene_visual.is_visible()
                assert (scene_visual.get_attribute("src") or "").startswith(
                    "data:image/svg+xml;base64,"
                )
                stage = page.locator("#world-stage")
                assert page.locator("#observer-scene-explorer").is_hidden()
                assert stage.is_visible()
                stage_box = stage.bounding_box()
                visual_box = scene_visual.bounding_box()
                assert stage_box is not None and stage_box["height"] >= 600
                assert visual_box is not None
                assert visual_box["width"] >= stage_box["width"] * 0.9
                assert visual_box["height"] >= stage_box["height"] * 0.9
                assert page.locator(".world-stage-hud").is_visible()
                assert page.locator(".world-stage-story").is_visible()
                assert page.locator(".world-action-dock").is_visible()
                people_copy = page.locator("#people-list").inner_text()
                known_copy = page.locator("#known-people-list").inner_text()
                assert "Alice" not in people_copy
                assert "Bob" not in people_copy
                assert "Alice" not in known_copy
                assert "Bob" in known_copy
                assert "位置未核实" in known_copy
                assert "Beijing" not in people_copy
                assert "世界视觉预览" in page.locator("#scene-visual-caption").inner_text()
                page.locator("#world-stage").screenshot(
                    path=str(review / "embodied-stage-desktop.png")
                )
                page.locator("#action-input").fill("让自己保持清醒")
                page.locator("#send-action").click()
                page.wait_for_function("document.body.innerText.includes('清醒')")
                assert page.evaluate("typeof replayAt === 'function'") is True
                body_after_action = page.locator("body").inner_text()
                assert "世界变化" in body_after_action
                assert all(
                    forbidden not in body_after_action
                    for forbidden in ("state_hash", "event_id", "branch_id", "profile_id")
                )
                replay_button = page.locator("#chronicle-list [data-replay-time]").first
                assert replay_button.count() >= 1
                for attempt in range(2):
                    replay_button.click()
                    try:
                        page.wait_for_selector("#stage-replay-banner:not([hidden])", timeout=8000)
                        break
                    except Exception:
                        if attempt == 0:
                            continue
                        print("status:", page.locator("#status").inner_text())
                        print("page_errors:", page_errors)
                        raise
                assert "回看" in page.locator("#stage-replay-banner").inner_text()
                assert "世界时间" in page.locator("#stage-replay-banner").inner_text()
                assert page.locator("#play-mode").inner_text() == "历史回看"
                assert page.locator("#send-action").is_disabled()
                assert page.locator("#action-input").is_disabled()
                replay_copy = page.locator("body").inner_text()
                assert all(
                    forbidden not in replay_copy
                    for forbidden in ("state_hash", "event_id", "branch_id", "profile_id")
                )
                page.locator("#world-stage").screenshot(
                    path=str(review / "replay-stage-desktop.png")
                )
                page.locator("#stage-replay-exit").click()
                assert page.locator("#stage-replay-banner").is_hidden()
                assert not page.locator("#send-action").is_disabled()
                assert not page.locator("#action-input").is_disabled()
                assert page.locator("#play-mode").inner_text() == "角色体验"
                expand = page.locator("#chronicle-expand")
                assert expand.is_visible()
                expand.click()
                page.wait_for_function(
                    "document.querySelector('#chronicle-expand')?.textContent === '收起纪事'"
                )
                assert page.locator("#chronicle-list [data-replay-time]").count() >= 1
                expand.click()
                page.wait_for_function(
                    "document.querySelector('#chronicle-expand')?.textContent === '查看完整纪事'"
                )
                assert not page_errors, page_errors
                parent_instance = page.evaluate("model.instanceId")
                page.locator("#fork-worldline").click()
                page.wait_for_selector("#home-view.is-active")
                page.wait_for_function(
                    "document.querySelector('#status')?.textContent.includes('新世界线')"
                )
                forked_instance = page.evaluate(
                    "window.__WANXIANG_LAST_FORKED_WORLDLINE__?.instance_id"
                )
                assert forked_instance and forked_instance != parent_instance
                page.wait_for_selector("[data-continue]")
                page.locator('[data-filter="recent"]').click()
                assert page.locator("#world-list [data-profile]").count() == 1
                page.locator('[data-filter="all"]').click()
                page.locator("#continue-slot [data-continue]").click()
                page.wait_for_selector("#play-view.is-active")
                page.locator("#worldline-toggle").click()
                page.wait_for_selector("#worldline-panel:not([hidden])")
                assert page.locator("#worldline-list li").count() == 2
                page.keyboard.press("Escape")
                assert page.locator("#worldline-panel").is_hidden()
                assert page.evaluate("document.activeElement.id") == "worldline-toggle"
                page.locator("#worldline-toggle").click()
                page.wait_for_selector("#worldline-panel:not([hidden])")
                page.locator(f'[data-compare-worldline="{forked_instance}"]').click()
                page.wait_for_selector("#worldline-compare:not([hidden])")
                compare_copy = page.locator("#worldline-compare").inner_text()
                assert "共同历史" in compare_copy
                assert "分叉点" in compare_copy
                assert "revision" not in compare_copy
                assert "当前状态相同" in compare_copy
                assert "没有结构差异" in compare_copy
                assert "最近纪事" in compare_copy
                page.locator(f'[data-switch-worldline="{forked_instance}"]').click()
                page.wait_for_function(f'model.instanceId === "{forked_instance}"')
                page.wait_for_function(
                    "document.querySelector('#status')?.textContent.includes('已切换')"
                )
                third = _api(
                    page,
                    f"/experience/player/instances/{forked_instance}/fork",
                    "POST",
                    {},
                )
                third_instance = str(cast(dict[str, object], third["worldline"])["instance_id"])
                page.locator("#worldline-toggle").click()
                page.wait_for_selector("#worldline-panel:not([hidden])")
                assert page.locator("#worldline-list li").count() == 3
                page.locator(f'[data-switch-worldline="{third_instance}"]').click()
                page.wait_for_function(f'model.instanceId === "{third_instance}"')
                page.wait_for_function(
                    "document.querySelector('#status')?.textContent.includes('已切换')"
                )
                fourth = _api(
                    page,
                    f"/experience/player/instances/{third_instance}/fork",
                    "POST",
                    {},
                )
                fourth_instance = str(cast(dict[str, object], fourth["worldline"])["instance_id"])
                page.locator("#worldline-toggle").click()
                page.wait_for_selector("#worldline-panel:not([hidden])")
                assert page.locator("#worldline-list li").count() == 4
                page.locator(f'[data-switch-worldline="{fourth_instance}"]').click()
                page.wait_for_function(f'model.instanceId === "{fourth_instance}"')
                page.wait_for_function(
                    "document.querySelector('#status')?.textContent.includes('已切换')"
                )
                for _ in range(6):
                    _api(
                        page,
                        f"/experience/player/instances/{fourth_instance}/fork",
                        "POST",
                        {},
                    )
                page.locator("#worldline-toggle").click()
                page.wait_for_selector("#worldline-panel:not([hidden])")
                assert page.locator("#worldline-list li").count() == 10
                labels = page.locator("#worldline-list .worldline-copy strong").all_inner_texts()
                assert any(label.startswith("世界线 10") for label in labels)
                assert page.locator('#worldline-list li[data-current="true"]').count() == 1
                assert page.locator("#worldline-list .worldline-badge").count() == 1
                page.keyboard.press("Escape")
                assert page.locator("#worldline-panel").is_hidden()
                page.set_viewport_size({"width": 390, "height": 844})
                page.evaluate("window.scrollTo(0, 0)")
                page.wait_for_timeout(50)
                assert (
                    page.evaluate(
                        "getComputedStyle(document.querySelector('#stage-focus-toggle')).minHeight"
                    )
                    == "44px"
                )
                assert page.evaluate(
                    "getComputedStyle(document.querySelector('.world-action-dock')).paddingBottom"
                ) not in {"0px", ""}
                page.locator("#worldline-toggle").click()
                page.wait_for_selector("#worldline-panel:not([hidden])")
                assert page.locator("#worldline-list li").count() == 10
                mobile_panel_box = page.locator("#worldline-panel").bounding_box()
                assert mobile_panel_box is not None
                assert mobile_panel_box["width"] <= 390
                assert (
                    page.evaluate(
                        "getComputedStyle(document.querySelector('[data-compare-worldline]')).minHeight"
                    )
                    == "44px"
                )
                page.keyboard.press("Escape")
                assert page.locator("#worldline-panel").is_hidden()
                mobile_stage_box = page.locator("#world-stage").bounding_box()
                mobile_dock_box = page.locator(".world-action-dock").bounding_box()
                assert mobile_stage_box is not None
                assert mobile_dock_box is not None
                assert mobile_dock_box["y"] >= (
                    mobile_stage_box["y"] + mobile_stage_box["height"] - 2
                )
                page.locator("#world-stage").screenshot(
                    path=str(review / "embodied-stage-mobile.png")
                )
                mobile_focus = page.locator("#stage-focus-toggle")
                mobile_focus.click()
                assert page.locator(".world-stage-story").is_hidden()
                assert page.locator("#scene-visual-image").is_visible()
                page.locator("#world-stage").screenshot(
                    path=str(review / "focused-stage-mobile.png")
                )
                mobile_focus.click()
                assert page.locator(".world-stage-story").is_visible()
                mobile = browser.new_page(viewport={"width": 390, "height": 844})
                mobile.goto(f"{base}/", wait_until="networkidle")
                mobile.screenshot(path=str(review / "mobile.png"), full_page=True)
                mobile.close()
            finally:
                browser.close()
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        assert not thread.is_alive()


@pytest.mark.e2e
def test_player_place_list_paginates_many_source_places(persist_db_path: pathlib.Path) -> None:
    places = [f"Site{chr(65 + index // 26)}{chr(65 + index % 26)}" for index in range(40)]
    content = (
        "# Chapter\nCharacter: Alice\n"
        + "".join(f"Alice arrived in {place}.\n" for place in places)
        + "rule: visitors register\n"
    )
    server, thread, base = _start(persist_db_path)
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 390, "height": 844})
                page_errors: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.goto(f"{base}/", wait_until="domcontentloaded")
                _api(
                    page,
                    "/studio/one-click",
                    "POST",
                    {
                        "job_id": "m95_many_places",
                        "profile": "book",
                        "semantic_provider": "local",
                        "sources": [
                            {
                                "source_id": "m95_many_places_source",
                                "kind": "text",
                                "content": content,
                                "stage": "E3",
                                "rights_approved": True,
                                "access": "private",
                                "private_analysis_allowed": True,
                                "package_inclusion_allowed": True,
                                "public_export_allowed": False,
                                "training_allowed": False,
                            }
                        ],
                    },
                )
                profile = _api(
                    page,
                    "/studio/jobs/m95_many_places/playable-profile",
                    "POST",
                    {
                        "owner_id": "studio",
                        "visibility": "public",
                        "display_name": "四十桥世界",
                        "description": "由四十个来源地点组成的测试世界。",
                    },
                )
                profile_id = str(cast(dict[str, object], profile["profile"])["profile_id"])
                page.reload(wait_until="networkidle")
                page.locator(f'#world-list [data-profile="{profile_id}"]').click()
                page.wait_for_selector("#detail-view.is-active")
                page.wait_for_selector("#visual-places .visual-place")
                assert page.locator("#visual-places .visual-place").count() == 36
                more = page.locator("#visual-place-more")
                assert more.is_visible()
                assert "还有 4 个" in more.inner_text()
                more.click()
                page.wait_for_function(
                    "document.querySelectorAll('#visual-places .visual-place').length === 40"
                )
                assert more.is_hidden()
                assert not page_errors, page_errors
            finally:
                browser.close()
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        assert not thread.is_alive()


@pytest.mark.e2e
def test_player_history_loads_earlier_pages_in_browser(persist_db_path: pathlib.Path) -> None:
    source = {
        "source_id": "m95_history_pages_source",
        "kind": "text",
        "content": (
            "# Chapter\nCharacter: Alice\nAlice arrived in Beijing in 1985.\n"
            "rule: visitors register\n"
        ),
        "stage": "E3",
        "rights_approved": True,
        "access": "private",
        "private_analysis_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": False,
        "training_allowed": False,
    }
    server, thread, base = _start(persist_db_path)
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000})
                page_errors: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.goto(f"{base}/", wait_until="domcontentloaded")
                _api(
                    page,
                    "/studio/one-click",
                    "POST",
                    {
                        "job_id": "m95_history_pages",
                        "profile": "book",
                        "semantic_provider": "local",
                        "sources": [source],
                    },
                )
                profile = _api(
                    page,
                    "/studio/jobs/m95_history_pages/playable-profile",
                    "POST",
                    {
                        "owner_id": "studio",
                        "visibility": "public",
                        "display_name": "长史世界",
                    },
                )
                profile_id = str(cast(dict[str, object], profile["profile"])["profile_id"])
                _api(
                    page,
                    "/experience/player/characters",
                    "POST",
                    {
                        "display_name": "沈砚",
                        "character_id": "ent_alice",
                        "compatible_profile_ids": [profile_id],
                        "identity": "守夜人",
                    },
                )
                entered = _api(
                    page,
                    f"/experience/player/worlds/{profile_id}/enter",
                    "POST",
                    {
                        "mode": "embodiment",
                        "session_id": "history_pages_session",
                        "character_id": "ent_alice",
                    },
                )
                instance = str(entered["instance_id"])
                for index in range(51):
                    _api(
                        page,
                        f"/experience/player/instances/{instance}/action",
                        "POST",
                        {"text": ("让自己保持清醒" if index % 2 == 0 else "让自己保持平静")},
                    )

                page.reload(wait_until="networkidle")
                page.locator("#continue-slot [data-continue]").click()
                page.wait_for_selector("#play-view.is-active")
                page.locator("#chronicle-expand").click()
                page.wait_for_function(
                    "document.querySelectorAll('#chronicle-list [data-replay-time]').length >= 50"
                )
                total = int(page.evaluate("Number(model.history.total)"))
                assert total > 50
                more = page.locator("#chronicle-more")
                assert more.is_visible()
                more.click()
                page.wait_for_function(
                    "document.querySelectorAll('#chronicle-list [data-replay-time]').length ==="
                    f" {total}"
                )
                assert more.is_hidden()
                times = cast(
                    list[int],
                    page.evaluate(
                        "[...document.querySelectorAll('#chronicle-list [data-replay-time]')]"
                        ".map(node=>Number(node.dataset.replayTime))"
                    ),
                )
                assert times == sorted(times, reverse=True)
                assert len(set(times)) == len(times)
                assert not page_errors, page_errors
            finally:
                browser.close()
    finally:
        server.should_exit = True
        thread.join(timeout=10)
        assert not thread.is_alive()
