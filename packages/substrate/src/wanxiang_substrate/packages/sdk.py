"""Python package authoring helpers + OpenAPI/version policy (G12C)."""

from __future__ import annotations

from wanxiang_substrate.packages.errors import InvalidManifest
from wanxiang_substrate.packages.model import PackageManifest, VersionConstraint


def validate_manifest_for_authoring(manifest: PackageManifest) -> tuple[str, ...]:
    """Public authoring helper: returns diagnostics (empty = valid)."""
    diagnostics: list[str] = []
    if manifest.schema_version <= 0:
        diagnostics.append("schema_version must be positive")
    if not manifest.name:
        diagnostics.append("name is required")
    for dep_id, constraint in manifest.dependencies:
        try:
            VersionConstraint(constraint)
        except InvalidManifest as exc:
            diagnostics.append(f"dependency {dep_id!r}: {exc}")
    return tuple(diagnostics)


PUBLIC_API_POLICY = (
    "vocabulary: worlds/instances/branches/commands/events/projections",
    "version policy: additive changes within v1; breaking changes require a new major",
    "sdk: openapi.json -> TypeScript client types, deterministic",
)
