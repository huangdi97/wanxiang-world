"""Explicit fork/intervention runner over the authoritative runtime (G95C)."""

from __future__ import annotations

from dataclasses import replace

from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.authoring.living_ports import LivingRuntimePort
from wanxiang_substrate.reality.errors import ExperimentError
from wanxiang_substrate.reality.intervention import (
    ExperimentInterventionRunner,
    ExperimentSetup,
    Intervention,
)
from wanxiang_substrate.world_lab.fork_ledger import InterventionLedger
from wanxiang_substrate.world_lab.fork_models import (
    FORK_SCHEMA_VERSION,
    ForkedInterventionRun,
    ForkProvenance,
    ForkRun,
    InterventionLedgerEntry,
    InterventionRun,
)


class ForkInterventionRunner:
    """Fork through the existing runtime and resume by replay verification."""

    def __init__(self, ledger: InterventionLedger | None = None) -> None:
        self.ledger = ledger or InterventionLedger()
        self.intervention_ledger = self.ledger
        self._branch_runner = ExperimentInterventionRunner()

    def fork(
        self,
        runtime: LivingRuntimePort,
        instance_id: WorldInstanceId,
        parent_branch_id: BranchId,
        setup: ExperimentSetup,
        intervention: Intervention,
        *,
        fork_revision: BranchRevision | int | None = None,
    ) -> ForkedInterventionRun:
        parent_state = runtime.current_state(instance_id, parent_branch_id)
        parent_events = runtime.events(instance_id, parent_branch_id)
        requested = _revision_value(fork_revision)
        resolved = _event_revision(intervention.trigger, parent_events)
        if resolved is not None and requested is not None and resolved != requested:
            raise ExperimentError("event trigger revision does not match explicit fork revision")
        effective = resolved if resolved is not None else requested
        branch = self._branch_runner.fork(
            runtime,
            instance_id,
            parent_branch_id,
            setup,
            intervention,
            fork_revision=None if effective is None else BranchRevision(effective),
        )
        provenance = ForkProvenance(
            provenance_id=f"fork-provenance:{intervention.intervention_id}:{branch.branch_ref}",
            instance_ref=instance_id.value,
            parent_branch_ref=parent_branch_id.value,
            parent_head_revision=parent_state.revision.value,
            parent_head_event_seq=len(parent_events),
            parent_head_hash=parent_state.semantic_hash(),
            fork_revision=branch.fork_revision,
            fork_event_seq=branch.fork_event_seq,
            fork_snapshot_ref=branch.fork_snapshot_ref,
            child_branch_ref=branch.branch_ref,
            intervention_id=intervention.intervention_id,
            artifact_ref=intervention.artifact_ref,
            trigger=intervention.trigger,
        )
        run_id = f"intervention-run:{intervention.intervention_id}:{branch.branch_ref}"
        run = ForkedInterventionRun(
            run_id=run_id,
            branch=branch,
            provenance=provenance,
            resume_cursor=branch.fork_revision,
        )
        self.ledger.append(
            InterventionLedgerEntry(
                entry_id=f"{run_id}:fork",
                run_id=run_id,
                provenance_id=provenance.provenance_id,
                branch_ref=branch.branch_ref,
                intervention_id=intervention.intervention_id,
                status="forked",
                cursor_revision=branch.fork_revision,
            )
        )
        return run

    start = fork

    def resume(
        self,
        runtime: LivingRuntimePort,
        run: ForkedInterventionRun,
        *,
        expected_revision: BranchRevision | int | None = None,
    ) -> ForkedInterventionRun:
        instance_id = WorldInstanceId(run.provenance.instance_ref)
        branch_id = BranchId(run.branch.branch_ref)
        current = runtime.current_state(instance_id, branch_id)
        expected = _revision_value(expected_revision)
        if expected is not None and current.revision.value != expected:
            raise ExperimentError("resumed branch revision does not match expected cursor")
        replayed = runtime.restore_and_replay(instance_id, branch_id)
        replay_state = getattr(replayed, "state", None)
        replay_hash = getattr(replay_state, "semantic_hash", lambda: "")()
        if not isinstance(replay_hash, str) or not replay_hash:
            raise ExperimentError("runtime replay did not return a semantic state hash")
        if replay_hash != current.semantic_hash():
            raise ExperimentError("resumed branch replay hash diverged")
        updated = replace(
            run,
            resume_cursor=current.revision.value,
            resume_count=run.resume_count + 1,
            status="resumed",
            replay_hash=replay_hash,
        )
        self.ledger.append(
            InterventionLedgerEntry(
                entry_id=f"{run.run_id}:resume:{updated.resume_count}",
                run_id=run.run_id,
                provenance_id=run.provenance.provenance_id,
                branch_ref=run.branch.branch_ref,
                intervention_id=run.provenance.intervention_id,
                status="resumed",
                cursor_revision=updated.resume_cursor,
                replay_hash=replay_hash,
            )
        )
        return updated


def _revision_value(value: BranchRevision | int | None) -> int | None:
    if value is None:
        return None
    if isinstance(value, BranchRevision):
        return value.value
    if type(value) is int and value >= 0:
        return value
    raise ExperimentError("fork revision must be a non-negative integer")


def _event_revision(trigger: object, events: tuple[object, ...]) -> int | None:
    if getattr(trigger, "kind", None) != "event":
        return None
    trigger_value = getattr(trigger, "value", None)
    for event in events:
        event_id = getattr(getattr(event, "event_id", None), "value", None)
        command_id = getattr(getattr(event, "command_id", None), "value", None)
        refs = {event_id, command_id, f"event:{event_id}", f"command:{command_id}"}
        if trigger_value in refs:
            revision = getattr(getattr(event, "revision", None), "value", None)
            if type(revision) is int and revision >= 0:
                return revision
    raise ExperimentError(f"event trigger {trigger_value!r} is not present in parent history")


__all__ = [
    "FORK_SCHEMA_VERSION",
    "ForkInterventionRunner",
    "ForkProvenance",
    "ForkRun",
    "ForkedInterventionRun",
    "InterventionLedger",
    "InterventionLedgerEntry",
    "InterventionRun",
]
