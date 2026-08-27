"""G96A: a real runtime snapshot can cross the ABI without mutating reality."""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_domain.delta import ProposedWorldDelta
from wanxiang_substrate.world_lab import (
    PhysicalProviderHealth,
    PhysicalResolution,
    PhysicalSimulationRequest,
    PhysicalSnapshot,
    PhysicalWorldProvider,
)


class _ProbePhysicalProvider:
    def health(self) -> PhysicalProviderHealth:
        return PhysicalProviderHealth(
            provider_id="provider:g96a:probe",
            version="1.0.0",
            available=True,
            deterministic=True,
            capabilities=("snapshot-read",),
        )

    def simulate(
        self,
        snapshot: PhysicalSnapshot,
        request: PhysicalSimulationRequest,
    ) -> PhysicalResolution:
        if request.snapshot_ref != snapshot.snapshot_ref:
            raise ValueError("request and snapshot refs differ")
        return PhysicalResolution(
            resolution_id=f"resolution:{request.request_id}",
            request_id=request.request_id,
            provider_id="provider:g96a:probe",
            provider_version="1.0.0",
            snapshot_ref=snapshot.snapshot_ref,
            snapshot_revision=snapshot.revision,
            status="resolved",
            proposed_delta=ProposedWorldDelta(),
            evidence_refs=(f"snapshot:{snapshot.state_hash}",),
        )


def test_runtime_state_remains_unchanged_across_physical_provider_boundary(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    world = runtime.create_world()
    before = runtime.current_state(world.instance_id, world.root_branch_id)
    snapshot = PhysicalSnapshot(
        snapshot_ref="snapshot:g96a:runtime",
        world_instance_ref=world.instance_id.value,
        branch_ref=world.root_branch_id.value,
        revision=before.revision.value,
        world_time_ticks=0,
        state_hash=before.semantic_hash(),
        event_refs=(),
    )
    request = PhysicalSimulationRequest(
        request_id="request:g96a:runtime",
        snapshot_ref=snapshot.snapshot_ref,
        snapshot_revision=snapshot.revision,
        step_ticks=1,
        seed=96,
    )
    provider: PhysicalWorldProvider = _ProbePhysicalProvider()
    resolution = provider.simulate(snapshot, request)
    after = runtime.current_state(world.instance_id, world.root_branch_id)

    assert provider.health().available is True
    assert resolution.status == "resolved"
    assert resolution.proposed_delta.is_empty()
    assert before.semantic_hash() == after.semantic_hash()
    assert runtime.events(world.instance_id, world.root_branch_id) == ()
