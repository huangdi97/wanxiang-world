"""Replay is read-only on the server, not only in the client.

Measured before this guard existed: replay was a purely client-side read mode, so a
direct action POST while the Player was showing a past world time still committed an
event. The guard is now session bookkeeping on the server — while a viewer is looking
at a past world time the session is *held*, and any action POST (player route or the
canonical route) is refused until the viewer returns to now, leaves, or continues.

These specs pin both halves: the refusal leaves canon untouched, and each documented
release path (return to now, leave + continue) lets the same session commit again.
"""

# pyright: reportPrivateUsage=false

from __future__ import annotations

from typing import Any, cast

from fastapi.testclient import TestClient
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.app import create_app

HEADERS = {"X-Wanxiang-User": "alice"}

SOURCE = {
    "source_id": "replay_guard_source",
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


def _seeded_instance() -> tuple[Any, str]:
    """A world owned by alice with one embodied session and one committed action."""

    client: Any = TestClient(create_app(build_reference_runtime()))
    created = client.post(
        "/studio/one-click",
        json={"job_id": "job_replay_guard", "profile": "book", "sources": [dict(SOURCE)]},
    )
    assert created.status_code == 201, created.text
    profile_id = str(
        client.post(
            "/studio/jobs/job_replay_guard/playable-profile",
            json={"owner_id": "alice", "visibility": "public", "display_name": "Replay World"},
        ).json()["profile"]["profile_id"]
    )
    character = client.post(
        "/experience/characters",
        headers=HEADERS,
        json={
            "display_name": "Alice",
            "character_id": "ent_alice",
            "compatible_profile_ids": [profile_id],
        },
    )
    assert character.status_code == 201, character.text
    entered = client.post(
        f"/experience/worlds/{profile_id}/enter",
        headers=HEADERS,
        json={"mode": "embodiment", "session_id": "session_replay", "character_id": "ent_alice"},
    )
    assert entered.status_code == 200, entered.text
    instance_id = str(entered.json()["instance"]["instance_id"])
    first = client.post(
        f"/experience/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "set status to awake"},
    )
    assert first.status_code == 200, first.text
    return client, instance_id


def _revision(client: Any, instance_id: str) -> int:
    observed = client.get(f"/experience/instances/{instance_id}", headers=HEADERS)
    assert observed.status_code == 200, observed.text
    return cast(int, observed.json()["revision"])


def _replay(client: Any, instance_id: str, at_ticks: int = 1) -> Any:
    return client.get(
        f"/experience/player/instances/{instance_id}/replay?at_ticks={at_ticks}",
        headers=HEADERS,
    )


def _chronicle_count(client: Any, instance_id: str) -> int:
    history = client.get(f"/experience/player/instances/{instance_id}/history", headers=HEADERS)
    assert history.status_code == 200, history.text
    return len(cast(list[object], history.json()["events"]))


def test_direct_action_while_replaying_is_refused_and_canon_is_untouched() -> None:
    client, instance_id = _seeded_instance()
    before_revision = _revision(client, instance_id)
    before_chronicle = _chronicle_count(client, instance_id)
    assert _replay(client, instance_id).status_code == 200

    refused = client.post(
        f"/experience/player/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "set status to away"},
    )
    assert refused.status_code == 422, refused.text
    body = cast(dict[str, Any], refused.json())
    assert body["code"] == "replay_read_only"
    assert cast(dict[str, Any], body["details"])["product_state"] == "REPLAY_READ_ONLY"
    assert "return to now first" in str(body["message"])

    # The canonical route is guarded by the same session hold, not by the URL.
    canonical = client.post(
        f"/experience/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "set status to away"},
    )
    assert canonical.status_code == 422, canonical.text
    assert canonical.json()["code"] == "replay_read_only"

    assert _revision(client, instance_id) == before_revision
    assert _chronicle_count(client, instance_id) == before_chronicle


def test_returning_to_now_releases_the_hold_and_the_session_commits_again() -> None:
    client, instance_id = _seeded_instance()
    before_revision = _revision(client, instance_id)
    assert _replay(client, instance_id).status_code == 200

    returned = client.post(
        f"/experience/player/instances/{instance_id}/replay/return",
        headers=HEADERS,
    )
    assert returned.status_code == 200, returned.text
    assert returned.json()["status"] == "at_now"
    assert returned.json()["replay"] is None

    committed = client.post(
        f"/experience/player/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "set status to away"},
    )
    assert committed.status_code == 200, committed.text
    assert committed.json()["status"] == "committed"
    assert _revision(client, instance_id) == before_revision + 1


def test_leaving_the_world_releases_the_hold() -> None:
    client, instance_id = _seeded_instance()
    assert _replay(client, instance_id).status_code == 200

    left = client.post(f"/experience/instances/{instance_id}/leave", headers=HEADERS)
    assert left.status_code == 200, left.text
    continued = client.post(f"/experience/instances/{instance_id}/continue", headers=HEADERS)
    assert continued.status_code == 200, continued.text

    committed = client.post(
        f"/experience/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "set status to away"},
    )
    assert committed.status_code == 200, committed.text


def test_a_session_that_never_replayed_is_not_held() -> None:
    client, instance_id = _seeded_instance()
    committed = client.post(
        f"/experience/instances/{instance_id}/action",
        headers=HEADERS,
        json={"text": "set status to tired"},
    )
    assert committed.status_code == 200, committed.text
