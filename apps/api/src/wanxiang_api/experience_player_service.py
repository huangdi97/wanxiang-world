"""Experience Player service contract (G18C).

End-user player flow: select world/scenario, start a session, project a
perspective, submit actions (revision-aware), and resync after disconnect.
All actions route through the server command pipeline (Commit Authority);
no client-side simulation.
"""

from __future__ import annotations

from typing import Any

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.projection.model import ProjectionRequest
from wanxiang_substrate.projection.service import ProjectionService


class PlayerResyncRequired(Exception):
    pass


class ExperiencePlayerService:
    def __init__(self, runtime: WorldRuntime) -> None:
        self._runtime = runtime

    def start_session(self, instance_id: WorldInstanceId) -> BranchId:
        branches = self._runtime.persistence.branches.list(instance_id)
        if not branches:
            raise ValueError("no branches for the selected world")
        return branches[0].branch_id

    def project(self, instance_id: WorldInstanceId, branch_id: BranchId, actor_id: str) -> Any:
        state = self._runtime.current_state(instance_id, branch_id)
        return ProjectionService(state).compose(
            ProjectionRequest(
                session_id="player", actor_id=actor_id, branch_id=branch_id, mode="text"
            )
        )

    def act(
        self,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
        expected_revision: int,
        action_type: str,
        payload: dict[str, Any],
        actor_id: str,
        command_id: str | None = None,
    ) -> dict[str, Any]:
        # Revision-aware submission: a stale command must resync from the server.
        state = self._runtime.current_state(instance_id, branch_id)
        if state.revision.value != expected_revision:
            raise PlayerResyncRequired(
                f"expected revision {expected_revision}, current {state.revision.value}"
            )
        result = self._runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(command_id or f"player_{expected_revision}"),
                instance_id=instance_id,
                branch_id=branch_id,
                expected_revision=self._runtime.current_state(instance_id, branch_id).revision,
                action_type=action_type,
                payload=payload,
                world_time=WorldTime(state.revision.value + 1),
                actor_id=__import__("wanxiang_domain.ids", fromlist=["ActorId"]).ActorId(actor_id),
            )
        )
        return {
            "revision": result.state.revision.value,
            "state_hash": result.state.semantic_hash(),
            "duplicate": result.duplicate,
        }
