"""G97E: browser-driven Studio, Workshop, and playable-world qualification."""

from __future__ import annotations

import json
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

_SOURCE_TEXT = (
    "# G97E browser source\nCharacter: Alice\nCharacter: Bob\n"
    "Alice arrived in Beijing in 1985.\nBob visited Beijing.\n"
    "relationship: Alice -> Bob\nrule: visitors register\n"
)


def _source_payload(source_id: str) -> dict[str, object]:
    return {
        "source_id": source_id,
        "kind": "text",
        "content": _SOURCE_TEXT + "\nWorkshop qualification path.\n",
        "version": "1",
        "stage": "E3",
        "owner": "g97e",
        "usage": "qualification",
        "rights_approved": True,
        "access": "private",
        "private_analysis_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": False,
        "training_allowed": False,
        "provenance": "synthetic:g97e-browser",
    }


def _browser_json(
    page: Page,
    path: str,
    *,
    method: str = "GET",
    body: dict[str, object] | None = None,
    headers: dict[str, str] | None = None,
    expected_status: int = 200,
) -> dict[str, Any]:
    request_headers = dict(headers or {})
    if body is not None:
        request_headers.setdefault("content-type", "application/json")
    result = cast(
        dict[str, Any],
        page.evaluate(
            """
            async ({path, method, body, headers}) => {
              const init = {method, headers: headers ?? {}};
              if (body !== null) init.body = JSON.stringify(body);
              const response = await fetch(path, init);
              return {status: response.status, body: await response.json()};
            }
            """,
            {"path": path, "method": method, "body": body, "headers": request_headers},
        ),
    )
    assert result["status"] == expected_status, result
    return cast(dict[str, Any], result["body"])


def _wait_output(page: Page, marker: str) -> str:
    page.wait_for_function(
        "marker => (document.getElementById('out')?.textContent ?? '').includes(marker)",
        arg=marker,
        timeout=30_000,
    )
    return page.locator("#out").text_content() or ""


def _launch_browser(browser_type: BrowserType) -> Browser:
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
    if executable is not None:
        return browser_type.launch(headless=True, executable_path=str(executable))
    return browser_type.launch(headless=True)


def _start_server(persist_db_path: pathlib.Path) -> tuple[uvicorn.Server, Thread, str]:
    runtime = make_world_runtime(
        persist_db_path,
        extra_resolvers=register_preview_resolvers,
    )
    config = uvicorn.Config(
        create_app(runtime),
        host="127.0.0.1",
        port=0,
        log_level="error",
    )
    server = uvicorn.Server(config)
    thread = Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + 15
    while not server.started and time.monotonic() < deadline:
        time.sleep(0.02)
    if not server.started or not server.servers:
        server.should_exit = True
        thread.join(timeout=5)
        raise RuntimeError("uvicorn did not start on an OS-selected port")
    servers = cast(Any, server.servers)
    port = int(servers[0].sockets[0].getsockname()[1])
    return server, thread, f"http://127.0.0.1:{port}"


