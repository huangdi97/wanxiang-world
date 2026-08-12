"""Structured agency/order error taxonomy."""

from __future__ import annotations

from wanxiang_domain.errors import WanxiangError


class AgencyError(WanxiangError):
    """Base error for agency substrate failures."""

    code = "agency_error"


class OrderStateConflict(AgencyError):
    code = "order_state_conflict"


class PolicyContextDenied(AgencyError):
    code = "policy_context_denied"
