"""Synthetic domain/world/scenario packages for G04A (explicitly synthetic)."""

from __future__ import annotations

from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion


def build_town_packages() -> tuple[PackageManifest, ...]:
    """Deterministic synthetic package graph:

    town-domain v1.0.0 (no deps)
    town-world  v1.0.0 (depends on town-domain ^1.0)
    town-scenario v1.0.0 (depends on town-world ^1.0)
    """
    domain = PackageManifest(
        package_id="town-domain",
        kind="domain",
        version=SemanticVersion(1, 0, 0),
        name="Town Domain",
        executable_trust="trusted",
    ).with_hash()
    world = PackageManifest(
        package_id="town-world",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name="Town World",
        dependencies=(("town-domain", "^1.0.0"),),
        executable_trust="trusted",
    ).with_hash()
    scenario = PackageManifest(
        package_id="town-scenario",
        kind="scenario",
        version=SemanticVersion(1, 0, 0),
        name="Town Scenario",
        dependencies=(("town-world", "^1.0.0"),),
        executable_trust="untrusted",
    ).with_hash()
    return (domain, world, scenario)


def build_conflicting_packages() -> tuple[PackageManifest, PackageManifest]:
    """Two versions of town-domain that cannot both satisfy a ^1.0 and ==2.0 pin."""
    v1 = PackageManifest(
        package_id="town-domain",
        kind="domain",
        version=SemanticVersion(1, 2, 0),
        name="Town Domain 1",
    ).with_hash()
    v2 = PackageManifest(
        package_id="town-domain",
        kind="domain",
        version=SemanticVersion(2, 0, 0),
        name="Town Domain 2",
    ).with_hash()
    return (v1, v2)
