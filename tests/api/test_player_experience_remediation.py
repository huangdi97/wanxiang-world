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


def test_session_cards_and_history_keep_worldline_state_separate() -> None:
    client = _client()
    plaza = client.get("/experience/player/plaza", headers=HEADERS).json()
    profile_id = str(plaza["worlds"][0]["profile_id"])
    entered = client.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={
            "mode": "embodiment",
            "session_id": "session_card_parent",
            "character_id": "ent_alice",
        },
    )
    parent = str(entered.json()["instance_id"])
    assert (
        client.post(
            f"/experience/player/instances/{parent}/action",
            headers=HEADERS,
            json={"text": "让自己保持清醒"},
        ).status_code
        == 200
    )
    fork = client.post(f"/experience/player/instances/{parent}/fork", headers=HEADERS)
    child = str(cast(dict[str, Any], fork.json()["worldline"])["instance_id"])
    assert (
        client.post(
            f"/experience/player/instances/{parent}/action",
            headers=HEADERS,
            json={"text": "让自己保持警觉"},
        ).status_code
        == 200
    )

    cards = cast(
        list[dict[str, Any]],
        client.get("/experience/player/plaza", headers=HEADERS).json()["recent_sessions"],
    )
    by_instance = {str(card["instance_id"]): card for card in cards}
    child_card = by_instance[child]
    parent_card = by_instance[parent]
    assert child_card["world_name"] == parent_card["world_name"] == "江南机关城"
    assert child_card["character_name"] == parent_card["character_name"]
    assert child_card["status"] == "saved"
    assert parent_card["status"] == "active"
    assert int(child_card["time"]["ticks"]) < int(parent_card["time"]["ticks"])
    assert child_card["events_since_leave"] == []

    child_history = client.get(
        f"/experience/player/instances/{child}/history",
        headers=HEADERS,
        params={"limit": 2},
    )
    assert child_history.status_code == 200
    child_body = cast(dict[str, Any], child_history.json())
    assert child_body["total"] >= 3
    assert child_body["returned"] == 2
    assert len(child_body["events"]) == 2
    assert child_body["has_more"] is True
    assert int(child_body["next_before"]) > 0
    older = client.get(
        f"/experience/player/instances/{child}/history",
        headers=HEADERS,
        params={"limit": 2, "before": int(child_body["next_before"])},
    )
    assert older.status_code == 200
    older_body = cast(dict[str, Any], older.json())
    assert older_body["returned"] == 2
    assert older_body["has_more"] is False
    assert older_body["next_before"] is None
    page_times = [int(item["time"]) for item in child_body["events"]]
    older_times = [int(item["time"]) for item in older_body["events"]]
    assert all(time < int(child_body["next_before"]) for time in older_times)
    assert len(set(page_times + older_times)) == 4
    for invalid in (0, 501):
        rejected = client.get(
            f"/experience/player/instances/{child}/history",
            headers=HEADERS,
            params={"limit": invalid},
        )
        assert rejected.status_code == 422
    negative = client.get(
        f"/experience/player/instances/{child}/history",
        headers=HEADERS,
        params={"before": -1},
    )
    assert negative.status_code == 422


