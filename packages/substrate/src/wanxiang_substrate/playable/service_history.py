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
    locale: str | None = None,
) -> dict[str, object]:
    """Return newest-first chronicle cards for one owned instance."""

    if limit < 1 or limit > _MAX_HISTORY:
        raise ValueError(f"history limit must be within [1, {_MAX_HISTORY}]")
    record = _owned_instance(service, instance_id, viewer_id)
    service.plaza.require_access(record.profile_id, viewer_id)
    events = tuple(
        service.runtime.worldline_events(
            WorldInstanceId(_runtime_instance_id(record)),
            BranchId(record.branch_id),
        )
    )
    if not events:
        return {"total": 0, "returned": 0, "events": []}
    copy = _copy_for(locale)
    selected = events[-limit:]
    cards = [_chronicle_card(event, record.actor_id, copy) for event in reversed(selected)]
    return {"total": len(events), "returned": len(cards), "events": cards}
