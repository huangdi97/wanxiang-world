"""Fail-closed runtime validation for third-party T3 submission receipts."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import cast

from wanxiang_substrate.assets.book_spatial_types import _SpatialSubmissionResult


def _validated_spatial_submission_receipt(value: object) -> tuple[str, str]:
    if isinstance(value, str):
        raw_task_ref: object = value
        raw_request_ref: object = ""
    elif isinstance(value, _SpatialSubmissionResult):
        raw_task_ref = cast(object, value.task_ref)
        raw_request_ref = cast(object, value.request_ref)
    else:
        raise ValueError("spatial provider returned an invalid submission receipt")

    if not isinstance(raw_task_ref, str) or not isinstance(raw_request_ref, str):
        raise ValueError("spatial provider returned an invalid submission receipt")
    task_ref, request_ref = raw_task_ref.strip(), raw_request_ref.strip()
    if not task_ref:
        raise ValueError("spatial provider returned an empty task reference")
    if (
        len(task_ref) > 2048
        or "\r" in task_ref
        or "\n" in task_ref
        or len(request_ref) > 2048
        or "\r" in request_ref
        or "\n" in request_ref
    ):
        raise ValueError("spatial provider returned an unsafe audit reference")
    return task_ref, request_ref