def test_public_visual_world_hides_cost_details_from_visitors() -> None:
    client: Any = TestClient(create_app(build_reference_runtime()))
    source = {
        "source_id": "m95_public_visual_source",
        "kind": "text",
        "content": (
            "# Chapter\nCharacter: Alice\nAlice arrived in Beijing in 1985.\n"
            "rule: visitors register\n"
        ),
        "stage": "E3",
        "rights_approved": True,
        "access": "public",
        "private_analysis_allowed": True,
        "package_inclusion_allowed": True,
        "public_export_allowed": True,
        "training_allowed": False,
    }
    created = client.post(
        "/studio/one-click",
        json={
            "job_id": "m95_public_visual_job",
            "profile": "book",
            "sources": [source],
        },
    )
    assert created.status_code == 201, created.text
    profile = client.post(
        "/studio/jobs/m95_public_visual_job/playable-profile",
        json={"owner_id": "studio", "visibility": "public", "display_name": "公共视觉世界"},
    )
    assert profile.status_code == 200, profile.text
    profile_id = str(profile.json()["profile"]["profile_id"])

    visitor = client.post(
        f"/experience/player/worlds/{profile_id}/visuals",
        headers={"X-Wanxiang-User": "guest"},
        json={"place_name": "Beijing"},
    )
    assert visitor.status_code == 200, visitor.text
    visitor_body = cast(dict[str, Any], visitor.json())
    for internal in (
        "deferred_used",
        "deferred_limit",
        "cost_units",
        "provider_calls",
        "cache_hits",
        "fallback_from_provider",
        "fallback_reason",
    ):
        assert internal not in visitor_body
    assert visitor_body["world"]["visual"]["places"]

    owner = client.post(
        f"/experience/player/worlds/{profile_id}/visuals",
        headers=HEADERS,
        json={"place_name": "Beijing"},
    )
    assert owner.status_code == 200, owner.text
    owner_body = cast(dict[str, Any], owner.json())
    assert owner_body["deferred_limit"] == 24
    assert "deferred_used" in owner_body


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
    places = cast(list[dict[str, Any]], detail.json()["world"]["visual"]["places"])
    assert places and places[0]["name"] == "Beijing"
    assert places[0]["generated"] is True
    assert places[0]["tier"] == "T0"
    assert places[0]["source_count"] == 1
    assert int(places[0]["source_evidence_count"]) >= 1
    generation = detail.json()["world"]["visual"]["generation"]
    assert generation == {"deferred_used": 0, "deferred_limit": 24}
    generated = client.post(
        f"/experience/player/worlds/{profile_id}/visuals",
        headers=HEADERS,
        json={"place_name": "Beijing"},
    )
    assert generated.status_code == 200
    assert generated.json()["deferred_used"] == 0
    assert generated.json()["deferred_limit"] == 24
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


def test_observer_cannot_fork_a_canonical_branch() -> None:
    client = _client()
    plaza = client.get("/experience/player/plaza", headers=HEADERS).json()
    profile_id = str(plaza["worlds"][0]["profile_id"])
    entered = client.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={"mode": "observer", "session_id": "m95_observer_fork_session"},
    )
    assert entered.status_code == 200
    instance_id = str(entered.json()["instance_id"])

    fork = client.post(
        f"/experience/player/instances/{instance_id}/fork",
        headers=HEADERS,
    )

    assert fork.status_code == 422
    assert fork.json()["code"] == "contract_error"
    assert "embodied character" in fork.json()["message"]


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


def test_player_replay_projects_a_past_tick_without_committing() -> None:
    client = _client()
    plaza = client.get("/experience/player/plaza", headers=HEADERS)
    profile_id = str(plaza.json()["worlds"][0]["profile_id"])
    entered = client.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={
            "mode": "embodiment",
            "session_id": "m95_replay_session",
            "character_id": "ent_alice",
        },
    )
    assert entered.status_code == 200
    instance_id = str(entered.json()["instance_id"])

    first = client.post(
        f"/experience/player/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "让自己保持清醒"},
    )
    assert first.status_code == 200
    first_view = cast(dict[str, Any], first.json()["view"])
    first_ticks = int(cast(dict[str, Any], first_view["time"])["ticks"])

    second = client.post(
        f"/experience/player/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "让自己保持警觉"},
    )
    assert second.status_code == 200
    second_view = cast(dict[str, Any], second.json()["view"])
    assert int(cast(dict[str, Any], second_view["time"])["ticks"]) > first_ticks

    replay = client.get(
        f"/experience/player/instances/{instance_id}/replay",
        headers=HEADERS,
        params={"at_ticks": first_ticks},
    )
    assert replay.status_code == 200
    body = cast(dict[str, Any], replay.json())
    replay_view = cast(dict[str, Any], body["view"])
    assert body["replay"]["at_ticks"] == first_ticks
    assert body["replay"]["world_ticks"] == first_ticks
    assert int(body["replay"]["event_count"]) >= 1
    # Replaying the first action's tick reproduces the projection observed then.
    assert replay_view["time"] == first_view["time"]
    assert replay_view["player"] == first_view["player"]
    assert replay_view["location"] == first_view["location"]
    assert replay_view["chronicle"] == first_view["chronicle"]
    assert replay_view["present_people"] == first_view["present_people"]
    assert "event_id" not in json.dumps(replay_view, ensure_ascii=False)

    # Replay is read-only: the head projection is unchanged after the call.
    head = client.get(f"/experience/player/instances/{instance_id}", headers=HEADERS).json()["view"]
    assert head["time"] == second_view["time"]
    assert head["player"]["status"] == second_view["player"]["status"]

    empty = client.get(
        f"/experience/player/instances/{instance_id}/replay",
        headers=HEADERS,
        params={"at_ticks": 0},
    )
    assert empty.status_code == 200
    assert empty.json()["replay"]["event_count"] == 0
    assert empty.json()["view"]["chronicle"] == []

    negative = client.get(
        f"/experience/player/instances/{instance_id}/replay",
        headers=HEADERS,
        params={"at_ticks": -1},
    )
    assert negative.status_code == 422


