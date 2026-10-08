"""Worldness and living-instance evidence over the canonical runtime ports."""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import cast

from wanxiang_substrate.authoring.living_ports import BranchResult, LivingRuntimePort, ReplayState
from wanxiang_substrate.authoring.worldness import (
    BranchIsolationProof,
    RepairLoop,
    RepairRun,
    WorldnessEvaluator,
    WorldnessInput,
    WorldnessScore,
    prove_branch_isolation,
)
from wanxiang_substrate.compile.assembler import WorldPackageDraft
from wanxiang_substrate.host import WorldHost
from wanxiang_substrate.preview import PreviewInstall, PreviewWorld, instantiate_preview


@dataclass(frozen=True, slots=True)
class ActionProof:
    action_type: str
    event_id: str
    event_seq: int
    before_hash: str
    after_hash: str
    proposal_validated: bool
    committed: bool
    replay_equal: bool

    def to_dict(self) -> dict[str, object]:
        return {
            "action_type": self.action_type,
            "event_id": self.event_id,
            "event_seq": self.event_seq,
            "before_hash": self.before_hash,
            "after_hash": self.after_hash,
            "proposal_validated": self.proposal_validated,
            "committed": self.committed,
            "replay_equal": self.replay_equal,
        }


@dataclass(frozen=True, slots=True)
class LivingInstanceRecord:
    instance_id: str
    world_package_version: str
    package_id: str
    preview_id: str
    domain_versions: tuple[tuple[str, str], ...]
    branch_id: str
    snapshot_id: str
    event_head: int
    runtime_profile: str
    state_hash: str
    action: ActionProof | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "instance_id": self.instance_id,
            "world_package_version": self.world_package_version,
            "package_id": self.package_id,
            "preview_id": self.preview_id,
            "domain_versions": [list(item) for item in self.domain_versions],
            "branch_id": self.branch_id,
            "snapshot_id": self.snapshot_id,
            "event_head": self.event_head,
            "runtime_profile": self.runtime_profile,
            "state_hash": self.state_hash,
            "action": self.action.to_dict() if self.action else None,
        }


@dataclass(frozen=True, slots=True)
class WorldnessRun:
    package_id: str
    preview_id: str
    score: WorldnessScore
    repair: RepairRun
    living: LivingInstanceRecord
    branch_proof: BranchIsolationProof
    parent_hash_after_probe: str
    child_hash_after_probe: str

    def to_dict(self) -> dict[str, object]:
        return {
            "package_id": self.package_id,
            "preview_id": self.preview_id,
            "passed": self.score.passed,
            "overall": self.score.overall,
            "gates": {
                "previewable": self.score.gates.previewable,
                "publishable": self.score.gates.publishable,
                "living_ready": self.score.gates.living_ready,
            },
            "violations": list(self.score.violations),
            "dimensions": [{"name": name, "score": score} for name, score in self.score.dimensions],
            "evidence": [
                {
                    "name": item.name,
                    "measurement": item.measurement,
                    "score": item.score,
                    "evidence": list(item.evidence),
                    "failure": item.failure,
                    "remediation": item.remediation,
                }
                for item in self.score.evidence
            ],
            "repair": {
                "rounds": self.repair.rounds,
                "converged": self.repair.converged,
                "score_count": len(self.repair.scores),
                "candidate_count": len(self.repair.candidates),
                "cycle_count": len(self.repair.cycles),
            },
            "branch_proof": {
                "source_fingerprint": self.branch_proof.source_fingerprint,
                "branch_ids": list(self.branch_proof.branch_ids),
                "isolated": self.branch_proof.isolated,
                "parent_hash_after_probe": self.parent_hash_after_probe,
                "child_hash_after_probe": self.child_hash_after_probe,
            },
            "living": self.living.to_dict(),
        }


def instantiate_living_world(
    runtime: LivingRuntimePort,
    package: WorldPackageDraft,
    install: PreviewInstall,
    *,
    runtime_profile: str = "reference-commit-authority",
) -> tuple[PreviewWorld, LivingInstanceRecord]:
    """Instantiate a package, checkpoint it, and return its observable record."""
    world = instantiate_preview(runtime, package, install)
    snapshot = runtime.create_checkpoint(world.instance_id, world.branch_id)
    state = runtime.current_state(world.instance_id, world.branch_id)
    events = runtime.events(world.instance_id, world.branch_id)
    return world, LivingInstanceRecord(
        instance_id=world.instance_id.value,
        world_package_version=str(package.manifest.version),
        package_id=package.package_id,
        preview_id=install.preview_id,
        domain_versions=package.domain_versions,
        branch_id=world.branch_id.value,
        snapshot_id=snapshot.snapshot_id.value,
        event_head=events[-1].event_seq.value if events else 0,
        runtime_profile=runtime_profile,
        state_hash=state.semantic_hash(),
    )


