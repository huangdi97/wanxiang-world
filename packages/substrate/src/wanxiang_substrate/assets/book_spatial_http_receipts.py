"""Validation for T3 HTTP provider submission and usage receipts."""

from __future__ import annotations

import hashlib

from wanxiang_substrate.assets.book_spatial_types import _SpatialSubmissionResult


def _submission_receipt(body: dict[str, object]) -> str | _SpatialSubmissionResult:
    task_ref = body.get("task_ref")
    if (
        not isinstance(task_ref, str)
        or not task_ref.strip()
        or len(task_ref) > 1024
        or "\r" in task_ref
        or "\n" in task_ref
    ):
        raise ValueError("spatial HTTP gateway returned invalid task_ref")
    task_ref = task_ref.strip()

    request_ref = body.get("request_ref", "")
    if (
        not isinstance(request_ref, str)
        or len(request_ref) > 2048
        or "\r" in request_ref
        or "\n" in request_ref
    ):
        raise ValueError("spatial HTTP gateway returned invalid request_ref")
    request_ref = request_ref.strip()
    return _SpatialSubmissionResult(task_ref, request_ref) if request_ref else task_ref


def _provider_usage_units(body: dict[str, object]) -> int | None:
    raw = body.get("usage_units")
    if raw is None:
        return None
    if isinstance(raw, bool) or not isinstance(raw, int) or raw < 0:
        raise ValueError("spatial HTTP gateway returned invalid usage_units")
    return raw


def _verified_artifact_sha256(item: dict[str, object], content: bytes) -> str:
    actual = hashlib.sha256(content).hexdigest()
    declared = item.get("content_sha256")
    if declared is None:
        return actual
    if (
        not isinstance(declared, str)
        or len(declared) != 64
        or any(char not in "0123456789abcdefABCDEF" for char in declared)
    ):
        raise ValueError("spatial HTTP gateway returned invalid content_sha256")
    if declared.casefold() != actual:
        raise ValueError("spatial HTTP artifact digest does not match downloaded bytes")
    return actual
