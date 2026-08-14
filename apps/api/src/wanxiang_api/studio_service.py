"""Studio / World IDE service contract (G18B).

Provides engineering/authoring operations over the public runtime WITHOUT direct
database access: command diagnosis, replay/branch state, diffs and audited
admin actions. Debug/admin operations require explicit privilege and are
audited. Studio never bypasses Commit Authority.
"""

from __future__ import annotations

from typing import Any

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.lineage import LineageGraph
from wanxiang_substrate.projection.model import ProjectionRequest
from wanxiang_substrate.projection.service import ProjectionService


class StudioRequiresAdmin(Exception):
    pass


class StudioService:
    def __init__(self, runtime: WorldRuntime, *, admin: bool = False) -> None:
        self._runtime = runtime
        self._admin = admin
        self._audit: list[dict[str, str]] = []

    def _record(self, action: str, detail: str) -> None:
        self._audit.append({"action": action, "detail": detail})

    def diagnose_command(self, instance_id: WorldInstanceId, command_id: str) -> dict[str, Any]:
        """Diagnose a command outcome from the event/audit stream (no raw DB)."""
        from wanxiang_domain.ids import CommandId

        store = self._runtime.persistence.event_store
        event = store.command_result_event(CommandId(command_id))
        result: dict[str, Any] = {"command_id": command_id, "committed": event is not None}
        if event is not None:
            result["event_seq"] = event.event_seq.value
            result["revision"] = event.revision.value
        self._record("diagnose", command_id)
        return result

    def branch_replay(self, instance_id: WorldInstanceId, branch_id: BranchId) -> dict[str, Any]:
        restored = self._runtime.restore_and_replay(instance_id, branch_id)
        self._record("branch_replay", branch_id.value)
        return {
            "used_snapshot": restored.used_snapshot,
            "revision": restored.state.revision.value,
            "hash": restored.state.semantic_hash(),
        }

    def branch_diff(
        self, instance_id: WorldInstanceId, branch_a: BranchId, branch_b: BranchId
    ) -> dict[str, Any]:
        diff = self._runtime.diff(instance_id, branch_a, branch_b)
        self._record("branch_diff", f"{branch_a.value}..{branch_b.value}")
        return {
            "added": [e.value for e in diff.added_entities],
            "removed": [e.value for e in diff.removed_entities],
            "updated": [e.value for e in diff.updated_entities],
        }

    def debug_projection(
        self, instance_id: WorldInstanceId, branch_id: BranchId, actor_id: str
    ) -> Any:
        """Dangerous admin action: debug projection requires explicit privilege."""
        if not self._admin:
            raise StudioRequiresAdmin("debug projection requires explicit admin privilege")
        state = self._runtime.current_state(instance_id, branch_id)
        snap = ProjectionService(state, admin=True).compose(
            ProjectionRequest(
                session_id="studio", actor_id=actor_id, branch_id=branch_id, mode="debug"
            )
        )
        self._record("debug_projection", branch_id.value)
        return snap

    def lineage_projection(self, graph: LineageGraph, node_id: str) -> dict[str, Any]:
        """Read-only lineage debug view (Studio never holds authority)."""
        ancestors = graph.ancestors(node_id)
        descendants = graph.descendants(node_id)
        promotion_origin = None
        for edge in graph.edges():
            if edge.child_node_id == node_id and edge.edge_kind == "promotion":
                promotion_origin = edge.origin_ref
                break
        self._record("lineage_projection", node_id)
        return {
            "node_id": node_id,
            "ancestors": list(ancestors),
            "descendants": list(descendants),
            "promotion_origin": promotion_origin,
        }

    def audit_log(self) -> tuple[dict[str, str], ...]:
        return tuple(self._audit)
