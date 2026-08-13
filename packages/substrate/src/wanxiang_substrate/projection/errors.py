"""Projection error taxonomy (G05D)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class ProjectionError(WanxiangError):
    """Base error for projection failures."""

    code = "projection_error"


class UnauthorizedProjection(ProjectionError):
    code = "unauthorized_projection"
