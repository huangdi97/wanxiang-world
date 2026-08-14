"""G18C: experience player web/2d continuity completion.

- A user returns to the authoritative advanced world after disconnect.
- Client resync works after a dropped connection (stale revision -> resync).
- All actions route through the server command pipeline.
- Basic accessibility: text projections carry labels/redaction for readers.
"""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_api.experience_player_service import (
    ExperiencePlayerService,
    PlayerResyncRequired,
)
from wanxiang_domain.ids import WorldInstanceId


def _runtime_with_world(persist_db_path: pathlib.Path):
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world(instance_id=WorldInstanceId("wld_player"))
    return runtime, w


def test_user_returns_to_authoritative_advanced_world(persist_db_path: pathlib.Path) -> None:
    runtime, _w = _runtime_with_world(persist_db_path)
    player = ExperiencePlayerService(runtime)
    branch = player.start_session(WorldInstanceId("wld_player"))
    player.act(
        WorldInstanceId("wld_player"),
        branch,
        0,
        "create_entity",
        {"entity_id": "me", "count": 1},
        "alice",
    )
    # User disconnects; the world advances autonomously.
    from wanxiang_substrate.population.scheduler import AutonomousScheduler

    runtime2 = make_world_runtime(persist_db_path)
    scheduler = AutonomousScheduler(runtime2, seed=3)
    scheduler.run(WorldInstanceId("wld_player"), branch, horizon_ticks=200)
    advanced = runtime2.current_state(WorldInstanceId("wld_player"), branch).revision.value
    # User reconnects: the projection reflects the advanced authoritative world.
    reconnected = ExperiencePlayerService(runtime2)
    snap = reconnected.project(WorldInstanceId("wld_player"), branch, "alice")
    assert snap.revision == advanced


def test_client_resync_after_dropped_connection(persist_db_path: pathlib.Path) -> None:
    runtime, _w = _runtime_with_world(persist_db_path)
    player = ExperiencePlayerService(runtime)
    branch = player.start_session(WorldInstanceId("wld_player"))
    player.act(
        WorldInstanceId("wld_player"),
        branch,
        0,
        "create_entity",
        {"entity_id": "a", "count": 1},
        "alice",
    )
    # A stale client submits with an old revision: rejected; resync then retry.
    with pytest.raises(PlayerResyncRequired):
        player.act(
            WorldInstanceId("wld_player"),
            branch,
            0,
            "create_entity",
            {"entity_id": "b", "count": 1},
            "alice",
        )
    snap = player.project(WorldInstanceId("wld_player"), branch, "alice")
    result = player.act(
        WorldInstanceId("wld_player"),
        branch,
        snap.revision,
        "create_entity",
        {"entity_id": "b", "count": 1},
        "alice",
    )
    assert result["duplicate"] is False


def test_all_actions_route_through_server_command_pipeline(
    persist_db_path: pathlib.Path,
) -> None:
    runtime, _w = _runtime_with_world(persist_db_path)
    player = ExperiencePlayerService(runtime)
    branch = player.start_session(WorldInstanceId("wld_player"))
    result = player.act(
        WorldInstanceId("wld_player"),
        branch,
        0,
        "create_entity",
        {"entity_id": "route_me", "count": 2},
        "alice",
    )
    # The action committed through the runtime (Commit Authority) and is in the stream.
    events = runtime.persistence.event_store.load(WorldInstanceId("wld_player"), branch)
    assert len(events) == 1
    assert result["revision"] == 1
    assert result["state_hash"]


def test_basic_accessibility_text_projection(persist_db_path: pathlib.Path) -> None:
    runtime, _w = _runtime_with_world(persist_db_path)
    player = ExperiencePlayerService(runtime)
    branch = player.start_session(WorldInstanceId("wld_player"))
    player.act(
        WorldInstanceId("wld_player"),
        branch,
        0,
        "create_entity",
        {"entity_id": "visible_thing", "count": 1},
        "alice",
    )
    snap = player.project(WorldInstanceId("wld_player"), branch, "alice")
    # Text projection items carry labels and redaction flags (reader-friendly).
    items = list(snap.items)
    assert items
    assert all(i.label for i in items)
    assert all(hasattr(i, "redacted") for i in items)
