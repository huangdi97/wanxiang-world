"""Lifecycle service: virtual clock drivers, catch-up and audit (G06A)."""

from __future__ import annotations

from wanxiang_application.world_runtime import WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.ids import BranchId, CommandId, WorldInstanceId
from wanxiang_domain.time import WorldTime

from wanxiang_substrate.lifecycle.model import LifecycleMode, LifecycleState
from wanxiang_substrate.lifecycle.resolver import (
    ACTION_SET_MODE,
    LIFECYCLE_COMPONENT,
    LIFECYCLE_ENTITY,
)
from wanxiang_substrate.temporal.query import TemporalQuery


class LifecycleService:
    """Drives and observes a persistent world lifecycle (deterministic)."""

    def __init__(
        self,
        runtime: WorldRuntime,
        instance_id: WorldInstanceId,
        branch_id: BranchId,
    ) -> None:
        self._runtime = runtime
        self._instance_id = instance_id
        self._branch_id = branch_id

    def set_mode(self, mode: LifecycleMode, *, tick: int | None = None) -> LifecycleState:
        state = self._runtime.current_state(self._instance_id, self._branch_id)
        current_tick = tick if tick is not None else TemporalQuery(state).now()
        self._runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"cmd_lifecycle_{state.revision.value}"),
                instance_id=self._instance_id,
                branch_id=self._branch_id,
                expected_revision=state.revision,
                action_type=ACTION_SET_MODE,
                payload={"mode": mode, "tick": current_tick},
                world_time=WorldTime(state.revision.value + 1),
            )
        )
        return self.current()

    def current(self) -> LifecycleState:
        state = self._runtime.current_state(self._instance_id, self._branch_id)
        entity = state.entity(LIFECYCLE_ENTITY)
        mode: LifecycleMode = "REALTIME"
        tick = TemporalQuery(state).now()
        updated = state.revision.value
        if entity is not None:
            for component in entity.components.values():
                if component.component_type == LIFECYCLE_COMPONENT:
                    value = str(component.fields.get("mode") or "REALTIME")
                    from wanxiang_substrate.lifecycle.model import LIFECYCLE_MODES

                    if value in LIFECYCLE_MODES:
                        mode = value  # type: ignore[assignment]
                    tick = int(component.fields.get("tick") or tick)
                    updated = int(component.fields.get("updated_revision") or updated)
        return LifecycleState(
            instance_id=self._instance_id,
            branch_id=self._branch_id,
            mode=mode,
            tick=tick,
            updated_revision=updated,
        )

    def advance(self, ticks: int) -> int:
        """Deterministic virtual-clock driver: advance world time by ticks."""
        if ticks < 0:
            raise ValueError("advance must be non-negative")
        state = self._runtime.current_state(self._instance_id, self._branch_id)
        self._runtime.submit_command(
            CommandEnvelope(
                command_id=CommandId(f"cmd_advance_{state.revision.value}"),
                instance_id=self._instance_id,
                branch_id=self._branch_id,
                expected_revision=state.revision,
                action_type="temporal.advance",
                payload={"ticks": ticks},
                world_time=WorldTime(state.revision.value + 1),
            )
        )
        return self._runtime.current_state(self._instance_id, self._branch_id).revision.value

    def catch_up(self, target_ticks: int) -> int:
        """Explicit catch-up policy after downtime (bounded by target)."""
        state = self._runtime.current_state(self._instance_id, self._branch_id)
        now = TemporalQuery(state).now()
        if target_ticks <= now:
            return now
        delta = target_ticks - now
        self.advance(delta)
        return TemporalQuery(self._runtime.current_state(self._instance_id, self._branch_id)).now()
