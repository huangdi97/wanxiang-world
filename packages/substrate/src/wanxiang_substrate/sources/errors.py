"""Structured source registry / source gate error taxonomy (G04B)."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class SourceError(WanxiangError):
    """Base error for source registry failures."""

    code = "source_error"


class SourceNotApproved(SourceError):
    code = "source_not_approved"


class RightsDenied(SourceError):
    code = "source_rights_denied"


class MaliciousSource(SourceError):
    code = "malicious_source"


class InvalidTransition(SourceError):
    code = "invalid_source_transition"


class DuplicateSource(SourceError):
    code = "duplicate_source"


class SourceNotFound(SourceError):
    code = "source_not_found"
