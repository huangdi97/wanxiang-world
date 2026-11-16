"""Map domain errors to structured HTTP errors."""

from __future__ import annotations

from typing import Any, cast

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from wanxiang_domain.errors import (
    Conflict,
    ContractError,
    DuplicateCommandConflict,
    IncompatibleVersion,
    NotFound,
    StaleRevision,
    ValidationRejected,
    WanxiangError,
)
from wanxiang_substrate.session.errors import (
    LeaseConflict,
    LeaseExpired,
    LeaseNotFound,
    SessionNotFound,
)
from wanxiang_substrate.sources.errors import SourceError

_FALLBACK_PRODUCT_STATE = "REJECTED"


def product_state_for(error: object) -> str:
    """Client-visible product state for a refusal; never empty.

    Failures declare their own state (the source taxonomy in
    `wanxiang_substrate.sources.errors` sets `product_state` per class); anything
    else is reported as a plain refusal so a client never receives a refusal whose
    `details` payload carries no diagnosis at all.
    """

    declared = getattr(error, "product_state", "")
    return declared if isinstance(declared, str) and declared else _FALLBACK_PRODUCT_STATE


def _string_keyed_details(value: object) -> dict[str, Any]:
    """Copy a JSON details mapping into a strictly typed, str-keyed dict."""

    if not isinstance(value, dict):
        return {}
    return {str(key): item for key, item in cast(dict[object, Any], value).items()}


def error_payload(error: WanxiangError) -> dict[str, Any]:
    """Structured body for one failure, always naming a product state."""

    payload = error.to_primitive()
    details = _string_keyed_details(payload.get("details"))
    details.setdefault("product_state", product_state_for(error))
    payload["details"] = details
    return payload


def _status(error: WanxiangError) -> int:
    if isinstance(error, (ContractError, ValidationRejected, IncompatibleVersion, SourceError)):
        return 422
    if isinstance(error, (LeaseConflict, LeaseExpired)):
        return 409
    if isinstance(error, (LeaseNotFound, SessionNotFound)):
        return 404
    if isinstance(error, (StaleRevision, DuplicateCommandConflict, Conflict)):
        return 409
    if isinstance(error, NotFound):
        return 404
    return 500


async def _wanxiang_error_handler(request: Request, exc: WanxiangError) -> JSONResponse:
    return JSONResponse(status_code=_status(exc), content=error_payload(exc))


def install_error_handler(app: FastAPI) -> None:
    app.exception_handler(WanxiangError)(_wanxiang_error_handler)
