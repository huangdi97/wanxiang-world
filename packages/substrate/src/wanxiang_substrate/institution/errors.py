"""Structured institution/authority error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class InstitutionError(WanxiangError):
    """Base error for institution substrate failures."""

    code = "institution_error"


class PermissionDeniedByInstitution(InstitutionError):
    code = "permission_denied_by_institution"


class DutyAlreadyComplete(InstitutionError):
    code = "duty_already_complete"
