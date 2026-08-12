"""Structured body/condition error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class BodyError(WanxiangError):
    """Base error for body/condition substrate failures."""

    code = "body_error"


class InvalidConditionRange(BodyError):
    code = "invalid_condition_range"


class BodyConstraintViolation(BodyError):
    code = "body_constraint_violation"
