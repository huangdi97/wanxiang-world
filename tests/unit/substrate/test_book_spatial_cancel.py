"""T3 cancellation is best-effort and never fabricates a terminal state."""

# pyright: reportPrivateUsage=false

from __future__ import annotations

import hashlib

import pytest
from wanxiang_substrate.assets.book_spatial_cancel import _request_spatial_cancellation
from wanxiang_substrate.assets.book_spatial_store import _InMemorySpatialJobStore
from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialGenerationProvider,
    _SpatialGenerationTicket,
)


class _CancelableProvider(_SpatialGenerationProvider):
    provider_id = "spatial:cancel-test"
    provider_version = "1"
    supports_cancel = True

    def __init__(self) -> None:
        self.cancels: list[tuple[str, str]] = []

    def cancel(self, task_ref: str, *, request_id: str) -> None:
        self.cancels.append((task_ref, request_id))


def _ticket(*, state: str = "running") -> _SpatialGenerationTicket:
    return _SpatialGenerationTicket(
        submission_id="submission-1",
        scene_key="scene-1",
        provider_id="spatial:cancel-test",
        provider_version="1",
        provider_task_ref="task-1",
        state=state,  # type: ignore[arg-type]
        reserved_cost_units=7,
        delivery_rights="source-gated",
        scope_key="world-1",
    )


def test_cancel_request_is_persisted_but_state_stays_nonterminal() -> None:
    provider = _CancelableProvider()
    jobs = _InMemorySpatialJobStore()
    jobs.put(_ticket())

    updated = _request_spatial_cancellation(provider, jobs, "submission-1")

    assert updated.state == "running"
    assert updated.cancellation_requested is True
    assert updated.reason == "cancellation_requested"
    request_id = hashlib.sha256(b"submission-1:cancel-v1").hexdigest()[:32]
    assert provider.cancels == [("task-1", request_id)]
    assert jobs.get("submission-1") == updated

    replay = _request_spatial_cancellation(provider, jobs, "submission-1")
    assert replay == updated
    assert len(provider.cancels) == 1


def test_cancel_fails_closed_for_unsupported_or_terminal_provider_state() -> None:
    jobs = _InMemorySpatialJobStore()
    jobs.put(_ticket())
    unsupported = _SpatialGenerationProvider()
    unsupported.provider_id = "spatial:cancel-test"
    unsupported.provider_version = "1"
    with pytest.raises(ValueError, match="does not support cancellation"):
        _request_spatial_cancellation(unsupported, jobs, "submission-1")

    jobs.put(_ticket(state="cancelled"))
    with pytest.raises(ValueError, match="only active spatial tasks"):
        _request_spatial_cancellation(_CancelableProvider(), jobs, "submission-1")
