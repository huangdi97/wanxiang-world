"""Artifact2Capability provider seam and the provider registry."""

from __future__ import annotations

from collections.abc import Mapping

import pytest
from wanxiang_foundry.candidate import ArtifactRef, CapabilityCandidate
from wanxiang_foundry.errors import CandidateError, RegistryError
from wanxiang_foundry.provider import Artifact2CapabilityProvider, ProviderRegistry
from wanxiang_foundry.reference_provider import RuleBasedFoundryProvider


class _SecondVersionProvider:
    """A second provider version used to prove versions coexist."""

    provider_id = "foundry-rule-based-reference"
    provider_version = "2.0.0"

    def propose(
        self, artifact: ArtifactRef, declaration: Mapping[str, object]
    ) -> CapabilityCandidate:
        raise CandidateError("second-version provider is not exercised here")


@pytest.mark.unit
def test_reference_provider_satisfies_the_protocol() -> None:
    assert isinstance(RuleBasedFoundryProvider(), Artifact2CapabilityProvider)


@pytest.mark.unit
def test_provider_registry_refuses_silent_replacement() -> None:
    registry = ProviderRegistry()
    registry.register(RuleBasedFoundryProvider())

    with pytest.raises(RegistryError):
        registry.register(RuleBasedFoundryProvider())

    assert registry.get("foundry-rule-based-reference", "1.0.0") is not None


@pytest.mark.unit
def test_provider_registry_keeps_versions_separately() -> None:
    registry = ProviderRegistry()
    registry.register(RuleBasedFoundryProvider())
    registry.register(_SecondVersionProvider())

    assert registry.versions("foundry-rule-based-reference") == ("1.0.0", "2.0.0")
    assert isinstance(registry.get("foundry-rule-based-reference", "2.0.0"), _SecondVersionProvider)


@pytest.mark.unit
def test_provider_registry_returns_none_for_unknown_provider() -> None:
    registry = ProviderRegistry()

    assert registry.get("missing", "0.0.0") is None
    assert registry.versions("missing") == ()
