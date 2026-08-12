"""Structured resolution/adjudication error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class ResolutionError(WanxiangError):
    """Base error for resolution/adjudication failures."""

    code = "resolution_error"


class ResolverVersionError(ResolutionError):
    code = "resolver_version_error"
