"""Fail-closed runtime validation for third-party T3 poll receipts."""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import cast

from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialArtifactCandidate,
    _SpatialGenerationTicket,
    _SpatialPollResult,
    _SpatialProjectionFrame,
    _SpatialProviderState,
)

_VALID_POLL_STATES = frozenset({"queued", "running", "succeeded", "failed", "cancelled", "expired"})


def _validated_spatial_poll_result(value: object) -> _SpatialPollResult:
    if not isinstance(value, _SpatialPollResult):
        raise ValueError("spatial provider returned an invalid poll receipt")

    raw_state = cast(object, value.state)
    raw_reason = cast(object, value.reason)
    raw_usage = cast(object, value.provider_usage_units)
    raw_artifacts = cast(object, value.artifacts)
    raw_frame = cast(object, value.projection_frame)

    if not isinstance(raw_state, str) or raw_state not in _VALID_POLL_STATES:
        raise ValueError("spatial provider returned an invalid poll state")
    if not isinstance(raw_reason, str):
        raise ValueError("spatial provider returned an invalid poll reason")
    if raw_usage is not None and (
        isinstance(raw_usage, bool) or not isinstance(raw_usage, int) or raw_usage < 0
    ):
        raise ValueError("spatial provider returned invalid usage units")
    if not isinstance(raw_artifacts, tuple):
        raise ValueError("spatial provider returned an invalid artifact receipt")
    artifact_rows = cast(tuple[object, ...], raw_artifacts)
    if any(not isinstance(item, _SpatialArtifactCandidate) for item in artifact_rows):
        raise ValueError("spatial provider returned an invalid artifact receipt")
    artifacts = cast(tuple[_SpatialArtifactCandidate, ...], artifact_rows)
    if raw_frame is not None and not isinstance(raw_frame, _SpatialProjectionFrame):
        raise ValueError("spatial provider returned an invalid projection frame")

    return _SpatialPollResult(
        state=cast(_SpatialProviderState, raw_state),
        artifacts=artifacts,
        reason=raw_reason,
        projection_frame=raw_frame,
        provider_usage_units=raw_usage,
    )


def _require_monotonic_spatial_poll(
    ticket: _SpatialGenerationTicket, result: _SpatialPollResult
) -> None:
    """Reject provider receipts that would make durable task/accounting state move backward."""
    previous_usage = ticket.provider_usage_units
    current_usage = result.provider_usage_units
    if previous_usage is not None and current_usage is not None and current_usage < previous_usage:
        raise ValueError("spatial provider usage units regressed")
    if ticket.state == "running" and result.state == "queued":
        raise ValueError("spatial provider task state regressed")
