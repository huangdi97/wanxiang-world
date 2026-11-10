"""Multi-source bundles must meet the raised coverage bar (intended policy).

Decision recorded 2026-11-04: adding a source to a bundle legitimately raises the
required capability set, so a bundle whose combined evidence does not cover it is
refused at compile time (`ZERO_COVERAGE`) instead of silently becoming a world.
This spec pins that policy: the same text compiles as one source, is refused when
split into a bundle that under-covers, and compiles again when concatenated.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import pathlib
from typing import Any, cast

import pytest
from playwright.sync_api import sync_playwright
from tests.integration.test_m95_player_experience_browser import _launch, _start

BOOK = (
    "# Chapter\nCharacter: Alice\nCharacter: Bob\n"
    "Alice arrived in Garden in 1985.\n"
    "Alice visited Harbor.\n"
    "Alice walked from Garden to Harbor.\n"
    "relationship: Alice -> Bob\nrule: visitors register\n"
)
NOTES = (
    "# Travel notes\nCharacter: Alice\n"
    "Alice visited Garden.\n"
    "Alice walked from Harbor to Garden.\n"
    "rule: visitors register\n"
)


def _source(source_id: str, content: str) -> dict[str, object]:
    return {
        "source_id": source_id,
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


def _one_click(page: Any, job_id: str, sources: list[dict[str, object]]) -> dict[str, Any]:
    return cast(
        dict[str, Any],
        page.evaluate(
            """async ({job, sources}) => {
              const response = await fetch('/studio/one-click', {
                method: 'POST',
                headers: {'content-type': 'application/json', 'x-wanxiang-user': 'studio'},
                body: JSON.stringify({
                  job_id: job, profile: 'book', semantic_provider: 'local', sources
                })
              });
              return {status: response.status, body: await response.json()};
            }""",
            {"job": job_id, "sources": sources},
        ),
    )


@pytest.mark.e2e
def test_bundle_must_cover_what_its_extra_source_requires(
    persist_db_path: pathlib.Path,
) -> None:
    server, _thread, base = _start(persist_db_path)
    try:
        with sync_playwright() as playwright:
            browser = _launch(playwright.chromium)
            try:
                page = browser.new_page(viewport={"width": 1280, "height": 800})
                page.goto(f"{base}/", wait_until="domcontentloaded")

                single = _one_click(
                    page,
                    "svw_cov_single",
                    [_source("svw_cov_single_src", BOOK + "Alice visited MarkerSingle.\n")],
                )
                assert single["status"] == 201, single

                concatenated = _one_click(
                    page,
                    "svw_cov_concat",
                    [
                        _source(
                            "svw_cov_concat_src",
                            BOOK + NOTES + "Alice visited MarkerConcat.\n",
                        )
                    ],
                )
                assert concatenated["status"] == 201, concatenated

                bundle = _one_click(
                    page,
                    "svw_cov_bundle",
                    [_source("svw_cov_book", BOOK), _source("svw_cov_notes", NOTES)],
                )
                # Refused, with a typed reason instead of a silently thinner world.
                assert bundle["status"] == 422, bundle
                body = cast(dict[str, Any], bundle["body"])
                assert body["code"] == "contract_error"
                assert "COMPLETION_REQUIRED" in str(body["message"])
                assert cast(dict[str, Any], body["details"])["product_state"] == "ZERO_COVERAGE"
            finally:
                browser.close()
    finally:
        server.should_exit = True
