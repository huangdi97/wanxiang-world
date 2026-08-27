"""G96D: reference physical proposals cross a real SQLite runtime boundary."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_substrate.world_lab import (
    PhysicalBody,
    PhysicalSimulationRequest,
    PhysicalSnapshot,
    ReferencePhysicalProvider,
)


def test_reference_physics_does_not_mutate_sqlite_reality(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    world = runtime.create_world()
    state = runtime.current_state(world.instance_id, world.root_branch_id)
    before_hash = state.semantic_hash()
    before_events = runtime.events(world.instance_id, world.root_branch_id)
    snapshot = PhysicalSnapshot(
        snapshot_ref="snapshot_g96d_runtime",
        world_instance_ref=world.instance_id.value,
        branch_ref=world.root_branch_id.value,
        revision=state.revision.value,
        world_time_ticks=0,
        state_hash=before_hash,
        bodies=(
            PhysicalBody(
                body_ref="entity_g96d_runtime_actor",
                position=(0.0, 0.0),
                velocity=(0.5, 0.0),
                radius=0.1,
            ),
        ),
    )
    request = PhysicalSimulationRequest(
        request_id="request_g96d_runtime",
        snapshot_ref=snapshot.snapshot_ref,
        snapshot_revision=snapshot.revision,
        action="step",
        actor_ref="entity_g96d_runtime_actor",
        step_ticks=4,
    )
    provider = ReferencePhysicalProvider("provider_g96d_runtime", "1.0.0")
    result = provider.simulate(snapshot, request)

    assert result.status == "resolved"
    assert result.evidence_refs
    assert result.replay_hash == provider.simulate(snapshot, request).replay_hash
    after = runtime.current_state(world.instance_id, world.root_branch_id)
    assert after.semantic_hash() == before_hash
    assert runtime.events(world.instance_id, world.root_branch_id) == before_events
