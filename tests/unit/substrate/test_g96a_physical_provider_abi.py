"""G96A: physical provider ABI is immutable and proposal-only."""

from __future__ import annotations

import inspect

import pytest
from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.world_lab import (
    PhysicalBody,
    PhysicalProviderHealth,
    PhysicalResolution,
    PhysicalSimulationRequest,
    PhysicalSnapshot,
    PhysicalWorldProvider,
)


def _snapshot() -> PhysicalSnapshot:
    return PhysicalSnapshot(
        snapshot_ref="snapshot:g96a",
        world_instance_ref="world:g96a",
        branch_ref="branch:g96a",
        revision=4,
        world_time_ticks=12,
        state_hash="statehash:g96a",
        bodies=(
            PhysicalBody("body:b", (2.0, 0.0), radius=0.5),
            PhysicalBody("body:a", (0.0, 0.0), velocity=(1.0, 0.0)),
        ),
        event_refs=("event:2", "event:1"),
    )


def test_snapshot_request_and_resolution_round_trip() -> None:
    snapshot = _snapshot()
    request = PhysicalSimulationRequest(
        request_id="request:g96a",
        snapshot_ref=snapshot.snapshot_ref,
        snapshot_revision=snapshot.revision,
        actor_ref="actor:g96a",
        target_position=(3.0, 1.0),
        step_ticks=2,
        seed=96,
        parameters=(("speed", 1.5),),
    )
    resolution = PhysicalResolution(
        resolution_id="resolution:g96a",
        request_id=request.request_id,
        provider_id="provider:reference-physical",
        provider_version="1.0.0",
        snapshot_ref=snapshot.snapshot_ref,
        snapshot_revision=snapshot.revision,
        status="resolved",
        proposed_delta=ProposedWorldDelta(),
        evidence_refs=("evidence:resolution:g96a",),
        diagnostics=(("collision_count", 0),),
    )

    assert PhysicalSnapshot.from_dict(snapshot.to_dict()) == snapshot
    assert PhysicalSimulationRequest.from_dict(request.to_dict()) == request
    restored = PhysicalResolution.from_dict(resolution.to_dict())
    assert restored == resolution
    assert restored.replay_hash == resolution.replay_hash
    assert snapshot.bodies[0].body_ref == "body:a"


def test_health_contract_and_provider_protocol_have_no_commit_surface() -> None:
    health = PhysicalProviderHealth(
        provider_id="provider:reference-physical",
        version="1.0.0",
        available=True,
        deterministic=True,
        capabilities=("navigation", "collision"),
    )
    assert PhysicalProviderHealth.from_dict(health.to_dict()) == health

    protocol_members = {
        name
        for name, _ in inspect.getmembers(PhysicalWorldProvider, inspect.isfunction)
        if not name.startswith("_")
    }
    assert protocol_members == {"health", "simulate"}
    assert not protocol_members.intersection({"append", "apply", "commit", "mutate", "submit"})


def test_non_resolved_output_cannot_smuggle_a_delta() -> None:
    with pytest.raises(ContractError, match="proposed delta"):
        PhysicalResolution(
            resolution_id="resolution:g96a:rejected",
            request_id="request:g96a",
            provider_id="provider:g96a",
            provider_version="1",
            snapshot_ref="snapshot:g96a",
            snapshot_revision=0,
            status="rejected",
            proposed_delta=ProposedWorldDelta(
                operations=(object(),),  # type: ignore[arg-type]
            ),
        )
