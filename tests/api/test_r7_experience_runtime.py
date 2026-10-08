"""R7 ExperienceRuntime coordinates sessions without owning a second reality."""

from __future__ import annotations

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_api.experience_player_service import ExperiencePlayerService, PlayerResyncRequired
from wanxiang_api.experience_runtime import ExperienceRuntime
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_substrate.playable.fabric import (
    DistributionAdapter,
    ExperienceBlueprint,
    InteractionProfile,
)


def _experience(player: ExperiencePlayerService) -> ExperienceRuntime:
    blueprint = ExperienceBlueprint(
        experience_id="exp:r7-runtime",
        world_ref="world:r7-runtime",
        interaction_profile_ref="interaction:r7-roleplay",
        projection_profile_ref="projection:text",
        locale_default="zh-CN",
        distribution_adapters=("web", "api"),
    )
    interaction = InteractionProfile(
        "interaction:r7-roleplay",
        allowed_actions=("create_entity", "set_status"),
    )
    adapters = (
        DistributionAdapter("web", "web"),
        DistributionAdapter("api", "api_agent"),
    )
    return ExperienceRuntime(player, blueprint, interaction, adapters)


@pytest.mark.integration
def test_enter_act_continue_share_one_canonical_worldline() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_experience_runtime"))
    experience = _experience(ExperiencePlayerService(runtime))

    entered = experience.enter(world.instance_id, "act_player")
    assert entered.branch_id == world.root_branch_id.value
    assert entered.locale == "zh-CN"
    assert {build.channel for build in entered.distributions} == {"web", "api_agent"}

    result = experience.act(
        world.instance_id,
        world.root_branch_id,
        expected_revision=0,
        action_type="create_entity",
        payload={"entity_id": "ent_runtime", "count": 1},
        actor_id="act_player",
        command_id="cmd_experience_runtime_create",
    )
    assert result.revision == 1
    assert runtime.current_state(world.instance_id, world.root_branch_id).revision.value == 1

    resumed = experience.continue_session(
        world.instance_id,
        world.root_branch_id,
        "act_player",
    )
    assert resumed.branch_id == entered.branch_id
    assert resumed.revision == 1
    assert runtime.events(world.instance_id, world.root_branch_id)[-1].revision.value == 1
    assert not hasattr(experience, "commit")
    assert not hasattr(experience, "event_store")


@pytest.mark.integration
def test_interaction_profile_and_revision_fail_closed() -> None:
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_experience_guards"))
    experience = _experience(ExperiencePlayerService(runtime))

    with pytest.raises(ValidationRejected, match="interaction profile"):
        experience.act(
            world.instance_id,
            world.root_branch_id,
            expected_revision=0,
            action_type="transfer_resource",
            payload={"source_id": "a", "target_id": "b", "amount": 1},
            actor_id="act_player",
        )

    experience.act(
        world.instance_id,
        world.root_branch_id,
        expected_revision=0,
        action_type="create_entity",
        payload={"entity_id": "ent_guard", "count": 0},
        actor_id="act_player",
        command_id="cmd_experience_guard_create",
    )
    with pytest.raises(PlayerResyncRequired):
        experience.act(
            world.instance_id,
            world.root_branch_id,
            expected_revision=0,
            action_type="set_status",
            payload={"entity_id": "ent_guard", "status": "stale"},
            actor_id="act_player",
        )


def test_blueprint_profile_or_adapter_drift_is_rejected() -> None:
    runtime = build_reference_runtime()
    player = ExperiencePlayerService(runtime)
    blueprint = ExperienceBlueprint(
        experience_id="exp:bad",
        world_ref="world:bad",
        interaction_profile_ref="interaction:expected",
        projection_profile_ref="projection:text",
        distribution_adapters=("web",),
    )

    with pytest.raises(ValueError, match="interaction profile"):
        ExperienceRuntime(
            player,
            blueprint,
            InteractionProfile("interaction:wrong"),
            (DistributionAdapter("web", "web"),),
        )

    with pytest.raises(ValueError, match="adapters"):
        ExperienceRuntime(
            player,
            blueprint,
            InteractionProfile("interaction:expected"),
            (DistributionAdapter("api", "api_agent"),),
        )