def test_player_history_lists_the_full_chronicle_newest_first() -> None:
    client = _client()
    plaza = client.get("/experience/player/plaza", headers=HEADERS)
    profile_id = str(plaza.json()["worlds"][0]["profile_id"])
    entered = client.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={
            "mode": "embodiment",
            "session_id": "m95_history_session",
            "character_id": "ent_alice",
        },
    )
    instance_id = str(entered.json()["instance_id"])
    for text in ("让自己保持清醒", "让自己保持警觉"):
        response = client.post(
            f"/experience/player/instances/{instance_id}/action",
            headers=HEADERS,
            json={"text": text},
        )
        assert response.status_code == 200

    history = client.get(
        f"/experience/player/instances/{instance_id}/history",
        headers=HEADERS,
    )
    assert history.status_code == 200
    body = cast(dict[str, Any], history.json())
    events = cast(list[dict[str, Any]], body["events"])
    assert body["total"] == len(events) >= 3
    assert body["returned"] == len(events)
    times = [int(item["time"]) for item in events]
    assert times == sorted(times, reverse=True)
    assert "event_id" not in json.dumps(body, ensure_ascii=False)
    assert "state_hash" not in json.dumps(body, ensure_ascii=False)
    assert "branch_id" not in json.dumps(body, ensure_ascii=False)

    page = client.get(
        f"/experience/player/instances/{instance_id}/history",
        headers=HEADERS,
        params={"limit": 1},
    )
    assert page.status_code == 200
    assert page.json()["returned"] == 1
    assert page.json()["total"] == body["total"]
    assert page.json()["events"][0]["time"] == times[0]

    for item in events:
        replay = client.get(
            f"/experience/player/instances/{instance_id}/replay",
            headers=HEADERS,
            params={"at_ticks": item["time"]},
        )
        assert replay.status_code == 200
        assert replay.json()["replay"]["world_ticks"] == item["time"]

    assert (
        client.get(
            f"/experience/player/instances/{instance_id}/history",
            headers=HEADERS,
            params={"limit": 0},
        ).status_code
        == 422
    )
    assert (
        client.get(
            f"/experience/player/instances/{instance_id}/history",
            headers=HEADERS,
            params={"limit": 501},
        ).status_code
        == 422
    )
    other = client.get(
        f"/experience/player/instances/{instance_id}/history",
        headers={"X-Wanxiang-User": "someone-else"},
    )
    assert other.status_code == 404


