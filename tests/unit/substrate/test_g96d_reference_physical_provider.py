"""G96D: the reference physical provider is deterministic and proposal-only."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_substrate.world_lab import (
    PhysicalBody,
    PhysicalSimulationRequest,
    PhysicalSnapshot,
    PhysicalWorldProvider,
    ReferencePhysicalProvider,
)


def _snapshot() -> PhysicalSnapshot:
    return PhysicalSnapshot(
        snapshot_ref="snapshot_g96d",
        world_instance_ref="world_g96d",
        branch_ref="branch_g96d",
        revision=3,
        world_time_ticks=10,
        state_hash="statehash_g96d",
        bodies=(
            PhysicalBody(
                body_ref="entity_g96d_actor",
                position=(0.0, 0.0),
                radius=0.25,
            ),
            PhysicalBody(
                body_ref="entity_g96d_wall",
                position=(1.5, 0.0),
                radius=0.5,
            ),
        ),
        event_refs=("event_g96d_snapshot",),
    )


def _request(*, target: tuple[float, float], revision: int = 3) -> PhysicalSimulationRequest:
    return PhysicalSimulationRequest(
        request_id="request_g96d",
        snapshot_ref="snapshot_g96d",
        snapshot_revision=revision,
        action="navigate",
        actor_ref="entity_g96d_actor",
        target_position=target,
        step_ticks=1,
        parameters=(("speed", 2.0),),
    )


def test_navigation_collision_and_replay_are_deterministic() -> None:
    provider = ReferencePhysicalProvider("provider_g96d", "1.0.0")
    snapshot = _snapshot()
    blocked = provider.simulate(snapshot, _request(target=(3.0, 0.0)))
    assert blocked.status == "rejected"
    assert blocked.proposed_delta.is_empty()
    assert dict(blocked.diagnostics)["outcome"] == "collision"
    assert dict(blocked.diagnostics)["blocked_by"] == "entity_g96d_wall"

    open_snapshot = replace(snapshot, bodies=(snapshot.bodies[0],))
    request = _request(target=(3.0, 0.0))
    resolved = provider.simulate(open_snapshot, request)
    assert resolved.status == "resolved"
    assert len(resolved.proposed_delta.operations) == 1
    assert resolved.replay_hash
    assert provider.simulate(open_snapshot, request) == resolved
    assert provider.health().deterministic is True
    assert isinstance(provider, PhysicalWorldProvider)

    restored = type(resolved).from_dict(resolved.to_dict())
    assert restored == resolved


def test_stale_snapshot_is_rejected_without_a_write_surface() -> None:
    provider = ReferencePhysicalProvider("provider_g96d", "1.0.0")
    result = provider.simulate(_snapshot(), _request(target=(1.0, 0.0), revision=4))
    assert result.status == "rejected"
    assert dict(result.diagnostics)["outcome"] == "snapshot_mismatch"
    assert not hasattr(provider, "commit")
    assert not hasattr(provider, "apply")
