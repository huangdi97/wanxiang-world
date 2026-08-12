"""Temporal component schema (versioned) on the M1 component model."""

from __future__ import annotations

from wanxiang_domain.entity import ComponentData
from wanxiang_domain.ids import ComponentId, EntityId
from wanxiang_domain.versions import SchemaVersion

TEMPORAL_SCHEMA_VERSION = SchemaVersion(1)

CLOCK_COMPONENT = "temporal.clock"
APPOINTMENT_COMPONENT = "temporal.appointment"
DEADLINE_COMPONENT = "temporal.deadline"
RECURRING_COMPONENT = "temporal.recurring"

CLOCK_ENTITY = EntityId("world_clock")


def clock_component(ticks: int, paused: bool = False) -> ComponentData:
    return ComponentData(
        component_id=ComponentId("clock"),
        component_type=CLOCK_COMPONENT,
        schema_version=TEMPORAL_SCHEMA_VERSION,
        fields={"ticks": ticks, "paused": paused},
    )


def appointment_component(
    appointment_id: EntityId,
    actor_id: EntityId,
    activity: str,
    start_ticks: int,
    end_ticks: int,
    state: str = "pending",
    window_start: int | None = None,
    window_end: int | None = None,
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"appt_{appointment_id.value}"),
        component_type=APPOINTMENT_COMPONENT,
        schema_version=TEMPORAL_SCHEMA_VERSION,
        fields={
            "appointment_id": appointment_id.value,
            "actor_id": actor_id.value,
            "activity": activity,
            "start_ticks": start_ticks,
            "end_ticks": end_ticks,
            "state": state,
            "window_start": window_start,
            "window_end": window_end,
        },
    )


def deadline_component(
    deadline_id: EntityId, target_id: EntityId, due_ticks: int, state: str = "pending"
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"dl_{deadline_id.value}"),
        component_type=DEADLINE_COMPONENT,
        schema_version=TEMPORAL_SCHEMA_VERSION,
        fields={
            "deadline_id": deadline_id.value,
            "target_id": target_id.value,
            "due_ticks": due_ticks,
            "state": state,
        },
    )


def recurring_component(
    recurring_id: EntityId,
    activity: str,
    anchor_ticks: int,
    interval_ticks: int,
    state: str = "active",
) -> ComponentData:
    return ComponentData(
        component_id=ComponentId(f"rec_{recurring_id.value}"),
        component_type=RECURRING_COMPONENT,
        schema_version=TEMPORAL_SCHEMA_VERSION,
        fields={
            "recurring_id": recurring_id.value,
            "activity": activity,
            "anchor_ticks": anchor_ticks,
            "interval_ticks": interval_ticks,
            "state": state,
        },
    )
