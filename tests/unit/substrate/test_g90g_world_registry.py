"""G90G: searchable World Registry over the existing package/trust boundary."""

from __future__ import annotations

import pytest
from wanxiang_substrate.packages import PackageManifest, SemanticVersion, UntrustedExecutable
from wanxiang_substrate.workshop import (
    PackageMetadata,
    PublishingProfile,
    RegistryPublishBlocked,
    RightsSummary,
    WorldRegistryCatalog,
)


def _publishing(package_id: str, *, visibility: str = "public") -> PublishingProfile:
    return PublishingProfile(
        f"profile:{package_id}",
        visibility,  # type: ignore[arg-type]
        "author",
        PackageMetadata(
            package_id,
            "1.0.0",
            "Registry Town",
            categories=("narrative",),
            tags=("reference",),
            compatibility=("v5.4",),
            provenance_refs=("intent:registry",),
        ),
        RightsSummary.creator_intent("intent:registry"),
    )


def test_registry_search_open_and_install_reuse_package_registry() -> None:
    catalog = WorldRegistryCatalog()
    manifest = PackageManifest(
        "world:registry-town",
        "world",
        SemanticVersion(1, 0, 0),
        "Registry Town",
    ).with_hash()
    entry = catalog.register(manifest, _publishing(manifest.package_id), label="official")
    assert catalog.search("town", label="official", runtime_version="v5.4") == (entry,)
    opened = catalog.open(entry.entry_id)
    assert opened.executable_loaded is False
    installed = catalog.install(entry.entry_id)
    assert installed.record.package_id == manifest.package_id


def test_untrusted_package_is_data_only_and_blocked_for_executable_install() -> None:
    catalog = WorldRegistryCatalog()
    manifest = PackageManifest(
        "world:untrusted",
        "world",
        SemanticVersion(1, 0, 0),
        "Untrusted World",
    ).with_hash()
    entry = catalog.register(manifest, _publishing(manifest.package_id))
    assert catalog.install(entry.entry_id).record.package_id == manifest.package_id
    with pytest.raises(UntrustedExecutable):
        catalog.install(entry.entry_id, executable_extensions=(".py",))


def test_blocked_rights_never_enter_registry() -> None:
    catalog = WorldRegistryCatalog()
    manifest = PackageManifest(
        "world:blocked",
        "world",
        SemanticVersion(1, 0, 0),
        "Blocked World",
    ).with_hash()
    profile = _publishing(manifest.package_id)
    blocked = PublishingProfile(
        profile.profile_id,
        profile.visibility,
        profile.owner_id,
        profile.metadata,
        RightsSummary(blocked_refs=("private_source",)),
    )
    with pytest.raises(RegistryPublishBlocked):
        catalog.register(manifest, blocked)
