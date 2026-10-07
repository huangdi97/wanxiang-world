"""Reproducible WorldRunArtifact: one saved, comparable, forkable world run.

The artifact is a product/research manifest over existing truth systems. It does
not copy canonical state: it pins version/runtime/history/trajectory/control refs
and derives a reproducibility fingerprint from those references.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.hashing import semantic_sha256


@dataclass(frozen=True, slots=True)
class WorldRunArtifact:
    artifact_id: str
    world_id: str
    worldline_id: str
    world_package_ref: str
    constitution_ref: str
    scenario_ref: str
    seed: str
    runtime_profile_ref: str
    runtime_lock_hash: str
    domain_refs: tuple[str, ...] = ()
    provider_bundle_refs: tuple[str, ...] = ()
    runtime_control_refs: tuple[str, ...] = ()
    commit_refs: tuple[str, ...] = ()
    snapshot_refs: tuple[str, ...] = ()
    actor_trajectory_refs: tuple[str, ...] = ()
    worldness_metrics: tuple[tuple[str, str], ...] = ()
    intervention_refs: tuple[str, ...] = ()
    branch_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "artifact_id",
            "world_id",
            "worldline_id",
            "world_package_ref",
            "constitution_ref",
            "scenario_ref",
            "seed",
            "runtime_profile_ref",
            "runtime_lock_hash",
        ):
            if not str(getattr(self, name)).strip():
                raise ValueError(f"{name} must be non-empty")
        metric_keys = [key for key, _value in self.worldness_metrics]
        if len(metric_keys) != len(set(metric_keys)):
            raise ValueError("worldness metric keys must be unique")

    @property
    def reproducibility_fingerprint(self) -> str:
        """Hash the run inputs and evidence refs without duplicating World state."""
        return semantic_sha256(
            {
                "world_id": self.world_id,
                "worldline_id": self.worldline_id,
                "world_package_ref": self.world_package_ref,
                "constitution_ref": self.constitution_ref,
                "domain_refs": sorted(self.domain_refs),
                "scenario_ref": self.scenario_ref,
                "seed": self.seed,
                "runtime_profile_ref": self.runtime_profile_ref,
                "runtime_lock_hash": self.runtime_lock_hash,
                "provider_bundle_refs": sorted(self.provider_bundle_refs),
                "runtime_control_refs": list(self.runtime_control_refs),
                "commit_refs": list(self.commit_refs),
                "snapshot_refs": list(self.snapshot_refs),
                "actor_trajectory_refs": list(self.actor_trajectory_refs),
                "worldness_metrics": sorted(self.worldness_metrics),
                "intervention_refs": list(self.intervention_refs),
                "branch_refs": sorted(self.branch_refs),
            }
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "artifact_id": self.artifact_id,
            "world_id": self.world_id,
            "worldline_id": self.worldline_id,
            "world_package_ref": self.world_package_ref,
            "constitution_ref": self.constitution_ref,
            "domain_refs": list(self.domain_refs),
            "scenario_ref": self.scenario_ref,
            "seed": self.seed,
            "runtime_profile_ref": self.runtime_profile_ref,
            "runtime_lock_hash": self.runtime_lock_hash,
            "provider_bundle_refs": list(self.provider_bundle_refs),
            "runtime_control_refs": list(self.runtime_control_refs),
            "commit_refs": list(self.commit_refs),
            "snapshot_refs": list(self.snapshot_refs),
            "actor_trajectory_refs": list(self.actor_trajectory_refs),
            "worldness_metrics": dict(self.worldness_metrics),
            "intervention_refs": list(self.intervention_refs),
            "branch_refs": list(self.branch_refs),
            "reproducibility_fingerprint": self.reproducibility_fingerprint,
            "canonical": False,
        }


__all__ = ["WorldRunArtifact"]
