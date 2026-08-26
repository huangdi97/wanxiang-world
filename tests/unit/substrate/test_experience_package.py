"""G88C: ExperiencePackage validation and rights boundary."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.playable import (
    EmbodimentPolicy,
    ExperiencePackage,
    PlayableWorldProfile,
    experience_from_profile,
)


def test_experience_round_trip_and_profile_adapter() -> None:
    package = ExperiencePackage(
        "exp:one",
        "world:one",
        "scenario:one",
        "projection:player",
        visibility="public",
        display_name="One",
        allowed_actions=("set_status", "transfer_resource"),
    )
    assert ExperiencePackage.from_dict(package.to_dict()) == package
    profile = PlayableWorldProfile(
        "profile:one",
        "world:one",
        "scenario:one",
        "runtime:one",
        "exp:one",
        "projection:player",
        visibility="public",
    )
    assert experience_from_profile(profile).experience_id == "exp:one"


def test_private_and_family_visibility_require_rights_metadata() -> None:
    with pytest.raises(ContractError):
        ExperiencePackage("exp", "world", "scenario", "projection")
    with pytest.raises(ContractError):
        ExperiencePackage(
            "exp",
            "world",
            "scenario",
            "projection",
            visibility="family-private",
            owner_id="u",
        )
    package = ExperiencePackage(
        "exp", "world", "scenario", "projection", visibility="private", owner_id="alice"
    )
    assert package.can_view("alice")
    assert not package.can_view("bob")
    assert not package.can_view(None)


def test_embodiment_cannot_bypass_single_lease_policy() -> None:
    with pytest.raises(ContractError):
        EmbodimentPolicy(max_controllers_per_actor=2)
    with pytest.raises(ContractError):
        ExperiencePackage(
            "exp",
            "world",
            "scenario",
            "projection",
            visibility="public",
            embodiment_policy=EmbodimentPolicy(embodiment_requires_lease=False),
        )
