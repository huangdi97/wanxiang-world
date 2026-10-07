"""WorldRunArtifact pins reproducibility evidence without becoming World truth."""

from __future__ import annotations

from wanxiang_research.world_run_artifact import WorldRunArtifact


def _artifact(**changes: object) -> WorldRunArtifact:
    values: dict[str, object] = {
        "artifact_id": "run:r7:001",
        "world_id": "world:r7",
        "worldline_id": "worldline:main",
        "world_package_ref": "world-package:r7@1",
        "constitution_ref": "constitution:r7@1",
        "domain_refs": ("domain:social@1", "domain:space@1"),
        "scenario_ref": "scenario:opening@1",
        "seed": "42",
        "runtime_profile_ref": "runtime:r7@1",
        "runtime_lock_hash": "lock:abc",
        "provider_bundle_refs": ("provider:model@1", "provider:history@1"),
        "runtime_control_refs": ("runtime-control:1", "runtime-control:2"),
        "commit_refs": ("event:1", "event:2"),
        "snapshot_refs": ("snapshot:2",),
        "actor_trajectory_refs": ("trajectory:actor-1:1",),
        "worldness_metrics": (("continuity", "1.0"),),
        "intervention_refs": ("intervention:1",),
        "branch_refs": ("branch:main", "branch:alt"),
    }
    values.update(changes)
    return WorldRunArtifact(**values)  # type: ignore[arg-type]


def test_fingerprint_is_deterministic_and_manifest_is_non_canonical() -> None:
    first = _artifact()
    second = _artifact(
        domain_refs=("domain:space@1", "domain:social@1"),
        provider_bundle_refs=("provider:history@1", "provider:model@1"),
        branch_refs=("branch:alt", "branch:main"),
    )

    assert first.reproducibility_fingerprint == second.reproducibility_fingerprint
    payload = first.to_dict()
    assert payload["canonical"] is False
    assert payload["commit_refs"] == ["event:1", "event:2"]
    assert "state" not in payload
    assert "prompt" not in payload


def test_fingerprint_changes_when_runtime_or_history_changes() -> None:
    baseline = _artifact().reproducibility_fingerprint
    assert _artifact(runtime_lock_hash="lock:def").reproducibility_fingerprint != baseline
    assert _artifact(commit_refs=("event:1", "event:3")).reproducibility_fingerprint != baseline
