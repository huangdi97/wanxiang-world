"""Verified Capability Marketplace cannot become a parallel trust system."""

from __future__ import annotations

from wanxiang_execution import ExecutionClass
from wanxiang_foundry.marketplace import (
    CapabilityDiscoveryQuery,
    VerifiedCapabilityMarketplace,
)

from tests.unit.foundry.conftest import admitted_package


def _marketplace() -> tuple[VerifiedCapabilityMarketplace, object]:
    registry, package = admitted_package()
    marketplace = VerifiedCapabilityMarketplace(registry)
    marketplace.publish(
        package.capability_id,
        package.version,
        maintainer="Wanxiang reference maintainer",
        license_summary="reference rights basis",
        permissions=("filesystem:scratch",),
        cost_model="free/reference",
        latency_class="interactive",
        failure_modes=("invalid-input", "runtime-failure"),
        compatible_domains=("science", "research"),
        compatible_world_versions=("r7",),
        security_status="C3-reference",
        last_verified_at="2026-10-07T00:00:00Z",
    )
    return marketplace, package


def test_discovery_exposes_verification_runtime_and_validity_without_activation() -> None:
    marketplace, package = _marketplace()
    found = marketplace.discover(
        CapabilityDiscoveryQuery(
            required_domains=("science",),
            compatible_world_version="r7",
            execution_class=ExecutionClass.PROCESS,
        )
    )

    assert len(found) == 1
    listing = found[0]
    assert listing.package_digest == package.package_digest()
    assert listing.promotion_level == package.promotion_level
    assert listing.knowledge_level == package.knowledge_level
    assert listing.validity_inputs == package.validity.supported_inputs
    assert listing.known_limitations == package.validity.known_limitations
    assert not hasattr(marketplace, "activate")
    assert not hasattr(marketplace, "commit")


def test_commercial_metadata_does_not_change_verification_tier() -> None:
    marketplace, package = _marketplace()
    listing = marketplace.get(package.capability_id, package.version)
    assert listing is not None
    assert listing.cost_model == "free/reference"
    assert listing.promotion_level == package.promotion_level


def test_revoked_capability_disappears_from_discovery() -> None:
    marketplace, package = _marketplace()
    registry = marketplace._registry  # noqa: SLF001 - verify lifecycle binding in qualification
    registry.revoke(package.capability_id, package.version, "security regression")

    assert marketplace.discover() == ()
    refreshed = marketplace.refresh_lifecycle(package.capability_id, package.version)
    assert refreshed.lifecycle_status == "REVOKED"
