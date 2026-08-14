"""Explicit, structured error taxonomy.

Callers distinguish rejection classes without parsing message strings.
"""

from __future__ import annotations

from typing import Any


class WanxiangError(Exception):
    """Base error for all Wanxiang domain/runtime failures."""

    code = "wanxiang_error"

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_primitive(self) -> dict[str, Any]:
        return {"code": self.code, "message": self.message, "details": self.details}


class ContractError(WanxiangError):
    code = "contract_error"


class ValidationRejected(WanxiangError):
    code = "validation_rejected"


class ConstitutionViolation(ValidationRejected):
    """A delta violates the world/root constitution (G30C)."""


class PermissionDenied(WanxiangError):
    code = "permission_denied"


class RightsDenied(WanxiangError):
    code = "rights_denied"


class NotFound(WanxiangError):
    code = "not_found"


class Conflict(WanxiangError):
    code = "conflict"


class StaleRevision(Conflict):
    code = "stale_revision"


class DuplicateCommandConflict(Conflict):
    code = "duplicate_command_conflict"


class IncompatibleVersion(WanxiangError):
    code = "incompatible_version"


class ReplayError(WanxiangError):
    code = "replay_error"


class CorruptEventStream(ReplayError):
    code = "corrupt_event_stream"


class PersistenceError(WanxiangError):
    code = "persistence_error"


class ExternalDependencyError(WanxiangError):
    code = "external_dependency_error"


class ExternalDataBlocked(WanxiangError):
    code = "external_data_blocked"
