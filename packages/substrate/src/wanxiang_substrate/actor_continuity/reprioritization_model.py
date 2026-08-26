"""Goal-priority policy inputs and propose-only outputs."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

from wanxiang_substrate.actor_continuity.goal_stack import ActorGoalStack

EvidenceKind = Literal["observation", "belief", "memory", "relationship", "event"]
EvidenceKindValues = ("observation", "belief", "memory", "relationship", "event")


def _validate_refs(values: tuple[str, ...], label: str) -> None:
    if any(not value.strip() for value in values):
        raise ContractError(f"{label} cannot contain blank references")
    if len(set(values)) != len(values):
        raise ContractError(f"{label} references must be unique")


@dataclass(frozen=True, slots=True)
class GoalEvidence:
    """Actor-authorized evidence that may influence a goal proposal."""

    evidence_ref: str
    actor_id: EntityId
    goal_id: EntityId
    kind: EvidenceKind
    impact: int
    summary: str

    def __post_init__(self) -> None:
        if not self.evidence_ref.strip() or not self.summary.strip():
            raise ContractError("goal evidence requires a reference and summary")
        if self.kind not in EvidenceKindValues:
            raise ContractError(f"invalid goal evidence kind {self.kind!r}")
        if not -100 <= self.impact <= 100:
            raise ContractError("goal evidence impact must be in [-100, 100]")


@dataclass(frozen=True, slots=True)
class GoalReprioritizationContext:
    """Read-only input supplied to a deterministic or provider policy."""

    actor_id: EntityId
    stack: ActorGoalStack
    now_ticks: int
    evidence: tuple[GoalEvidence, ...] = ()
    seed: int = 0

    def __post_init__(self) -> None:
        if self.stack.actor_id != self.actor_id:
            raise ContractError("goal policy context actor does not match stack")
        if self.now_ticks < 0:
            raise ContractError("goal policy time cannot be negative")
        if self.seed < 0:
            raise ContractError("goal policy seed cannot be negative")
        if any(item.actor_id != self.actor_id for item in self.evidence):
            raise ContractError("goal evidence belongs to a different actor")
        if any(self.stack.goal(item.goal_id) is None for item in self.evidence):
            raise ContractError("goal evidence targets an unknown goal")


@dataclass(frozen=True, slots=True)
class GoalReprioritizationProposal:
    """Uncommitted policy output with reason and evidence lineage."""

    proposal_ref: str
    actor_id: EntityId
    goal_id: EntityId
    base_revision: int
    from_priority: int
    to_priority: int
    policy_ref: str
    reason: str
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.proposal_ref.strip() or not self.policy_ref.strip() or not self.reason.strip():
            raise ContractError("goal proposal requires ref, policy and reason")
        if self.base_revision < 0:
            raise ContractError("goal proposal base revision cannot be negative")
        if not 0 <= self.from_priority <= 100 or not 0 <= self.to_priority <= 100:
            raise ContractError("goal proposal priority must be in [0, 100]")
        if self.from_priority == self.to_priority:
            raise ContractError("goal proposal must change priority")
        _validate_refs(self.evidence_refs, "goal proposal evidence")

    def to_dict(self) -> dict[str, object]:
        return {
            "proposal_ref": self.proposal_ref,
            "actor_id": self.actor_id.value,
            "goal_id": self.goal_id.value,
            "base_revision": self.base_revision,
            "from_priority": self.from_priority,
            "to_priority": self.to_priority,
            "policy_ref": self.policy_ref,
            "reason": self.reason,
            "evidence_refs": list(self.evidence_refs),
        }


# Concise vocabulary for callers that describe this as a priority proposal.
GoalPriorityProposal = GoalReprioritizationProposal


def proposal_from_dict(value: Mapping[str, object]) -> GoalReprioritizationProposal:
    """Decode provider output only after the typed contract is checked."""
    required = (
        value.get("proposal_ref"),
        value.get("actor_id"),
        value.get("goal_id"),
        value.get("policy_ref"),
        value.get("reason"),
    )
    if not all(isinstance(item, str) for item in required):
        raise ContractError("invalid goal proposal serialization")
    refs = value.get("evidence_refs", [])
    if not isinstance(refs, list):
        raise ContractError("invalid goal proposal evidence refs")
    ref_values: list[str] = []
    for item in cast(list[object], refs):
        if not isinstance(item, str):
            raise ContractError("invalid goal proposal evidence refs")
        ref_values.append(item)
    numbers = (
        value.get("base_revision"),
        value.get("from_priority"),
        value.get("to_priority"),
    )
    if not all(isinstance(item, int) and not isinstance(item, bool) for item in numbers):
        raise ContractError("invalid goal proposal numeric fields")
    return GoalReprioritizationProposal(
        proposal_ref=required[0],  # type: ignore[arg-type]
        actor_id=EntityId(required[1]),  # type: ignore[arg-type]
        goal_id=EntityId(required[2]),  # type: ignore[arg-type]
        base_revision=numbers[0],  # type: ignore[arg-type]
        from_priority=numbers[1],  # type: ignore[arg-type]
        to_priority=numbers[2],  # type: ignore[arg-type]
        policy_ref=required[3],  # type: ignore[arg-type]
        reason=required[4],  # type: ignore[arg-type]
        evidence_refs=tuple(ref_values),
    )
