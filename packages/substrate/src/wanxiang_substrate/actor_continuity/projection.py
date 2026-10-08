"""Permission-filtered actor continuity timeline for frontend clients."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.goal_stack import ActorGoalStack
from wanxiang_substrate.actor_continuity.relationship_graph import RelationshipGraph
from wanxiang_substrate.epistemic.model import BeliefAssertion, MemoryRecord

ProjectionCategory = Literal["goal", "memory", "belief", "relationship", "action"]


@dataclass(frozen=True, slots=True)
class ActionExplanation:
    """Why refs attached to an action projection; no private content required."""

    action_ref: str
    actor_id: EntityId
    at_ticks: int
    reason: str
    goal_refs: tuple[str, ...] = ()
    memory_refs: tuple[str, ...] = ()
    belief_refs: tuple[str, ...] = ()
    relationship_refs: tuple[str, ...] = ()
    public: bool = False

    def __post_init__(self) -> None:
        if not self.action_ref.strip() or not self.reason.strip() or self.at_ticks < 0:
            raise ContractError("action explanation requires ref, reason, and valid time")

    @property
    def why_refs(self) -> tuple[str, ...]:
        return tuple(
            sorted(
                set(self.goal_refs)
                | set(self.memory_refs)
                | set(self.belief_refs)
                | set(self.relationship_refs)
            )
        )


@dataclass(frozen=True, slots=True)
class ContinuityTimelineItem:
    category: ProjectionCategory
    subject_id: str
    at_ticks: int
    summary: str
    source_refs: tuple[str, ...] = ()
    why_refs: tuple[str, ...] = ()
    private: bool = False
    redacted: bool = False

    def to_dict(self) -> dict[str, object]:
        return {
            "category": self.category,
            "subject_id": self.subject_id,
            "at_ticks": self.at_ticks,
            "summary": self.summary,
            "source_refs": list(self.source_refs),
            "why_refs": list(self.why_refs),
            "private": self.private,
            "redacted": self.redacted,
        }


@dataclass(frozen=True, slots=True)
class ActorContinuitySnapshot:
    """Stable frontend read model with explicit redaction categories."""

    viewer_actor_id: EntityId
    target_actor_id: EntityId
    at_ticks: int
    items: tuple[ContinuityTimelineItem, ...]
    redacted_categories: tuple[ProjectionCategory, ...] = ()

    def timeline(self) -> tuple[ContinuityTimelineItem, ...]:
        return self.items

    def to_dict(self) -> dict[str, object]:
        return {
            "viewer_actor_id": self.viewer_actor_id.value,
            "target_actor_id": self.target_actor_id.value,
            "at_ticks": self.at_ticks,
            "redacted_categories": list(self.redacted_categories),
            "timeline": [item.to_dict() for item in self.items],
        }


class ActorContinuityProjection:
    """Build a read-only Goal/Memory/Belief/Relationship timeline."""

    def compose(
        self,
        *,
        viewer_actor_id: EntityId,
        target_actor_id: EntityId,
        at_ticks: int,
        goals: ActorGoalStack | None = None,
        memories: tuple[MemoryRecord, ...] = (),
        beliefs: tuple[BeliefAssertion, ...] = (),
        relationships: RelationshipGraph | None = None,
        actions: tuple[ActionExplanation, ...] = (),
        admin: bool = False,
    ) -> ActorContinuitySnapshot:
        if at_ticks < 0:
            raise ContractError("continuity projection time cannot be negative")
        self._validate_actor_inputs(target_actor_id, goals, memories, beliefs, actions)
        actor_cognition = admin or viewer_actor_id == target_actor_id
        items: list[ContinuityTimelineItem] = []
        redacted: list[ProjectionCategory] = []
        if actor_cognition:
            items.extend(_goal_items(goals, at_ticks))
            items.extend(_memory_items(memories, at_ticks))
            items.extend(_belief_items(beliefs, at_ticks))
        else:
            redacted.extend(("goal", "memory", "belief"))
        if relationships is not None:
            items.extend(_relationship_items(relationships, viewer_actor_id, at_ticks, admin))
        items.extend(
            _action_items(actions, viewer_actor_id, target_actor_id, actor_cognition, at_ticks)
        )
        return ActorContinuitySnapshot(
            viewer_actor_id=viewer_actor_id,
            target_actor_id=target_actor_id,
            at_ticks=at_ticks,
            items=tuple(
                sorted(items, key=lambda item: (item.at_ticks, item.category, item.subject_id))
            ),
            redacted_categories=tuple(redacted),
        )

    @staticmethod
    def _validate_actor_inputs(
        target: EntityId,
        goals: ActorGoalStack | None,
        memories: tuple[MemoryRecord, ...],
        beliefs: tuple[BeliefAssertion, ...],
        actions: tuple[ActionExplanation, ...],
    ) -> None:
        if goals is not None and goals.actor_id != target:
            raise ContractError("goal projection targets a different actor")
        if any(item.actor_id != target for item in memories + beliefs + actions):
            raise ContractError("continuity projection contains a different actor")


def _goal_items(goals: ActorGoalStack | None, at_ticks: int) -> list[ContinuityTimelineItem]:
    if goals is None:
        return []
    return [
        ContinuityTimelineItem(
            "goal",
            item.goal_id.value,
            min(at_ticks, item.updated_at_ticks),
            item.statement,
            source_refs=item.provenance.refs,
            private=True,
        )
        for item in goals.ordered()
    ]


def _memory_items(
    memories: tuple[MemoryRecord, ...], at_ticks: int
) -> list[ContinuityTimelineItem]:
    return [
        ContinuityTimelineItem(
            "memory",
            item.memory_id.value,
            item.at_ticks,
            item.content_ref,
            source_refs=item.perception_refs,
            private=True,
        )
        for item in memories
        if not item.forgotten and item.at_ticks <= at_ticks
    ]


def _belief_items(
    beliefs: tuple[BeliefAssertion, ...], at_ticks: int
) -> list[ContinuityTimelineItem]:
    return [
        ContinuityTimelineItem(
            "belief",
            item.belief_id.value,
            item.at_ticks,
            f"{item.proposition} ({item.stance}, confidence={item.confidence:.3f})",
            source_refs=tuple(ref for ref in (item.source_ref,) if ref),
            private=True,
        )
        for item in beliefs
        if item.at_ticks <= at_ticks
    ]


def _relationship_items(
    graph: RelationshipGraph, viewer: EntityId, at_ticks: int, admin: bool
) -> list[ContinuityTimelineItem]:
    return [
        ContinuityTimelineItem(
            "relationship",
            item.relationship_id,
            item.valid_from,
            item.relation_type,
            source_refs=item.event_refs,
            private=item.visibility != "public",
        )
        for item in graph.visible_to(viewer, at_ticks=at_ticks, admin=admin)
    ]


def _action_items(
    actions: tuple[ActionExplanation, ...],
    viewer: EntityId,
    target: EntityId,
    actor_cognition: bool,
    at_ticks: int,
) -> list[ContinuityTimelineItem]:
    items: list[ContinuityTimelineItem] = []
    for action in actions:
        if action.at_ticks > at_ticks or action.actor_id != target:
            continue
        visible = actor_cognition or (action.public and viewer != target)
        if not visible:
            continue
        items.append(
            ContinuityTimelineItem(
                "action",
                action.action_ref,
                action.at_ticks,
                action.reason,
                why_refs=action.why_refs if actor_cognition else (),
                private=not action.public,
            )
        )
    return items
