"""G17F: registry publish, install, upgrade, deprecation & dependency resolution.

- Publishing a new version does not change an existing pinned install.
- Upgrade requires explicit action (upgrade_candidate) and a new install.
- Dependency conflicts produce actionable failures.
- Deprecated/yanked packages remain identifiable for old world history.
"""

from __future__ import annotations

import pytest
from wanxiang_substrate.packages.errors import DependencyConflict
from wanxiang_substrate.packages.lifecycle import RegistryLifecycle
from wanxiang_substrate.packages.model import UNTRUSTED, PackageManifest, SemanticVersion
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry


def _manifest(
    package_id: str, version: tuple[int, int, int], deps: tuple[tuple[str, str], ...] = ()
) -> PackageManifest:
    return PackageManifest(
        package_id=package_id,
        kind="domain",
        version=SemanticVersion(*version),
        name=package_id,
        dependencies=deps,
        executable_trust=UNTRUSTED,
    ).with_hash()


def test_new_publish_does_not_change_existing_install() -> None:
    reg = InMemoryPackageRegistry()
    lc = RegistryLifecycle(reg)
    lc.publish(_manifest("lib-a", (1, 0, 0)))
    v1 = lc.install("lib-a", SemanticVersion(1, 0, 0))
    # Publish v2; the v1 install record is unchanged.
    lc.publish(_manifest("lib-a", (2, 0, 0)))
    v2_install = lc.install("lib-a", SemanticVersion(2, 0, 0))
    assert v1.package_version == SemanticVersion(1, 0, 0)
    assert v2_install.package_version == SemanticVersion(2, 0, 0)
    assert v1.lock_hash != v2_install.lock_hash


def test_upgrade_requires_explicit_action() -> None:
    reg = InMemoryPackageRegistry()
    lc = RegistryLifecycle(reg)
    lc.publish(_manifest("lib-a", (1, 0, 0)))
    lc.publish(_manifest("lib-a", (1, 5, 0)))
    lc.publish(_manifest("lib-a", (2, 0, 0)))
    assert lc.upgrade_candidate("lib-a", SemanticVersion(1, 0, 0)) == SemanticVersion(1, 5, 0)
    # The running instance is not auto-upgraded; explicit install is required.
    install_v1 = lc.install("lib-a", SemanticVersion(1, 0, 0))
    assert install_v1.package_version == SemanticVersion(1, 0, 0)


def test_dependency_conflict_actionable() -> None:
    reg = InMemoryPackageRegistry()
    lc = RegistryLifecycle(reg)
    lc.publish(_manifest("lib-a", (1, 0, 0)))
    lc.publish(_manifest("lib-a", (2, 0, 0)))
    app = _manifest(
        "app",
        (1, 0, 0),
        deps=(("lib-a", "^1.0.0"), ("lib-a", "==2.0.0")),
    )
    lc.publish(app)
    with pytest.raises(DependencyConflict):
        lc.install("app")


def test_deprecated_and_yanked_remain_identifiable() -> None:
    reg = InMemoryPackageRegistry()
    lc = RegistryLifecycle(reg)
    lc.publish(_manifest("lib-a", (1, 0, 0)))
    lc.deprecate("lib-a", "1.0.0", "replaced by v2")
    lc.yank("lib-a", "1.0.0")
    # Metadata remains: old world history is reproducible.
    assert reg.get("lib-a", SemanticVersion(1, 0, 0)) is not None
    assert lc.is_deprecated("lib-a", SemanticVersion(1, 0, 0)) == "replaced by v2"
    assert lc.is_yanked("lib-a", SemanticVersion(1, 0, 0)) is True
    # New installs of a yanked version are rejected, but the metadata stays.
    with pytest.raises(ValueError):
        lc.install("lib-a", SemanticVersion(1, 0, 0))
    assert reg.get("lib-a", SemanticVersion(1, 0, 0)) is not None
