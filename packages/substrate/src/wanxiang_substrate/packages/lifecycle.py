"""Registry lifecycle: publish, deprecate/yank, upgrade candidate, pin (G17F).

Running instances never auto-upgrade: publishing a new version leaves existing
installs pinned. Deprecation/yank preserves historical metadata so old world
history stays reproducible (yank never erases).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from wanxiang_substrate.packages.install import PackageInstaller
from wanxiang_substrate.packages.model import PackageManifest, SemanticVersion
from wanxiang_substrate.packages.registry import InMemoryPackageRegistry


@dataclass
class RegistryLifecycle:
    """High-level registry operations over the public registry."""

    registry: InMemoryPackageRegistry
    _deprecations: dict[tuple[str, str], str] = field(default_factory=dict)
    _yanked: set[tuple[str, str]] = field(default_factory=set)

    def publish(self, manifest: PackageManifest) -> None:
        self.registry.register(manifest)

    def deprecate(self, package_id: str, version: str, reason: str) -> None:
        self._deprecations[(package_id, version)] = reason

    def yank(self, package_id: str, version: str) -> None:
        # Yank blocks NEW installs but preserves the metadata for old history.
        self._yanked.add((package_id, version))

    def is_deprecated(self, package_id: str, version: SemanticVersion) -> str | None:
        return self._deprecations.get(
            (package_id, f"{version.major}.{version.minor}.{version.patch}")
        )

    def is_yanked(self, package_id: str, version: SemanticVersion) -> bool:
        return (package_id, f"{version.major}.{version.minor}.{version.patch}") in self._yanked

    def upgrade_candidate(
        self, package_id: str, current: SemanticVersion
    ) -> SemanticVersion | None:
        newer = [v for v in self.registry.versions(package_id) if v > current]
        return min(newer) if newer else None

    def install(
        self, root_id: str, version: SemanticVersion | None = None, *, check_yank: bool = True
    ) -> Any:
        if version is not None and check_yank and self.is_yanked(root_id, version):
            raise ValueError(f"package {root_id}@{version} is yanked for new installs")
        return PackageInstaller().install(self.registry, root_id, root_version=version)
