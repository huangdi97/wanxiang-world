"""Typed refusals for the authoring *request* (before any source work starts).

Measured defect (2026-11-13): an empty source list, an unknown source profile and a
profile/kind mismatch raised a bare `ValueError` from the one-click entry point, so the
API answered `500 Internal Server Error` with no structured body and no diagnosis.

A malformed request is a client mistake, so it must be a typed refusal that names a
product state — the same contract every other refusal follows.
"""

from __future__ import annotations

from wanxiang_domain.errors import ContractError


class AuthoringRequestRejected(ContractError):
    """The authoring request itself is invalid (profile, sources, kind combination)."""

    code = "authoring_request_rejected"
    product_state = "REQUEST_REJECTED"
