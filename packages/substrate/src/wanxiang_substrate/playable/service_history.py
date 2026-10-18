"""Player-safe chronicle history over committed events.

History is a read model: it lists committed event cards in reverse world-time
order and never exposes event ids, revisions, hashes, or storage identities.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.playable.player_i18n import _copy_for
from wanxiang_substrate.playable.player_projection_support import _chronicle_card
from wanxiang_substrate.playable.service_session import _owned_instance
from wanxiang_substrate.playable.service_support import _runtime_instance_id

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService

_MAX_HISTORY = 500


def _history(
    service: PlayableService,
    instance_id: str,
    *,
    viewer_id: str,
    limit: int = 200,
    before: int | None = None,
    locale: str | None = None,
) -> dict[str, object]:
    """Return newest-first chronicle cards for one owned instance."""

    if limit < 1 or limit > _MAX_HISTORY:
        raise ValueError(f"history limit must be within [1, {_MAX_HISTORY}]")
    if before is not None and before < 0:
        raise ValueError("history before must be non-negative")
    record = _owned_instance(service, instance_id, viewer_id)
    service.plaza.require_access(record.profile_id, viewer_id)
    world_instance = WorldInstanceId(_runtime_instance_id(record))
    all_events = tuple(service.runtime.worldline_events(world_instance, BranchId(record.branch_id)))
    if before is not None:
        events = tuple(event for event in all_events if event.world_time.ticks < before)
    else:
        events = all_events
    if not events:
        return {
            "total": len(all_events),
            "returned": 0,
            "events": [],
            "has_more": False,
            "next_before": None,
        }
    copy = _copy_for(locale)
    selected = events[-limit:]
    cards = [_chronicle_card(event, record.actor_id, copy) for event in reversed(selected)]
    has_more = len(events) > len(selected)
    return {
        "total": len(all_events),
        "returned": len(cards),
        "events": cards,
        "has_more": has_more,
        "next_before": selected[0].world_time.ticks if has_more else None,
    }
