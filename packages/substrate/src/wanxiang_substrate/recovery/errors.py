"""Recovery / budget error taxonomy (G06C)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class RecoveryError(WanxiangError):
    """Base error for recovery failures."""

    code = "recovery_error"


class BudgetExceeded(RecoveryError):
    code = "resource_budget_exceeded"


class CorruptSnapshot(RecoveryError):
    code = "corrupt_snapshot"


class NoSnapshot(RecoveryError):
    code = "no_snapshot"
