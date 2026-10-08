"""Validated decoding for actor-goal revision records."""

from __future__ import annotations

from collections.abc import Mapping
from typing import cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.goal_model import ActorGoal, GoalRevisionEvent


def event_from_dict(value: Mapping[str, object]) -> GoalRevisionEvent:
    event_ref = value.get("event_ref")
    actor_id = value.get("actor_id")
    goal_id = value.get("goal_id")
    sequence = value.get("sequence")
    kind = value.get("kind")
    at_ticks = value.get("at_ticks")
    reason = value.get("reason")
    after = value.get("after")
    before = value.get("before")
    evidence = value.get("evidence_refs", [])
    if not all(isinstance(item, str) for item in (event_ref, actor_id, goal_id, kind, reason)):
        raise ContractError("invalid serialized goal revision")
    if not isinstance(sequence, int) or isinstance(sequence, bool):
        raise ContractError("serialized goal revision sequence must be an integer")
    if not isinstance(at_ticks, int) or isinstance(at_ticks, bool):
        raise ContractError("serialized goal revision time must be an integer")
    if not isinstance(after, Mapping) or (before is not None and not isinstance(before, Mapping)):
        raise ContractError("serialized goal revision values are invalid")
    if not isinstance(evidence, list):
        raise ContractError("serialized goal evidence refs are invalid")
    evidence_values: list[str] = []
    for item in cast(list[object], evidence):
        if not isinstance(item, str):
            raise ContractError("serialized goal evidence refs are invalid")
        evidence_values.append(item)
    return GoalRevisionEvent(
        event_ref=cast(str, event_ref),
        actor_id=EntityId(cast(str, actor_id)),
        goal_id=EntityId(cast(str, goal_id)),
        sequence=sequence,
        kind=cast(str, kind),  # type: ignore[arg-type]
        at_ticks=at_ticks,
        reason=cast(str, reason),
        before=ActorGoal.from_dict(cast(Mapping[str, object], before))
        if before is not None
        else None,
        after=ActorGoal.from_dict(cast(Mapping[str, object], after)),
        evidence_refs=tuple(evidence_values),
    )
