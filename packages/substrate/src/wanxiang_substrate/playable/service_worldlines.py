"""Player worldline list: branches of one runtime instance with product handles.

Only records owned by the viewer are listed. The canonical branch metadata is
read-only; the view exposes no event ids, hashes, or storage refs.
"""

# pyright: reportPrivateUsage=false, reportUnusedFunction=false

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wanxiang_domain.entity import EntityState, RelationState
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, WorldInstanceId
from wanxiang_runtime.diff import StateDiff
from wanxiang_runtime.state import InMemoryCanonicalState

from wanxiang_substrate.playable.player_i18n import _copy_for, _PlayerCopy
from wanxiang_substrate.playable.player_projection_support import (
    _CATEGORY_KEYS,
    _entity_name,
)
from wanxiang_substrate.playable.player_service import player_observe
from wanxiang_substrate.playable.service_session import _owned_instance
from wanxiang_substrate.playable.service_support import _runtime_instance_id
from wanxiang_substrate.playable.store import ExperienceInstanceRecord

if TYPE_CHECKING:
    from wanxiang_substrate.playable.service import PlayableService

_MAX_DIFF_ITEMS = 20


def _belongs(record: ExperienceInstanceRecord, runtime_id: str) -> bool:
    return (record.runtime_instance_id or record.instance_id) == runtime_id


def _summary(
    service: PlayableService,
    record: ExperienceInstanceRecord,
    viewer_id: str,
    locale: str | None,
) -> dict[str, object]:
    view = player_observe(service, record.instance_id, viewer_id, locale=locale)
    time = view.get("time")
    player = view.get("player")
    people = view.get("present_people")
    time_row = cast(dict[str, object], time) if isinstance(time, dict) else None
    player_row = cast(dict[str, object], player) if isinstance(player, dict) else None
    names: list[str] = []
    if isinstance(people, list):
        for item in cast(list[object], people):
            row = cast(dict[str, object], item) if isinstance(item, dict) else None
            name = row.get("name") if row is not None else None
            if isinstance(name, str) and name:
                names.append(name)
    return {
        "instance_id": record.instance_id,
        "world_time": time_row.get("ticks", 0) if time_row is not None else 0,
        "location": view.get("location"),
        "status": player_row.get("status") if player_row is not None else None,
        "present_people": names,
    }


def _entity_card(
    kind: str,
    entity: EntityState | None,
    copy: _PlayerCopy,
) -> dict[str, object] | None:
    if entity is None:
        return None
    category = copy.text(_CATEGORY_KEYS.get(entity.entity_type.casefold(), "category_state"))
    return {"kind": kind, "name": _entity_name(entity, copy), "category": category}


def _relation_card(
    kind: str,
    relation: RelationState | None,
    state: InMemoryCanonicalState,
    copy: _PlayerCopy,
) -> dict[str, object] | None:
    if relation is None:
        return None
    source = state.entity(relation.source_id)
    target = state.entity(relation.target_id)
    label = f"{_entity_name(source, copy)} — {_entity_name(target, copy)}"
    return {"kind": kind, "name": label, "category": relation.relation_type}


def _differences(
    delta: StateDiff,
    left_state: InMemoryCanonicalState,
    right_state: InMemoryCanonicalState,
    locale: str | None,
) -> dict[str, object]:
    """Player-safe structural diff: names and categories, never ids or hashes."""

    copy = _copy_for(locale)
    items: list[dict[str, object]] = []

    def collect(card: dict[str, object] | None) -> None:
        if card is not None:
            items.append(card)

    for entity_id in delta.added_entities:
        collect(_entity_card("added_entity", right_state.entity(entity_id), copy))
    for entity_id in delta.removed_entities:
        collect(_entity_card("removed_entity", left_state.entity(entity_id), copy))
    for entity_id in delta.updated_entities:
        collect(_entity_card("updated_entity", right_state.entity(entity_id), copy))
    for relation_id in delta.added_relations:
        collect(
            _relation_card("added_relation", right_state.relation(relation_id), right_state, copy)
        )
    for relation_id in delta.removed_relations:
        collect(
            _relation_card("removed_relation", left_state.relation(relation_id), left_state, copy)
        )
    return {
        "total": len(items),
        "truncated": len(items) > _MAX_DIFF_ITEMS,
        "items": items[:_MAX_DIFF_ITEMS],
    }


