"""M95 remediation: Chinese Player projection over the real playable chain."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import json
from typing import Any, cast

import wanxiang_substrate.playable.player_i18n as player_i18n
from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app
from wanxiang_api.player_ui_asset import player_html

HEADERS = {"X-Wanxiang-User": "studio"}


def _source() -> dict[str, object]:
    return {
        "source_id": "m95_zh_projection_source",
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


def _client() -> Any:
    app = create_app(build_reference_runtime())
    client: Any = TestClient(app)
    response = client.post(
        "/studio/one-click",
        json={"job_id": "m95_zh_projection_job", "profile": "book", "sources": [_source()]},
    )
    assert response.status_code == 201
    profile = client.post(
        "/studio/jobs/m95_zh_projection_job/playable-profile",
        json={
            "owner_id": "studio",
            "visibility": "public",
            "display_name": "江南机关城",
            "description": "一座沿水道展开的机关城，机关与人情都从清晨开始。",
            "scenario_name": "潮汐门初启",
            "opening_hint": "先听一听城门内外的水声，再决定往哪里走。",
        },
    )
    assert profile.status_code == 200
    profile_id = str(profile.json()["profile"]["profile_id"])
    character = client.post(
        "/experience/player/characters",
        headers=HEADERS,
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
    assert character.status_code == 201
    return client


def test_player_projection_is_chinese_and_uses_committed_state_diff() -> None:
    client = _client()
    plaza = client.get("/experience/player/plaza", headers=HEADERS)
    assert plaza.status_code == 200
    world = cast(dict[str, Any], plaza.json()["worlds"][0])
    assert world["name"] == "江南机关城"
    assert world["description"].startswith("一座沿水道")
    assert world["status"] == "可以进入"
    assert world["counts"]["characters"] == 2
    assert world["is_public"] is True
    english_characters = client.get(
        "/experience/player/characters",
        headers={**HEADERS, "X-Wanxiang-Locale": "en-US"},
    )
    assert english_characters.status_code == 200
    assert english_characters.json()["locale"] == "en-US"
    profile_id = str(world["profile_id"])

    detail = client.get(f"/experience/player/worlds/{profile_id}", headers=HEADERS)
    assert detail.status_code == 200
    assert detail.json()["world"]["scenario"]["name"] == "潮汐门初启"
    assert detail.json()["characters"][0]["name"] == "沈砚"
    assert detail.json()["world"]["mode"] == "角色体验"
    assert detail.json()["world"]["setting"]["location"] == "Beijing"
    assert detail.json()["characters"][0]["knowledge_boundary"] == "只知道自己亲眼见过的事。"

    entered = client.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={"mode": "embodiment", "session_id": "m95_zh_session", "character_id": "ent_alice"},
    )
    assert entered.status_code == 200
    instance_id = str(entered.json()["instance_id"])
    assert entered.json()["view"]["player"]["name"] == "沈砚"

    action = client.post(
        f"/experience/player/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "让自己保持清醒"},
    )
    assert action.status_code == 200
    body = cast(dict[str, Any], action.json())
    assert body["status"] == "committed"
    assert body["changed"] is True
    changes = cast(list[dict[str, Any]], body["view"]["recent_changes"])
    assert any("清醒" in str(item["summary"]) for item in changes)
    assert body["view"]["time"]["ticks"] > 0
    assert "state_hash" not in json.dumps(body["view"], ensure_ascii=False)
    assert "event_id" not in json.dumps(body["view"], ensure_ascii=False)

    left = client.post(f"/experience/player/instances/{instance_id}/leave", headers=HEADERS)
    assert left.status_code == 200
    continuation = client.get("/experience/player/plaza", headers=HEADERS).json()["continue"]
    assert continuation["instance_id"] == instance_id
    assert continuation["status"] == "saved"
    assert continuation["last_location"] == "沉水巷"
    assert continuation["leave_time"]["ticks"] > 0
    assert continuation["events_since_leave"] == []
    assert continuation["last_change"]["summary"]
    resumed_plaza = client.get("/experience/player/plaza", headers=HEADERS).json()
    assert resumed_plaza["worlds"][0]["can_continue"] is True
    assert resumed_plaza["worlds"][0]["status"] == "可继续"
    resumed = client.post(f"/experience/player/instances/{instance_id}/continue", headers=HEADERS)
    assert resumed.status_code == 200
    assert resumed.json()["view"]["player"]["name"] == "沈砚"


def test_player_lease_conflict_is_structured_and_not_reported_as_network_failure() -> None:
    client = _client()
    plaza = client.get("/experience/player/plaza", headers=HEADERS)
    profile_id = str(plaza.json()["worlds"][0]["profile_id"])
    first = client.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={"mode": "embodiment", "session_id": "m95_lease_first", "character_id": "ent_alice"},
    )
    assert first.status_code == 200

    conflict = client.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={"mode": "embodiment", "session_id": "m95_lease_second", "character_id": "ent_alice"},
    )
    assert conflict.status_code == 409
    assert conflict.json()["code"] == "embodiment_lease_conflict"
    assert "error_lease_conflict" in client.get("/", headers=HEADERS).text


def test_player_entry_is_separate_from_english_studio_surface() -> None:
    client: Any = TestClient(create_app(build_reference_runtime()))
    player = client.get("/")
    assert player.status_code == 200
    assert player.headers["cache-control"] == "no-store"
    assert '<html lang="zh-CN"' in player.text
    assert "创造世界，进入世界，让世界继续发生。" in player.text
    for copy in ("推荐世界", "我的世界", "最近经历", "我的角色", "以此角色进入"):
        assert copy in player.text
    assert "World Plaza" not in player.text
    assert "enterPlayable" not in player.text
    studio = client.get("/studio/ui")
    assert studio.status_code == 200
    assert "World Plaza" in studio.text


def test_player_locale_catalog_defaults_to_chinese_and_supports_explicit_english() -> None:
    assert player_i18n._normalize_locale(None) == "zh-CN"
    assert player_i18n._normalize_locale("de-DE") == "zh-CN"
    assert player_i18n._normalize_locale("en-US") == "en-US"
    assert (
        player_i18n._copy_for("zh-CN").strings.keys()
        == player_i18n._copy_for("en-US").strings.keys()
    )

    chinese = player_html()
    english = player_html("en-US")
    assert '<html lang="zh-CN"' in chinese
    assert "创造世界，进入世界，让世界继续发生。" in chinese
    assert '<html lang="en-US"' in english
    assert "Create worlds, enter worlds, let them keep happening." in english
    assert "创造世界，进入世界，让世界继续发生。" not in english

    client: Any = TestClient(create_app(build_reference_runtime()))
    response = client.get("/?locale=en-US", headers={"accept-language": "zh-CN"})
    assert response.status_code == 200
    assert '<html lang="en-US"' in response.text
    fallback = client.get("/?locale=de-DE", headers={"accept-language": "en-US"})
    assert fallback.status_code == 200
    assert '<html lang="zh-CN"' in fallback.text
