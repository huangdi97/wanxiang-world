"""Institution, authority, duty & norm substrate (G02E)."""

from wanxiang_substrate.institution.components import (
    DUTY_COMPONENT,
    MEMBERSHIP_COMPONENT,
    PERMISSION_COMPONENT,
    ROLE_COMPONENT,
    SANCTION_COMPONENT,
)
from wanxiang_substrate.institution.errors import (
    DutyAlreadyComplete,
    InstitutionError,
    PermissionDeniedByInstitution,
)
from wanxiang_substrate.institution.fixture import build_institution_fixture_commands
from wanxiang_substrate.institution.model import (
    Duty,
    Membership,
    PermissionDecision,
    Role,
)
from wanxiang_substrate.institution.query import InstitutionQuery
from wanxiang_substrate.institution.resolver import register_institution_resolvers

__all__ = [
    "DUTY_COMPONENT",
    "Duty",
    "DutyAlreadyComplete",
    "InstitutionError",
    "InstitutionQuery",
    "MEMBERSHIP_COMPONENT",
    "Membership",
    "PERMISSION_COMPONENT",
    "PermissionDecision",
    "PermissionDeniedByInstitution",
    "ROLE_COMPONENT",
    "Role",
    "SANCTION_COMPONENT",
    "build_institution_fixture_commands",
    "register_institution_resolvers",
]
