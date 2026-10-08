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
        {"job_id": "m95_browser_job", "profile": "book", "sources": [source]},
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
                assert not page_errors, page_errors
                assert page.locator('input[name="character"]').count() == 1, page.locator(
                    "#detail-view"
                ).inner_html()
                assert "以此角色进入" in page.locator("#detail-view").inner_text()
                page.locator('input[name="character"]').check()
                page.locator("#enter-world").click()
                page.wait_for_function(
                    "document.querySelector('#play-world-name')?.textContent === '江南机关城'"
                )
                page.locator("#action-input").fill("让自己保持清醒")
                page.locator("#send-action").click()
                page.wait_for_function("document.body.innerText.includes('清醒')")
                body_after_action = page.locator("body").inner_text()
                assert "世界变化" in body_after_action
                assert all(
                    forbidden not in body_after_action
                    for forbidden in ("state_hash", "event_id", "branch_id", "profile_id")
                )
                page.locator("#leave-world").click()
                page.wait_for_selector("[data-continue]")
                page.locator('[data-filter="recent"]').click()
                assert page.locator("#world-list [data-profile]").count() == 1
                page.locator('[data-filter="all"]').click()
                page.locator("#continue-slot [data-continue]").click()
                page.wait_for_selector("#play-view.is-active")
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
