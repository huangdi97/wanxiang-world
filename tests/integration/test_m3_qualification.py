"""M3 qualification: bounded agents can live inside the world.

Deterministic synthetic scenario: at least two actors and one organization.
Alice observes a private/partial event, forms a belief, receives a correction,
executes a multi-step skill, and changes a bounded capability. Bob never
receives knowledge he never observed or was not told.
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
from wanxiang_domain.ids import ActorId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.actions.registry import ActionRegistry, register_reference_actions
from wanxiang_substrate.actions.validator import ActionValidator
from wanxiang_substrate.capability.query import CapabilityQuery
from wanxiang_substrate.capability.resolver import register_capability_resolvers
from wanxiang_substrate.epistemic.query import EpistemicQuery
from wanxiang_substrate.epistemic.resolver import register_epistemic_resolvers
from wanxiang_substrate.institution.components import (
    membership_component,
    role_component,
)
from wanxiang_substrate.institution.resolver import register_institution_resolvers
from wanxiang_substrate.material.components import (
    custody_component,
    info_payload_component,
    item_component,
)
from wanxiang_substrate.material.query import MaterialQuery
from wanxiang_substrate.material.resolver import register_material_resolvers
from wanxiang_substrate.observation.query import PerspectiveService
from wanxiang_substrate.observation.resolver import register_observation_resolvers
from wanxiang_substrate.skills.model import SkillDefinition, SkillStep
from wanxiang_substrate.skills.registry import SkillRegistry
from wanxiang_substrate.skills.resolver import register_skill_resolvers
from wanxiang_substrate.skills.runtime import SkillRuntime
from wanxiang_substrate.spatial.components import (
    place_component,
    portal_component,
    position_component,
)
from wanxiang_substrate.spatial.query import SpatialQuery
from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component
from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

INSTANCE = WorldInstanceId("wld_m3")
HUB = EntityId("hub")
RECIPIENT_HOUSE = EntityId("recipient_house")
ALICE = EntityId("alice")
BOB = EntityId("bob")
WRITER = EntityId("writer")
RECIPIENT = EntityId("recipient")
LETTER = EntityId("letter_1")
PAYLOAD = EntityId("payload_letter_1")
GUILD = EntityId("guild")
ROLE_COURIER = EntityId("role_courier")
MEMBERSHIP_ALICE = EntityId("membership_alice")


def m3_delta() -> ProposedWorldDelta:
    """Combined deterministic world: town, courier guild, letter + sealed payload."""
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=CLOCK_ENTITY,
                entity_type="temporal.clock",
                components=(clock_component(0, paused=False),),
            ),
            EntityCreate(
                entity_id=HUB,
                entity_type="spatial.place",
                components=(place_component(EntityId("town"), "hub"),),
            ),
            EntityCreate(
                entity_id=RECIPIENT_HOUSE,
                entity_type="spatial.place",
                components=(place_component(EntityId("town"), "recipient_house"),),
            ),
            EntityCreate(
                entity_id=EntityId("door_hub"),
                entity_type="spatial.portal",
                components=(portal_component(HUB, RECIPIENT_HOUSE, state="open"),),
            ),
            EntityCreate(entity_id=GUILD, entity_type="institution.organization", components=()),
            EntityCreate(
                entity_id=ROLE_COURIER,
                entity_type="institution.role",
                components=(role_component(ROLE_COURIER, "courier", ("deliver",)),),
            ),
            EntityCreate(
                entity_id=MEMBERSHIP_ALICE,
                entity_type="institution.membership",
                components=(membership_component(MEMBERSHIP_ALICE, ALICE, ROLE_COURIER, GUILD, 0),),
            ),
            EntityCreate(
                entity_id=ALICE,
                entity_type="person",
                components=(position_component(ALICE, HUB),),
            ),
            EntityCreate(
                entity_id=BOB,
                entity_type="person",
                components=(position_component(BOB, RECIPIENT_HOUSE),),
            ),
            EntityCreate(
                entity_id=WRITER,
                entity_type="person",
                components=(position_component(WRITER, HUB),),
            ),
            EntityCreate(
                entity_id=RECIPIENT,
                entity_type="person",
                components=(position_component(RECIPIENT, RECIPIENT_HOUSE),),
            ),
            EntityCreate(
                entity_id=LETTER,
                entity_type="material.item",
                components=(
                    item_component(LETTER, "letter"),
                    custody_component(LETTER, WRITER),
                ),
            ),
            EntityCreate(
                entity_id=PAYLOAD,
                entity_type="material.info_payload",
                components=(
                    info_payload_component(LETTER, "ref://confidential/body", state="sealed"),
                ),
            ),
        )
    )


def make_m3_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_spatial_resolvers(registry)
        register_material_resolvers(registry)
        register_temporal_resolvers(registry)
        register_institution_resolvers(registry)
        register_observation_resolvers(registry)
        register_epistemic_resolvers(registry)
        register_skill_resolvers(registry)
        register_capability_resolvers(registry)
        registry.register("m3.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate(command: object, state: object) -> ProposedWorldDelta:
    return m3_delta()


def submit(
    runtime: WorldRuntime,
    w: CreateWorldResult,
    action: str,
    payload: Mapping[str, FieldValue],
    actor: str | None = None,
) -> None:
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    revision = state.revision.value
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId(f"cmd_m3_{revision}_{action.replace('.', '_')}"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(revision),
            action_type=action,
            payload=payload,
            actor_id=ActorId(actor) if actor else None,
            world_time=WorldTime(revision + 1),
        )
    )


@pytest.fixture
def m3_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_m3_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_m3_instantiate"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="m3.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )
    yield runtime, w
    cleanup_db_file(path)


def _courier_skill() -> SkillDefinition:
    return SkillDefinition(
        skill_id=EntityId("skill_courier"),
        version=1,
        name="courier_run",
        required_permission="deliver",
        steps=(
            SkillStep(
                "take",
                "material.transfer",
                {
                    "item_id": LETTER.value,
                    "from_custodian": WRITER.value,
                    "to_custodian": ALICE.value,
                },
                requires_capability="delivery:2",
                duration_ticks=5,
                cost=1,
            ),
            SkillStep(
                "move",
                "spatial.move",
                {"entity_id": ALICE.value, "target_place_id": RECIPIENT_HOUSE.value},
                requires_capability="delivery:2",
                duration_ticks=20,
                cost=2,
            ),
            SkillStep(
                "hand_over",
                "material.transfer",
                {
                    "item_id": LETTER.value,
                    "from_custodian": ALICE.value,
                    "to_custodian": RECIPIENT.value,
                },
                requires_capability="delivery:2",
                duration_ticks=5,
                cost=1,
            ),
        ),
    )


@pytest.mark.integration
def test_m3_bounded_agent_vertical(m3_world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = m3_world

    # 1) Organization exists and Alice is a guild member; grant the courier
    #    permission used by the skill gate.
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(GUILD) is not None
    assert state.entity(MEMBERSHIP_ALICE) is not None
    submit(
        runtime,
        w,
        "institution.grant_permission",
        {
            "permission_id": "perm_deliver",
            "actor_id": ALICE.value,
            "permission": "deliver",
            "target": "global",
            "granter_id": "guild_admin",
            "start_ticks": 0,
            "end_ticks": 100_000,
        },
    )

    # 2) Alice learns the delivery capability from declared practice evidence
    #    (6 practices -> level 2), before she may run the skill.
    submit(
        runtime,
        w,
        "capability.record_practice",
        {
            "record_id": "pr_a1",
            "actor_id": ALICE.value,
            "capability": "delivery",
            "practice_count": 3,
            "evidence_ref": "evid://route/1",
        },
    )
    submit(
        runtime,
        w,
        "capability.record_practice",
        {
            "record_id": "pr_a2",
            "actor_id": ALICE.value,
            "capability": "delivery",
            "practice_count": 3,
            "evidence_ref": "evid://route/2",
        },
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    learned = CapabilityQuery(state).capability(ALICE, "delivery")
    assert learned is not None and learned.level == 2
    assert learned.evidence_refs == ("evid://route/1", "evid://route/2")

    # 3) Bob moves from the recipient house to the hub; Alice (at the hub)
    #    observes a private/partial event. The sealed payload never leaks.
    submit(
        runtime,
        w,
        "spatial.move",
        {"entity_id": BOB.value, "target_place_id": HUB.value},
        actor=BOB.value,
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert SpatialQuery(state).location(BOB) == HUB
    events = runtime.events(w.instance_id, w.root_branch_id)
    observations = PerspectiveService(state).context_for(ALICE, events)
    movement = [o for o in observations if o.fact.kind == "movement"]
    assert movement
    for obs in observations:
        assert "confidential" not in repr(obs.fact)

    # 4) Observation, belief, memory and canonical truth stay separate.
    submit(
        runtime,
        w,
        "epistemic.adopt_belief",
        {
            "belief_id": "belief_bob_left",
            "actor_id": ALICE.value,
            "proposition": "bob_has_left_his_post",
            "confidence": 0.6,
            "at_ticks": 20,
        },
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(EntityId("belief_bob_left")) is not None
    assert state.entity(EntityId("belief_bob_left")).entity_type == "epistemic.belief"  # type: ignore[union-attr]
    # Observations are derived read-models, not canonical entities.
    assert state.entity(EntityId("observation_bob_move")) is None

    # 5) Alice receives a correction; the temporal epistemic graph preserves
    #    the contradiction/correction lineage.
    submit(
        runtime,
        w,
        "epistemic.correct_belief",
        {
            "belief_id": "belief_bob_left",
            "new_belief_id": "belief_bob_returned",
            "actor_id": ALICE.value,
            "proposition": "bob_has_left_his_post",
            "confidence": 0.9,
            "at_ticks": 30,
        },
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    query = EpistemicQuery(state, now_ticks=30)
    active = query.active_belief(ALICE, "bob_has_left_his_post")
    assert active is not None and active.belief_id == EntityId("belief_bob_returned")
    assert active.supersedes == EntityId("belief_bob_left")
    assert len(query.belief_history(ALICE, "bob_has_left_his_post")) == 2

    # 6) Bob never receives knowledge he never observed: no belief, no memory
    #    of Alice's private observation, and no capability she earned.
    assert query.active_belief(BOB, "bob_has_left_his_post") is None
    assert not any("belief_bob" in m.content_ref for m in query.memories(BOB))
    assert CapabilityQuery(state).capability(BOB, "delivery") is None

    # 7) Alice executes a multi-step skill; every step passes normal
    #    validation through the authoritative path and requires her capability.
    registry = SkillRegistry()
    registry.register(_courier_skill())
    skill = SkillRuntime(runtime, registry, INSTANCE, w.root_branch_id)
    completed = skill.execute(EntityId("skill_inst_1"), EntityId("skill_courier"), ALICE)
    assert completed == ["take", "move", "hand_over"]
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert MaterialQuery(state).custodian(LETTER) == RECIPIENT
    assert SpatialQuery(state).location(ALICE) == RECIPIENT_HOUSE

    # 8) The completed run is itself evidence-backed practice: capability
    #    changes and remains bounded.
    submit(
        runtime,
        w,
        "capability.record_practice",
        {
            "record_id": "pr_a3",
            "actor_id": ALICE.value,
            "capability": "delivery",
            "practice_count": 3,
            "evidence_ref": "evid://route/3",
        },
    )
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    grown = CapabilityQuery(state).capability(ALICE, "delivery")
    assert grown is not None and grown.level == 3
    assert 0 <= grown.level <= 10
    assert 0.0 <= grown.mastery <= 1.0
    assert 0.0 <= grown.confidence <= 1.0
    assert "evid://route/3" in grown.evidence_refs

    # 9) ActionValidator rejects what is epistemically impossible for Bob:
    #    reading the sealed letter payload he never observed.
    action_registry = ActionRegistry()
    register_reference_actions(action_registry)
    validator = ActionValidator(action_registry)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    rejected = validator.validate(
        CommandEnvelope(
            command_id=CommandId("cmd_m3_read_bob"),
            instance_id=INSTANCE,
            branch_id=w.root_branch_id,
            expected_revision=state.revision,
            action_type="material.read_payload",
            payload={"item_id": LETTER.value},
            actor_id=ActorId(BOB.value),
            world_time=WorldTime(state.revision.value + 1),
        ),
        state,
    )
    assert rejected.ok is False
    assert any(issue.code == "no_knowledge" for issue in rejected.issues)

    # 10) No policy owns Commit Authority: everything was committed through the
    #     authoritative path and replays to the identical canonical state.
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()
    assert state.revision.value >= 10
