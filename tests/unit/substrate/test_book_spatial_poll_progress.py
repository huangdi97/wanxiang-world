"""T3 provider poll receipts must never regress durable job/accounting state."""

# pyright: reportPrivateUsage=false

import pytest
from wanxiang_substrate.assets.book_spatial_poll_validation import (
    _require_monotonic_spatial_poll,
)
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialGenerationTicket,
    _SpatialPollResult,
)


def _ticket(*, state: str, usage: int | None) -> _SpatialGenerationTicket:
    return _SpatialGenerationTicket(
        submission_id="submission",
        scene_key="scene",
        provider_id="provider",
        provider_version="1",
        provider_task_ref="task",
        state=state,  # type: ignore[arg-type]
        reserved_cost_units=10,
        delivery_rights="source-gated",
        provider_usage_units=usage,
    )


def test_t3_usage_receipt_cannot_decrease_across_polls() -> None:
    ticket = _ticket(state="running", usage=6)

    with pytest.raises(ValueError, match="usage units regressed"):
        _require_monotonic_spatial_poll(
            ticket,
            _SpatialPollResult("running", provider_usage_units=5),
        )


def test_t3_running_task_cannot_regress_to_queued() -> None:
    ticket = _ticket(state="running", usage=6)

    with pytest.raises(ValueError, match="task state regressed"):
        _require_monotonic_spatial_poll(
            ticket,
            _SpatialPollResult("queued", provider_usage_units=6),
        )


def test_t3_poll_progress_allows_forward_or_equal_receipts() -> None:
    ticket = _ticket(state="running", usage=6)

    _require_monotonic_spatial_poll(
        ticket,
        _SpatialPollResult("running", provider_usage_units=6),
    )
    _require_monotonic_spatial_poll(
        ticket,
        _SpatialPollResult("succeeded", provider_usage_units=7),
    )
    _require_monotonic_spatial_poll(
        ticket,
        _SpatialPollResult("running", provider_usage_units=None),
    )
