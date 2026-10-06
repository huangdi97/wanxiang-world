"""Read-only observer Experience over the authoritative WorldRuntime.

R7 Gate H needs more than one Experience to consume the same canonical world.
This adapter deliberately exposes only observation: it owns no state, caches no
second truth and has no command/commit path. Player/actor Experiences may mutate
through Commit Authority; this observer sees those committed consequences through
the shared runtime read path.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_application.world_runtime import WorldRuntime


@dataclass(frozen=True, slots=True)
class ObserverExperienceView:
    """A small research/observer projection derived from canonical history."""

    instance_id: str
    branch_id: str
    revision: int
    state_hash: str
    event_count: int
    latest_event_id: str | None


class ObserverExperienceService:
    """Read-only Experience sharing the injected runtime with other Experiences."""

    def __init__(self, runtime: WorldRuntime) -> None:
        self._runtime = runtime

    def observe(self, instance_id: WorldInstanceId, branch_id: BranchId) -> ObserverExperienceView:
        """Observe one worldline without owning or mutating canonical state."""
        state = self._runtime.current_state(instance_id, branch_id)
        events = self._runtime.events(instance_id, branch_id)
        latest_event_id = events[-1].event_id.value if events else None
        return ObserverExperienceView(
            instance_id=instance_id.value,
            branch_id=branch_id.value,
            revision=state.revision.value,
            state_hash=state.semantic_hash(),
            event_count=len(events),
            latest_event_id=latest_event_id,
        )


__all__ = ["ObserverExperienceService", "ObserverExperienceView"]
