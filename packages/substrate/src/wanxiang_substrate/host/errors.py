"""World host error taxonomy (G05A)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class HostError(WanxiangError):
    """Base error for world host failures."""

    code = "host_error"


class HostNotFound(HostError):
    code = "host_not_found"


class HostNotRunning(HostError):
    code = "host_not_running"


class InvalidHostTransition(HostError):
    code = "invalid_host_transition"
