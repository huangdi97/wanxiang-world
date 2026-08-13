"""Lifecycle error taxonomy (G06A)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class LifecycleError(WanxiangError):
    """Base error for lifecycle failures."""

    code = "lifecycle_error"


class InvalidLifecycleTransition(LifecycleError):
    code = "invalid_lifecycle_transition"
