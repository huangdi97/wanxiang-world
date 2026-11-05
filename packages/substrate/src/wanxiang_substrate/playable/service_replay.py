"""Read-only historical replay projections for Player instances.

Replay rebuilds a *derived* observation from committed events at one world
time. It never appends events, never changes canonical state, and exposes no
event ids, revisions, or storage identities to the Player.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING

from wanxiang_domain.errors import NotFound
from wanxiang_domain.hierarchy import EventSeq
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.playable.player_projection import player_observation
from wanxiang_substrate.playable.service_session import _owned_instance
from wanxiang_substrate.playable.service_support import _runtime_instance_id

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def _actor_identity(service: PlayableService, actor_id: str) -> tuple[str, str]:
    if not actor_id:
        return ("", "")
    try:
        character = service.store.get_character(actor_id)
    except NotFound:
        return ("", "")
    return (character.display_name, character.starting_location)


def _replay_at(
    service: PlayableService,
    instance_id: str,
    *,
    viewer_id: str,
    at_ticks: int,
    locale: str | None = None,
) -> dict[str, object]:
    """Project the instance as of ``at_ticks`` without touching the head state."""

    if at_ticks < 0:
        raise ValueError("replay at_ticks must be non-negative")
    record = _owned_instance(service, instance_id, viewer_id)
    profile = service.plaza.require_access(record.profile_id, viewer_id)
    world_instance = WorldInstanceId(_runtime_instance_id(record))
    branch = BranchId(record.branch_id)
    events = tuple(service.runtime.worldline_events(world_instance, branch))
    eligible = tuple(event for event in events if event.world_time.ticks <= at_ticks)
    if eligible:
        target = eligible[-1]
        target_branch = target.branch_id
        upto_seq = target.event_seq.value
    else:
        # Before the first committed event the worldline is the empty root state.
        target_branch = events[0].branch_id if events else branch
        upto_seq = 0
    state = service.runtime.state_at(world_instance, target_branch, upto_seq=EventSeq(upto_seq))
    actor_name, actor_starting_location = _actor_identity(service, record.actor_id)
    view = player_observation(
        profile,
        service.packages.get(record.profile_id),
        state,
        eligible,
        actor_id=record.actor_id,
        actor_name=actor_name,
        actor_starting_location=actor_starting_location,
        locale=locale,
        visual_assets=service.visual_assets(record.profile_id, viewer_id=viewer_id),
        # T3 attachments are current derived projection assets, not revision-bound
        # history. Until a spatial manifest is explicitly tied to a historical
        # revision, replay must not make a later generated 3D asset appear to
        # have existed at this moment.
        spatial_assets=None,
        spatial_frames=None,
        visual_access_allowed=service.visual_access_allowed(
            record.profile_id,
            viewer_id=viewer_id,
        ),
    )
    view["replay"] = {
        "at_ticks": at_ticks,
        "world_ticks": eligible[-1].world_time.ticks if eligible else 0,
        "event_count": len(eligible),
    }
    return view
