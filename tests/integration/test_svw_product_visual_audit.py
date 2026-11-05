"""Visual audit of the real Player product across viewports (SVW evidence).

This is evidence generation, not a subjective verdict: it boots the real server,
seeds a source-grounded world, walks every player surface and records measured
facts (console errors, horizontal overflow, touch-target sizes, image alt
coverage) next to the screenshots. Human immersion judgement stays separate.
"""

# ruff: noqa: E501
from __future__ import annotations

import json
import os
import pathlib
import time
from threading import Thread
from typing import Any, cast

import pytest
from playwright.sync_api import Browser, Page, sync_playwright
from tests.conftest import make_world_runtime
from wanxiang_api.app import create_app
from wanxiang_substrate.preview.runtime import register_preview_resolvers

AUDIT_DIR = pathlib.Path(
    os.environ.get("WANXIANG_VISUAL_AUDIT_DIR", "CURRENT_PRODUCT_VISUAL_AUDIT")
)
HEADERS = {"content-type": "application/json", "x-wanxiang-user": "studio"}
VIEWPORTS: dict[str, dict[str, int]] = {
    "desktop": {"width": 1440, "height": 1000},
    "laptop": {"width": 1280, "height": 800},
    "mobile": {"width": 390, "height": 844},
    "small": {"width": 320, "height": 720},
}
CANONICAL_DESKTOP = (
    "home",
    "world-detail",
    "atlas",
    "observer",
    "embodiment",
    "focus-mode",
    "history",
    "worldline",
    "t2",
    "t3",
)
CANONICAL_MOBILE = (
    "home",
    "world-detail",
    "observer",
    "embodiment",
    "focus",
    "history",
    "t2",
    "t3",
)
INTERACTIVE = "button,a[href],input,select,summary,textarea"
SOURCE_CONTENT = (
    "# Chapter One\nThe lantern keeper walked the harbour wall.\n"
    "Character: 沈砚\nCharacter: 阿箬\nCharacter: 老桥\n"
    "沈砚 来到江南城。\n沈砚 来到机关桥。\n阿箬 来到望月亭。\n"
    "沈砚 来到潮汐港。\n老桥 来到青石巷。\n沈砚 来到沉水巷。\n"
    "沈砚 来到潮汐门。\n阿箬 来到书院。\n老桥 来到盐仓。\n"
    "沈砚 arrived in 石桥. 阿箬 arrived in 花园. 老桥 arrived in 市集.\n"
    "relationship: 沈砚 -> 阿箬\nrule: visitors register at the gate\n"
)
SOURCE = {
    "source_id": "svw_visual_audit_source",
    "kind": "text",
    "content": SOURCE_CONTENT,
    "stage": "E3",
    "rights_approved": True,
    "access": "private",
    "private_analysis_allowed": True,
    "package_inclusion_allowed": True,
    "public_export_allowed": False,
    "training_allowed": False,
}

MEASURE = """
(() => {
  const viewport = {w: window.innerWidth, h: window.innerHeight};
  const controls = Array.from(document.querySelectorAll(
    'button,a[href],input,select,summary,textarea'
  )).filter(node => {
    const rect = node.getBoundingClientRect();
    const style = getComputedStyle(node);
    return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
  });
  const small = controls.filter(node => node.getBoundingClientRect().height < 44).length;
  const images = Array.from(document.images);
  return {
    viewport,
    docScrollWidth: document.documentElement.scrollWidth,
    bodyScrollWidth: document.body.scrollWidth,
    controls: controls.length,
    controlsUnder44: small,
    images: images.length,
    imagesWithoutAlt: images.filter(node => !node.getAttribute('alt')).length,
    stageHeight: Math.round((document.querySelector('#world-stage')?.getBoundingClientRect().height) || 0),
    observerGateVisible: Boolean(document.querySelector('#observer-gate')?.checkVisibility?.()),
    actionInputDisabled: Boolean(document.querySelector('#action-input')?.disabled),
    locale: document.documentElement.lang,
  };
})()
"""


def _start(path: pathlib.Path) -> tuple[Any, Thread, str]:
    runtime = make_world_runtime(path, extra_resolvers=register_preview_resolvers)
    import uvicorn

    server = uvicorn.Server(
        uvicorn.Config(create_app(runtime), host="127.0.0.1", port=0, log_level="error")
    )
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 20
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.02)
    servers = cast(Any, server.servers)
    return server, thread, f"http://127.0.0.1:{int(servers[0].sockets[0].getsockname()[1])}"


