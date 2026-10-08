"""Player projection adapter over the shared playable service ports."""

# pyright: reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wanxiang_domain.errors import NotFound
from wanxiang_domain.event import CommittedEvent
from wanxiang_domain.ids import BranchId, WorldInstanceId

from wanxiang_substrate.playable.player_projection import (
    player_observation,
    player_world_detail,
)
from wanxiang_substrate.playable.state_diff import CommittedStateDiff
from wanxiang_substrate.playable.store import ExperienceInstanceRecord

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService


def player_world(
    service: PlayableService,
    profile_id: str,
    *,
    viewer_id: str,
    locale: str | None = None,
) -> dict[str, object]:
    """Return the non-technical world detail projection for Player UI."""

    profile = service.plaza.require_access(profile_id, viewer_id)
    return player_world_detail(profile, service.packages.get(profile_id), locale=locale)


def player_observe(
    service: PlayableService,
    instance_id: str,
    viewer_id: str,
    *,
    diff: CommittedStateDiff | None = None,
    locale: str | None = None,
    events_since_revision: int | None = None,
) -> dict[str, object]:
    """Return a player-safe view derived from the shared runtime read path."""

    record = service.store.get_instance(instance_id)
    if record.owner_id != viewer_id:
        raise NotFound(f"playable instance {instance_id!r} not found")
    profile = service.plaza.require_access(record.profile_id, viewer_id)
    world_instance_id = WorldInstanceId(record.instance_id)
    branch_id = BranchId(record.branch_id)
    state = service.runtime.current_state(world_instance_id, branch_id)
    actor_name = ""
    actor_starting_location = ""
    if record.actor_id:
        try:
            character = service.store.get_character(record.actor_id)
            actor_name = character.display_name
            actor_starting_location = character.starting_location
        except NotFound:
            actor_name = ""
    events = tuple(service.runtime.events(world_instance_id, branch_id))
    effective_events_since_revision = events_since_revision
    if effective_events_since_revision is None and not record.session_id:
        effective_events_since_revision = record.last_revision
    view = player_observation(
        profile,
        service.packages.get(record.profile_id),
        state,
        events,
        actor_id=record.actor_id,
        actor_name=actor_name,
        diff=diff,
        locale=locale,
        events_since_revision=effective_events_since_revision,
    )
    view["session"] = _session_summary(record, view, events, actor_starting_location)
    return view


def _session_summary(
    record: ExperienceInstanceRecord,
    view: dict[str, object],
    events: tuple[CommittedEvent, ...],
    actor_starting_location: str,
) -> dict[str, object]:
    """Return the resume summary without exposing runtime identifiers."""

    left = not record.session_id
    player = cast(dict[str, object], view["player"])
    location = view.get("location") or player.get("location")
    if not location:
        location = actor_starting_location or None

    leave_time: dict[str, int] | None = None
    if left and record.last_revision > 0:
        leave_event = next(
            (
                event
                for event in reversed(tuple(events))
                if event.event_seq.value <= record.last_revision
            ),
            None,
        )
        if leave_event is not None:
            leave_time = {"ticks": leave_event.world_time.ticks}
    return {
        "world_name": cast(dict[str, object], view["world"])["name"],
        "character_name": player["name"],
        "time": view["time"],
        "last_location": location,
        "leave_time": leave_time,
        "events_since_leave": view["events_since_leave"],
        "last_change": view["last_committed_change"],
        "status": "saved" if left else "active",
    }
