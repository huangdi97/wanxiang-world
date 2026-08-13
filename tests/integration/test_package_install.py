"""G04E: package install, export & migration compatibility."""

from __future__ import annotations

import pytest
from wanxiang_substrate.packages.errors import (
    IncompatiblePackage,
    InvalidManifest,
    UntrustedExecutable,
)
from wanxiang_substrate.packages.fixture import build_town_packages
from wanxiang_substrate.packages.install import (
    PackageInstaller,
    export_install,
    install_export_hash,
)
from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry


def _registry() -> InMemoryPackageRegistry:
    registry = InMemoryPackageRegistry()
    for manifest in build_town_packages():
        registry.register(manifest)
    return registry


@pytest.mark.unit
def test_install_export_roundtrip() -> None:
    registry = _registry()
    record = PackageInstaller().install(registry, "town-scenario", install_id="inst_1")
    exported = export_install(record)
    assert exported["package"] == "town-scenario"
    assert exported["version"] == "1.0.0"
    assert "town-domain" in [pin[0] for pin in record.pins]
    assert exported["lock_hash"] == record.lock_hash
    # Stable export hash: same install exports identically.
    assert install_export_hash(exported) == install_export_hash(export_install(record))


@pytest.mark.unit
def test_tampered_hash_rejected() -> None:
    registry = _registry()
    tampered = PackageManifest(
        package_id="town-domain",
        kind="domain",
        version=SemanticVersion(1, 0, 0),
        name="Town Domain",
        content_hash="0" * 64,
    )
    # Registration verifies the content hash and rejects tampering.
    with pytest.raises(InvalidManifest):
        registry.register(tampered)


@pytest.mark.unit
def test_untrusted_package_cannot_install_executables() -> None:
    registry = InMemoryPackageRegistry()
    registry.register(
        PackageManifest(
            package_id="plugin",
            kind="domain",
            version=SemanticVersion(1, 0, 0),
            name="Plugin",
            executable_trust="untrusted",
        ).with_hash()
    )
    with pytest.raises(UntrustedExecutable):
        PackageInstaller().install(
            registry,
            "plugin",
            executable_extensions=(".py",),
        )


@pytest.mark.unit
def test_incompatible_dependency_rejected() -> None:
    from wanxiang_substrate.packages.errors import MissingDependency

    registry = InMemoryPackageRegistry()
    registry.register(
        PackageManifest(
            package_id="town-domain",
            kind="domain",
            version=SemanticVersion(1, 0, 0),
            name="Town Domain",
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="root",
            kind="world",
            version=SemanticVersion(1, 0, 0),
            name="Root",
            dependencies=(("town-domain", ">=2.0.0"),),
        ).with_hash()
    )
    with pytest.raises(MissingDependency):
        PackageInstaller().install(registry, "root")


@pytest.mark.unit
def test_publishing_v2_does_not_mutate_v1_pinned_instance() -> None:
    registry = _registry()
    installer = PackageInstaller()
    v1 = installer.install(registry, "town-scenario", install_id="inst_v1")
    v1_hash = v1.lock_hash
    # Publish v2 of town-world and town-scenario.
    registry.register(
        PackageManifest(
            package_id="town-world",
            kind="world",
            version=SemanticVersion(2, 0, 0),
            name="Town World 2",
            dependencies=(("town-domain", "^1.0.0"),),
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="town-scenario",
            kind="scenario",
            version=SemanticVersion(2, 0, 0),
            name="Town Scenario 2",
            dependencies=(("town-world", "^2.0.0"),),
        ).with_hash()
    )
    v2 = installer.install(registry, "town-scenario", install_id="inst_v2")
    assert v2.package_version == SemanticVersion(2, 0, 0)
    # The v1-pinned install record is untouched.
    assert v1.lock_hash == v1_hash
    assert v1.version_for("town-world") == SemanticVersion(1, 0, 0)


@pytest.mark.unit
def test_explicit_upgrade_records_fork_requirement() -> None:
    registry = _registry()
    installer = PackageInstaller()
    v1 = installer.install(registry, "town-scenario", install_id="inst_v1")
    # Upgrade to v2 with an incompatible major bump on town-domain.
    registry.register(
        PackageManifest(
            package_id="town-domain",
            kind="domain",
            version=SemanticVersion(2, 0, 0),
            name="Town Domain 2",
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="town-world",
            kind="world",
            version=SemanticVersion(2, 0, 0),
            name="Town World 2",
            dependencies=(("town-domain", "^2.0.0"),),
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="town-scenario",
            kind="scenario",
            version=SemanticVersion(2, 0, 0),
            name="Town Scenario 2",
            dependencies=(("town-world", "^2.0.0"),),
        ).with_hash()
    )
    with pytest.raises(IncompatiblePackage):
        installer.upgrade(registry, v1, SemanticVersion(2, 0, 0), install_id="inst_v2")