def _seed(base: str) -> str:
    """Create the audited world through the same routes a client would call."""

    import httpx

    client = httpx.Client(base_url=base, headers=HEADERS, timeout=300.0)
    created = client.post(
        "/studio/one-click",
        json={
            "job_id": "svw_visual_audit_job",
            "profile": "book",
            "semantic_provider": "local",
            "sources": [SOURCE],
        },
    )
    assert created.status_code < 300, created.text
    profile = client.post(
        "/studio/jobs/svw_visual_audit_job/playable-profile",
        json={
            "owner_id": "studio",
            "visibility": "public",
            "display_name": "\u6c5f\u5357\u673a\u5173\u57ce",
            "description": "\u4e00\u5ea7\u6cbf\u6c34\u9053\u5c55\u5f00\u7684\u673a\u5173\u57ce\uff0c\u673a\u5173\u4e0e\u4eba\u60c5\u90fd\u4ece\u6e05\u6668\u5f00\u59cb\u3002",
            "scenario_name": "\u6f6e\u6c50\u95e8\u521d\u542f",
            "opening_hint": "\u5148\u542c\u4e00\u542c\u57ce\u95e8\u5185\u5916\u7684\u6c34\u58f0\uff0c\u518d\u51b3\u5b9a\u5f80\u54ea\u91cc\u8d70\u3002",
        },
    )
    assert profile.status_code < 300, profile.text
    profile_id = str(profile.json()["profile"]["profile_id"])
    character = client.post(
        "/experience/player/characters",
        json={
            "display_name": "\u6c88\u781a",
            "character_id": "ent_alice",
            "compatible_profile_ids": [profile_id],
            "identity": "\u5b88\u591c\u4eba",
            "intro": "\u719f\u6089\u57ce\u95e8\u4e0e\u6c34\u9053\u7684\u5b88\u591c\u4eba\u3002",
            "stance": "\u8c28\u614e\u89c2\u5bdf",
            "starting_location": "\u6c89\u6c34\u5df7",
            "knowledge_boundary": "\u53ea\u77e5\u9053\u81ea\u5df1\u4eb2\u773c\u89c1\u8fc7\u7684\u4e8b\u3002",
        },
    )
    assert character.status_code < 300, character.text
    return profile_id


def _launch(browser_type: Any) -> Browser:
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


def _shot(page: Page, name: str, *, full: bool = False) -> None:
    AUDIT_DIR.joinpath("screenshots").mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(AUDIT_DIR / "screenshots" / f"{name}.png"), full_page=full)


def _capture(page: Page, audit: dict[str, Any], name: str, surface: str, viewport: str) -> None:
    _shot(page, name)
    record = page.evaluate(MEASURE)
    record.update(
        {"file": f"screenshots/{name}.png", "surface": surface, "viewportLabel": viewport}
    )
    audit["captures"].append(record)


def _element_shot(
    page: Page, selector: str, name: str, audit: dict[str, Any], surface: str, viewport: str
) -> None:
    locator = page.locator(selector)
    AUDIT_DIR.joinpath("screenshots").mkdir(parents=True, exist_ok=True)
    if locator.count() and locator.first.is_visible():
        locator.first.screenshot(path=str(AUDIT_DIR / "screenshots" / f"{name}.png"))
    else:
        _shot(page, name)
    record = page.evaluate(MEASURE)
    record.update(
        {"file": f"screenshots/{name}.png", "surface": surface, "viewportLabel": viewport}
    )
    audit["captures"].append(record)


