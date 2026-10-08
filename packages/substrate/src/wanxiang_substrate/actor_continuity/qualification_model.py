"""Checkpoint and result contracts for accelerated continuity qualification."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.goal_stack import ActorGoalStack
from wanxiang_substrate.actor_continuity.projection import ActionExplanation
from wanxiang_substrate.actor_continuity.relationship_graph import RelationshipGraph
from wanxiang_substrate.actor_continuity.relationship_model import RelationshipState
from wanxiang_substrate.epistemic.model import BeliefAssertion, MemoryRecord


@dataclass(frozen=True, slots=True)
class ContinuityActorBundle:
    actor_id: EntityId
    goals: ActorGoalStack
    memories: tuple[MemoryRecord, ...] = ()
    beliefs: tuple[BeliefAssertion, ...] = ()
    actions: tuple[ActionExplanation, ...] = ()

    def __post_init__(self) -> None:
        if self.goals.actor_id != self.actor_id:
            raise ContractError("continuity goals target a different actor")
        if any(
            item.actor_id != self.actor_id for item in self.memories + self.beliefs + self.actions
        ):
            raise ContractError("continuity bundle contains a different actor")


@dataclass(frozen=True, slots=True)
class ContinuityCheckpoint:
    source_package_ref: str
    world_instance_refs: tuple[str, ...]
    day: int
    at_ticks: int
    actors: tuple[ContinuityActorBundle, ...]
    relationships: RelationshipGraph

    def __post_init__(self) -> None:
        if not self.source_package_ref.strip() or not self.world_instance_refs:
            raise ContractError("continuity checkpoint requires source and world refs")
        if self.day < 0 or self.at_ticks < 0:
            raise ContractError("continuity checkpoint time is invalid")
        if len({item.actor_id for item in self.actors}) != len(self.actors):
            raise ContractError("continuity checkpoint actor ids must be unique")

    def to_dict(self) -> dict[str, object]:
        return {
            "source_package_ref": self.source_package_ref,
            "world_instance_refs": list(self.world_instance_refs),
            "day": self.day,
            "at_ticks": self.at_ticks,
            "actors": [_actor_dict(item) for item in self.actors],
            "relationships": {
                "states": [_relationship_dict(item) for item in self.relationships.states],
                "revisions": [
                    {
                        "event_ref": event.event_ref,
                        "sequence": event.sequence,
                        "at_ticks": event.at_ticks,
                        "reason": event.reason,
                        "before_id": event.before.relationship_id if event.before else None,
                        "after_id": event.after.relationship_id,
                    }
                    for event in self.relationships.revisions
                ],
            },
        }

    def digest(self) -> str:
        encoded = json.dumps(
            self.to_dict(), ensure_ascii=False, sort_keys=True, separators=(",", ":")
        )
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

    def resume(self) -> ContinuityCheckpoint:
        """Rebuild an immutable checkpoint object as a leave/re-enter boundary."""
        return ContinuityCheckpoint(
            source_package_ref=self.source_package_ref,
            world_instance_refs=tuple(self.world_instance_refs),
            day=self.day,
            at_ticks=self.at_ticks,
            actors=tuple(self.actors),
            relationships=RelationshipGraph(
                states=tuple(self.relationships.states),
                revisions=tuple(self.relationships.revisions),
            ),
        )


@dataclass(frozen=True, slots=True)
class ContinuityQualificationResult:
    source_package_ref: str
    world_instance_refs: tuple[str, ...]
    actor_ids: tuple[str, ...]
    days_completed: int
    final_digest: str
    replay_digest: str
    leave_reenter_digest: str
    goal_revision_count: int
    memory_count: int
    belief_revision_count: int
    relationship_revision_count: int

    @property
    def replay_equal(self) -> bool:
        return self.final_digest == self.replay_digest

    @property
    def leave_reenter_equal(self) -> bool:
        return self.final_digest == self.leave_reenter_digest

    def to_dict(self) -> dict[str, object]:
        return {
            "source_package_ref": self.source_package_ref,
            "world_instance_refs": list(self.world_instance_refs),
            "actor_ids": list(self.actor_ids),
            "days_completed": self.days_completed,
            "final_digest": self.final_digest,
            "replay_digest": self.replay_digest,
            "leave_reenter_digest": self.leave_reenter_digest,
            "replay_equal": self.replay_equal,
            "leave_reenter_equal": self.leave_reenter_equal,
            "goal_revision_count": self.goal_revision_count,
            "memory_count": self.memory_count,
            "belief_revision_count": self.belief_revision_count,
            "relationship_revision_count": self.relationship_revision_count,
        }


def _actor_dict(bundle: ContinuityActorBundle) -> dict[str, object]:
    return {
        "actor_id": bundle.actor_id.value,
        "goals": bundle.goals.to_dict(),
        "memories": [_memory_dict(item) for item in bundle.memories],
        "beliefs": [_belief_dict(item) for item in bundle.beliefs],
        "actions": [_action_dict(item) for item in bundle.actions],
    }


def _memory_dict(memory: MemoryRecord) -> dict[str, object]:
    return {
        "memory_id": memory.memory_id.value,
        "actor_id": memory.actor_id.value,
        "kind": memory.kind,
        "content_ref": memory.content_ref,
        "at_ticks": memory.at_ticks,
        "salience": memory.salience,
        "perception_refs": list(memory.perception_refs),
        "decay_rate": memory.decay_rate,
        "reinforcement_count": memory.reinforcement_count,
        "forgotten": memory.forgotten,
    }


def _belief_dict(belief: BeliefAssertion) -> dict[str, object]:
    return {
        "belief_id": belief.belief_id.value,
        "actor_id": belief.actor_id.value,
        "proposition": belief.proposition,
        "confidence": belief.confidence,
        "at_ticks": belief.at_ticks,
        "source_ref": belief.source_ref,
        "status": belief.status,
        "stance": belief.stance,
        "supersedes": belief.supersedes.value if belief.supersedes else None,
    }


def _action_dict(action: ActionExplanation) -> dict[str, object]:
    return {
        "action_ref": action.action_ref,
        "actor_id": action.actor_id.value,
        "at_ticks": action.at_ticks,
        "reason": action.reason,
        "why_refs": list(action.why_refs),
        "public": action.public,
    }


def _relationship_dict(state: RelationshipState) -> dict[str, object]:
    return {
        "relationship_id": state.relationship_id,
        "source_actor_id": state.source_actor_id.value,
        "target_actor_id": state.target_actor_id.value,
        "relation_type": state.relation_type,
        "dimensions": state.dimensions.to_dict(),
        "valid_from": state.valid_from,
        "valid_to": state.valid_to,
        "event_refs": list(state.event_refs),
        "visibility": state.visibility,
    }