def test_player_worldline_fork_returns_a_detached_branch_handle() -> None:
    client = _client()
    plaza = client.get("/experience/player/plaza", headers=HEADERS)
    profile_id = str(plaza.json()["worlds"][0]["profile_id"])
    entered = client.post(
        f"/experience/player/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={
            "mode": "embodiment",
            "session_id": "m95_fork_session",
            "character_id": "ent_alice",
        },
    )
    instance_id = str(entered.json()["instance_id"])
    action = client.post(
        f"/experience/player/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "让自己保持清醒"},
    )
    assert action.status_code == 200
    parent_view = cast(
        dict[str, Any],
        client.get(f"/experience/player/instances/{instance_id}", headers=HEADERS).json()["view"],
    )

    fork = client.post(
        f"/experience/player/instances/{instance_id}/fork",
        headers=HEADERS,
    )
    assert fork.status_code == 200
    worldline = cast(dict[str, Any], fork.json()["worldline"])
    assert "branch_id" not in json.dumps(worldline, ensure_ascii=False)
    assert "revision" not in json.dumps(worldline, ensure_ascii=False)
    child = str(worldline["instance_id"])
    assert child != instance_id
    assert worldline["parent_instance_id"] == instance_id
    child_view = cast(
        dict[str, Any],
        client.get(f"/experience/player/instances/{child}", headers=HEADERS).json()["view"],
    )
    assert child_view["time"] == parent_view["time"]
    assert child_view["player"] == parent_view["player"]
    assert child_view["chronicle"] == parent_view["chronicle"]
    assert (
        client.get(f"/experience/player/instances/{instance_id}", headers=HEADERS).json()["view"][
            "player"
        ]
        == parent_view["player"]
    )
    assert (
        client.post(
            f"/experience/player/instances/{instance_id}/fork",
            headers={"X-Wanxiang-User": "someone-else"},
        ).status_code
        == 404
    )

    listing = client.get(
        f"/experience/player/instances/{child}/worldlines",
        headers=HEADERS,
    )
    assert listing.status_code == 200
    cards = cast(list[dict[str, Any]], listing.json()["worldlines"])
    assert {str(card["instance_id"]) for card in cards} == {instance_id, child}
    assert listing.json()["branches"] == 2
    child_card = next(card for card in cards if card["instance_id"] == child)
    assert child_card["current"] is True
    assert child_card["forked"] is True
    assert "branch_id" not in json.dumps(cards, ensure_ascii=False)
    assert "revision" not in json.dumps(cards, ensure_ascii=False)
    shared = client.get(
        f"/experience/player/instances/{instance_id}/compare",
        headers=HEADERS,
        params={"with": child},
    )
    assert shared.status_code == 200
    shared_body = cast(dict[str, Any], shared.json())
    assert shared_body["identical"] is True
    assert shared_body["common"]["shared"] is True
    assert "revision" not in json.dumps(shared_body, ensure_ascii=False)
    assert shared_body["diverged_events"] == {"left": 0, "right": 0}
    assert shared_body["differences"] == {"total": 0, "truncated": False, "items": []}
    assert shared_body["recent"]["left"] == shared_body["recent"]["right"]
    assert (
        client.get(
            f"/experience/player/instances/{child}/worldlines",
            headers={"X-Wanxiang-User": "someone-else"},
        ).status_code
        == 404
    )

    assert (
        client.post(
            f"/experience/player/instances/{instance_id}/leave",
            headers=HEADERS,
        ).status_code
        == 200
    )
    continued = client.post(
        f"/experience/player/instances/{child}/continue",
        headers=HEADERS,
    )
    assert continued.status_code == 200
    assert str(continued.json()["instance_id"]) == child
    child_action = client.post(
        f"/experience/player/instances/{child}/action",
        headers=HEADERS,
        json={"text": "让自己保持警觉"},
    )
    assert child_action.status_code == 200
    child_after = cast(
        dict[str, Any],
        client.get(f"/experience/player/instances/{child}", headers=HEADERS).json()["view"],
    )
    parent_after = cast(
        dict[str, Any],
        client.get(f"/experience/player/instances/{instance_id}", headers=HEADERS).json()["view"],
    )
    assert child_after["player"] != parent_after["player"]
    assert parent_after["player"] == parent_view["player"]
    diverged = client.get(
        f"/experience/player/instances/{instance_id}/compare",
        headers=HEADERS,
        params={"with": child},
    )
    assert diverged.status_code == 200
    diverged_body = cast(dict[str, Any], diverged.json())
    assert diverged_body["identical"] is False
    assert diverged_body["diverged_events"] == {"left": 0, "right": 1}
    assert diverged_body["right"]["status"] == "警觉"
    assert diverged_body["differences"]["total"] >= 1
    left_recent = cast(list[dict[str, Any]], diverged_body["recent"]["left"])
    right_recent = cast(list[dict[str, Any]], diverged_body["recent"]["right"])
    assert right_recent[-1]["time"] > left_recent[-1]["time"]


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
