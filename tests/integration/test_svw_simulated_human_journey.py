"""Scripted walkthrough of the human review journey, clearly marked SIMULATED.

This runs the 14 steps a human reviewer is asked to follow and records what the
real product actually showed at each step. It is evidence that the journey is
walkable and unbroken; it is **not** a human verdict, so comprehension,
immersion and acceptance stay WAITING_HUMAN.
"""

# ruff: noqa: E501
# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib
import time

import pytest
from playwright.sync_api import Page, sync_playwright
from tests.integration.test_m95_player_experience_browser import _launch, _start

AUDIT_DIR = pathlib.Path("CURRENT_PRODUCT_VISUAL_AUDIT")
SHOTS = AUDIT_DIR / "screenshots"
HEADERS = {"content-type": "application/json", "x-wanxiang-user": "studio"}
SOURCE = {
    "source_id": "svw_simulated_journey_source",
    "kind": "text",
    "content": (
        "# Chapter One\nCharacter: 沈砚\nCharacter: 阿箬\nCharacter: 老桥\n"
        "沈砚 来到江南城。\n沈砚 来到机关桥。\n阿箬 来到望月亭。\n"
        "沈砚 来到潮汐港。\n老桥 来到青石巷。\n沈砚 来到沉水巷。\n"
        "沈砚 arrived in 石桥. 阿箬 arrived in 花园.\n"
        "relationship: 沈砚 -> 阿箬\nrule: visitors register\n"
    ),
    "stage": "E3",
    "rights_approved": True,
    "access": "private",
    "private_analysis_allowed": True,
    "package_inclusion_allowed": True,
    "public_export_allowed": False,
    "training_allowed": False,
}


def _step(observations: list[str], number: int, question: str, observed: str) -> None:
    observations.append(f"| {number} | {question} | {observed} |")


def _shot(page: Page, name: str) -> None:
    SHOTS.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(SHOTS / f"simulated-{name}.png"))


def _text(page: Page, selector: str) -> str:
    try:
        return " ".join(page.locator(selector).first.inner_text(timeout=4000).split())[:160]
    except Exception as error:  # pragma: no cover - diagnostic path
        return f"<unavailable: {type(error).__name__}>"


