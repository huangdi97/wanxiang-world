"""Verified Capability Marketplace projections over the Foundry registry.

The marketplace is discovery metadata, not a second trust system. A listing must
bind to an already-admitted CapabilityPackage by package digest; commercial
terms, ranking hints or maintainer metadata can never upgrade verification or
activate a capability.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_execution import ExecutionClass
from wanxiang_foundry.errors import RegistryError
from wanxiang_foundry.levels import KnowledgeLevel, PromotionLevel
from wanxiang_foundry.registry import VerifiedCapabilityRegistry


@dataclass(frozen=True, slots=True)
class CapabilityMarketplaceListing:
    capability_id: str
    version: str
    package_digest: str
    maintainer: str
    license_summary: str
    permissions: tuple[str, ...]
    cost_model: str
    latency_class: str
    failure_modes: tuple[str, ...]
    compatible_domains: tuple[str, ...]
    compatible_world_versions: tuple[str, ...]
    security_status: str
    last_verified_at: str
    promotion_level: PromotionLevel
    knowledge_level: KnowledgeLevel
    runtime_class: ExecutionClass
    validity_inputs: tuple[str, ...]
    known_limitations: tuple[str, ...]
    lifecycle_status: str

    def __post_init__(self) -> None:
        for name in (
            "capability_id",
            "version",
            "package_digest",
            "maintainer",
            "license_summary",
            "cost_model",
            "latency_class",
            "security_status",
            "last_verified_at",
            "lifecycle_status",
        ):
            if not str(getattr(self, name)).strip():
                raise RegistryError(f"marketplace {name} must be non-empty")
        for name in (
            "permissions",
            "failure_modes",
            "compatible_domains",
            "compatible_world_versions",
        ):
            values = getattr(self, name)
            if any(not value.strip() for value in values) or len(values) != len(set(values)):
                raise RegistryError(f"marketplace {name} must contain unique non-empty values")


@dataclass(frozen=True, slots=True)
class CapabilityDiscoveryQuery:
    required_domains: tuple[str, ...] = ()
    compatible_world_version: str = ""
    execution_class: ExecutionClass | None = None
    include_deprecated: bool = False


class VerifiedCapabilityMarketplace:
    """Read-only discovery catalog backed by the verified capability registry."""

    def __init__(self, registry: VerifiedCapabilityRegistry) -> None:
        self._registry = registry
        self._listings: dict[tuple[str, str], CapabilityMarketplaceListing] = {}

    def publish(
        self,
        capability_id: str,
        version: str,
        *,
        maintainer: str,
        license_summary: str,
        permissions: tuple[str, ...],
        cost_model: str,
        latency_class: str,
        failure_modes: tuple[str, ...],
        compatible_domains: tuple[str, ...],
        compatible_world_versions: tuple[str, ...],
        security_status: str,
        last_verified_at: str,
    ) -> CapabilityMarketplaceListing:
        package = self._registry.get(capability_id, version)
        if package is None:
            raise RegistryError("marketplace cannot publish an unregistered capability")
        promotion = self._registry.promotions(capability_id, version)
        if promotion is None or promotion.level is not PromotionLevel.C3_VERIFIED:
            raise RegistryError("marketplace requires a C3-verified capability")
        status = self._registry.status(capability_id, version)
        if status is None or status in {"SUSPENDED", "REVOKED"}:
            raise RegistryError(f"marketplace cannot publish lifecycle status {status!r}")
        key = (capability_id, version)
        if key in self._listings:
            raise RegistryError(f"marketplace listing already exists for {capability_id}@{version}")
        listing = CapabilityMarketplaceListing(
            capability_id=capability_id,
            version=version,
            package_digest=package.package_digest(),
            maintainer=maintainer,
            license_summary=license_summary,
            permissions=permissions,
            cost_model=cost_model,
            latency_class=latency_class,
            failure_modes=failure_modes,
            compatible_domains=compatible_domains,
            compatible_world_versions=compatible_world_versions,
            security_status=security_status,
            last_verified_at=last_verified_at,
            promotion_level=package.promotion_level,
            knowledge_level=package.knowledge_level,
            runtime_class=package.runtime.execution_class,
            validity_inputs=package.validity.supported_inputs,
            known_limitations=package.validity.known_limitations,
            lifecycle_status=status,
        )
        self._listings[key] = listing
        return listing

    def refresh_lifecycle(
        self, capability_id: str, version: str
    ) -> CapabilityMarketplaceListing:
        key = (capability_id, version)
        listing = self._listings.get(key)
        if listing is None:
            raise RegistryError(f"marketplace listing not found for {capability_id}@{version}")
        status = self._registry.status(capability_id, version)
        if status is None:
            raise RegistryError("marketplace registry binding disappeared")
        updated = replace(listing, lifecycle_status=status)
        self._listings[key] = updated
        return updated

    def get(self, capability_id: str, version: str) -> CapabilityMarketplaceListing | None:
        return self._listings.get((capability_id, version))

    def discover(
        self, query: CapabilityDiscoveryQuery = CapabilityDiscoveryQuery()
    ) -> tuple[CapabilityMarketplaceListing, ...]:
        results: list[CapabilityMarketplaceListing] = []
        for key, listing in self._listings.items():
            status = self._registry.status(*key)
            if status not in {"ACTIVE", "DEPRECATED"}:
                continue
            if status == "DEPRECATED" and not query.include_deprecated:
                continue
            package = self._registry.get(*key)
            if package is None or package.package_digest() != listing.package_digest:
                raise RegistryError("marketplace package binding no longer verifies")
            if query.execution_class is not None and listing.runtime_class is not query.execution_class:
                continue
            if query.required_domains and not set(query.required_domains).issubset(
                listing.compatible_domains
            ):
                continue
            if (
                query.compatible_world_version
                and query.compatible_world_version not in listing.compatible_world_versions
            ):
                continue
            results.append(replace(listing, lifecycle_status=status))
        return tuple(
            sorted(
                results,
                key=lambda item: (
                    item.capability_id,
                    item.version,
                    item.package_digest,
                ),
            )
        )


__all__ = [
    "CapabilityDiscoveryQuery",
    "CapabilityMarketplaceListing",
    "VerifiedCapabilityMarketplace",
]
