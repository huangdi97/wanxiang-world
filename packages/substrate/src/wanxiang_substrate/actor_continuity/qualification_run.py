"""Deterministic seven-day actor continuity qualification runner."""

from __future__ import annotations

from dataclasses import dataclass, replace

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.goal_model import ActorGoal, GoalProvenance
from wanxiang_substrate.actor_continuity.goal_stack import ActorGoalStack
from wanxiang_substrate.actor_continuity.projection import ActionExplanation
from wanxiang_substrate.actor_continuity.qualification_model import (
    ContinuityActorBundle,
    ContinuityCheckpoint,
    ContinuityQualificationResult,
)
from wanxiang_substrate.actor_continuity.relationship_graph import RelationshipGraph
from wanxiang_substrate.actor_continuity.relationship_model import (
    RelationshipDimensions,
    RelationshipState,
)
from wanxiang_substrate.actor_continuity.reprioritization_model import (
    GoalEvidence,
    GoalReprioritizationContext,
)
from wanxiang_substrate.actor_continuity.reprioritization_policy import (
    DeterministicGoalReprioritizationPolicy,
    apply_goal_reprioritization,
)
from wanxiang_substrate.epistemic.belief_revision import BeliefEvidence, BeliefRevisionEngine
from wanxiang_substrate.epistemic.model import BeliefAssertion, MemoryRecord


@dataclass(frozen=True, slots=True)
class ContinuityQualificationSeed:
    source_package_ref: str
    world_instance_refs: tuple[str, ...]
    actor_ids: tuple[EntityId, ...]
    days: int = 7
    ticks_per_day: int = 24
    seed: int = 0

    def __post_init__(self) -> None:
        if not self.source_package_ref.strip() or not self.world_instance_refs:
            raise ContractError("qualification seed requires source and world refs")
        if len(self.actor_ids) < 2 or len(set(self.actor_ids)) != len(self.actor_ids):
            raise ContractError("qualification requires at least two distinct actors")
        if self.days < 7 or self.ticks_per_day < 1 or self.seed < 0:
            raise ContractError("qualification duration or seed is invalid")


