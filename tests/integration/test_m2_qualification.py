"""M2 qualification: deterministic living world integrated vertical.

Runs a synthetic house/micro-town for 72 in-world hours with multiple actors,
rooms/portals, schedules, material objects, a sealed information payload, body
constraints, duties/permissions and background population scheduling ? with no
user input after instantiation. Proves M1 invariants remain green.
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
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.body.components import condition_component
from wanxiang_substrate.body.query import BodyQuery
from wanxiang_substrate.institution.components import (
    duty_component,
    membership_component,
    role_component,
)
from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.material.components import (
    custody_component,
    info_payload_component,
    item_component,
)
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.population.components import resolution_component
from wanxiang_substrate.population.model import SchedulerConfig
from wanxiang_substrate.population.scheduler import AutonomousScheduler
from wanxiang_substrate.spatial.components import (
    place_component,
    portal_component,
    position_component,
)
from wanxiang_substrate.spatial.query import SpatialQuery
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component
from wanxiang_substrate.temporal.query import TemporalQuery

DAY = 100
INSTANCE = WorldInstanceId("wld_m2")
HALL = EntityId("hall")
KITCHEN = EntityId("kitchen")
STUDY = EntityId("study")
ALICE = EntityId("alice")
BOB = EntityId("bob")
HEALTHY = EntityId("healthy")
TIRED = EntityId("tired")
LETTER = EntityId("letter_1")
MESSENGER = EntityId("messenger")
RECIPIENT = EntityId("recipient")
ROLE_MEMBER = EntityId("role_member")
DUTY_GUARD = EntityId("duty_guard")


def m2_delta() -> ProposedWorldDelta:
    """Combined synthetic world: house + conditions + sealed letter + club."""
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
                components=(place_component(EntityId("house"), "hall", capacity=8),),
            ),
            EntityCreate(
                entity_id=KITCHEN,
                entity_type="spatial.place",
                components=(place_component(EntityId("house"), "kitchen", capacity=4),),
            ),
            EntityCreate(
                entity_id=STUDY,
                entity_type="spatial.place",
                components=(
                    place_component(EntityId("house"), "study", capacity=2, privacy="restricted"),
                ),
            ),
            EntityCreate(
                entity_id=EntityId("door_hk"),
                entity_type="spatial.portal",
                components=(portal_component(HALL, KITCHEN, state="open"),),
            ),
            EntityCreate(
                entity_id=EntityId("door_hs"),
                entity_type="spatial.portal",
                components=(portal_component(HALL, STUDY, state="open"),),
            ),
            EntityCreate(
                entity_id=ALICE,
                entity_type="person",
                components=(
                    position_component(ALICE, HALL),
                    condition_component(health=100, energy=90, sleep=80, mobility=100),
                    resolution_component(ALICE, "focus", rate_ticks=20),
                ),
            ),
            EntityCreate(
                entity_id=BOB,
                entity_type="person",
                components=(
                    position_component(BOB, KITCHEN),
                    condition_component(health=100, energy=85, sleep=75, mobility=100),
                    resolution_component(BOB, "lightweight", rate_ticks=50),
                ),
            ),
            EntityCreate(
                entity_id=HEALTHY,
                entity_type="person",
                components=(
                    position_component(HEALTHY, HALL),
                    condition_component(health=100, energy=95, sleep=90, mobility=100),
                ),
            ),
            EntityCreate(
                entity_id=TIRED,
                entity_type="person",
                components=(
                    position_component(TIRED, HALL),
                    condition_component(health=100, energy=8, sleep=80, mobility=100),
                ),
            ),
            EntityCreate(
                entity_id=LETTER,
                entity_type="material.item",
                components=(
                    item_component(LETTER, "letter"),
                    custody_component(LETTER, MESSENGER),
                ),
            ),
            EntityCreate(
                entity_id=EntityId(f"payload_{LETTER.value}"),
                entity_type="material.info_payload",
                components=(info_payload_component(LETTER, "ref://m2/letter", state="sealed"),),
            ),
            EntityCreate(entity_id=MESSENGER, entity_type="person", components=()),
            EntityCreate(entity_id=RECIPIENT, entity_type="person", components=()),
            EntityCreate(
                entity_id=ROLE_MEMBER,
                entity_type="institution.role",
                components=(role_component(ROLE_MEMBER, "member", ("enter.study",)),),
            ),
            EntityCreate(
                entity_id=EntityId("membership_alice"),
                entity_type="institution.membership",
                components=(
                    membership_component(
                        EntityId("membership_alice"),
                        ALICE,
                        ROLE_MEMBER,
                        EntityId("club"),
                        0,
                        10_000,
                    ),
                ),
            ),
            EntityCreate(
                entity_id=DUTY_GUARD,
                entity_type="institution.duty",
                components=(duty_component(DUTY_GUARD, ALICE, "guard_rounds", due_ticks=DAY),),
            ),
        )
    )


def make_m2_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def _instantiate_m2(_command: CommandEnvelope, _state: object) -> ProposedWorldDelta:
        return m2_delta()

    def register(registry: ResolverRegistry) -> None:
        from wanxiang_substrate.body.resolver import register_body_resolvers
        from wanxiang_substrate.institution.resolver import register_institution_resolvers
        from wanxiang_substrate.material.resolver import register_material_resolvers
        from wanxiang_substrate.population.resolver import register_population_resolvers
        from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
        from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

        register_spatial_resolvers(registry)
        register_temporal_resolvers(registry)
        register_body_resolvers(registry)
        register_material_resolvers(registry)
        register_institution_resolvers(registry)
        register_population_resolvers(registry)
        registry.register("m2.instantiate", _instantiate_m2)

    return make_world_runtime(path, extra_resolvers=register)


def submit(
    runtime: WorldRuntime,
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
    actor_id: str | None = None,
) -> object:
    from wanxiang_domain.ids import ActorId

    return runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(command_id),
            instance_id=INSTANCE,
            branch_id=branch,
            expected_revision=BranchRevision(revision),
            action_type=action,
            payload=payload,
            actor_id=ActorId(actor_id) if actor_id else None,
            world_time=WorldTime(revision + 1),
        )
    )


@pytest.fixture
def m2_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_m2_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_m2_init"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="m2.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    yield runtime, w
    cleanup_db_file(path)


@pytest.mark.integration
def test_m2_72h_integrated_living_world(m2_world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = m2_world

    # --- Pre-scheduler manual actions exercise spatial/material/body/institution.
    # 1. Healthy moves hall->kitchen (open door).
    submit(
        runtime,
        w.root_branch_id,
        1,
        "spatial.move",
        {"entity_id": HEALTHY.value, "target_place_id": KITCHEN.value},
        "cmd_m1",
        actor_id=HEALTHY.value,
    )
    # 2. Tired cannot move (fatigue blocks otherwise valid path).
    from wanxiang_substrate.body.errors import BodyConstraintViolation

    with pytest.raises(BodyConstraintViolation):
        submit(
            runtime,
            w.root_branch_id,
            2,
            "spatial.move",
            {"entity_id": TIRED.value, "target_place_id": KITCHEN.value},
            "cmd_m2",
            actor_id=TIRED.value,
        )
    # 3. Alice (member) can enter restricted study; Bob cannot.
    submit(
        runtime,
        w.root_branch_id,
        2,
        "spatial.move",
        {"entity_id": ALICE.value, "target_place_id": STUDY.value},
        "cmd_m3",
        actor_id=ALICE.value,
    )
    from wanxiang_substrate.institution.errors import PermissionDeniedByInstitution

    with pytest.raises(PermissionDeniedByInstitution):
        submit(
            runtime,
            w.root_branch_id,
            3,
            "spatial.move",
            {"entity_id": BOB.value, "target_place_id": STUDY.value},
            "cmd_m4",
            actor_id=BOB.value,
        )
    # 4. Messenger holds sealed letter (custody) but payload stays sealed.
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    info = MaterialQuery(state).payload(LETTER)
    assert info is not None and info.state == "sealed" and info.readers == ()
    # 5. Transfer letter messenger->recipient; recipient reads.
    submit(
        runtime,
        w.root_branch_id,
        3,
        "material.transfer",
        {"item_id": LETTER.value, "from_custodian": "messenger", "to_custodian": "recipient"},
        "cmd_m5",
    )
    submit(
        runtime,
        w.root_branch_id,
        4,
        "material.read_payload",
        {"item_id": LETTER.value, "reader_id": "recipient"},
        "cmd_m6",
    )

    # --- Run the autonomous scheduler for 72 in-world hours with no user input.
    scheduler = AutonomousScheduler(
        runtime, seed=1234, config=SchedulerConfig(max_events_per_tick=8, total_event_budget=2000)
    )
    result = scheduler.run(w.instance_id, w.root_branch_id, horizon_ticks=72 * DAY, run_id="m2_72h")

    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert TemporalQuery(state).now() == 72 * DAY
    assert result.events_submitted > 100
    assert result.queue_stats["peak_tick_events"] <= 8

    # --- Post-run invariant checks.
    # World time monotonic; M1 replay reproduces the same canonical hash.
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()

    # Spatial reachability/access/capacity still coherent.
    spatial = SpatialQuery(state)
    assert spatial.location(ALICE) == STUDY  # unchanged by scheduler (no movement scheduled)
    assert spatial.location(HEALTHY) == KITCHEN
    assert spatial.reachable(HALL, KITCHEN)

    # Body condition stays bounded after scheduler rests.
    condition = BodyQuery(state).condition(ALICE)
    assert condition is not None and 0 <= condition.energy <= 100

    # Material custody conserved (letter still with recipient).
    assert MaterialQuery(state).custodian(LETTER) == RECIPIENT

    # Institution permission still works.
    decision = InstitutionQuery(state, now_ticks=72 * DAY).check_permission(ALICE, "enter.study")
    assert decision.allow is True
    assert (
        InstitutionQuery(state, now_ticks=72 * DAY).check_permission(BOB, "enter.study").allow
        is False
    )

    # Scheduler run recorded for deterministic restore.
    runs = (
        __import__("wanxiang_substrate.population.query", fromlist=["PopulationQuery"])
        .PopulationQuery(state)
        .scheduler_runs()
    )
    assert any(r["seed"] == 1234 for r in runs)
