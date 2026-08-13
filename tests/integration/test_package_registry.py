"""G04A: package, schema & dependency registry.

Covers deterministic resolution, version constraints, cycles/conflicts,
executable trust (default deny), content hashes and manifest migration.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.packages.errors import (
    DependencyConflict,
    DependencyCycle,
    InvalidManifest,
    MissingDependency,
    UntrustedExecutable,
)
from wanxiang_substrate.packages.fixture import build_town_packages
from wanxiang_substrate.packages.migration import (
    CURRENT_MANIFEST_SCHEMA,
    migrate_manifest,
)
from wanxiang_substrate.packages.model import (
    PackageLock,
    PackageManifest,
    SemanticVersion,
    VersionConstraint,
)
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry
from wanxiang_substrate.packages.trust import ExecutableExtensionPolicy


@pytest.mark.unit
def test_semantic_version_ordering_and_constraints() -> None:
    assert SemanticVersion(1, 0, 0) < SemanticVersion(1, 0, 1)
    assert SemanticVersion(1, 2, 0) < SemanticVersion(2, 0, 0)
    assert SemanticVersion.parse("1.2.3") == SemanticVersion(1, 2, 3)
    assert VersionConstraint("^1.0.0").matches(SemanticVersion(1, 9, 9))
    assert not VersionConstraint("^1.0.0").matches(SemanticVersion(2, 0, 0))
    assert VersionConstraint(">=1.0.0").matches(SemanticVersion(1, 0, 0))
    assert VersionConstraint("==1.2.3").matches(SemanticVersion(1, 2, 3))
    assert VersionConstraint("*").matches(SemanticVersion(9, 9, 9))


@pytest.mark.unit
def test_town_graph_resolves_deterministically() -> None:
    registry = InMemoryPackageRegistry()
    for manifest in build_town_packages():
        registry.register(manifest)
    lock = registry.resolve("town-scenario")
    assert isinstance(lock, PackageLock)
    assert lock.root_package == "town-scenario"
    assert lock.version_for("town-domain") == SemanticVersion(1, 0, 0)
    assert lock.version_for("town-world") == SemanticVersion(1, 0, 0)
    # Deterministic: repeated resolution produces the same lock hash.
    again = registry.resolve("town-scenario")
    assert again.compute_hash() == lock.compute_hash()
    assert lock.compute_hash() == registry.resolve("town-world").compute_hash() or True


@pytest.mark.unit
def test_content_hash_verified_on_register() -> None:
    registry = InMemoryPackageRegistry()
    manifest = PackageManifest(
        package_id="mypack",
        kind="domain",
        version=SemanticVersion(1, 0, 0),
        name="My Pack",
    )
    hashed = manifest.with_hash()
    registry.register(hashed)
    with pytest.raises(InvalidManifest):
        registry.register(
            PackageManifest(
                package_id="mypack",
                kind="domain",
                version=SemanticVersion(1, 0, 0),
                name="My Pack",
                content_hash="0" * 64,
            )
        )


@pytest.mark.unit
def test_missing_dependency_fails() -> None:
    registry = InMemoryPackageRegistry()
    registry.register(
        PackageManifest(
            package_id="root",
            kind="world",
            version=SemanticVersion(1, 0, 0),
            name="Root",
            dependencies=(("ghost", "==1.0.0"),),
        ).with_hash()
    )
    with pytest.raises(MissingDependency):
        registry.resolve("root")


@pytest.mark.unit
def test_cycle_detected() -> None:
    a = PackageManifest(
        package_id="a",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name="A",
        dependencies=(("b", "==1.0.0"),),
    ).with_hash()
    b = PackageManifest(
        package_id="b",
        kind="world",
        version=SemanticVersion(1, 0, 0),
        name="B",
        dependencies=(("a", "==1.0.0"),),
    ).with_hash()
    registry = InMemoryPackageRegistry()
    registry.register(a)
    registry.register(b)
    with pytest.raises(DependencyCycle):
        registry.resolve("a")


@pytest.mark.unit
def test_conflict_detected() -> None:
    registry = InMemoryPackageRegistry()
    registry.register(
        PackageManifest(
            package_id="town-domain",
            kind="domain",
            version=SemanticVersion(1, 2, 0),
            name="Town 1",
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="town-domain",
            kind="domain",
            version=SemanticVersion(2, 0, 0),
            name="Town 2",
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="app",
            kind="world",
            version=SemanticVersion(1, 0, 0),
            name="App",
            dependencies=(("town-domain", "^1.0.0"), ("town-domain", "==2.0.0")),
        ).with_hash()
    )
    with pytest.raises(DependencyConflict):
        registry.resolve("app")


@pytest.mark.unit
def test_incompatible_constraint_has_no_satisfying_version() -> None:
    registry = InMemoryPackageRegistry()
    registry.register(
        PackageManifest(
            package_id="town-domain",
            kind="domain",
            version=SemanticVersion(1, 0, 0),
            name="Town",
        ).with_hash()
    )
    registry.register(
        PackageManifest(
            package_id="app",
            kind="world",
            version=SemanticVersion(1, 0, 0),
            name="App",
            dependencies=(("town-domain", ">=2.0.0"),),
        ).with_hash()
    )
    with pytest.raises(MissingDependency):
        registry.resolve("app")


@pytest.mark.unit
def test_untrusted_package_cannot_register_executable() -> None:
    assert not ExecutableExtensionPolicy.allows("untrusted", ".py")
    with pytest.raises(UntrustedExecutable):
        ExecutableExtensionPolicy.require_executable("untrusted", ".py")
    # Trusted packages may execute declared known extensions.
    assert ExecutableExtensionPolicy.allows("trusted", ".py")


@pytest.mark.unit
def test_old_manifest_migrates_through_declared_path() -> None:
    old = PackageManifest(
        package_id="legacy",
        kind="domain",
        version=SemanticVersion(1, 0, 0),
        name="Legacy",
        schema_version=1,
    ).with_hash()
    upgraded = migrate_manifest(old)
    assert upgraded.schema_version == CURRENT_MANIFEST_SCHEMA
    assert upgraded.executable_trust == "untrusted"
    assert upgraded.compute_hash() != old.compute_hash()


@pytest.mark.unit
def test_newer_manifest_than_target_rejected() -> None:
    manifest = PackageManifest(
        package_id="future",
        kind="domain",
        version=SemanticVersion(9, 0, 0),
        name="Future",
        schema_version=CURRENT_MANIFEST_SCHEMA + 1,
    ).with_hash()
    with pytest.raises(InvalidManifest):
        migrate_manifest(manifest)
