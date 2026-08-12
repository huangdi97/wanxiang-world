"""Structured temporal error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class TemporalError(WanxiangError):
    """Base error for temporal substrate failures."""

    code = "temporal_error"


class BackwardTimeError(TemporalError):
    code = "backward_time"


class ScheduleConflict(TemporalError):
    code = "schedule_conflict"


class DeadlineMissed(TemporalError):
    code = "deadline_missed"


class TimeWindowViolation(TemporalError):
    code = "time_window_violation"
