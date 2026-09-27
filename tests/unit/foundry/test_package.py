"""Capability package digest stability and the WorldEffect safety invariant."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace

import pytest
from wanxiang_foundry.errors import ArtifactError
from wanxiang_foundry.package import CapabilityPackage, OutputClass, WorldEffect


@pytest.mark.unit
def test_package_digest_is_stable(
    package_with_digest: Callable[[str], CapabilityPackage],
) -> None:
    package = package_with_digest("0" * 64)

    assert package.package_digest() == package.package_digest()


@pytest.mark.unit
def test_package_digest_changes_when_a_field_changes(
    package_with_digest: Callable[[str], CapabilityPackage],
) -> None:
    package = package_with_digest("0" * 64)
    other = replace(package, version="2.0.0")

    assert package.package_digest() != other.package_digest()


@pytest.mark.unit
@pytest.mark.parametrize("value", ["observation", "proposal", "projection"])
def test_world_effect_accepts_proposal_only_classes(value: str) -> None:
    effect = WorldEffect.from_output_class(value)

    assert effect.allowed_output_class is OutputClass(value)


@pytest.mark.unit
@pytest.mark.parametrize("value", ["canonical_write", "world_mutation", "commit", ""])
def test_world_effect_refuses_canonical_write_output_class(value: str) -> None:
    with pytest.raises(ArtifactError):
        WorldEffect.from_output_class(value)


@pytest.mark.unit
def test_package_rejects_non_hex_digest(
    package_with_digest: Callable[[str], CapabilityPackage],
) -> None:
    package = package_with_digest("0" * 64)

    with pytest.raises(ArtifactError):
        replace(package, artifact_digest="short")


@pytest.mark.unit
def test_package_rejects_empty_provenance(
    package_with_digest: Callable[[str], CapabilityPackage],
) -> None:
    package = package_with_digest("0" * 64)

    with pytest.raises(ArtifactError):
        replace(package, provenance=())
