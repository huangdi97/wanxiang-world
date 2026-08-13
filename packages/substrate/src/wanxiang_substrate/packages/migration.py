"""Package manifest schema migrations and compatibility matrix (G04A)."""

from __future__ import annotations

from collections.abc import Callable

from wanxiang_substrate.packages.errors import InvalidManifest
from wanxiang_substrate.packages.model import (
    UNTRUSTED,
    PackageManifest,
    SemanticVersion,
)

CURRENT_MANIFEST_SCHEMA = 2


def _migrate_v1_to_v2(manifest: PackageManifest) -> PackageManifest:
    """v1 manifests gain an explicit executable_trust (default untrusted)."""
    return PackageManifest(
        package_id=manifest.package_id,
        kind=manifest.kind,
        version=manifest.version,
        name=manifest.name,
        dependencies=manifest.dependencies,
        schema_version=CURRENT_MANIFEST_SCHEMA,
        content_hash=manifest.content_hash,
        executable_trust=manifest.executable_trust or UNTRUSTED,
        compat=manifest.compat,
    )


# schema_version -> migrator (v1 source manifests are upgraded to current).
_MIGRATIONS: dict[int, Callable[[PackageManifest], PackageManifest]] = {
    1: _migrate_v1_to_v2,
}


def migrate_manifest(
    manifest: PackageManifest, target_schema: int = CURRENT_MANIFEST_SCHEMA
) -> PackageManifest:
    """Upgrade an older manifest through declared migration steps."""
    if manifest.schema_version == target_schema:
        return manifest
    if manifest.schema_version > target_schema:
        raise InvalidManifest(
            f"manifest schema {manifest.schema_version} is newer than target {target_schema}"
        )
    migrator = _MIGRATIONS.get(manifest.schema_version)
    if migrator is None:
        raise InvalidManifest(f"no migration path from manifest schema {manifest.schema_version}")
    upgraded = migrator(manifest)
    return migrate_manifest(upgraded, target_schema)


# Backwards-compatibility matrix: package pairs whose major versions are known
# compatible. Used by the instance pinning/install gate.
COMPATIBILITY_MATRIX: tuple[tuple[str, SemanticVersion, str, SemanticVersion], ...] = (
    ("town-domain", SemanticVersion(1, 0, 0), "town-world", SemanticVersion(1, 0, 0)),
    ("town-domain", SemanticVersion(2, 0, 0), "town-world", SemanticVersion(2, 0, 0)),
)


def compatible(
    package_id: str,
    version: SemanticVersion,
    other_id: str,
    other_version: SemanticVersion,
) -> bool:
    for pid, ver, oid, over in COMPATIBILITY_MATRIX:
        if pid == package_id and ver == version and oid == other_id and over == other_version:
            return True
    return False