def evaluate_living_world(
    runtime: LivingRuntimePort,
    world: PreviewWorld,
    package: WorldPackageDraft,
    living: LivingInstanceRecord,
) -> tuple[WorldnessRun, LivingInstanceRecord]:
    """Perform a real action, branch probe, replay, and dimensional evaluation."""
    before = runtime.current_state(world.instance_id, world.branch_id)
    before_hash = before.semantic_hash()
    first_entity = before.entities()[0] if before.entities() else None
    if first_entity is None:
        raise ValueError("living preview has no entity for the action proof")
    action_type = "set_status"
    world.step(action_type, {"entity_id": first_entity.entity_id.value, "status": "awake"})
    after = runtime.current_state(world.instance_id, world.branch_id)
    after_hash = after.semantic_hash()
    events = runtime.events(world.instance_id, world.branch_id)
    if not events:
        raise ValueError("living action produced no committed event")
    replayed = runtime.restore_and_replay(world.instance_id, world.branch_id)
    replay_state = cast("ReplayState", replayed).state
    replay_equal = replay_state.semantic_hash() == after_hash
    event = events[-1]
    action = ActionProof(
        action_type=action_type,
        event_id=event.event_id.value,
        event_seq=event.event_seq.value,
        before_hash=before_hash,
        after_hash=after_hash,
        proposal_validated=bool(event.delta.operations),
        committed=True,
        replay_equal=replay_equal,
    )
    updated_living = LivingInstanceRecord(
        instance_id=living.instance_id,
        world_package_version=living.world_package_version,
        package_id=living.package_id,
        preview_id=living.preview_id,
        domain_versions=living.domain_versions,
        branch_id=living.branch_id,
        snapshot_id=living.snapshot_id,
        event_head=event.event_seq.value,
        runtime_profile=living.runtime_profile,
        state_hash=after_hash,
        action=action,
    )
    child = cast("BranchResult", runtime.create_branch(world.instance_id, world.branch_id))
    child_host = WorldHost(runtime, world.instance_id, child.branch_id)
    child_world = PreviewWorld(
        world.install, runtime, child_host, world.instance_id, child.branch_id
    )
    child_world.step(
        action_type,
        {"entity_id": first_entity.entity_id.value, "status": "branch-probe"},
    )
    parent_hash_after_probe = runtime.current_state(
        world.instance_id, world.branch_id
    ).semantic_hash()
    child_hash_after_probe = runtime.current_state(
        world.instance_id, child.branch_id
    ).semantic_hash()
    parent_unchanged = parent_hash_after_probe == after_hash
    child_changed = child_hash_after_probe != after_hash
    branch_value = WorldnessInput(
        entity_count=len(package.draft.entities),
        relation_count=len(package.draft.relations),
        event_count=len(events),
        source_count=len(package.draft.source_refs),
        uncertainty=package.draft.uncertainty,
        replay_equal=replay_equal,
        branch_isolated=parent_unchanged,
        draft_id=package.draft_id,
        draft_revision=package.draft_revision,
        source_refs=package.draft.source_refs,
        domain_refs=tuple(item[0] for item in package.domain_versions),
        completion_refs=package.draft.completion_items,
        package_id=package.package_id,
        provider_ids=tuple(
            item for item in (package.draft.compiler_metadata.get("provider_id", ""),) if item
        ),
        place_count=len(package.draft.places),
        object_count=len(package.draft.objects),
        object_required=bool(package.draft.objects),
        evidence_coverage=package.evidence_coverage,
        action_committed=action.committed and action.proposal_validated,
        action_evidence_refs=("runtime.commit", "runtime.replay")
        if action.committed and action.proposal_validated
        else (),
    )
    branch_proof = prove_branch_isolation(
        branch_value, world.branch_id.value, child.branch_id.value
    )
    branch_proof = replace(
        branch_proof,
        isolated=branch_proof.isolated and parent_unchanged and child_changed,
    )
    branch_value = replace(
        branch_value, branch_isolated=branch_value.branch_isolated and branch_proof.isolated
    )
    score = WorldnessEvaluator().evaluate(branch_value)
    repair = RepairLoop().run(branch_value, rounds=2)
    return (
        WorldnessRun(
            package.package_id,
            world.install.preview_id,
            score,
            repair,
            updated_living,
            branch_proof,
            parent_hash_after_probe,
            child_hash_after_probe,
        ),
        updated_living,
    )


__all__ = [
    "ActionProof",
    "LivingInstanceRecord",
    "LivingRuntimePort",
    "WorldnessRun",
    "evaluate_living_world",
    "instantiate_living_world",
]
