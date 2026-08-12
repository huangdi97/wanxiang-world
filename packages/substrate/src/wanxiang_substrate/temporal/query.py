"""Deterministic temporal queries over canonical state (read-only)."""

from __future__ import annotations

from collections.abc import Mapping

from wanxiang_domain.ids import EntityId
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.temporal.components import (
    APPOINTMENT_COMPONENT,
    CLOCK_COMPONENT,
    DEADLINE_COMPONENT,
    RECURRING_COMPONENT,
)
from wanxiang_substrate.temporal.model import (
    Appointment,
    Calendar,
    Deadline,
    RecurringEvent,
    TimeWindowConstraint,
    WorldClock,
)


class TemporalQuery:
    """Read-only temporal graph over the canonical state."""

    def __init__(self, state: InMemoryCanonicalState) -> None:
        self._clock = WorldClock(ticks=0, paused=False)
        self._appointments: dict[EntityId, Appointment] = {}
        self._deadlines: dict[EntityId, Deadline] = {}
        self._recurring: dict[EntityId, RecurringEvent] = {}
        self._scan(state)

    def _scan(self, state: InMemoryCanonicalState) -> None:
        for entity in state.entities():
            for component in entity.components.values():
                if component.component_type == CLOCK_COMPONENT:
                    ticks = _int(component.fields, "ticks")
                    paused = component.fields.get("paused", False)
                    self._clock = WorldClock(
                        ticks=ticks, paused=isinstance(paused, bool) and paused
                    )
                elif component.component_type == APPOINTMENT_COMPONENT:
                    appointment = _appointment_from(component.fields)
                    if appointment is not None:
                        self._appointments[appointment.appointment_id] = appointment
                elif component.component_type == DEADLINE_COMPONENT:
                    deadline = _deadline_from(component.fields)
                    if deadline is not None:
                        self._deadlines[deadline.deadline_id] = deadline
                elif component.component_type == RECURRING_COMPONENT:
                    recurring = _recurring_from(component.fields)
                    if recurring is not None:
                        self._recurring[recurring.recurring_id] = recurring

    def clock(self) -> WorldClock:
        return self._clock

    def now(self) -> int:
        return self._clock.ticks

    def calendar(self, day_length_ticks: int = 100) -> Calendar:
        return Calendar(day_length_ticks=day_length_ticks)

    def appointments(self) -> dict[EntityId, Appointment]:
        return dict(self._appointments)

    def appointment(self, appointment_id: EntityId) -> Appointment | None:
        return self._appointments.get(appointment_id)

    def due_appointments(self, at_ticks: int | None = None) -> tuple[Appointment, ...]:
        now = at_ticks if at_ticks is not None else self.now()
        return tuple(
            sorted(
                (
                    appt
                    for appt in self._appointments.values()
                    if appt.start_ticks <= now < appt.end_ticks
                ),
                key=lambda a: (a.start_ticks, a.appointment_id.value),
            )
        )

    def appointments_between(self, start: int, end: int) -> tuple[Appointment, ...]:
        return tuple(
            sorted(
                (
                    appt
                    for appt in self._appointments.values()
                    if appt.start_ticks < end and appt.end_ticks > start
                ),
                key=lambda a: (a.start_ticks, a.appointment_id.value),
            )
        )

    def conflicts(self, actor_id: EntityId, start: int, end: int) -> tuple[Appointment, ...]:
        return tuple(
            appt
            for appt in self.appointments_between(start, end)
            if appt.actor_id == actor_id and appt.state != "done"
        )

    def deadlines(self) -> dict[EntityId, Deadline]:
        return dict(self._deadlines)

    def due_deadlines(self, at_ticks: int | None = None) -> tuple[Deadline, ...]:
        now = at_ticks if at_ticks is not None else self.now()
        return tuple(
            sorted(
                (
                    dl
                    for dl in self._deadlines.values()
                    if dl.due_ticks <= now and dl.state == "pending"
                ),
                key=lambda d: (d.due_ticks, d.deadline_id.value),
            )
        )

    def recurring(self) -> dict[EntityId, RecurringEvent]:
        return dict(self._recurring)

    def next_occurrences(
        self, recurring_id: EntityId, horizon_ticks: int, *, cap: int = 100
    ) -> tuple[int, ...]:
        event = self._recurring.get(recurring_id)
        if event is None or event.state != "active":
            return ()
        return event.occurrences(horizon_ticks, cap=cap)


def _int(fields: Mapping[str, object], key: str, default: int = 0) -> int:
    value = fields.get(key, default)
    return value if isinstance(value, int) and not isinstance(value, bool) else default


def _str(fields: Mapping[str, object], key: str) -> str | None:
    value = fields.get(key)
    return value if isinstance(value, str) else None


def _appointment_from(fields: Mapping[str, object]) -> Appointment | None:
    appointment_id = _str(fields, "appointment_id")
    actor_id = _str(fields, "actor_id")
    activity = _str(fields, "activity")
    if appointment_id is None or actor_id is None or activity is None:
        return None
    window = None
    ws = fields.get("window_start")
    we = fields.get("window_end")
    if isinstance(ws, int) and isinstance(we, int):
        window = TimeWindowConstraint(ws, we)
    return Appointment(
        appointment_id=EntityId(appointment_id),
        actor_id=EntityId(actor_id),
        activity=activity,
        start_ticks=_int(fields, "start_ticks"),
        end_ticks=_int(fields, "end_ticks"),
        state=_str(fields, "state") or "pending",  # type: ignore[arg-type]
        window=window,
    )


def _deadline_from(fields: Mapping[str, object]) -> Deadline | None:
    deadline_id = _str(fields, "deadline_id")
    target_id = _str(fields, "target_id")
    if deadline_id is None or target_id is None:
        return None
    return Deadline(
        deadline_id=EntityId(deadline_id),
        target_id=EntityId(target_id),
        due_ticks=_int(fields, "due_ticks"),
        state=_str(fields, "state") or "pending",  # type: ignore[arg-type]
    )


def _recurring_from(fields: Mapping[str, object]) -> RecurringEvent | None:
    recurring_id = _str(fields, "recurring_id")
    activity = _str(fields, "activity")
    if recurring_id is None or activity is None:
        return None
    return RecurringEvent(
        recurring_id=EntityId(recurring_id),
        activity=activity,
        anchor_ticks=_int(fields, "anchor_ticks"),
        interval_ticks=_int(fields, "interval_ticks", 1),
        state=_str(fields, "state") or "active",  # type: ignore[arg-type]
    )
