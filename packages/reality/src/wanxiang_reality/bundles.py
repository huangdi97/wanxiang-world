"""R7 Profile / Bundle / Lock / Artifact composition contracts.

A Bundle is an editable/default composition unit above Cordis. It names seams,
providers, world dimensions and executable artifacts; it owns no canonical
state. Multiple bundles may be stacked, but semantic conflicts fail closed
unless an explicit BundlePatch resolves the *world-profile* dimension conflict.

This module intentionally keeps RealityProfile changes out of ordinary patching:
switching reality semantics is a migration concern, not a convenience override.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from wanxiang_reality.errors import ProfileError
from wanxiang_reality.hashing import canonical_digest
from wanxiang_reality.profiles import WorldProfile
from wanxiang_reality.versions import Version

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, slots=True)
class RuntimeArtifact:
    """Addressable executable/provider artifact identity."""

    package_name: str
    version: Version
    integrity_hash: str
    source_provenance: str
    build_provenance: str
    signature: str = ""

    def __post_init__(self) -> None:
        for name in ("package_name", "source_provenance", "build_provenance"):
            if not str(getattr(self, name)).strip():
                raise ProfileError(f"runtime artifact {name} must not be empty")
        if not _SHA256_RE.fullmatch(self.integrity_hash):
            raise ProfileError("runtime artifact integrity_hash must be lowercase sha256 hex")


@dataclass(frozen=True, slots=True)
class WorldBundle:
    """Composable default slice for a WorldProfile."""

    bundle_id: str
    version: Version
    reality_profile_ref: str
    required_seams: tuple[str, ...] = ()
    providers: tuple[str, ...] = ()
    dimensions: dict[str, str] = field(default_factory=dict)
    artifacts: tuple[RuntimeArtifact, ...] = ()

    def __post_init__(self) -> None:
        if not self.bundle_id.strip():
            raise ProfileError("bundle_id must not be empty")
        if not self.reality_profile_ref.strip():
            raise ProfileError("bundle reality_profile_ref must not be empty")
        _require_sorted_unique("required_seams", self.required_seams)
        _require_sorted_unique("providers", self.providers)
        if any(not key.strip() or not value.strip() for key, value in self.dimensions.items()):
            raise ProfileError("bundle dimensions must contain non-empty keys and values")
        artifact_names = [artifact.package_name for artifact in self.artifacts]
        if artifact_names != sorted(set(artifact_names)):
            raise ProfileError("bundle artifacts must be sorted by unique package_name")

    @property
    def ref(self) -> str:
        return f"{self.bundle_id}@{self.version}"


@dataclass(frozen=True, slots=True)
class BundlePatch:
    """Explicit profile override; never changes RealityProfile semantics."""

    add_providers: tuple[str, ...] = ()
    remove_providers: tuple[str, ...] = ()
    dimension_overrides: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_sorted_unique("add_providers", self.add_providers)
        _require_sorted_unique("remove_providers", self.remove_providers)
        overlap = sorted(set(self.add_providers) & set(self.remove_providers))
        if overlap:
            raise ProfileError(f"bundle patch adds and removes the same providers: {overlap}")
        if any(not key.strip() or not value.strip() for key, value in self.dimension_overrides.items()):
            raise ProfileError("bundle patch dimension overrides must be non-empty")


@dataclass(frozen=True, slots=True)
class ResolvedBundleStack:
    """Deterministic bundle resolution result used to build a RuntimeLock."""

    world_profile: WorldProfile
    bundle_refs: tuple[str, ...]
    required_seams: tuple[str, ...]
    artifacts: tuple[RuntimeArtifact, ...]
    digest: str

    def artifact_hashes(self) -> dict[str, str]:
        return {artifact.package_name: artifact.integrity_hash for artifact in self.artifacts}


def _require_sorted_unique(field_name: str, values: tuple[str, ...]) -> None:
    if list(values) != sorted(set(values)):
        raise ProfileError(f"{field_name} must be sorted and free of duplicates")


def resolve_bundle_stack(
    bundles: tuple[WorldBundle, ...],
    *,
    profile_id: str,
    version: Version,
    patch: BundlePatch | None = None,
) -> ResolvedBundleStack:
    """Resolve ordered bundles into one versioned WorldProfile.

    Bundle order is part of the digest, but conflicts are not silently
    last-write-wins. A conflicting world dimension requires an explicit patch.
    RealityProfile refs and executable artifact identities must agree across all
    bundles; changing either is migration/security-sensitive.
    """
    if not bundles:
        raise ProfileError("at least one bundle is required")
    if not profile_id.strip():
        raise ProfileError("resolved world profile_id must not be empty")
    refs = tuple(bundle.ref for bundle in bundles)
    if len(set(refs)) != len(refs):
        raise ProfileError("bundle stack must not contain duplicate bundle refs")

    reality_refs = {bundle.reality_profile_ref for bundle in bundles}
    if len(reality_refs) != 1:
        raise ProfileError(
            "bundle stack cannot silently combine multiple RealityProfile refs"
        )
    reality_profile_ref = next(iter(reality_refs))

    seams: set[str] = set()
    providers: set[str] = set()
    dimensions: dict[str, str] = {}
    conflicts: dict[str, tuple[str, str]] = {}
    artifacts: dict[str, RuntimeArtifact] = {}

    for bundle in bundles:
        seams.update(bundle.required_seams)
        providers.update(bundle.providers)
        for name, value in bundle.dimensions.items():
            existing = dimensions.get(name)
            if existing is not None and existing != value:
                conflicts[name] = (existing, value)
            else:
                dimensions[name] = value
        for artifact in bundle.artifacts:
            existing_artifact = artifacts.get(artifact.package_name)
            if existing_artifact is not None and existing_artifact != artifact:
                raise ProfileError(
                    f"bundle artifact conflict for {artifact.package_name!r}"
                )
            artifacts[artifact.package_name] = artifact

    resolved_patch = patch or BundlePatch()
    unresolved = sorted(set(conflicts) - set(resolved_patch.dimension_overrides))
    if unresolved:
        raise ProfileError(
            f"bundle dimension conflicts require explicit overrides: {unresolved}"
        )
    for name, value in resolved_patch.dimension_overrides.items():
        dimensions[name] = value

    providers.update(resolved_patch.add_providers)
    providers.difference_update(resolved_patch.remove_providers)

    world = WorldProfile(
        profile_id=profile_id,
        version=version,
        reality_profile_ref=reality_profile_ref,
        providers=tuple(sorted(providers)),
        dimensions=dict(sorted(dimensions.items())),
    )
    artifact_tuple = tuple(artifacts[name] for name in sorted(artifacts))
    seam_tuple = tuple(sorted(seams))
    projection = {
        "world_profile": {
            "profile_id": world.profile_id,
            "version": str(world.version),
            "reality_profile_ref": world.reality_profile_ref,
            "providers": list(world.providers),
            "dimensions": world.dimensions,
        },
        "bundle_refs": list(refs),
        "required_seams": list(seam_tuple),
        "artifacts": [
            {
                "package_name": artifact.package_name,
                "version": str(artifact.version),
                "integrity_hash": artifact.integrity_hash,
                "source_provenance": artifact.source_provenance,
                "build_provenance": artifact.build_provenance,
                "signature": artifact.signature,
            }
            for artifact in artifact_tuple
        ],
    }
    return ResolvedBundleStack(
        world_profile=world,
        bundle_refs=refs,
        required_seams=seam_tuple,
        artifacts=artifact_tuple,
        digest=canonical_digest(projection),
    )


__all__ = [
    "BundlePatch",
    "ResolvedBundleStack",
    "RuntimeArtifact",
    "WorldBundle",
    "resolve_bundle_stack",
]
