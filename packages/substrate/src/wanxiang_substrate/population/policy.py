"""Deterministic no-LLM scheduler policy for substrate-level behavior."""

from __future__ import annotations

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime


class DeterministicPolicy:
    """Produces deterministic commands for scheduled actors (no LLM).

    Focus actors rest (restore energy) at their rate; actors with due duties
    complete them first. Command ids are derived deterministically so replay is
    stable and duplicate wakeups cannot duplicate effects.
    """

    def __init__(self, instance_id: WorldInstanceId, branch_id: BranchId) -> None:
        self._instance_id = instance_id
        self._branch_id = branch_id

    def build_command(
        self,
        actor_id: EntityId,
        action: str,
        expected_revision: int,
        ticks: int,
        seq: int,
    ) -> CommandEnvelope:
        if action == "scheduler.rest":
            return CommandEnvelope(
                command_id=CommandId(f"sched_rest_{actor_id.value}_{ticks}_{seq}"),
                instance_id=self._instance_id,
                branch_id=self._branch_id,
                expected_revision=BranchRevision(expected_revision),
                action_type="body.rest",
                payload={"actor_id": actor_id.value, "ticks": 5},
                actor_id=None,
                world_time=WorldTime(ticks),
            )
        if action == "scheduler.complete_duty":
            raise ValidationRejected("complete_duty requires a duty id payload")
        raise ValidationRejected(f"unsupported scheduled action {action!r}")
