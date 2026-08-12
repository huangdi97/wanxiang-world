"""Structured observation/visibility error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class ObservationError(WanxiangError):
    """Base error for observation substrate failures."""

    code = "observation_error"


class InvalidVisibility(ObservationError):
    code = "invalid_visibility"
