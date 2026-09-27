"""Artifact2Capability provider seam and registry.

The foundry must never hard-code one conversion method. Artifact2Capability is
the contract; Paper2Agent is one replaceable provider, never the base. New
providers register with a provider_id/provider_version pair; registering the same
pair twice is refused so a provider cannot be silently replaced.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Protocol, runtime_checkable

from wanxiang_foundry.candidate import ArtifactRef, CapabilityCandidate
from wanxiang_foundry.errors import RegistryError


@runtime_checkable
class Artifact2CapabilityProvider(Protocol):
    """A replaceable provider that proposes a capability from an artifact.

    Attributes:
        provider_id: Stable provider id.
        provider_version: Provider version string.
    """

    provider_id: str
    provider_version: str

    def propose(
        self, artifact: ArtifactRef, declaration: Mapping[str, object]
    ) -> CapabilityCandidate:
        """Propose a capability candidate from an artifact and declaration.

        Args:
            artifact: The source artifact reference.
            declaration: Declared fields describing the intended capability.

        Returns:
            A proposal-only capability candidate.
        """
        ...


class ProviderRegistry:
    """A registry of Artifact2Capability providers keyed by id and version."""

    def __init__(self) -> None:
        self._providers: dict[tuple[str, str], Artifact2CapabilityProvider] = {}

    def register(self, provider: Artifact2CapabilityProvider) -> None:
        """Register a provider, refusing a silent replacement of id+version.

        Args:
            provider: Provider to register.

        Raises:
            RegistryError: If a provider with this id and version already exists.
        """
        key = (provider.provider_id, provider.provider_version)
        if key in self._providers:
            raise RegistryError(
                "provider already registered for provider_id="
                f"{provider.provider_id!r} provider_version={provider.provider_version!r}"
            )
        self._providers[key] = provider

    def get(self, provider_id: str, provider_version: str) -> Artifact2CapabilityProvider | None:
        """Return the provider for id+version, or None when absent."""
        return self._providers.get((provider_id, provider_version))

    def versions(self, provider_id: str) -> tuple[str, ...]:
        """Return the registered versions for provider_id, sorted."""
        return tuple(sorted(version for (pid, version) in self._providers if pid == provider_id))
