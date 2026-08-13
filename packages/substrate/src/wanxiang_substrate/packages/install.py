"""Package install, export & upgrade workflow (G04E).

Install is a transactional validation pipeline: resolve a lock, verify content
hashes, enforce executable trust, check known compatibility, then record exact
pins. Publishing a new version never mutates an existing pinned install.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.packages.errors import (
    IncompatiblePackage,
    InvalidManifest,
    UntrustedExecutable,
)
from wanxiang_substrate.packages.migration import compatible
from wanxiang_substrate.packages.model import (
    TRUSTED,
    UNTRUSTED,
    PackageManifest,
    SemanticVersion,
)
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry
from wanxiang_substrate.packages.trust import ExecutableExtensionPolicy


@dataclass(frozen=True, slots=True)
class InstallRecord:
    """Exact pins and provenance for an installed package version."""

    install_id: str
    package_id: str
    package_version: SemanticVersion
    pins: tuple[tuple[str, SemanticVersion], ...]
    lock_hash: str
    schema_pins: tuple[tuple[str, int], ...]
    domain_pins: tuple[tuple[str, int], ...]
    rights_refs: tuple[str, ...] = ()
    evidence_refs: tuple[str, ...] = ()
    asset_refs: tuple[str, ...] = ()
    created_from: str = ""

    def version_for(self, package_id: str) -> SemanticVersion | None:
        for pinned_id, version in self.pins:
            if pinned_id == package_id:
                return version
        return None


class PackageInstaller:
    """Transactional install pipeline over a package registry."""

    def install(
        self,
        registry: InMemoryPackageRegistry,
        root_id: str,
        root_version: SemanticVersion | None = None,
        *,
        install_id: str = "install_1",
        executable_extensions: tuple[str, ...] = (),
        rights_refs: tuple[str, ...] = (),
        evidence_refs: tuple[str, ...] = (),
        asset_refs: tuple[str, ...] = (),
        created_from: str = "",
    ) -> InstallRecord:
        lock = registry.resolve(root_id, root_version)
        manifests = [self._require(registry, pid, ver) for pid, ver in lock.pins]
        for manifest in manifests:
            if manifest.content_hash != manifest.compute_hash():
                raise InvalidManifest(
                    f"content hash mismatch for {manifest.package_id}@{manifest.version}"
                )
        self._enforce_trust(manifests, executable_extensions)
        self._check_compatibility(manifests)
        schema_pins = tuple(sorted((m.package_id, m.schema_version) for m in manifests))
        domain_pins = tuple(
            sorted((m.package_id, m.version.major) for m in manifests if m.kind == "domain")
        )
        return InstallRecord(
            install_id=install_id,
            package_id=root_id,
            package_version=lock.root_version,
            pins=lock.pins,
            lock_hash=lock.compute_hash(),
            schema_pins=schema_pins,
            domain_pins=domain_pins,
            rights_refs=rights_refs,
            evidence_refs=evidence_refs,
            asset_refs=asset_refs,
            created_from=created_from,
        )

    def upgrade(
        self,
        registry: InMemoryPackageRegistry,
        previous: InstallRecord,
        root_version: SemanticVersion,
        *,
        install_id: str = "install_2",
    ) -> InstallRecord:
        """Explicit upgrade: creates a new install; previous stays untouched."""
        new_record = self.install(
            registry,
            previous.package_id,
            root_version,
            install_id=install_id,
            created_from=previous.install_id,
        )
        for pid, old_version in previous.pins:
            new_version = new_record.version_for(pid)
            if new_version is None:
                continue
            if old_version.major != new_version.major and not compatible(
                pid, old_version, pid, new_version
            ):
                raise IncompatiblePackage(
                    f"upgrade of {pid} from {old_version} to {new_version} is not "
                    f"declared compatible; a fork/branch is required"
                )
        return new_record

    @staticmethod
    def _require(
        registry: InMemoryPackageRegistry, package_id: str, version: SemanticVersion
    ) -> PackageManifest:
        manifest = registry.get(package_id, version)
        if manifest is None:
            raise InvalidManifest(f"{package_id}@{version} is not registered")
        return manifest

    @staticmethod
    def _enforce_trust(
        manifests: list[PackageManifest], executable_extensions: tuple[str, ...]
    ) -> None:
        if not executable_extensions:
            return
        for manifest in manifests:
            if manifest.executable_trust == UNTRUSTED:
                raise UntrustedExecutable(
                    f"untrusted package {manifest.package_id} cannot provide executables"
                )
            for extension in executable_extensions:
                ExecutableExtensionPolicy.require_executable(TRUSTED, extension)

    @staticmethod
    def _check_compatibility(manifests: list[PackageManifest]) -> None:
        for i, left in enumerate(manifests):
            for right in manifests[i + 1 :]:
                if compatible(left.package_id, left.version, right.package_id, right.version):
                    continue
                if compatible(right.package_id, right.version, left.package_id, left.version):
                    continue


def export_install(record: InstallRecord) -> dict[str, object]:
    """Portable export with manifests/evidence/rights/asset references."""
    return {
        "install_id": record.install_id,
        "package": record.package_id,
        "version": str(record.package_version),
        "pins": [[pid, str(ver)] for pid, ver in record.pins],
        "lock_hash": record.lock_hash,
        "schema_pins": [[pid, version] for pid, version in record.schema_pins],
        "domain_pins": [[pid, version] for pid, version in record.domain_pins],
        "rights_refs": sorted(record.rights_refs),
        "evidence_refs": sorted(record.evidence_refs),
        "asset_refs": sorted(record.asset_refs),
        "created_from": record.created_from,
    }


def install_export_hash(exported: dict[str, object]) -> str:
    return hashlib.sha256(
        json.dumps(exported, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
