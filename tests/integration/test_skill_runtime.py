"""G03F: skill runtime ? step expansion through the authoritative path."""

from __future__ import annotations

import pathlib
from collections.abc import Iterator

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.errors import ContractError
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.material.components import custody_component, item_component
from wanxiang_substrate.skills.errors import InvalidSkillStep, SkillPrerequisiteError
from wanxiang_substrate.skills.model import SkillDefinition, SkillStep
from wanxiang_substrate.skills.registry import (
    DELIVER_LETTER,
    INSPECT_OBJECT,
    SkillRegistry,
    register_reference_skills,
)
from wanxiang_substrate.skills.resolver import register_skill_resolvers
from wanxiang_substrate.skills.runtime import SkillRuntime
from wanxiang_substrate.spatial.components import (
    place_component,
    portal_component,
    position_component,
)
from wanxiang_substrate.temporal.components import CLOCK_ENTITY, clock_component

INSTANCE = WorldInstanceId("wld_skill")
HUB = EntityId("hub")
RECIPIENT_HOUSE = EntityId("recipient_house")
WRITER = EntityId("writer")
MESSENGER = EntityId("messenger")
RECIPIENT = EntityId("recipient")
LETTER = EntityId("letter_1")


def skill_world_delta() -> ProposedWorldDelta:
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
            EntityCreate(entity_id=WRITER, entity_type="person", components=()),
            EntityCreate(
                entity_id=MESSENGER,
                entity_type="person",
                components=(position_component(MESSENGER, HUB),),
            ),
            EntityCreate(entity_id=RECIPIENT, entity_type="person", components=()),
            EntityCreate(
                entity_id=LETTER,
                entity_type="material.item",
                components=(
                    item_component(LETTER, "letter"),
                    custody_component(LETTER, WRITER),
                ),
            ),
        )
    )


def make_skill_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def _instantiate(_command: CommandEnvelope, _state: object) -> ProposedWorldDelta:
        return skill_world_delta()

    def register(registry: ResolverRegistry) -> None:
        from wanxiang_substrate.institution.resolver import register_institution_resolvers
        from wanxiang_substrate.material.resolver import register_material_resolvers
        from wanxiang_substrate.spatial.resolver import register_spatial_resolvers
        from wanxiang_substrate.temporal.resolver import register_temporal_resolvers

        register_spatial_resolvers(registry)
        register_material_resolvers(registry)
        register_temporal_resolvers(registry)
        register_institution_resolvers(registry)
        register_skill_resolvers(registry)
        registry.register("skill_test.instantiate", _instantiate)

    return make_world_runtime(path, extra_resolvers=register)


def _instantiate_world(runtime: WorldRuntime, branch: BranchId) -> None:
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_skill_world"),
            instance_id=INSTANCE,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="skill_test.instantiate",
            payload={},
            world_time=WorldTime(1),
        )
    )


def _grant_deliver(runtime: WorldRuntime, branch: BranchId, revision: int) -> None:
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_grant_deliver"),
            instance_id=INSTANCE,
            branch_id=branch,
            expected_revision=BranchRevision(revision),
            action_type="institution.grant_permission",
            payload={
                "permission_id": "perm_deliver",
                "actor_id": MESSENGER.value,
                "permission": "deliver",
                "target": "global",
                "granter_id": "admin",
                "start_ticks": 0,
                "end_ticks": 100_000,
            },
            world_time=WorldTime(revision + 1),
        )
    )


@pytest.fixture
def skill_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_skill_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    _instantiate_world(runtime, w.root_branch_id)
    yield runtime, w
    cleanup_db_file(path)


def _registry() -> SkillRegistry:
    registry = SkillRegistry()
    register_reference_skills(registry)
    return registry


@pytest.mark.unit
def test_skill_model_and_registry() -> None:
    registry = _registry()
    deliver = registry.get(DELIVER_LETTER)
    assert deliver is not None and len(deliver.steps) == 3
    assert deliver.required_permission == "deliver"
    assert registry.get(INSPECT_OBJECT) is not None
    with pytest.raises(ContractError):
        SkillDefinition(EntityId("x"), 0, "bad", ())  # version 0


@pytest.mark.integration
def test_deliver_letter_skill_executes_steps(
    skill_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = skill_world
    _grant_deliver(runtime, w.root_branch_id, 1)
    skill = SkillRuntime(runtime, _registry(), INSTANCE, w.root_branch_id)
    completed = skill.execute(EntityId("skill_inst_1"), DELIVER_LETTER, MESSENGER)
    assert completed == ["take", "move", "hand_over"]
    from wanxiang_substrate.skills.components import SKILL_INSTANCE_COMPONENT

    state = runtime.current_state(w.instance_id, w.root_branch_id)
    inst = state.entity(EntityId("skill_inst_1"))
    assert inst is not None
    component = next(
        c for c in inst.components.values() if c.component_type == SKILL_INSTANCE_COMPONENT
    )
    assert component.fields["state"] == "completed"


@pytest.mark.integration
def test_insufficient_permission_blocks_start(
    skill_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = skill_world
    skill = SkillRuntime(runtime, _registry(), INSTANCE, w.root_branch_id)
    with pytest.raises(SkillPrerequisiteError):
        skill.execute(EntityId("skill_inst_x"), DELIVER_LETTER, MESSENGER)


@pytest.mark.integration
def test_invalid_step_fails_explicitly(skill_world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = skill_world
    _grant_deliver(runtime, w.root_branch_id, 1)
    registry = SkillRegistry()
    registry.register(
        SkillDefinition(
            skill_id=EntityId("skill_bad"),
            version=1,
            name="bad_skill",
            steps=(
                SkillStep(
                    "take",
                    "material.transfer",
                    {
                        "item_id": "ghost_item",
                        "from_custodian": WRITER.value,
                        "to_custodian": MESSENGER.value,
                    },
                ),
            ),
        )
    )
    skill = SkillRuntime(runtime, registry, INSTANCE, w.root_branch_id)
    with pytest.raises(InvalidSkillStep):
        skill.execute(EntityId("skill_inst_bad"), EntityId("skill_bad"), MESSENGER)


@pytest.mark.integration
def test_skill_effects_replay(skill_world: tuple[WorldRuntime, CreateWorldResult]) -> None:
    runtime, w = skill_world
    _grant_deliver(runtime, w.root_branch_id, 1)
    skill = SkillRuntime(runtime, _registry(), INSTANCE, w.root_branch_id)
    skill.execute(EntityId("skill_inst_r"), DELIVER_LETTER, MESSENGER)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()