def _walk(
    page: Page, base: str, audit: dict[str, Any], viewport: str, surfaces: tuple[str, ...]
) -> None:
    page.goto(base, wait_until="domcontentloaded")
    page.wait_for_timeout(2200)
    if "home" in surfaces:
        _capture(page, audit, f"home-{viewport}", "home", viewport)
    page.locator("#world-list [data-profile]").first.click()
    page.wait_for_timeout(1400)
    if "world-detail" in surfaces:
        _capture(page, audit, f"world-detail-{viewport}", "world-detail", viewport)
    if "atlas" in surfaces:
        _element_shot(page, "#visual-gallery-wrap", f"atlas-{viewport}", audit, "atlas", viewport)
    for tier in ("t2", "t3"):
        if tier not in surfaces:
            continue
        panel = "#panorama-upgrade-panel" if tier == "t2" else "#spatial-upgrade-panel"
        _element_shot(
            page, panel, f"{tier}-contract-{viewport}", audit, f"{tier}-contract", viewport
        )
    if "observer" in surfaces:
        page.locator("#enter-observer").click()
        page.wait_for_timeout(2200)
        _capture(page, audit, f"observer-{viewport}", "observer", viewport)
        page.locator("#leave-world").click()
        page.wait_for_timeout(1400)
    if "embodiment" in surfaces or "focus-mode" in surfaces or "focus" in surfaces:
        page.locator("#world-list [data-profile]").first.click()
        page.wait_for_timeout(1200)
        radios = page.locator('input[name="character"]')
        if radios.count():
            radios.first.check()
        page.locator("#enter-world").click()
        page.wait_for_timeout(2400)
        if "embodiment" in surfaces:
            _capture(page, audit, f"embodiment-{viewport}", "embodiment", viewport)
        focus = "focus-mode" if "focus-mode" in surfaces else "focus"
        if focus in surfaces and page.locator("#stage-focus-toggle").is_enabled():
            page.locator("#stage-focus-toggle").click()
            page.wait_for_timeout(800)
            _capture(page, audit, f"{focus}-{viewport}", focus, viewport)
            page.locator("#stage-focus-toggle").click()
            page.wait_for_timeout(600)
        if "history" in surfaces:
            expand = page.locator("#chronicle-expand")
            if expand.is_visible():
                expand.click()
                page.wait_for_timeout(1500)
            _capture(page, audit, f"history-{viewport}", "history", viewport)
        if "worldline" in surfaces:
            page.locator("#worldline-toggle").click()
            page.wait_for_timeout(1200)
            _capture(page, audit, f"worldline-{viewport}", "worldline", viewport)
            page.locator("#worldline-close").click()
            page.wait_for_timeout(400)
        if page.locator("#leave-world").is_visible():
            page.locator("#leave-world").click()
            page.wait_for_timeout(1200)


def _write_index(audit: dict[str, Any]) -> None:
    lines = [
        "# Current product visual audit",
        "",
        "Screenshots captured from the real server (uvicorn + Chrome) over a "
        "source-grounded world. Measured facts live in `audit.json`; the human",
        "immersion verdict remains `WAITING_HUMAN`.",
        "",
        "| file | surface | viewport | controls < 44px | horizontal overflow | console errors |",
        "|---|---|---|---|---|---|",
    ]
    for record in audit["captures"]:
        overflow = record["docScrollWidth"] - record["viewport"]["w"]
        lines.append(
            "| `{file}` | {surface} | {w}x{h} | {small} | {overflow} | {errors} |".format(
                file=record["file"],
                surface=record["surface"],
                w=record["viewport"]["w"],
                h=record["viewport"]["h"],
                small=record["controlsUnder44"],
                overflow=overflow,
                errors=len(record.get("pageErrors", [])),
            )
        )
    lines.append("")
    lines.append(f"Totals: {len(audit['captures'])} captures.")
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    (AUDIT_DIR / "SCREENSHOT_INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


@pytest.mark.e2e
def test_product_visual_audit_across_viewports(persist_db_path: pathlib.Path) -> None:
    server, _thread, base = _start(persist_db_path)
    audit: dict[str, Any] = {"captures": [], "head": _head()}
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                for viewport, size in VIEWPORTS.items():
                    errors: list[str] = []
                    page = browser.new_page(viewport=cast(Any, size), locale="zh-CN")
                    page.on("pageerror", lambda error, sink=errors: sink.append(str(error)))
                    surfaces = (
                        CANONICAL_DESKTOP if viewport in {"desktop", "laptop"} else CANONICAL_MOBILE
                    )
                    _seed(base)
                    start = len(audit["captures"])
                    _walk(page, base, audit, viewport, surfaces)
                    for record in audit["captures"][start:]:
                        record["pageErrors"] = list(errors)
                    page.close()
            finally:
                browser.close()
    finally:
        server.should_exit = True
    _write_index(audit)
    (AUDIT_DIR / "audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    assert len(audit["captures"]) >= len(CANONICAL_DESKTOP) + 1
    assert all(
        record["docScrollWidth"] <= record["viewport"]["w"] + 1 for record in audit["captures"]
    ), [
        record for record in audit["captures"] if record["docScrollWidth"] > record["viewport"]["w"]
    ]


def _head() -> str:
    import subprocess

    result = subprocess.run(
        ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=False
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"