@pytest.mark.e2e
def test_browser_drives_studio_workshop_and_private_playable_world(
    persist_db_path: pathlib.Path,
) -> None:
    server, server_thread, base = _start_server(persist_db_path)
    job_id = "job_g97e_browser"
    user_headers = {"X-Wanxiang-User": "studio"}
    try:
        with sync_playwright() as playwright:
            browser = _launch_browser(playwright.chromium)
            try:
                page = browser.new_page()
                page.goto(f"{base}/studio/ui", wait_until="domcontentloaded")
                assert page.title() == "Wanxiang Studio"
                assert page.get_by_role("heading", name="Playable World").is_visible()
                assert page.get_by_role("button", name="World Plaza").is_visible()

                page.locator("#job").fill(job_id)
                page.locator("#provider").fill("")
                page.locator("#source").fill(_SOURCE_TEXT)
                page.get_by_role("button", name="Run authoring").click()
                _wait_output(page, job_id)

                draft = _browser_json(page, f"/studio/jobs/{job_id}/draft")
                draft_body = cast(dict[str, Any], draft["draft"])
                assert float(draft_body["coverage"]) > 0.0
                assert draft_body["unresolved_rights"] == []

                page.get_by_role("button", name="Build").click()
                _wait_output(page, '"package_id"')
                page.get_by_role("button", name="Preview").click()
                _wait_output(page, '"preview_id"')
                published = _browser_json(page, f"/studio/jobs/{job_id}/publish", method="POST")
                assert published["publishable"] is True

                workshop = _browser_json(page, "/workshop")
                assert set(cast(list[object], workshop["creation_modes"])) == {
                    "source",
                    "prompt",
                    "hybrid",
                }
                workshop_result = _browser_json(
                    page,
                    "/workshop/from-source",
                    method="POST",
                    body={
                        "workshop_id": "g97e_browser_workshop",
                        "owner_id": "studio",
                        "profile": "book",
                        "visibility": "private",
                        "display_name": "Browser Private World",
                        "semantic_provider": "local_semantic_v1",
                        "sources": [_source_payload("g97e_browser_workshop_source")],
                    },
                    expected_status=201,
                )
                private_profile = cast(dict[str, Any], workshop_result["playable_profile"])
                profile_id = str(private_profile["profile_id"])
                assert private_profile["visibility"] == "private"
                assert workshop_result["publishing"]["publishable"] is True

                character = _browser_json(
                    page,
                    "/experience/characters",
                    method="POST",
                    headers={**user_headers, "content-type": "application/json"},
                    body={
                        "display_name": "Alice",
                        "character_id": "ent_alice",
                        "compatible_profile_ids": [profile_id],
                    },
                    expected_status=201,
                )
                assert character["character_id"] == "ent_alice"

                owner_plaza = _browser_json(page, "/experience/plaza", headers=user_headers)
                owner_worlds = cast(list[object], owner_plaza["my_worlds"])
                assert profile_id in {
                    str(cast(dict[str, Any], card)["profile_id"]) for card in owner_worlds
                }
                guest_plaza = _browser_json(
                    page,
                    "/experience/plaza",
                    headers={"X-Wanxiang-User": "guest"},
                )
                guest_worlds = cast(list[object], guest_plaza["worlds"])
                assert profile_id not in {
                    str(cast(dict[str, Any], card)["profile_id"]) for card in guest_worlds
                }

                page.locator("#playProfile").fill(profile_id)
                page.locator("#playCharacter").fill("ent_alice")
                page.locator("#playSession").fill("g97e_browser_session")
                page.locator("#playAction").fill("set status to awake")
                page.get_by_role("button", name="Enter playable world").click()
                entered_text = _wait_output(page, '"instance_id"')
                entered = cast(dict[str, Any], json.loads(entered_text))
                instance_id = str(cast(dict[str, Any], entered["instance"])["instance_id"])

                page.get_by_role("button", name="Free action").click()
                action_text = _wait_output(page, '"event_id"')
                action = cast(dict[str, Any], json.loads(action_text))
                assert action["proposal"]["status"] == "proposed"
                assert action["diff"]["no_change"] is False
                assert action["event_id"]

                page.get_by_role("button", name="Leave").click()
                _wait_output(page, '"left"')
                page.get_by_role("button", name="Continue").click()
                continued_text = _wait_output(page, '"state_hash"')
                continued = cast(dict[str, Any], json.loads(continued_text))
                continued_instance = cast(dict[str, Any], continued["instance"])
                assert continued_instance["instance_id"] == instance_id
                assert continued["state_hash"] == action["state_hash"]

                responses = {
                    "draft": draft,
                    "published": published,
                    "workshop": workshop_result,
                    "owner_plaza": owner_plaza,
                    "guest_plaza": guest_plaza,
                    "action": action,
                    "continued": continued,
                }
                assert _SOURCE_TEXT not in json.dumps(responses, ensure_ascii=False)
            finally:
                browser.close()
    finally:
        server.should_exit = True
        server_thread.join(timeout=10)
        assert not server_thread.is_alive()
