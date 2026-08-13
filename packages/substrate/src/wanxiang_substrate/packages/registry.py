"""Local package registry ports and in-memory adapter (G04A)."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Sequence
from typing import Protocol

from wanxiang_substrate.packages.errors import InvalidManifest, PackageNotFound
from wanxiang_substrate.packages.model import PackageLock, PackageManifest, SemanticVersion
from wanxiang_substrate.packages.resolver import DependencyResolver


class PackageRegistry(Protocol):
    """Port for a local package store (no remote requirement)."""

    def register(self, manifest: PackageManifest) -> None: ...
    def get(self, package_id: str, version: SemanticVersion) -> PackageManifest | None: ...
    def versions(self, package_id: str) -> Sequence[SemanticVersion]: ...
    def resolve(self, root_id: str, root_version: SemanticVersion | None = None) -> PackageLock: ...


class InMemoryPackageRegistry:
    """Deterministic local registry; content hashes verified on register."""

    def __init__(self) -> None:
        self._manifests: dict[tuple[str, SemanticVersion], PackageManifest] = {}
        self._resolver: DependencyResolver | None = None

    def register(self, manifest: PackageManifest) -> None:
        hashed = manifest.with_hash()
        if manifest.content_hash and manifest.content_hash != hashed.content_hash:
            raise InvalidManifest(
                f"content hash mismatch for {manifest.package_id}@{manifest.version}"
            )
        self._manifests[(hashed.package_id, hashed.version)] = hashed

    def get(self, package_id: str, version: SemanticVersion) -> PackageManifest | None:
        return self._manifests.get((package_id, version))

    def versions(self, package_id: str) -> Sequence[SemanticVersion]:
        found = [version for (pid, version) in self._manifests if pid == package_id]
        return tuple(sorted(found, reverse=True))

    def resolve(self, root_id: str, root_version: SemanticVersion | None = None) -> PackageLock:
        from wanxiang_substrate.packages.resolver import DependencyResolver

        if self._resolver is None:
            self._resolver = DependencyResolver(self._manifests)
        return self._resolver.resolve(root_id, root_version)

    def manifest_json(self, package_id: str, version: SemanticVersion) -> str:
        manifest = self.get(package_id, version)
        if manifest is None:
            raise PackageNotFound(f"{package_id}@{version} not found")
        return json.dumps(manifest.canonical(), sort_keys=True, separators=(",", ":"))


def content_sha256(payload: str) -> str:
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