def _compare_worldlines(
    service: PlayableService,
    instance_id: str,
    *,
    other_instance_id: str,
    viewer_id: str,
    locale: str | None = None,
) -> dict[str, object]:
    """Compare two owned worldlines of the same runtime instance without ids."""

    left = _owned_instance(service, instance_id, viewer_id)
    right = _owned_instance(service, other_instance_id, viewer_id)
    service.plaza.require_access(left.profile_id, viewer_id)
    service.plaza.require_access(right.profile_id, viewer_id)
    runtime_id = _runtime_instance_id(left)
    if _runtime_instance_id(right) != runtime_id:
        raise ValueError("worldlines belong to different runtime instances")
    world_instance = WorldInstanceId(runtime_id)
    _common_branch, common_revision = service.runtime.worldline_compare_point(
        world_instance,
        BranchId(left.branch_id),
        BranchId(right.branch_id),
    )
    left_state = service.runtime.current_state(world_instance, BranchId(left.branch_id))
    right_state = service.runtime.current_state(world_instance, BranchId(right.branch_id))
    delta = cast(
        StateDiff,
        service.runtime.diff(
            world_instance,
            BranchId(left.branch_id),
            BranchId(right.branch_id),
        ),
    )

    def diverged_events(record: ExperienceInstanceRecord) -> int:
        events = service.runtime.events(world_instance, BranchId(record.branch_id))
        return sum(1 for event in events if event.revision.value > common_revision)

    return {
        "common": {"revision": common_revision},
        "identical": left_state.semantic_hash() == right_state.semantic_hash(),
        "diverged_events": {
            "left": diverged_events(left),
            "right": diverged_events(right),
        },
        "left": _summary(service, left, viewer_id, locale),
        "right": _summary(service, right, viewer_id, locale),
        "differences": _differences(delta, left_state, right_state, locale),
    }


def _branch_metadata(
    service: PlayableService,
    runtime_id: str,
) -> tuple[int, dict[str, int]]:
    count = 0
    revisions: dict[str, int] = {}
    for branch in service.runtime.worldline_branches(WorldInstanceId(runtime_id)):
        branch_id = getattr(branch, "branch_id", None)
        if not isinstance(branch_id, BranchId):
            continue
        count += 1
        ancestry = getattr(branch, "ancestry", None)
        fork_revision = getattr(ancestry, "fork_revision", None)
        if isinstance(fork_revision, BranchRevision):
            revisions[branch_id.value] = fork_revision.value
    return count, revisions


def _worldlines(
    service: PlayableService,
    instance_id: str,
    *,
    viewer_id: str,
) -> dict[str, object]:
    """List the viewer's worldline handles for the instance's runtime branch set."""

    record = _owned_instance(service, instance_id, viewer_id)
    service.plaza.require_access(record.profile_id, viewer_id)
    runtime_id = _runtime_instance_id(record)
    branch_count, fork_revisions = _branch_metadata(service, runtime_id)
    records = [item for item in service.store.list_instances() if _belongs(item, runtime_id)]
    records.sort(
        key=lambda item: (
            fork_revisions.get(item.branch_id) is not None,
            fork_revisions.get(item.branch_id) or 0,
            item.instance_id,
        )
    )
    world_instance = WorldInstanceId(runtime_id)
    cards: list[dict[str, object]] = []
    for item in records:
        branch = BranchId(item.branch_id)
        events = tuple(service.runtime.worldline_events(world_instance, branch))
        state = service.runtime.current_state(world_instance, branch)
        cards.append(
            {
                "instance_id": item.instance_id,
                "branch_id": item.branch_id,
                "current": item.instance_id == instance_id,
                "active_session": bool(item.session_id),
                "mode": item.mode,
                "revision": state.revision.value,
                "world_time": events[-1].world_time.ticks if events else 0,
                "forked_from_revision": fork_revisions.get(item.branch_id),
            }
        )
    return {
        "instance_id": instance_id,
        "branches": branch_count,
        "worldlines": cards,
    }