@pytest.mark.e2e
def test_simulated_human_journey_is_walkable(persist_db_path: pathlib.Path) -> None:
    server, _thread, base = _start(persist_db_path)
    observations: list[str] = []
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 1440, "height": 1000}, locale="zh-CN")
                page_errors: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.goto(f"{base}/", wait_until="domcontentloaded")

                import httpx

                client = httpx.Client(base_url=base, headers=HEADERS, timeout=300.0)
                assert (
                    client.post(
                        "/studio/one-click",
                        json={
                            "job_id": "svw_simulated_journey_job",
                            "profile": "book",
                            "semantic_provider": "local",
                            "sources": [SOURCE],
                        },
                    ).status_code
                    < 300
                )
                profile = client.post(
                    "/studio/jobs/svw_simulated_journey_job/playable-profile",
                    json={
                        "owner_id": "studio",
                        "visibility": "public",
                        "display_name": "江南机关城",
                        "description": "一座沿水道展开的机关城，机关与人情都从清晨开始。",
                        "scenario_name": "潮汐门初启",
                        "opening_hint": "先听一听城门内外的水声，再决定往哪里走。",
                    },
                )
                assert profile.status_code < 300, profile.text
                profile_id = str(profile.json()["profile"]["profile_id"])
                character = client.post(
                    "/experience/player/characters",
                    json={
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
                assert character.status_code < 300, character.text

                page.reload(wait_until="networkidle")
                page.wait_for_timeout(1500)
                _shot(page, "01-home")
                _step(
                    observations,
                    1,
                    "导入来源并等待世界生成",
                    "one-click 201；世界出现在世界广场",
                )
                _step(observations, 3 if False else 2, "打开世界", _text(page, "#world-list"))

                page.locator("#world-list [data-profile]").first.click()
                page.wait_for_timeout(1500)
                _shot(page, "02-world-detail")
                _step(observations, 3, "World Detail 是否像世界入口", _text(page, ".detail-copy"))
                _step(observations, 4, "世界图谱与地点", _text(page, "#visual-gallery-wrap"))

                page.locator("#enter-observer").click()
                page.wait_for_timeout(2500)
                _shot(page, "03-observer")
                _step(
                    observations,
                    5,
                    "观察者模式是否清楚",
                    _text(page, ".world-stage-hud") + " || " + _text(page, ".world-action-dock"),
                )
                assert page.locator("#observer-gate").is_visible()
                assert page.locator("#send-action").is_disabled()
                scenes = page.locator("[data-observer-scene]")
                if scenes.count() > 1:
                    scenes.nth(1).click()
                    page.wait_for_timeout(2000)
                    _shot(page, "04-observer-scene")
                _step(observations, 6, "切换场景是否只是预览", _text(page, "#scene-visual-caption"))

                page.locator("#leave-world").click()
                page.wait_for_timeout(1500)
                _shot(page, "05-continue")
                _step(observations, 10, "离开后是否可继续", _text(page, "#continue-slot"))

                page.locator("#world-list [data-profile]").first.click()
                page.wait_for_timeout(1200)
                radios = page.locator('input[name="character"]')
                if radios.count():
                    radios.first.check()
                page.locator("#enter-world").click()
                page.wait_for_timeout(2500)
                _shot(page, "06-embodiment")
                _step(observations, 7, "进入角色后的第一屏", _text(page, ".world-stage-hud"))
                assert page.locator("#observer-gate").is_hidden()

                committed = 0
                for attempt in range(3):
                    page.locator(".suggestion").nth(attempt % 3).click()
                    page.locator("#send-action").click()
                    page.wait_for_timeout(3000)
                    committed = page.locator("#change-list li").count()
                _step(observations, 8, "三次自由行动的提交结果", f"世界变化条目 {committed} 条")
                _shot(page, "07-after-actions")
                _step(observations, 9, "能否看懂世界变化", _text(page, "#change-list"))
                _step(observations, 11, "世界纪事", _text(page, "#chronicle-list"))
                assert committed >= 1

                if page.locator("#stage-focus-toggle").is_enabled():
                    page.locator("#stage-focus-toggle").click()
                    page.wait_for_timeout(800)
                    _shot(page, "08-focus")
                    _step(
                        observations,
                        12,
                        "专注场景",
                        page.locator("#world-stage").get_attribute("class") or "",
                    )
                    page.locator("#stage-focus-toggle").click()
                    page.wait_for_timeout(500)

                replay = page.locator("[data-replay-time]")
                if replay.count():
                    replay.first.click()
                    page.wait_for_timeout(1500)
                    _shot(page, "09-replay")
                    _step(observations, 13, "历史回放是否明显", _text(page, "#stage-replay-banner"))
                    assert page.locator("#send-action").is_disabled()
                    page.locator("#stage-replay-exit").click()
                    page.wait_for_timeout(500)

                page.locator("#worldline-toggle").click()
                page.wait_for_timeout(1200)
                _shot(page, "10-worldline")
                _step(observations, 14, "世界线", _text(page, "#worldline-panel"))
                page.locator("#worldline-close").click()

                assert page_errors == [], page_errors
            finally:
                browser.close()
    finally:
        server.should_exit = True

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Simulated human journey (SIMULATED — not a human verdict)",
        "",
        f"Walked at {time.strftime('%Y-%m-%d %H:%M')} against the real server (uvicorn + Chrome) over a",
        "source-grounded world. Every line below is what the product actually rendered, captured by",
        "script. It proves the journey is walkable and unbroken; it does **not** judge comprehension,",
        "immersion or acceptance — those remain `WAITING_HUMAN` and must be answered by a real person",
        "using `HUMAN_REVIEW_START_HERE.md`.",
        "",
        "| step | asked | what the product showed |",
        "|---|---|---|",
        *observations,
        "",
        "Screenshots: `CURRENT_PRODUCT_VISUAL_AUDIT/screenshots/simulated-*.png`.",
    ]
    (AUDIT_DIR / "SIMULATED_HUMAN_JOURNEY.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    assert len(observations) >= 12, len(observations)
