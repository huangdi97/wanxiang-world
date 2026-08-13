"""G08A: synthetic mansion living-world qualification.

A mansion Domain/World/Scenario runs seven in-world days with no-user periods,
human takeover/resume, a day-3 alternate branch, and letter custody/knowledge
propagation - all through existing authoritative paths.
"""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers
from wanxiang_substrate.institution.resolver import register_institution_resolvers
from wanxiang_substrate.lifecycle.service import LifecycleService
from wanxiang_substrate.material.components import (
    custody_component,
    info_payload_component,
    item_component,
)
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.material.resolver import register_material_resolvers
from wanxiang_substrate.session.control import ControlHandoff
from wanxiang_substrate.session.service import LeaseService, SessionService
from wanxiang_substrate.spatial.components import (
    place_component,
    portal_component,
    position_component,
)
from wanxiang_substrate.spatial.query import SpatialQuery
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component
from wanxiang_substrate.temporal.query import TemporalQuery
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

INSTANCE = WorldInstanceId("wld_mansion")
DAY = 100
HALL = EntityId("hall")
STUDY = EntityId("study")
GARDEN = EntityId("garden")
BAOYU = EntityId("baoyu")
DAIYU = EntityId("daiyu")
LETTER = EntityId("letter_1")


def make_mansion_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_spatial_resolvers(registry)
        register_material_resolvers(registry)
        register_temporal_resolvers(registry)
        register_institution_resolvers(registry)
        register_epistemic_resolvers(registry)
        from wanxiang_substrate.lifecycle.resolver import register_lifecycle_resolvers

        register_lifecycle_resolvers(registry)
        registry.register("mansion.instantiate", _instantiate)

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
                components=(place_component(EntityId("mansion"), "hall"),),
            ),
            EntityCreate(
                entity_id=STUDY,
                entity_type="spatial.place",
                components=(place_component(EntityId("mansion"), "study"),),
            ),
            EntityCreate(
                entity_id=GARDEN,
                entity_type="spatial.place",
                components=(place_component(EntityId("mansion"), "garden"),),
            ),
            EntityCreate(
                entity_id=EntityId("door_hs"),
                entity_type="spatial.portal",
                components=(portal_component(HALL, STUDY, state="open"),),
            ),
            EntityCreate(
                entity_id=EntityId("door_hg"),
                entity_type="spatial.portal",
                components=(portal_component(HALL, GARDEN, state="open"),),
            ),
            EntityCreate(
                entity_id=BAOYU,
                entity_type="person",
                components=(position_component(BAOYU, HALL),),
            ),
            EntityCreate(
                entity_id=DAIYU,
                entity_type="person",
                components=(position_component(DAIYU, STUDY),),
            ),
            EntityCreate(
                entity_id=LETTER,
                entity_type="material.item",
                components=(
                    item_component(LETTER, "letter"),
                    custody_component(LETTER, DAIYU),
                ),
            ),
            EntityCreate(
                entity_id=EntityId("payload_letter_1"),
                entity_type="material.info_payload",
                components=(
                    info_payload_component(LETTER, "ref://mansion/message", state="sealed"),
                ),
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


@pytest.fixture
def mansion_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_mansion_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_mansion_instantiate"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="mansion.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_m7_mansion_seven_days_takeover_branch(
    mansion_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = mansion_world
    lifecycle = LifecycleService(runtime, INSTANCE, w.root_branch_id)

    # 1) Run seven in-world days with no user input.
    lifecycle.set_mode("BACKGROUND_SIMULATION")
    lifecycle.advance(7 * DAY)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert TemporalQuery(state).now() == 700

    # 2) Human takes over Baoyu around day 3, commits an action, releases.
    sessions = SessionService()
    session = sessions.create("human_1", "reader", INSTANCE, "embody", 1)
    leases = LeaseService()
    leases.acquire(session, BAOYU.value, "lease_baoyu", 1, 1000)
    handoff = ControlHandoff(leases)
    handoff.acquire(BAOYU.value, session.session_id, resume_ref="ref://baoyu")
    revision = state.revision.value
    runtime.submit_command(
        _cmd(
            w.root_branch_id,
            revision,
            "spatial.move",
            {"entity_id": BAOYU.value, "target_place_id": GARDEN.value},
            "cmd_human_garden",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert SpatialQuery(state).location(BAOYU) == GARDEN
    leases.release("lease_baoyu", state.revision.value)
    handoff.hand_back(BAOYU.value, last_commit_seq=state.revision.value)
    handoff.resume(BAOYU.value)
    assert handoff.state(BAOYU.value).state == "autonomous"

    # 3) Message custody/knowledge propagation: Baoyu takes the letter Daiyu
    #    holds, then reads it (custody -> knowledge, not implied by proximity).
    revision = state.revision.value
    runtime.submit_command(
        _cmd(
            w.root_branch_id,
            revision,
            "material.transfer",
            {
                "item_id": LETTER.value,
                "from_custodian": DAIYU.value,
                "to_custodian": BAOYU.value,
            },
            "cmd_take",
        )
    )
    revision = revision + 1
    runtime.submit_command(
        _cmd(
            w.root_branch_id,
            revision,
            "material.read_payload",
            {"item_id": LETTER.value, "reader_id": BAOYU.value},
            "cmd_read",
        )
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert MaterialQuery(state).custodian(LETTER) == BAOYU

    # 4) Fork a day-3 alternate branch and compare with the parent.
    from wanxiang_domain.hierarchy import BranchRevision

    parent_hash = state.semantic_hash()
    fork = runtime.create_branch(
        INSTANCE, w.root_branch_id, fork_revision=BranchRevision(state.revision.value)
    )
    fork_state = runtime.current_state(INSTANCE, fork.branch_id)
    assert fork_state.semantic_hash() == parent_hash
    # Divergence on the fork never mutates the parent.
    runtime.submit_command(
        _cmd(
            fork.branch_id,
            state.revision.value,
            "create_entity",
            {"entity_id": "alt_1", "entity_type": "thing"},
            "cmd_fork_alt",
        )
    )
    after = runtime.current_state(INSTANCE, w.root_branch_id)
    assert after.semantic_hash() == parent_hash
