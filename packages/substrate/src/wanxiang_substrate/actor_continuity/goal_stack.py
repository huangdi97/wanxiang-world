"""Immutable, replayable actor goal stack projection."""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass, replace
from typing import cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.goal_model import (
    GOAL_STACK_SCHEMA_VERSION,
    ActorGoal,
    GoalRevisionEvent,
    GoalRevisionKind,
    GoalTier,
    to_json,
)
from wanxiang_substrate.actor_continuity.goal_serialization import event_from_dict

_TIER_ORDER: dict[GoalTier, int] = {
    "life_motive": 0,
    "long_term": 1,
    "medium_term": 2,
    "short_term": 3,
    "intent": 4,
}


@dataclass(frozen=True, slots=True)
class ActorGoalStack:
    """Actor-local desired outcomes; no method mutates canonical world state."""

    actor_id: EntityId
    goals: tuple[ActorGoal, ...] = ()
    revisions: tuple[GoalRevisionEvent, ...] = ()
    revision: int = 0
    schema_version: int = GOAL_STACK_SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != GOAL_STACK_SCHEMA_VERSION:
            raise ContractError(f"unsupported actor goal schema {self.schema_version}")
        if self.revision != len(self.revisions):
            raise ContractError("goal stack revision must equal revision event count")
        ids = {goal.goal_id for goal in self.goals}
        if len(ids) != len(self.goals):
            raise ContractError("goal ids must be unique")
        if any(goal.actor_id != self.actor_id for goal in self.goals):
            raise ContractError("goal stack contains a different actor")
        for goal in self.goals:
            if any(dependency not in ids for dependency in goal.dependencies):
                raise ContractError("goal dependency must refer to a goal in the stack")
        if any(event.actor_id != self.actor_id for event in self.revisions):
            raise ContractError("goal revision belongs to a different actor")

    @classmethod
    def empty(cls, actor_id: EntityId) -> ActorGoalStack:
        return cls(actor_id=actor_id)

    def goal(self, goal_id: EntityId) -> ActorGoal | None:
        return next((item for item in self.goals if item.goal_id == goal_id), None)

    def active(self) -> tuple[ActorGoal, ...]:
        return tuple(item for item in self.ordered() if item.status == "active")

    def ordered(self) -> tuple[ActorGoal, ...]:
        return tuple(
            sorted(
                self.goals,
                key=lambda item: (_TIER_ORDER[item.tier], -item.priority, item.goal_id.value),
            )
        )

    def ready(self) -> tuple[ActorGoal, ...]:
        """Return active goals whose dependencies are all completed."""
        by_id = {item.goal_id: item for item in self.goals}
        return tuple(
            item
            for item in self.ordered()
            if item.status == "active"
            and all(by_id[dependency].status == "completed" for dependency in item.dependencies)
        )

    def add_goal(
        self,
        goal: ActorGoal,
        *,
        event_ref: str,
        at_ticks: int,
        reason: str,
        evidence_refs: tuple[str, ...] = (),
    ) -> tuple[ActorGoalStack, GoalRevisionEvent]:
        if goal.actor_id != self.actor_id:
            raise ContractError("goal targets a different actor")
        if self.goal(goal.goal_id) is not None:
            raise ContractError(f"goal {goal.goal_id.value!r} already exists")
        event = GoalRevisionEvent(
            event_ref=event_ref,
            actor_id=self.actor_id,
            goal_id=goal.goal_id,
            sequence=self.revision + 1,
            kind="created",
            at_ticks=at_ticks,
            reason=reason,
            after=goal,
            evidence_refs=evidence_refs,
        )
        return self.apply(event), event

    def revise_goal(
        self,
        goal: ActorGoal,
        *,
        event_ref: str,
        at_ticks: int,
        reason: str,
        evidence_refs: tuple[str, ...] = (),
    ) -> tuple[ActorGoalStack, GoalRevisionEvent]:
        before = self.goal(goal.goal_id)
        if before is None:
            raise ContractError(f"goal {goal.goal_id.value!r} does not exist")
        if goal.actor_id != self.actor_id:
            raise ContractError("goal targets a different actor")
        if before == goal:
            raise ContractError("goal revision must change the goal")
        kind: GoalRevisionKind = "revised"
        if (
            before.priority != goal.priority
            and replace(before, priority=goal.priority, updated_at_ticks=goal.updated_at_ticks)
            == goal
        ):
            kind = "reprioritized"
        elif (
            before.status != goal.status
            and replace(before, status=goal.status, updated_at_ticks=goal.updated_at_ticks) == goal
        ):
            kind = "status_changed"
        event = GoalRevisionEvent(
            event_ref=event_ref,
            actor_id=self.actor_id,
            goal_id=goal.goal_id,
            sequence=self.revision + 1,
            kind=kind,
            at_ticks=at_ticks,
            reason=reason,
            before=before,
            after=goal,
            evidence_refs=evidence_refs,
        )
        return self.apply(event), event

    def reprioritize(
        self,
        goal_id: EntityId,
        priority: int,
        *,
        event_ref: str,
        at_ticks: int,
        reason: str,
        evidence_refs: tuple[str, ...] = (),
    ) -> tuple[ActorGoalStack, GoalRevisionEvent]:
        current = self.goal(goal_id)
        if current is None:
            raise ContractError(f"goal {goal_id.value!r} does not exist")
        updated = replace(current, priority=priority, updated_at_ticks=at_ticks)
        return self.revise_goal(
            updated,
            event_ref=event_ref,
            at_ticks=at_ticks,
            reason=reason,
            evidence_refs=evidence_refs,
        )

    def apply(self, event: GoalRevisionEvent) -> ActorGoalStack:
        """Apply an already-authorized projection event for deterministic replay."""
        if event.actor_id != self.actor_id or event.sequence != self.revision + 1:
            raise ContractError("goal revision sequence or actor does not match stack")
        current = self.goal(event.goal_id)
        if event.kind == "created":
            if current is not None:
                raise ContractError("replay cannot create an existing goal")
            goals = self.goals + (event.after,)
        else:
            if current is None or event.before != current:
                raise ContractError("goal revision before value does not match stack")
            goals = tuple(
                event.after if item.goal_id == event.goal_id else item for item in self.goals
            )
        return ActorGoalStack(
            actor_id=self.actor_id,
            goals=goals,
            revisions=self.revisions + (event,),
            revision=event.sequence,
            schema_version=self.schema_version,
        )

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "actor_id": self.actor_id.value,
            "revision": self.revision,
            "goals": [item.to_dict() for item in self.ordered()],
            "revisions": [item.to_dict() for item in self.revisions],
        }

    def serialize(self) -> str:
        return to_json(self.to_dict())

    to_json = serialize

    @classmethod
    def from_dict(cls, value: Mapping[str, object]) -> ActorGoalStack:
        schema = value.get("schema_version")
        actor_id = value.get("actor_id")
        revision = value.get("revision")
        goals = value.get("goals", [])
        revisions = value.get("revisions", [])
        if schema != GOAL_STACK_SCHEMA_VERSION or not isinstance(actor_id, str):
            raise ContractError("unsupported or invalid actor goal stack serialization")
        if not isinstance(revision, int) or isinstance(revision, bool):
            raise ContractError("serialized goal stack revision must be an integer")
        if not isinstance(goals, list):
            raise ContractError("serialized goals must be objects")
        goal_values: list[Mapping[str, object]] = []
        for item in cast(list[object], goals):
            if not isinstance(item, Mapping):
                raise ContractError("serialized goals must be objects")
            goal_values.append(cast(Mapping[str, object], item))
        if not isinstance(revisions, list):
            raise ContractError("serialized goal revisions must be objects")
        revision_values: list[Mapping[str, object]] = []
        for item in cast(list[object], revisions):
            if not isinstance(item, Mapping):
                raise ContractError("serialized goal revisions must be objects")
            revision_values.append(cast(Mapping[str, object], item))
        expected_goals = tuple(ActorGoal.from_dict(item) for item in goal_values)
        stack = cls(actor_id=EntityId(actor_id))
        for raw_event in revision_values:
            stack = stack.apply(event_from_dict(raw_event))
        if stack.revision != revision:
            raise ContractError("serialized goal stack revision does not replay")
        if {item.goal_id: item for item in stack.goals} != {
            item.goal_id: item for item in expected_goals
        }:
            raise ContractError("serialized goal snapshot does not match its revisions")
        return stack

    @classmethod
    def deserialize(cls, value: str) -> ActorGoalStack:
        raw = json.loads(value)
        if not isinstance(raw, Mapping):
            raise ContractError("serialized actor goal stack must be an object")
        return cls.from_dict(cast(Mapping[str, object], raw))

    @classmethod
    def replay(cls, actor_id: EntityId, events: Iterable[GoalRevisionEvent]) -> ActorGoalStack:
        stack = cls.empty(actor_id)
        for event in events:
            stack = stack.apply(event)
        return stack
