"""WorldEnvironment facade: honest subset of the future host contract.

Only methods with real behavior are exposed; nothing is faked. Unsupported
operations (reset, background advance, multiplayer) are intentionally absent.
"""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.entity import FieldValue
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.snapshot import SnapshotMetadata
from wanxiang_domain.time import WorldTime
from wanxiang_runtime.branch import BranchMetadata

from wanxiang_application.world_runtime import (
    CreateWorldResult,
    SubmitCommandResult,
    WorldRuntime,
)


class WorldEnvironment:
    """Deterministic synthetic environment facade (M1 subset)."""

    def __init__(self, runtime: WorldRuntime) -> None:
        self._runtime = runtime

    def create(self, instance_id: WorldInstanceId | None = None) -> CreateWorldResult:
        return self._runtime.create_world(instance_id=instance_id)

    def observe(self, instance_id: WorldInstanceId, branch_id: BranchId) -> dict[str, object]:
        from wanxiang_runtime.state import state_to_primitive

        return state_to_primitive(self._runtime.current_state(instance_id, branch_id))

    def legal_actions(self) -> tuple[str, ...]:
        return self._runtime.action_types()

    def step(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        action_type: str,
        payload: Mapping[str, FieldValue],
        *,
        expected_revision: int,
        command_id: CommandId | None = None,
        world_time: WorldTime | None = None,
    ) -> SubmitCommandResult:
        from wanxiang_domain.command import CommandEnvelope
        from wanxiang_domain.hierarchy import BranchRevision

        command = CommandEnvelope(
            command_id=command_id or CommandId.generate(),
            instance_id=instance_id,
            branch_id=branch_id,
            expected_revision=BranchRevision(expected_revision),
            action_type=action_type,
            payload=payload,
            world_time=world_time,
        )
        return self._runtime.submit_command(command)

    def checkpoint(self, instance_id: WorldInstanceId, branch_id: BranchId) -> SnapshotMetadata:
        return self._runtime.create_checkpoint(instance_id, branch_id)

    def restore(self, instance_id: WorldInstanceId, branch_id: BranchId) -> dict[str, object]:
        from wanxiang_runtime.state import state_to_primitive

        result = self._runtime.restore_and_replay(instance_id, branch_id)
        return {
            "state": state_to_primitive(result.state),
            "used_snapshot": result.used_snapshot,
        }

    def branch(self, instance_id: WorldInstanceId, parent_branch_id: BranchId) -> BranchMetadata:
        return self._runtime.create_branch(instance_id, parent_branch_id)

    def metrics(self, instance_id: WorldInstanceId) -> dict[str, int]:
        return self._runtime.metrics(instance_id)

    def close(self) -> None:
        """Release resources. In-memory/SQLite adapters manage their own pools."""
        return None
