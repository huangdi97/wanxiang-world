"""Fail-closed runtime validation for third-party T3 poll receipts."""

from __future__ import annotations

from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialPollResult,
    _SpatialProjectionFrame,
)

_VALID_POLL_STATES = frozenset(
    {"queued", "running", "succeeded", "failed", "cancelled", "expired"}
)


def _validated_spatial_poll_result(value: object) -> _SpatialPollResult:
    if not isinstance(value, _SpatialPollResult):
        raise ValueError("spatial provider returned an invalid poll receipt")
    if value.state not in _VALID_POLL_STATES:
        raise ValueError("spatial provider returned an invalid poll state")
    if not isinstance(value.reason, str):
        raise ValueError("spatial provider returned an invalid poll reason")
    usage = value.provider_usage_units
    if usage is not None and (
        isinstance(usage, bool) or not isinstance(usage, int) or usage < 0
    ):
        raise ValueError("spatial provider returned invalid usage units")
    if not isinstance(value.artifacts, tuple) or any(
        not isinstance(item, _SpatialArtifactCandidate) for item in value.artifacts
    ):
        raise ValueError("spatial provider returned an invalid artifact receipt")
    if value.projection_frame is not None and not isinstance(
        value.projection_frame, _SpatialProjectionFrame
    ):
        raise ValueError("spatial provider returned an invalid projection frame")
    return value
