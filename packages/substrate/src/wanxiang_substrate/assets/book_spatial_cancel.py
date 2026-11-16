"""Best-effort cancellation for derived T3 generation jobs.

A cancellation request is not terminal provider truth. The ticket remains in its
current nonterminal state until normal polling reports cancelled/failed/succeeded.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

import hashlib
from dataclasses import replace

from wanxiang_substrate.assets.book_spatial_types import (
    _SpatialGenerationProvider,
    _SpatialGenerationTicket,
    _SpatialJobStore,
)


def _request_spatial_cancellation(
    provider: _SpatialGenerationProvider,
    jobs: _SpatialJobStore,
    submission_id: str,
) -> _SpatialGenerationTicket:
    ticket = jobs.get(submission_id)
    if ticket is None:
        raise KeyError(submission_id)
    if (
        ticket.provider_id != provider.provider_id
        or ticket.provider_version != provider.provider_version
    ):
        raise ValueError("configured spatial provider does not match persisted ticket")
    if ticket.state not in {"submitted", "queued", "running"}:
        raise ValueError("only active spatial tasks may request cancellation")
    if not provider.supports_cancel:
        raise ValueError("spatial provider does not support cancellation")
    if not ticket.provider_task_ref:
        raise ValueError("spatial cancellation requires a provider task reference")
    if ticket.cancellation_requested:
        return ticket

    request_id = hashlib.sha256(f"{submission_id}:cancel-v1".encode()).hexdigest()[:32]
    provider.cancel(ticket.provider_task_ref, request_id=request_id)
    updated = replace(
        ticket,
        cancellation_requested=True,
        reason="cancellation_requested",
    )
    jobs.put(updated)
    return updated
