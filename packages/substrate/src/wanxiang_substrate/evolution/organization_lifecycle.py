"""Public G93E organization lifecycle proposal facade."""

from wanxiang_substrate.evolution.organization_lifecycle_core import (
    AUTHORITY_PERMISSIONS,
    DEFAULT_AUTHORITY_POLICY,
    OrganizationAuthorityPolicy,
    empty_organization,
    organization_state_from_canonical,
)
from wanxiang_substrate.evolution.organization_membership import (
    create_organization_proposal,
    propose_join,
    propose_leave,
    propose_role_change,
)
from wanxiang_substrate.evolution.organization_model import (
    ORGANIZATION_ACTIONS,
    OrganizationAction,
    OrganizationLifecycleEvent,
    OrganizationLifecycleState,
    OrganizationResource,
    OrganizationStatus,
)
from wanxiang_substrate.evolution.organization_permissions import (
    apply_organization_proposal,
    propose_dissolve,
    propose_permission_grant,
    propose_permission_revoke,
    review_organization_proposal,
    split_child_projection,
)
from wanxiang_substrate.evolution.organization_proposal import OrganizationLifecycleProposal
from wanxiang_substrate.evolution.organization_split import propose_split

OrganizationState = OrganizationLifecycleState
OrganizationLifecycleProjection = OrganizationLifecycleState

__all__ = [
    "AUTHORITY_PERMISSIONS",
    "DEFAULT_AUTHORITY_POLICY",
    "ORGANIZATION_ACTIONS",
    "OrganizationAction",
    "OrganizationAuthorityPolicy",
    "OrganizationLifecycleEvent",
    "OrganizationLifecycleProjection",
    "OrganizationLifecycleProposal",
    "OrganizationLifecycleState",
    "OrganizationResource",
    "OrganizationState",
    "OrganizationStatus",
    "apply_organization_proposal",
    "create_organization_proposal",
    "empty_organization",
    "organization_state_from_canonical",
    "propose_dissolve",
    "propose_join",
    "propose_leave",
    "propose_permission_grant",
    "propose_permission_revoke",
    "propose_role_change",
    "propose_split",
    "review_organization_proposal",
    "split_child_projection",
]
