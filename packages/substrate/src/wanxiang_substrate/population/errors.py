"""Structured population/scheduler error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class PopulationError(WanxiangError):
    """Base error for population/scheduler substrate failures."""

    code = "population_error"


class SchedulerBudgetExceeded(PopulationError):
    code = "scheduler_budget_exceeded"