class SevenDayContinuityQualification:
    """Run actor projection transitions against a source-created package ref."""

    def __init__(self, seed: ContinuityQualificationSeed) -> None:
        self.seed = seed
        self._policy = DeterministicGoalReprioritizationPolicy("continuity-reference-v1")
        self._belief_engine = BeliefRevisionEngine()

    def run(self) -> ContinuityQualificationResult:
        initial = self._initial_checkpoint()
        final = self._advance(initial)
        replayed = self._advance(self._initial_checkpoint())
        reentered = final.resume()
        return ContinuityQualificationResult(
            source_package_ref=self.seed.source_package_ref,
            world_instance_refs=self.seed.world_instance_refs,
            actor_ids=tuple(actor.value for actor in self.seed.actor_ids),
            days_completed=final.day,
            final_digest=final.digest(),
            replay_digest=replayed.digest(),
            leave_reenter_digest=reentered.digest(),
            goal_revision_count=sum(len(item.goals.revisions) for item in final.actors),
            memory_count=sum(len(item.memories) for item in final.actors),
            belief_revision_count=sum(max(0, len(item.beliefs) - 1) for item in final.actors),
            relationship_revision_count=len(final.relationships.revisions),
        )

    def _initial_checkpoint(self) -> ContinuityCheckpoint:
        actors = tuple(
            ContinuityActorBundle(
                actor_id=actor_id,
                goals=ActorGoalStack.empty(actor_id),
                beliefs=(
                    BeliefAssertion(
                        EntityId(f"belief_{actor_id.value}_0"),
                        actor_id,
                        "the source-created world persists",
                        0.5,
                        0,
                    ),
                ),
            )
            for actor_id in self.seed.actor_ids
        )
        return ContinuityCheckpoint(
            source_package_ref=self.seed.source_package_ref,
            world_instance_refs=self.seed.world_instance_refs,
            day=0,
            at_ticks=0,
            actors=actors,
            relationships=RelationshipGraph(),
        )

    def _advance(self, checkpoint: ContinuityCheckpoint) -> ContinuityCheckpoint:
        current = checkpoint
        for day in range(checkpoint.day + 1, self.seed.days + 1):
            current = self._advance_day(current, day)
        return current

    def _advance_day(self, checkpoint: ContinuityCheckpoint, day: int) -> ContinuityCheckpoint:
        at_ticks = day * self.seed.ticks_per_day
        updated_actors: list[ContinuityActorBundle] = []
        for bundle in checkpoint.actors:
            memory = self._memory(bundle.actor_id, day, at_ticks)
            stack = self._update_goal(bundle.goals, bundle.actor_id, memory, day, at_ticks)
            belief_revision = self._update_belief(bundle, day, at_ticks)
            action = ActionExplanation(
                action_ref=f"action:{bundle.actor_id.value}:{day}",
                actor_id=bundle.actor_id,
                at_ticks=at_ticks,
                reason="continued the source-created actor trajectory",
                goal_refs=(f"goal_{bundle.actor_id.value}",),
                memory_refs=(memory.memory_id.value,),
                belief_refs=(belief_revision.after.belief_id.value,),
            )
            updated_actors.append(
                ContinuityActorBundle(
                    actor_id=bundle.actor_id,
                    goals=stack,
                    memories=bundle.memories + (memory,),
                    beliefs=bundle.beliefs + (belief_revision.after,),
                    actions=bundle.actions + (action,),
                )
            )
        relationships = self._update_relationships(checkpoint.relationships, day, at_ticks)
        return ContinuityCheckpoint(
            source_package_ref=checkpoint.source_package_ref,
            world_instance_refs=checkpoint.world_instance_refs,
            day=day,
            at_ticks=at_ticks,
            actors=tuple(updated_actors),
            relationships=relationships,
        )

    def _memory(self, actor_id: EntityId, day: int, at_ticks: int) -> MemoryRecord:
        return MemoryRecord(
            memory_id=EntityId(f"memory_{actor_id.value}_{day}"),
            actor_id=actor_id,
            kind="observation",
            content_ref=f"memory://{self.seed.source_package_ref}/{actor_id.value}/{day}",
            at_ticks=at_ticks,
            salience=0.6,
            source_perception_refs=(
                f"perception:{self.seed.source_package_ref}:{actor_id.value}:{day}",
            ),
            decay_rate=0.01,
        )

    def _update_goal(
        self,
        stack: ActorGoalStack,
        actor_id: EntityId,
        memory: MemoryRecord,
        day: int,
        at_ticks: int,
    ) -> ActorGoalStack:
        if stack.goal(EntityId(f"goal_{actor_id.value}")) is None:
            goal = ActorGoal(
                goal_id=EntityId(f"goal_{actor_id.value}"),
                actor_id=actor_id,
                tier="long_term",
                statement="remain coherent across the source-created world",
                priority=50,
                provenance=GoalProvenance("experience", (self.seed.source_package_ref,), "entry"),
                created_at_ticks=0,
            )
            stack, _ = stack.add_goal(
                goal,
                event_ref=f"goal:create:{actor_id.value}",
                at_ticks=0,
                reason="actor entered the source-created world",
            )
        goal_id = EntityId(f"goal_{actor_id.value}")
        context = GoalReprioritizationContext(
            actor_id=actor_id,
            stack=stack,
            now_ticks=at_ticks,
            seed=self.seed.seed,
            evidence=(
                GoalEvidence(
                    f"evidence:{memory.memory_id.value}",
                    actor_id,
                    goal_id,
                    "memory",
                    1,
                    "daily observation reinforces continuity",
                ),
            ),
        )
        proposals = self._policy.propose(context)
        if not proposals:
            return stack
        return apply_goal_reprioritization(
            stack,
            proposals[0],
            event_ref=f"goal:revise:{actor_id.value}:{day}",
            at_ticks=at_ticks,
        )[0]

    def _update_belief(self, bundle: ContinuityActorBundle, day: int, at_ticks: int):
        before = bundle.beliefs[-1]
        return self._belief_engine.revise(
            before,
            revision_id=f"belief:revise:{bundle.actor_id.value}:{day}",
            kind="support",
            evidence=BeliefEvidence(
                f"memory:{bundle.actor_id.value}:{day}",
                bundle.actor_id,
                at_ticks,
                0.05,
                "present",
            ),
            reason="daily actor-visible observation supports persistence",
            new_belief_id=EntityId(f"belief_{bundle.actor_id.value}_{day}"),
        )

    def _update_relationships(
        self, graph: RelationshipGraph, day: int, at_ticks: int
    ) -> RelationshipGraph:
        source, target = self.seed.actor_ids[:2]
        relation_id = f"relation_{source.value}_{target.value}"
        current = graph.state(relation_id)
        if current is None:
            state = RelationshipState(
                relation_id,
                source,
                target,
                "co-presence",
                RelationshipDimensions(trust=0.1),
                at_ticks,
                event_refs=(f"world:event:{day}",),
                visibility="participants",
            )
            return graph.add(
                state,
                event_ref=f"relation:create:{day}",
                at_ticks=at_ticks,
                reason="actors share a source-created world",
            )[0]
        state = replace(
            current,
            valid_from=at_ticks,
            dimensions=replace(current.dimensions, trust=min(1.0, current.dimensions.trust + 0.05)),
            event_refs=current.event_refs + (f"world:event:{day}",),
        )
        return graph.revise(
            state,
            event_ref=f"relation:revise:{day}",
            at_ticks=at_ticks,
            reason="continued shared experience",
        )[0]
