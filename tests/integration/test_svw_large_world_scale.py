"""A hundred-place source world stays bounded, searchable and unclipped.

Scale evidence for the Player: the place surface must render a bounded subset
with progressive reveal instead of one node per extracted place, search must
stay usable, and the narrow viewport must not scroll sideways.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
import pathlib
import time
from typing import Any, cast

import pytest
from playwright.sync_api import sync_playwright
from tests.integration.test_m95_player_experience_browser import _api, _launch, _start

PLACES = [f"Site{chr(65 + index // 26)}{chr(65 + index % 26)}" for index in range(100)]
PLACE_PAGE_LIMIT = 40
SEARCH_BUDGET_SECONDS = 5.0


def _content() -> str:
    return (
        "# Chapter\nCharacter: Alice\n"
        + "".join(f"Alice arrived in {place}.\n" for place in PLACES)
        + "Character: Bob\nBob arrived in Site000.\n"
        + "rule: visitors register\n"
    )


@pytest.mark.e2e
def test_hundred_place_world_stays_usable_on_a_narrow_viewport(
    persist_db_path: pathlib.Path,
) -> None:
    server, _thread, base = _start(persist_db_path)
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 320, "height": 720})
                page_errors: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.goto(f"{base}/", wait_until="domcontentloaded")
                _api(
                    page,
                    "/studio/one-click",
                    "POST",
                    {
                        "job_id": "svw_scale_job",
                        "profile": "book",
                        "semantic_provider": "local",
                        "sources": [
                            {
                                "source_id": "svw_scale_source",
                                "kind": "text",
                                "content": _content(),
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
                    "/studio/jobs/svw_scale_job/playable-profile",
                    "POST",
                    {
                        "owner_id": "studio",
                        "visibility": "public",
                        "display_name": "一百地点世界",
                        "description": "由一百个来源地点组成的规模测试世界。",
                    },
                )
                profile_id = str(cast(dict[str, Any], profile["profile"])["profile_id"])
                page.reload(wait_until="networkidle")
                page.locator(f'#world-list [data-profile="{profile_id}"]').click()
                page.wait_for_selector("#visual-places .visual-place")

                rendered = page.locator("#visual-places .visual-place").count()
                assert 0 < rendered <= PLACE_PAGE_LIMIT, rendered
                assert page.locator("#visual-place-more").is_visible()
                assert len(PLACES) > PLACE_PAGE_LIMIT

                started = time.monotonic()
                page.fill("#visual-place-search", "SiteDV")
                page.wait_for_timeout(200)
                assert page.locator("#visual-places .visual-place").count() == 1
                assert "SiteDV" in page.locator("#visual-places").inner_text()
                assert time.monotonic() - started < SEARCH_BUDGET_SECONDS

                assert (
                    page.evaluate("document.documentElement.scrollWidth")
                    <= page.evaluate("window.innerWidth") + 1
                )
                assert page_errors == []
            finally:
                browser.close()
    finally:
        server.should_exit = True


BIG_PEOPLE = [f"Person{chr(65 + index // 26)}{chr(65 + index % 26)}" for index in range(400)]
BIG_PLACES = [f"Site{chr(65 + index // 26)}{chr(65 + index % 26)}" for index in range(60)]
COMPILE_BUDGET_SECONDS = 60.0
PAYLOAD_BUDGET_BYTES = 400_000
INITIAL_SCENE_LIMIT = 3


def _big_content() -> str:
    return (
        "# Chapter\n"
        + "".join(f"Character: {person}\n" for person in BIG_PEOPLE)
        + "".join(f"{person} arrived in SiteAA.\n" for person in BIG_PEOPLE[:120])
        + "".join(f"PersonAA arrived in {place}.\n" for place in BIG_PLACES)
        + "".join(f"{person} met PersonAB in SiteAA.\n" for person in BIG_PEOPLE[:200])
        + "relationship: PersonAA -> PersonAB\nrule: visitors register\n"
    )


@pytest.mark.e2e
def test_large_entity_world_keeps_initial_visuals_bounded(
    persist_db_path: pathlib.Path,
) -> None:
    """A long source compiles fast and does not generate every scene upfront."""

    server, _thread, base = _start(persist_db_path)
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 320, "height": 720})
                page_errors: list[str] = []
                page.on("pageerror", lambda error: page_errors.append(str(error)))
                page.goto(f"{base}/", wait_until="domcontentloaded")
                started = time.monotonic()
                _api(
                    page,
                    "/studio/one-click",
                    "POST",
                    {
                        "job_id": "svw_entities_job",
                        "profile": "book",
                        "semantic_provider": "local",
                        "sources": [
                            {
                                "source_id": "svw_entities_source",
                                "kind": "text",
                                "content": _big_content(),
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
                compile_seconds = time.monotonic() - started
                profile = _api(
                    page,
                    "/studio/jobs/svw_entities_job/playable-profile",
                    "POST",
                    {
                        "owner_id": "studio",
                        "visibility": "public",
                        "display_name": "长文本世界",
                        "description": "由数百实体与数十地点组成的长来源世界。",
                    },
                )
                profile_id = str(cast(dict[str, Any], profile["profile"])["profile_id"])
                page.reload(wait_until="networkidle")
                page.locator(f'#world-list [data-profile="{profile_id}"]').click()
                page.wait_for_selector("#visual-places .visual-place")

                world = _api(page, f"/experience/player/worlds/{profile_id}")
                visual = cast(
                    dict[str, Any], cast(dict[str, Any], world["world"]).get("visual") or {}
                )
                places = cast(list[object], visual.get("places") or [])
                scenes = cast(list[object], visual.get("scenes") or [])

                assert compile_seconds < COMPILE_BUDGET_SECONDS, compile_seconds
                assert len(places) >= 50, len(places)
                # Bounded initial generation: a few key scenes, not one per place.
                assert 0 < len(scenes) <= INITIAL_SCENE_LIMIT, len(scenes)
                assert len(scenes) < len(places)
                assert len(json.dumps(world, ensure_ascii=False)) < PAYLOAD_BUDGET_BYTES
                assert page.locator("#visual-places .visual-place").count() <= PLACE_PAGE_LIMIT
                assert (
                    page.evaluate("document.documentElement.scrollWidth")
                    <= page.evaluate("window.innerWidth") + 1
                )
                assert page_errors == []
            finally:
                browser.close()
    finally:
        server.should_exit = True
