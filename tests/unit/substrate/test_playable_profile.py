"""G88B: versioned PlayableWorldProfile contracts."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import ContractError
from wanxiang_substrate.playable import (
    InMemoryPlayableStore,
    PlayableWorldProfile,
    ProjectionProfile,
    RuntimeProfile,
    ScenarioProfile,
    profile_from_world_package,
)


def profile() -> PlayableWorldProfile:
    return PlayableWorldProfile(
        profile_id="experience:book-1",
        world_package_ref="world:wd_book-1",
        scenario_ref="default",
        runtime_profile_ref="reference-commit-authority",
        experience_package_ref="experience:book-1",
        projection_profile_ref="default-player",
        visibility="public",
        display_name="Book world",
        tags=("literary",),
    )


def test_profile_and_supporting_profiles_round_trip() -> None:
    current = profile()
    assert PlayableWorldProfile.from_dict(current.to_dict()) == current
    assert (
        ScenarioProfile.from_dict(
            ScenarioProfile("default", "world:wd_book-1").to_dict()
        ).scenario_id
        == "default"
    )
    assert RuntimeProfile.from_dict(RuntimeProfile("reference").to_dict()).simulation_lod == "L0"
    assert (
        ProjectionProfile.from_dict(ProjectionProfile("default-player").to_dict()).show_state_diff
        is True
    )


def test_profile_reads_v0_aliases_and_writes_v1() -> None:
    old = {
        "profile_id": "experience:old",
        "package_id": "world:old",
        "scenario_id": "default",
        "runtime_id": "reference",
        "visibility": "private",
    }
    current = PlayableWorldProfile.from_dict(old)
    assert current.world_package_ref == "world:old"
    assert current.to_dict()["schema_version"] == 1


def test_invalid_refs_visibility_and_store_replacement_are_rejected() -> None:
    with pytest.raises(ContractError):
        PlayableWorldProfile("bad", "", "default", "runtime", "experience", "projection")
    with pytest.raises(ContractError):
        PlayableWorldProfile(
            "bad",
            "world",
            "default",
            "runtime",
            "experience",
            "projection",
            visibility="team",  # type: ignore[arg-type]
        )
    store = InMemoryPlayableStore()
    store.save_profile(profile())
    with pytest.raises(ContractError):
        store.save_profile(
            PlayableWorldProfile(
                "experience:book-1",
                "world:other",
                "default",
                "reference-commit-authority",
                "experience:book-1",
                "default-player",
                visibility="public",
            )
        )


def test_profile_from_v54_package_only_keeps_refs() -> None:
    class Manifest:
        name = "Source-created world"

    class Package:
        package_id = "world:source-created"
        manifest = Manifest()

    built = profile_from_world_package(Package(), visibility="public")
    assert built.world_package_ref == "world:source-created"
    assert built.display_name == "Source-created world"
    assert built.owner_id == ""
