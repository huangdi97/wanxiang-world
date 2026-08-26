"""World Registry catalog adapter over the existing package registry/install port."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError, NotFound

from wanxiang_substrate.packages import (
    InMemoryPackageRegistry,
    InstallRecord,
    PackageInstaller,
    PackageManifest,
    SemanticVersion,
)
from wanxiang_substrate.workshop.publishing import PublishingPolicy, PublishingProfile

RegistryLabel = Literal["official", "community"]


class RegistryPublishBlocked(ContractError):
    code = "world_registry_publish_blocked"


class RegistryEntryNotFound(NotFound):
    code = "world_registry_entry_not_found"


@dataclass(frozen=True, slots=True)
class WorldRegistryEntry:
    entry_id: str
    package_id: str
    version: SemanticVersion
    display_name: str
    label: RegistryLabel
    visibility: str
    owner_id: str
    categories: tuple[str, ...]
    tags: tuple[str, ...]
    compatibility: tuple[str, ...]
    provenance_refs: tuple[str, ...]
    manifest_hash: str
    listed: bool
    executable_trust: str

    def __post_init__(self) -> None:
        if not self.entry_id or not self.package_id or not self.display_name.strip():
            raise ContractError("registry entry requires id, package and display name")
        if self.label not in {"official", "community"}:
            raise ContractError(f"unsupported registry label {self.label!r}")
        if not self.provenance_refs:
            raise ContractError("registry entry requires package provenance")
        if any(not value.strip() for value in (*self.categories, *self.tags)):
            raise ContractError("registry categories and tags must be non-empty")

    def compatible_with(self, runtime_version: str) -> bool:
        return not self.compatibility or runtime_version in self.compatibility

    def to_dict(self) -> dict[str, object]:
        return {
            "entry_id": self.entry_id,
            "package_id": self.package_id,
            "version": str(self.version),
            "display_name": self.display_name,
            "label": self.label,
            "visibility": self.visibility,
            "owner_id": self.owner_id,
            "categories": list(self.categories),
            "tags": list(self.tags),
            "compatibility": list(self.compatibility),
            "provenance_refs": list(self.provenance_refs),
            "manifest_hash": self.manifest_hash,
            "listed": self.listed,
            "executable_trust": self.executable_trust,
        }


@dataclass(frozen=True, slots=True)
class WorldOpenRecord:
    entry: WorldRegistryEntry
    opened_by: str
    executable_loaded: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "entry": self.entry.to_dict(),
            "opened_by": self.opened_by,
            "executable_loaded": self.executable_loaded,
        }


@dataclass(frozen=True, slots=True)
class WorldInstall:
    entry_id: str
    record: InstallRecord


class WorldRegistryCatalog:
    """Search/index facade; package storage and install semantics stay shared."""

    def __init__(self, packages: InMemoryPackageRegistry | None = None) -> None:
        self.packages = packages or InMemoryPackageRegistry()
        self._entries: dict[str, WorldRegistryEntry] = {}
        self._installer = PackageInstaller()

    def register(
        self,
        manifest: PackageManifest,
        publishing: PublishingProfile,
        *,
        label: RegistryLabel = "community",
    ) -> WorldRegistryEntry:
        if manifest.kind != "world":
            raise RegistryPublishBlocked("only world manifests can enter the World Registry")
        if manifest.package_id != publishing.metadata.package_id:
            raise RegistryPublishBlocked("publishing metadata package id does not match manifest")
        if str(manifest.version) != publishing.metadata.version:
            raise RegistryPublishBlocked("publishing metadata version does not match manifest")
        decision = PublishingPolicy().assess(publishing)
        if not decision.publishable:
            raise RegistryPublishBlocked("; ".join(decision.reasons))
        self.packages.register(manifest)
        stored = self.packages.get(manifest.package_id, manifest.version)
        if stored is None:
            raise RegistryPublishBlocked("package registry did not retain the manifest")
        entry_id = f"{manifest.package_id}@{manifest.version}"
        entry = WorldRegistryEntry(
            entry_id,
            stored.package_id,
            stored.version,
            publishing.metadata.display_name,
            label,
            publishing.visibility,
            publishing.owner_id,
            publishing.metadata.categories,
            publishing.metadata.tags,
            publishing.metadata.compatibility,
            publishing.metadata.provenance_refs,
            stored.content_hash,
            decision.visible_in_plaza,
            stored.executable_trust,
        )
        self._entries[entry_id] = entry
        return entry

    def get(self, entry_id: str, *, viewer_id: str | None = None) -> WorldRegistryEntry:
        entry = self._entries.get(entry_id)
        if entry is None or not self._visible(entry, viewer_id):
            raise RegistryEntryNotFound(f"world registry entry {entry_id!r} not found")
        return entry

    def search(
        self,
        query: str = "",
        *,
        viewer_id: str | None = None,
        label: RegistryLabel | None = None,
        category: str | None = None,
        tag: str | None = None,
        runtime_version: str | None = None,
    ) -> tuple[WorldRegistryEntry, ...]:
        needle = query.strip().lower()
        found: list[WorldRegistryEntry] = []
        for entry in self._entries.values():
            if not self._visible(entry, viewer_id):
                continue
            if label is not None and entry.label != label:
                continue
            if category is not None and category not in entry.categories:
                continue
            if tag is not None and tag not in entry.tags:
                continue
            if runtime_version is not None and not entry.compatible_with(runtime_version):
                continue
            searchable = " ".join((entry.display_name, *entry.categories, *entry.tags)).lower()
            if needle and needle not in searchable:
                continue
            found.append(entry)
        return tuple(sorted(found, key=lambda item: (item.display_name.lower(), item.entry_id)))

    def open(self, entry_id: str, *, viewer_id: str | None = None) -> WorldOpenRecord:
        entry = self.get(entry_id, viewer_id=viewer_id)
        return WorldOpenRecord(entry, viewer_id or "anonymous")

    def install(
        self,
        entry_id: str,
        *,
        viewer_id: str | None = None,
        executable_extensions: tuple[str, ...] = (),
    ) -> WorldInstall:
        entry = self.get(entry_id, viewer_id=viewer_id)
        record = self._installer.install(
            self.packages,
            entry.package_id,
            entry.version,
            install_id=f"install:{entry.entry_id}",
            executable_extensions=executable_extensions,
            rights_refs=entry.provenance_refs,
            evidence_refs=entry.provenance_refs,
            created_from=entry.entry_id,
        )
        return WorldInstall(entry.entry_id, record)

    @staticmethod
    def _visible(entry: WorldRegistryEntry, viewer_id: str | None) -> bool:
        if entry.visibility == "public":
            return entry.listed
        return bool(viewer_id) and viewer_id == entry.owner_id


__all__ = [
    "RegistryEntryNotFound",
    "RegistryPublishBlocked",
    "WorldInstall",
    "WorldOpenRecord",
    "WorldRegistryCatalog",
    "WorldRegistryEntry",
]
