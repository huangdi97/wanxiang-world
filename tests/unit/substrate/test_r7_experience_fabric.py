"""R7 ExperienceBlueprint / Interaction / Distribution contracts."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.playable.experience import ExperiencePackage
from wanxiang_substrate.playable.fabric import (
    DistributionAdapter,
    ExperienceBlueprint,
    InteractionProfile,
    build_distribution,
    experience_card,
)
from wanxiang_substrate.playable.models import ProjectionProfile


def test_blueprint_adapts_existing_experience_without_owning_world_state() -> None:
    package = ExperiencePackage(
        "exp:r7-roleplay",
        "world:r7",
        "scenario:opening",
        "projection:web",
        visibility="public",
        display_name="R7 roleplay",
    )
    interaction = InteractionProfile(
        "interaction:roleplay-free",
        input_models=("natural_language", "ui"),
        allowed_actions=("set_status",),
    )
    blueprint = ExperienceBlueprint.from_package(
        package,
        interaction_profile_ref=interaction.profile_id,
        distribution_adapters=("web", "api"),
    )

    assert blueprint.world_ref == package.world_package_ref
    assert blueprint.locale_default == "zh-CN"
    assert blueprint.same_worldline_required is True
    assert "state" not in blueprint.__dataclass_fields__
    assert "event_store" not in blueprint.__dataclass_fields__


def test_projection_profile_reads_committed_reality_and_has_no_write_authority() -> None:
    profile = ProjectionProfile(
        projection_id="projection:web-text-2d",
        provider_ref="native_web@1",
        capabilities=("text", "map_2d"),
        state_source="canonical_read_model",
        fallback="text",
    )

    assert profile.write_authority == "none"
    assert profile.state_source == "canonical_read_model"
    assert ProjectionProfile.from_dict(profile.to_dict()) == profile
    assert "state" not in profile.__dataclass_fields__
    assert "event_store" not in profile.__dataclass_fields__


def test_projection_profile_rejects_invalid_fallback() -> None:
    with pytest.raises(ContractError, match="write authority"):
        ProjectionProfile(
            projection_id="projection:illegal-writer",
            provider_ref="visual_model@1",
            capabilities=("text",),
            write_authority="commit",  # type: ignore[arg-type]
        )
    with pytest.raises(ContractError, match="fallback"):
        ProjectionProfile(
            projection_id="projection:3d-only",
            provider_ref="spatial_provider@1",
            capabilities=("scene_3d",),
            fallback="text",
        )


def test_distribution_build_is_deterministic_and_contains_only_refs() -> None:
    blueprint = ExperienceBlueprint(
        experience_id="exp:r7-observer",
        world_ref="world:r7",
        interaction_profile_ref="interaction:observe",
        projection_profile_ref="projection:research",
        experience_type="observe",
        distribution_adapters=("web",),
    )
    adapter = DistributionAdapter(
        "web",
        "web",
        capability_matrix=("text", "state_diff", "deep_link"),
        storage_model="cache_only",
    )

    first = build_distribution(blueprint, adapter)
    second = build_distribution(blueprint, adapter)
    assert first == second
    assert first.world_ref == "world:r7"
    assert first.build_id.startswith("dist:")
    assert "state" not in first.__dataclass_fields__
    assert "event_store" not in first.__dataclass_fields__


def test_distribution_adapter_cannot_claim_canonical_storage() -> None:
    with pytest.raises(ContractError, match="canonical-state"):
        DistributionAdapter("bad", "web", storage_model="canonical")


def test_card_is_safe_entry_projection() -> None:
    blueprint = ExperienceBlueprint(
        experience_id="exp:r7-card",
        world_ref="world:r7",
        interaction_profile_ref="interaction:roleplay",
        projection_profile_ref="projection:web",
    )
    card = experience_card(
        blueprint,
        title="江南机关城",
        promise="进入同一个持续发生的世界",
        recommended_role="机关师",
        deep_link="/worlds/r7?experience=exp:r7-card",
    )
    assert card.world_ref == blueprint.world_ref
    assert card.locale == "zh-CN"
    assert card.continue_enabled is True
