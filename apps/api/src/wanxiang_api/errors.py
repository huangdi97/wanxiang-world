"""Map domain errors to structured HTTP errors."""

from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from wanxiang_domain.errors import (
    Conflict,
    DuplicateCommandConflict,
    IncompatibleVersion,
    NotFound,
    StaleRevision,
    ValidationRejected,
    WanxiangError,
)
from wanxiang_substrate.sources.errors import SourceError


def _status(error: WanxiangError) -> int:
    if isinstance(error, (ValidationRejected, IncompatibleVersion, SourceError)):
        return 422
    if isinstance(error, (StaleRevision, DuplicateCommandConflict, Conflict)):
        return 409
    if isinstance(error, NotFound):
        return 404
    return 500


async def _wanxiang_error_handler(request: Request, exc: WanxiangError) -> JSONResponse:
    return JSONResponse(status_code=_status(exc), content=exc.to_primitive())


def install_error_handler(app: FastAPI) -> None:
    app.exception_handler(WanxiangError)(_wanxiang_error_handler)
