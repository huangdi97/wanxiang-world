"""R7 Profile / Bundle / Lock / Artifact composition tests."""

from __future__ import annotations

import pytest
from wanxiang_reality.bundles import (
    BundlePatch,
    RuntimeArtifact,
    WorldBundle,
    resolve_bundle_stack,
)
from wanxiang_reality.errors import ProfileError
from wanxiang_reality.versions import Version

SHA_A = "a" * 64
SHA_B = "b" * 64


def _artifact(name: str, digest: str = SHA_A) -> RuntimeArtifact:
    return RuntimeArtifact(
        package_name=name,
        version=Version(1, 0, 0),
        integrity_hash=digest,
        source_provenance=f"repo:{name}",
        build_provenance="ci:reference",
    )


def _base() -> WorldBundle:
    return WorldBundle(
        bundle_id="wanxiang-base",
        version=Version(1, 0, 0),
        reality_profile_ref="reality.reference@1.0.0",
        required_seams=("wanxiang.authority@1", "wanxiang.history@1"),
        providers=("provider.history.memory",),
        dimensions={
            "actors": "actors.none",
            "capabilities": "capabilities.none",
            "distribution": "distribution.web",
            "experience": "experience.observe",
            "memory": "memory.none",
            "projection": "projection.text",
            "simulation": "simulation.none",
            "space": "space.graph",
            "time": "time.linear",
        },
        artifacts=(_artifact("wanxiang-base-runtime"),),
    )


def test_bundle_stack_resolves_deterministically_into_world_profile() -> None:
    overlay = WorldBundle(
        bundle_id="wanxiang-agent-world",
        version=Version(1, 0, 0),
        reality_profile_ref="reality.reference@1.0.0",
        required_seams=("wanxiang.actor@1",),
        providers=("provider.actor.reference",),
        dimensions={"actors": "actors.agent"},
        artifacts=(_artifact("wanxiang-agent-runtime", SHA_B),),
    )
    patch = BundlePatch(dimension_overrides={"actors": "actors.agent"})

    first = resolve_bundle_stack(
        (_base(), overlay),
        profile_id="world.agent.reference",
        version=Version(1, 0, 0),
        patch=patch,
    )
    second = resolve_bundle_stack(
        (_base(), overlay),
        profile_id="world.agent.reference",
        version=Version(1, 0, 0),
        patch=patch,
    )

    assert first == second
    assert first.digest == second.digest
    assert first.world_profile.providers == (
        "provider.actor.reference",
        "provider.history.memory",
    )
    assert first.world_profile.dimensions["actors"] == "actors.agent"
    assert first.required_seams == (
        "wanxiang.actor@1",
        "wanxiang.authority@1",
        "wanxiang.history@1",
    )
    assert first.artifact_hashes() == {
        "wanxiang-agent-runtime": SHA_B,
        "wanxiang-base-runtime": SHA_A,
    }


def test_dimension_conflict_fails_without_explicit_patch() -> None:
    overlay = WorldBundle(
        bundle_id="wanxiang-research",
        version=Version(1, 0, 0),
        reality_profile_ref="reality.reference@1.0.0",
        dimensions={"experience": "experience.experiment"},
    )
    with pytest.raises(ProfileError, match="explicit overrides"):
        resolve_bundle_stack(
            (_base(), overlay),
            profile_id="world.research.reference",
            version=Version(1, 0, 0),
        )


def test_bundle_stack_cannot_silently_mix_reality_profiles() -> None:
    other = WorldBundle(
        bundle_id="wanxiang-other-reality",
        version=Version(1, 0, 0),
        reality_profile_ref="reality.other@2.0.0",
    )
    with pytest.raises(ProfileError, match="RealityProfile"):
        resolve_bundle_stack(
            (_base(), other),
            profile_id="world.bad",
            version=Version(1, 0, 0),
        )


def test_artifact_identity_conflict_fails_closed() -> None:
    conflicting = WorldBundle(
        bundle_id="wanxiang-conflicting-artifact",
        version=Version(1, 0, 0),
        reality_profile_ref="reality.reference@1.0.0",
        artifacts=(_artifact("wanxiang-base-runtime", SHA_B),),
    )
    with pytest.raises(ProfileError, match="artifact conflict"):
        resolve_bundle_stack(
            (_base(), conflicting),
            profile_id="world.bad",
            version=Version(1, 0, 0),
        )


def test_provider_patch_is_explicit_and_does_not_change_reality_profile() -> None:
    result = resolve_bundle_stack(
        (_base(),),
        profile_id="world.patched",
        version=Version(1, 0, 0),
        patch=BundlePatch(
            add_providers=("provider.model.reference",),
            remove_providers=("provider.history.memory",),
        ),
    )

    assert result.world_profile.reality_profile_ref == "reality.reference@1.0.0"
    assert result.world_profile.providers == ("provider.model.reference",)


@pytest.mark.parametrize("digest", ["", "ABC", "x" * 64, "a" * 63])
def test_runtime_artifact_requires_lowercase_sha256(digest: str) -> None:
    with pytest.raises(ProfileError, match="sha256"):
        _artifact("broken", digest)
