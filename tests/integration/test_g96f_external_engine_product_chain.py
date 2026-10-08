"""G96F: blocked external capability discovery preserves SQLite reality."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_substrate.world_lab import BlockedExternalEngineAdapter


def test_external_engine_block_is_explicit_and_read_only(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    world = runtime.create_world()
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    before_hash = state.semantic_hash()
    before_events = runtime.events(world.instance_id, world.root_branch_id)

    capability = BlockedExternalEngineAdapter(
        engine_id="phaser",
        engine_kind="renderer",
        reason="No external renderer executable or browser session is provisioned",
    ).discover()

    assert capability.availability == "external_blocked"
    assert capability.external_blocked is True
    assert capability.reason.startswith("No external renderer")
    after = runtime.current_state(world.instance_id, world.root_branch_id)
    assert after.semantic_hash() == before_hash
    assert runtime.events(world.instance_id, world.root_branch_id) == before_events
