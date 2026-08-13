"""Deterministic dependency resolver for package manifests (G04A)."""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from wanxiang_substrate.packages.errors import (
    DependencyConflict,
    DependencyCycle,
    MissingDependency,
)
from wanxiang_substrate.packages.model import PackageLock, PackageManifest, SemanticVersion


class DependencyResolver:
    """Resolves a package graph to a stable lock, deterministic by ordering.

    Rules: dependencies are processed in sorted order; the highest satisfying
    version wins; a package requested twice with incompatible constraints is a
    conflict; any cycle is a hard error (no partial lock).
    """

    def __init__(self, registry: Mapping[tuple[str, SemanticVersion], PackageManifest]) -> None:
        self._registry = registry

    def resolve(
        self,
        root_id: str,
        root_version: SemanticVersion | None = None,
    ) -> PackageLock:
        pinned: dict[str, SemanticVersion] = {}
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(package_id: str, constraint: str | None) -> None:
            if package_id in visiting:
                raise DependencyCycle(f"dependency cycle involving {package_id!r}")
            existing = pinned.get(package_id)
            if existing is not None:
                _verify_compatible(package_id, existing, constraint)
                return
            if package_id in visited:
                return
            visiting.add(package_id)
            versions = self._available(package_id)
            if not versions:
                raise MissingDependency(f"package {package_id!r} is not registered")
            chosen: SemanticVersion | None = None
            if constraint is not None:
                chosen = self._pick_matching(package_id, versions, constraint)
                if chosen is None:
                    raise MissingDependency(
                        f"no version of {package_id!r} satisfies {constraint!r}"
                    )
            else:
                chosen = versions[0]
            pinned[package_id] = chosen
            manifest = self._manifest(package_id, chosen)
            for dep_id, dep_constraint in manifest.dependencies:
                visit(dep_id, dep_constraint)
            visiting.remove(package_id)
            visited.add(package_id)

        visit(root_id, None)
        if root_version is not None and pinned[root_id] != root_version:
            raise MissingDependency(
                f"root {root_id!r} resolved to {pinned[root_id]} not {root_version}"
            )
        pins = tuple(sorted(pinned.items(), key=lambda item: item[0]))
        return PackageLock(
            root_package=root_id,
            root_version=pinned[root_id],
            pins=pins,
        )

    def _available(self, package_id: str) -> Sequence[SemanticVersion]:
        versions = [
            version
            for (pid, version) in self._registry  # type: ignore[union-attr]
            if pid == package_id
        ]
        return tuple(sorted(versions, reverse=True))

    def _manifest(self, package_id: str, version: SemanticVersion) -> PackageManifest:
        manifest = self._registry.get((package_id, version))
        if manifest is None:
            raise MissingDependency(f"package {package_id!r}@{version} is not registered")
        return manifest

    def _pick_matching(
        self, package_id: str, versions: Sequence[SemanticVersion], constraint: str
    ) -> SemanticVersion | None:
        from wanxiang_substrate.packages.model import VersionConstraint

        parsed = VersionConstraint(constraint)
        for version in versions:
            if parsed.matches(version):
                return version
        return None


def _verify_compatible(package_id: str, pinned: SemanticVersion, constraint: str | None) -> None:
    """A package already pinned must satisfy every later constraint."""
    if constraint is None:
        return
    from wanxiang_substrate.packages.model import VersionConstraint

    if not VersionConstraint(constraint).matches(pinned):
        raise DependencyConflict(
            f"package {package_id!r} pinned to {pinned} does not satisfy {constraint!r}"
        )
