"""Resolved Bundle stack -> RuntimeLock binding."""

from __future__ import annotations

import pytest
from wanxiang_reality.bundles import RuntimeArtifact, WorldBundle, resolve_bundle_stack
from wanxiang_reality.composition import build_runtime_lock_from_stack
from wanxiang_reality.errors import RuntimeLockError
from wanxiang_reality.profiles import RealityProfile
from wanxiang_reality.versions import Version

SHA = "a" * 64


def _reality() -> RealityProfile:
    return RealityProfile(
        profile_id="reality.bundle-test",
        version=Version(1, 0, 0),
        required_seams=("wanxiang.authority@1", "wanxiang.history@1"),
    )


def _resolved():
    bundle = WorldBundle(
        bundle_id="wanxiang-base",
        version=Version(1, 0, 0),
        reality_profile_ref="reality.bundle-test@1.0.0",
        required_seams=("wanxiang.authority@1", "wanxiang.history@1"),
        providers=("provider.history.memory",),
        dimensions={
            "actors": "actors.none",
            "capabilities": "capabilities.none",
            "distribution": "distribution.web",
            "experience": "experience.observe",
            "memory": "memory.none",
            "projection": "projection.text",
            "simulation": "simulation.none",
            "space": "space.graph",
            "time": "time.linear",
        },
        artifacts=(
            RuntimeArtifact(
                package_name="wanxiang-base-runtime",
                version=Version(1, 0, 0),
                integrity_hash=SHA,
                source_provenance="repo:wanxiang-base",
                build_provenance="ci:bundle-test",
            ),
        ),
    )
    return resolve_bundle_stack(
        (bundle,),
        profile_id="world.bundle-test",
        version=Version(1, 0, 0),
    )


def _build(**overrides: object):
    kwargs: dict[str, object] = {
        "world_id": "world-1",
        "world_instance_id": "instance-1",
        "worldline_id": "worldline-1",
        "composition_runtime": "cordis",
        "composition_runtime_version": "4.0.0-rc.10",
        "service_contract_versions": {
            "wanxiang.authority@1": "1.0.0",
            "wanxiang.history@1": "1.0.0",
        },
        "provider_versions": {"provider.history.memory": "1.0.0"},
        "schema_versions": {"canonical": "1"},
        "migration_lineage": ("genesis",),
        "runtime_config_hash": "config-sha",
    }
    kwargs.update(overrides)
    return build_runtime_lock_from_stack(_reality(), _resolved(), **kwargs)  # type: ignore[arg-type]


def test_resolved_stack_artifacts_and_digest_are_pinned_into_runtime_lock() -> None:
    lock = _build()

    assert lock.artifact_hashes == {"wanxiang-base-runtime": SHA}
    assert lock.world_profile_ref == "world.bundle-test@1.0.0"
    assert lock.migration_lineage[-1].startswith("bundle-stack:")
    lock.validate()


def test_missing_required_seam_fails_closed() -> None:
    with pytest.raises(RuntimeLockError, match="unpinned service seams"):
        _build(service_contract_versions={"wanxiang.history@1": "1.0.0"})


def test_missing_provider_fails_closed() -> None:
    with pytest.raises(RuntimeLockError, match="unpinned providers"):
        _build(provider_versions={})


def test_reality_profile_mismatch_is_not_a_bundle_override() -> None:
    wrong = RealityProfile(
        profile_id="reality.other",
        version=Version(1, 0, 0),
        required_seams=("wanxiang.authority@1",),
    )
    with pytest.raises(RuntimeLockError, match="reality profile"):
        build_runtime_lock_from_stack(
            wrong,
            _resolved(),
            world_id="world-1",
            world_instance_id="instance-1",
            worldline_id="worldline-1",
            composition_runtime="cordis",
            composition_runtime_version="4.0.0-rc.10",
            service_contract_versions={
                "wanxiang.authority@1": "1.0.0",
                "wanxiang.history@1": "1.0.0",
            },
            provider_versions={"provider.history.memory": "1.0.0"},
            schema_versions={"canonical": "1"},
            migration_lineage=("genesis",),
            runtime_config_hash="config-sha",
        )
