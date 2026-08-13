"""Session / embodiment / control error taxonomy (G05B, G05C)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class SessionError(WanxiangError):
    """Base error for session failures."""

    code = "session_error"


class LeaseConflict(SessionError):
    code = "embodiment_lease_conflict"


class LeaseNotFound(SessionError):
    code = "embodiment_lease_not_found"


class LeaseExpired(SessionError):
    code = "embodiment_lease_expired"


class SessionNotFound(SessionError):
    code = "session_not_found"


class InvalidHandoff(SessionError):
    code = "invalid_control_handoff"


class ShadowCannotCommit(SessionError):
    code = "shadow_cannot_commit"
