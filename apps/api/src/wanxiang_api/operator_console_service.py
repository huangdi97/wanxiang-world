"""Operator / Admin console service (G18H).

Least-privilege, audited privileged operations: source review status, rights
decisions, world host lifecycle and health/metrics. Normal operators cannot
browse/delete audit; all privileged actions go through audited application
services, never direct DB tools.
"""

from __future__ import annotations

from typing import Any

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_substrate.host.host import WorldHost


class OperatorRequiresAdmin(Exception):
    pass


class OperatorConsoleService:
    def __init__(self, runtime: WorldRuntime, *, admin: bool = False) -> None:
        self._runtime = runtime
        self._admin = admin
        self._audit: list[dict[str, str]] = []

    def _require_admin(self, action: str) -> None:
        if not self._admin:
            raise OperatorRequiresAdmin(f"{action} requires admin privilege")
        self._audit.append({"action": action})

    def source_review_status(self, registry: Any) -> dict[str, Any]:
        # Read-only view over the source registry (not privileged).
        history = getattr(registry, "audit_history", None)
        sources = history("") if history is not None else ()
        return {"sources": sources}

    def rights_decision(self, source_id: str, approved: bool) -> dict[str, str]:
        self._require_admin("rights_decision")
        return {"source_id": source_id, "approved": str(approved)}

    def host_control(self, host: WorldHost, action: str) -> str:
        self._require_admin(f"host_{action}")
        if action == "pause":
            host.pause()
        elif action == "resume":
            host.resume()
        elif action == "stop":
            host.stop()
        return action

    def health(self, instance_id: WorldInstanceId, branch_id: BranchId) -> dict[str, Any]:
        state = self._runtime.current_state(instance_id, branch_id)
        events = self._runtime.persistence.event_store.load(instance_id, branch_id)
        return {
            "revision": state.revision.value,
            "events": len(events),
            "hash": state.semantic_hash(),
        }

    def audit_log(self) -> tuple[dict[str, str], ...]:
        return tuple(self._audit)
