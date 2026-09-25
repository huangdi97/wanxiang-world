"""Behaviour of versions, reality/world profiles and the R7 runtime lock."""

from __future__ import annotations

from dataclasses import replace

import pytest
from wanxiang_reality.errors import ProfileError, RuntimeLockError, VersionError
from wanxiang_reality.profiles import (
    RealityProfile,
    RuntimeLock,
    WorldProfile,
    build_runtime_lock,
    profile_hash,
)
from wanxiang_reality.versions import Version

pytestmark = pytest.mark.unit

REQUIRED_WORLD_DIMENSIONS = {
    "time",
    "space",
    "actors",
    "memory",
    "simulation",
    "capabilities",
    "experience",
    "projection",
    "distribution",
}


def _dimensions(*, omit: str | None = None) -> dict[str, str]:
    return {name: name for name in sorted(REQUIRED_WORLD_DIMENSIONS) if name != omit}


def _reality_profile() -> RealityProfile:
    return RealityProfile(
        profile_id="reality.core",
        version=Version(1, 0, 0),
        required_seams=("wanxiang.authority@1", "wanxiang.history@1"),
        optional_seams=("wanxiang.replay@1",),
    )


def _world_profile() -> WorldProfile:
    return WorldProfile(
        profile_id="world.standard",
        version=Version(1, 0, 0),
        reality_profile_ref="reality.core@1.0.0",
        providers=("provider.physical.reference",),
        dimensions=_dimensions(),
    )


def _build_lock() -> RuntimeLock:
    return build_runtime_lock(
        _reality_profile(),
        _world_profile(),
        world_id="world-1",
        world_instance_id="instance-1",
        worldline_id="worldline-1",
        composition_runtime="cordis",
        composition_runtime_version="1.0.0",
        service_contract_versions={"wanxiang.history@1": "1"},
        provider_versions={"provider.physical.reference": "1.0.0"},
        artifact_hashes={"artifact.world": "abc"},
        schema_versions={"canonical": "1"},
        migration_lineage=("baseline",),
        runtime_config_hash="config-hash",
    )


def test_version_parse_accepts_one_two_or_three_components() -> None:
    assert Version.parse("1") == Version(1, 0, 0)
    assert Version.parse("1.2") == Version(1, 2, 0)
    assert Version.parse("1.2.3") == Version(1, 2, 3)
    assert str(Version(1, 2, 3)) == "1.2.3"


@pytest.mark.parametrize(
    "text",
    ["", "1.2.3.4", "1.x", "1..2", "abc", "-1", "1.2.3 ", "1.2.3-beta"],
)
def test_version_parse_rejects_garbage(text: str) -> None:
    with pytest.raises(VersionError):
        Version.parse(text)


def test_version_ordering_and_major_compatibility() -> None:
    assert Version(1, 2, 3) < Version(1, 2, 4)
    assert Version(1, 9, 9) < Version(2, 0, 0)
    assert Version(1, 0, 0).compatible(Version(1, 9, 9))
    assert not Version(2, 0, 0).compatible(Version(1, 9, 9))


def test_major_upgrade_requires_a_higher_major() -> None:
    assert Version(2, 0, 0).is_major_upgrade_from(Version(1, 9, 9))
    assert not Version(1, 1, 0).is_major_upgrade_from(Version(1, 0, 0))


def test_unknown_required_seam_is_rejected() -> None:
    with pytest.raises(ProfileError):
        RealityProfile(
            profile_id="reality.bad",
            version=Version(1, 0, 0),
            required_seams=("wanxiang.unknown@1",),
        )


def test_overlapping_required_and_optional_seams_is_rejected() -> None:
    with pytest.raises(ProfileError):
        RealityProfile(
            profile_id="reality.bad",
            version=Version(1, 0, 0),
            required_seams=("wanxiang.history@1",),
            optional_seams=("wanxiang.history@1",),
        )


def test_unsorted_required_seams_are_rejected() -> None:
    with pytest.raises(ProfileError):
        RealityProfile(
            profile_id="reality.bad",
            version=Version(1, 0, 0),
            required_seams=("wanxiang.history@1", "wanxiang.authority@1"),
        )


def test_world_profile_missing_a_required_dimension_is_rejected() -> None:
    with pytest.raises(ProfileError):
        WorldProfile(
            profile_id="world.bad",
            version=Version(1, 0, 0),
            reality_profile_ref="reality.core@1.0.0",
            providers=("provider.physical.reference",),
            dimensions=_dimensions(omit="distribution"),
        )


def test_world_profile_with_an_unknown_dimension_is_rejected() -> None:
    dimensions = _dimensions()
    dimensions["gravity"] = "gravity"

    with pytest.raises(ProfileError):
        WorldProfile(
            profile_id="world.bad",
            version=Version(1, 0, 0),
            reality_profile_ref="reality.core@1.0.0",
            providers=("provider.physical.reference",),
            dimensions=dimensions,
        )


def test_build_runtime_lock_validates_and_has_a_stable_digest() -> None:
    lock = _build_lock()

    lock.validate()
    assert lock.lock_digest() == lock.lock_digest()
    assert lock.lock_digest() == _build_lock().lock_digest()
    assert lock.reality_profile_hash == profile_hash(_reality_profile())
    assert lock.reality_profile_ref == "reality.core@1.0.0"
    assert lock.world_definition_version == "1.0.0"


def test_tampered_empty_service_contract_versions_is_rejected() -> None:
    tampered = replace(_build_lock(), service_contract_versions={})

    with pytest.raises(RuntimeLockError):
        tampered.validate()


def test_tampered_invalid_contract_version_is_rejected() -> None:
    tampered = replace(
        _build_lock(),
        service_contract_versions={"wanxiang.history@1": "v1"},
    )

    with pytest.raises(RuntimeLockError):
        tampered.validate()


def test_tampered_empty_world_id_is_rejected() -> None:
    tampered = replace(_build_lock(), world_id="")

    with pytest.raises(RuntimeLockError):
        tampered.validate()
