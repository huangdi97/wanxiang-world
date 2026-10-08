"""Bind a resolved Profile/Bundle/Artifact composition into one RuntimeLock.

This is deliberately a bridge, not another manager layer. Bundle resolution
describes the desired composition; RuntimeLock freezes the exact runnable
interpretation. The bridge fails closed if a required seam/provider/artifact
cannot be accounted for.
"""

from __future__ import annotations

from wanxiang_reality.bundles import ResolvedBundleStack
from wanxiang_reality.errors import RuntimeLockError
from wanxiang_reality.profiles import RealityProfile, RuntimeLock, build_runtime_lock


def build_runtime_lock_from_stack(
    reality: RealityProfile,
    resolved: ResolvedBundleStack,
    *,
    world_id: str,
    world_instance_id: str,
    worldline_id: str,
    composition_runtime: str,
    composition_runtime_version: str,
    service_contract_versions: dict[str, str],
    provider_versions: dict[str, str],
    schema_versions: dict[str, str],
    migration_lineage: tuple[str, ...],
    runtime_config_hash: str,
) -> RuntimeLock:
    """Freeze one resolved bundle stack into the canonical RuntimeLock shape."""
    reality_ref = f"{reality.profile_id}@{reality.version}"
    if resolved.world_profile.reality_profile_ref != reality_ref:
        raise RuntimeLockError(
            "resolved bundle stack reality profile does not match the supplied RealityProfile"
        )

    missing_seams = sorted(set(resolved.required_seams) - set(service_contract_versions))
    if missing_seams:
        raise RuntimeLockError(f"resolved bundle stack has unpinned service seams: {missing_seams}")

    missing_providers = sorted(set(resolved.world_profile.providers) - set(provider_versions))
    if missing_providers:
        raise RuntimeLockError(f"resolved bundle stack has unpinned providers: {missing_providers}")

    artifact_hashes = resolved.artifact_hashes()
    if not artifact_hashes:
        raise RuntimeLockError("resolved bundle stack must bind at least one runtime artifact")

    lineage = (*migration_lineage, f"bundle-stack:{resolved.digest}")
    return build_runtime_lock(
        reality,
        resolved.world_profile,
        world_id=world_id,
        world_instance_id=world_instance_id,
        worldline_id=worldline_id,
        composition_runtime=composition_runtime,
        composition_runtime_version=composition_runtime_version,
        service_contract_versions=dict(service_contract_versions),
        provider_versions=dict(provider_versions),
        artifact_hashes=artifact_hashes,
        schema_versions=dict(schema_versions),
        migration_lineage=lineage,
        runtime_config_hash=runtime_config_hash,
    )


__all__ = ["build_runtime_lock_from_stack"]
