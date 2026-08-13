"""M5 qualification: human can enter a persistent world without authority.

Hosted synthetic world + Studio/Phaser sessions: acquire lease, take over an
actor, commit actions, release, deterministic controller resumes, clients
disconnect while the world continues, process restarts, reconnect, and the
canonical semantic hash is preserved.
"""

from __future__ import annotations

import pathlib
from collections.abc import Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.host.host import HostRegistry, WorldHost
from wanxiang_substrate.institution.resolver import register_institution_resolvers
from wanxiang_substrate.projection.model import ProjectionRequest
from wanxiang_substrate.projection.service import ProjectionService
from wanxiang_substrate.session.control import ControlHandoff, ShadowPolicy
from wanxiang_substrate.session.errors import ShadowCannotCommit
from wanxiang_substrate.session.service import LeaseService, SessionService
from wanxiang_substrate.spatial.components import (
    place_component,
    portal_component,
    position_component,
)
from wanxiang_substrate.spatial.query import SpatialQuery
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

INSTANCE = WorldInstanceId("wld_m5")
HALL = EntityId("hall")
KITCHEN = EntityId("kitchen")
ALICE = EntityId("alice")
BOB = EntityId("bob")


def make_m5_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_spatial_resolvers(registry)
        register_temporal_resolvers(registry)
        register_institution_resolvers(registry)
        registry.register("m5.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(
                entity_id=HALL,
                entity_type="spatial.place",
                components=(place_component(EntityId("town"), "hall"),),
            ),
            EntityCreate(
                entity_id=KITCHEN,
                entity_type="spatial.place",
                components=(place_component(EntityId("town"), "kitchen"),),
            ),
            EntityCreate(
                entity_id=EntityId("door_hk"),
                entity_type="spatial.portal",
                components=(portal_component(HALL, KITCHEN, state="open"),),
            ),
            EntityCreate(
                entity_id=ALICE,
                entity_type="person",
                components=(position_component(ALICE, HALL),),
            ),
            EntityCreate(
                entity_id=BOB,
                entity_type="person",
                components=(position_component(BOB, KITCHEN),),
            ),
        )
    )


def _cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


@pytest.mark.integration
def test_m5_hosted_world_lease_handoff_restart_continuity() -> None:
    path = fresh_db_path()
    try:
        runtime = make_m5_runtime(path)
        w = runtime.create_world(instance_id=INSTANCE)
        runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId("cmd_m5_instantiate"),
                instance_id=INSTANCE,
                branch_id=w.root_branch_id,
                expected_revision=BranchRevision(0),
                action_type="m5.instantiate",
                payload={},
                world_time=WorldTime(1),
            )
        )
        host = WorldHost(runtime, INSTANCE, w.root_branch_id)
        hosts = HostRegistry()
        hosts.register(host)

        # Studio + Phaser sessions connect to the hosted world.
        sessions = SessionService()
        studio = sessions.create("studio_1", "human", INSTANCE, "embody", 1)
        sessions.create("phaser_1", "player", INSTANCE, "embody", 2)
        leases = LeaseService()
        shadow = ShadowPolicy()

        # 1) Acquire an embodiment lease on Alice and take over control.
        lease = leases.acquire(studio, ALICE.value, "lease_alice", 1, 100)
        handoff = ControlHandoff(leases)
        handoff.acquire(ALICE.value, studio.session_id, resume_ref="ref://alice_resume")
        assert handoff.state(ALICE.value).state == "human_control"

        # 2) Human commits actions through the command API (normal history).
        revision = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
        host.submit(
            _cmd(
                w.root_branch_id,
                revision,
                "spatial.move",
                {"entity_id": ALICE.value, "target_place_id": KITCHEN.value},
                "cmd_human_move",
            )
        )
        state = runtime.current_state(w.instance_id, w.root_branch_id)
        assert SpatialQuery(state).location(ALICE) == KITCHEN

        # 3) Shadow can only advise; it cannot commit canonical actions.
        with pytest.raises(ShadowCannotCommit):
            shadow.commit(actor_id=ALICE.value)

        # 4) Release control; the deterministic controller resumes.
        revision = runtime.current_state(w.instance_id, w.root_branch_id).revision.value
        handoff.hand_back(ALICE.value, last_commit_seq=revision)
        leases.release(lease.lease_id, revision)
        resumed = handoff.resume(ALICE.value)
        assert resumed.state == "autonomous"
        assert leases.primary_controller(ALICE.value) is None

        # 5) All clients disconnect while the hosted world continues.
        hosts.shutdown()
        state = runtime.current_state(w.instance_id, w.root_branch_id)
        continued_hash = state.semantic_hash()

        # 6) Restart the process on the same DB and reconnect a projection.
        runtime2 = make_m5_runtime(path)
        events = runtime2.events(INSTANCE, w.root_branch_id)
        replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
        assert replayed.semantic_hash() == continued_hash

        # 7) Reconnected client reconstructs the view from the server projection.
        reconnect_state = runtime2.current_state(INSTANCE, w.root_branch_id)
        projection = ProjectionService(reconnect_state).compose(
            ProjectionRequest(
                session_id="phaser_reconnect",
                actor_id=ALICE.value,
                branch_id=w.root_branch_id,
                mode="map",
            )
        )
        assert projection.revision == reconnect_state.revision.value
        assert projection.entity(ALICE.value) is not None
        assert projection.entity(KITCHEN.value) is not None
    finally:
        cleanup_db_file(path)
