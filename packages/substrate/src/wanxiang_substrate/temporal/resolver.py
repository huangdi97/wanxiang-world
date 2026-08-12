"""Temporal resolvers: advance clock / schedule through the M1 authority."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, EntityUpdate, ProposedWorldDelta
from wanxiang_domain.entity import ComponentData
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import EntityId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.temporal.components import (
    APPOINTMENT_COMPONENT,
    CLOCK_ENTITY,
    appointment_component,
    clock_component,
    deadline_component,
    recurring_component,
)
from wanxiang_substrate.temporal.errors import (
    BackwardTimeError,
    ScheduleConflict,
    TimeWindowViolation,
)
from wanxiang_substrate.temporal.query import TemporalQuery

ACTION_ADVANCE = "temporal.advance"
ACTION_ADVANCE_TO = "temporal.advance_to"
ACTION_SCHEDULE_APPOINTMENT = "temporal.schedule_appointment"
ACTION_SET_DEADLINE = "temporal.set_deadline"
ACTION_DEFINE_RECURRING = "temporal.define_recurring"
ACTION_MARK_DONE = "temporal.mark_appointment_done"
ACTION_INSTANTIATE = "temporal.instantiate"


def register_temporal_resolvers(registry: ResolverRegistry) -> None:
    """Register temporal actions on a resolver registry (deterministic)."""
    registry.register(ACTION_ADVANCE, _resolve_advance)
    registry.register(ACTION_ADVANCE_TO, _resolve_advance_to)
    registry.register(ACTION_SCHEDULE_APPOINTMENT, _resolve_schedule)
    registry.register(ACTION_SET_DEADLINE, _resolve_deadline)
    registry.register(ACTION_DEFINE_RECURRING, _resolve_recurring)
    registry.register(ACTION_MARK_DONE, _resolve_mark_done)
    registry.register(ACTION_INSTANTIATE, _resolve_instantiate)


def _str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value:
        raise ValidationRejected(f"payload field {key!r} must be a non-empty string")
    return value


def _int(payload: Mapping[str, object], key: str, default: int | None = None) -> int:
    value = payload.get(key, default)
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationRejected(f"payload field {key!r} must be an integer")
    return value


def _clock_update(now: int, paused: bool = False) -> EntityUpdate:
    return EntityUpdate(
        entity_id=CLOCK_ENTITY,
        components=(clock_component(now, paused),),
    )


def _ensure_clock(state: InMemoryCanonicalState) -> None:
    if state.entity(CLOCK_ENTITY) is None:
        raise ValidationRejected("world clock entity does not exist (instantiate calendar first)")


def _resolve_advance(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("time advance requires current state")
    payload = dict(command.payload)
    delta = _int(payload, "ticks")
    if delta < 0:
        raise BackwardTimeError("cannot advance world time by a negative delta")
    query = TemporalQuery(state)
    _ensure_clock(state)
    if query.clock().paused:
        raise ValidationRejected("world clock is paused")
    now = query.now()
    return ProposedWorldDelta(operations=(_clock_update(now + delta),))


def _resolve_advance_to(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("time advance requires current state")
    payload = dict(command.payload)
    target = _int(payload, "ticks")
    query = TemporalQuery(state)
    _ensure_clock(state)
    if target < query.now():
        raise BackwardTimeError(f"cannot move world time backward to {target}")
    return ProposedWorldDelta(operations=(_clock_update(target),))


def _resolve_schedule(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("scheduling requires current state")
    payload = dict(command.payload)
    appointment_id = EntityId(_str(payload, "appointment_id"))
    actor_id = EntityId(_str(payload, "actor_id"))
    activity = _str(payload, "activity")
    start = _int(payload, "start_ticks")
    end = _int(payload, "end_ticks")
    if end <= start:
        raise ValidationRejected("appointment end must be after start")
    query = TemporalQuery(state)
    if query.appointment(appointment_id) is not None:
        raise ValidationRejected(f"appointment {appointment_id.value} already exists")
    if query.conflicts(actor_id, start, end):
        raise ScheduleConflict(f"actor {actor_id.value} already has an appointment in that window")
    ws = payload.get("window_start")
    we = payload.get("window_end")
    if ws is not None or we is not None:
        window_start = ws if isinstance(ws, int) else start
        window_end = we if isinstance(we, int) else end
        if start < window_start or end > window_end:
            raise TimeWindowViolation("appointment does not fit in the time window")
        return ProposedWorldDelta(
            operations=(
                EntityCreate(
                    entity_id=appointment_id,
                    entity_type="temporal.appointment",
                    components=(
                        appointment_component(
                            appointment_id,
                            actor_id,
                            activity,
                            start,
                            end,
                            window_start=window_start,
                            window_end=window_end,
                        ),
                    ),
                ),
            )
        )
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=appointment_id,
                entity_type="temporal.appointment",
                components=(appointment_component(appointment_id, actor_id, activity, start, end),),
            ),
        )
    )


def _resolve_deadline(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    deadline_id = EntityId(_str(payload, "deadline_id"))
    target_id = EntityId(_str(payload, "target_id"))
    due = _int(payload, "due_ticks")
    if due < 0:
        raise ValidationRejected("deadline due ticks must be non-negative")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=deadline_id,
                entity_type="temporal.deadline",
                components=(deadline_component(deadline_id, target_id, due),),
            ),
        )
    )


def _resolve_recurring(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    payload = dict(command.payload)
    recurring_id = EntityId(_str(payload, "recurring_id"))
    activity = _str(payload, "activity")
    anchor = _int(payload, "anchor_ticks")
    interval = _int(payload, "interval_ticks")
    if interval <= 0:
        raise ValidationRejected("recurrence interval must be positive")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=recurring_id,
                entity_type="temporal.recurring",
                components=(recurring_component(recurring_id, activity, anchor, interval),),
            ),
        )
    )


def _resolve_mark_done(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    if state is None:
        raise ValidationRejected("marking done requires current state")
    payload = dict(command.payload)
    appointment_id = EntityId(_str(payload, "appointment_id"))
    query = TemporalQuery(state)
    appointment = query.appointment(appointment_id)
    if appointment is None:
        raise ValidationRejected(f"appointment {appointment_id.value} does not exist")
    entity = state.entity(appointment_id)
    assert entity is not None
    current = next(
        (c for c in entity.components.values() if c.component_type == APPOINTMENT_COMPONENT), None
    )
    if current is None:
        raise ValidationRejected(f"entity {appointment_id.value} is not an appointment")
    fields = dict(current.fields)
    fields["state"] = "done"
    updated = ComponentData(
        component_id=current.component_id,
        component_type=APPOINTMENT_COMPONENT,
        schema_version=current.schema_version,
        fields=fields,
    )
    return ProposedWorldDelta(
        operations=(EntityUpdate(entity_id=appointment_id, components=(updated,)),)
    )


def _resolve_instantiate(
    command: CommandEnvelope, state: InMemoryCanonicalState | None
) -> ProposedWorldDelta:
    """Instantiate a registered deterministic temporal fixture via the authority."""
    from wanxiang_substrate.temporal.fixture import FIXTURE_DELTAS

    payload = dict(command.payload)
    name = _str(payload, "fixture")
    version = payload.get("version", 1)
    if version != 1:
        raise ValidationRejected(f"unsupported fixture version {version!r}")
    builder = FIXTURE_DELTAS.get(name)
    if builder is None:
        raise ValidationRejected(f"unknown fixture {name!r}")
    return builder()
