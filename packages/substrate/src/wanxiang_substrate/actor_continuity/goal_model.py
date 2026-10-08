"""Immutable actor-goal contracts, kept outside canonical world truth."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, cast

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

GoalTier = Literal["life_motive", "long_term", "medium_term", "short_term", "intent"]
GoalTierValues = ("life_motive", "long_term", "medium_term", "short_term", "intent")
ActorGoalStatus = Literal["active", "paused", "completed", "abandoned"]
GoalStatusValues = ("active", "paused", "completed", "abandoned")
GoalRevisionKind = Literal["created", "revised", "reprioritized", "status_changed"]
GoalRevisionKindValues = ("created", "revised", "reprioritized", "status_changed")
ProvenanceKind = Literal["actor", "memory", "belief", "observation", "relationship", "experience"]
ProvenanceKindValues = (
    "actor",
    "memory",
    "belief",
    "observation",
    "relationship",
    "experience",
)
GOAL_STACK_SCHEMA_VERSION = 1


def _refs(values: tuple[str, ...], label: str) -> None:
    if any(not value.strip() for value in values):
        raise ContractError(f"{label} cannot contain blank references")
    if len(set(values)) != len(values):
        raise ContractError(f"{label} references must be unique")


@dataclass(frozen=True, slots=True)
class GoalProvenance:
    """Actor-facing rationale and references, never a world-truth record."""

    kind: ProvenanceKind
    refs: tuple[str, ...] = ()
    rationale: str = ""

    def __post_init__(self) -> None:
        if self.kind not in ProvenanceKindValues:
            raise ContractError(f"invalid goal provenance kind {self.kind!r}")
        _refs(self.refs, "goal provenance")
        if len(self.rationale) > 2000:
            raise ContractError("goal provenance rationale is too long")

    def to_dict(self) -> dict[str, object]:
        return {"kind": self.kind, "refs": list(self.refs), "rationale": self.rationale}

    @classmethod
    def from_dict(cls, value: Mapping[str, object]) -> GoalProvenance:
        kind = value.get("kind")
        refs = value.get("refs", [])
        rationale = value.get("rationale", "")
        if not isinstance(kind, str) or not isinstance(refs, list):
            raise ContractError("invalid goal provenance serialization")
        ref_values: list[str] = []
        for item in cast(list[object], refs):
            if not isinstance(item, str):
                raise ContractError("goal provenance references must be text")
            ref_values.append(item)
        if not isinstance(rationale, str):
            raise ContractError("goal provenance rationale must be text")
        return cls(kind=kind, refs=tuple(ref_values), rationale=rationale)  # type: ignore[arg-type]


@dataclass(frozen=True, slots=True)
class ActorGoal:
    """A desired actor outcome; it has no canonical entity or truth fields."""

    goal_id: EntityId
    actor_id: EntityId
    tier: GoalTier
    statement: str
    priority: int
    dependencies: tuple[EntityId, ...] = ()
    deadline_ticks: int | None = None
    provenance: GoalProvenance = GoalProvenance("actor")
    status: ActorGoalStatus = "active"
    created_at_ticks: int = 0
    updated_at_ticks: int = 0

    def __post_init__(self) -> None:
        if self.tier not in GoalTierValues:
            raise ContractError(f"invalid goal tier {self.tier!r}")
        if not self.statement.strip() or len(self.statement) > 2000:
            raise ContractError("goal statement must contain 1-2000 characters")
        if not 0 <= self.priority <= 100:
            raise ContractError("goal priority must be in [0, 100]")
        if len(set(self.dependencies)) != len(self.dependencies):
            raise ContractError("goal dependencies must be unique")
        if self.goal_id in self.dependencies:
            raise ContractError("goal cannot depend on itself")
        if self.deadline_ticks is not None and self.deadline_ticks < 0:
            raise ContractError("goal deadline cannot be negative")
        if self.status not in GoalStatusValues:
            raise ContractError(f"invalid goal status {self.status!r}")
        if self.created_at_ticks < 0 or self.updated_at_ticks < self.created_at_ticks:
            raise ContractError("goal timestamps must be ordered and non-negative")

    def to_dict(self) -> dict[str, object]:
        return {
            "goal_id": self.goal_id.value,
            "actor_id": self.actor_id.value,
            "tier": self.tier,
            "statement": self.statement,
            "priority": self.priority,
            "dependencies": [item.value for item in self.dependencies],
            "deadline_ticks": self.deadline_ticks,
            "provenance": self.provenance.to_dict(),
            "status": self.status,
            "created_at_ticks": self.created_at_ticks,
            "updated_at_ticks": self.updated_at_ticks,
        }

    @classmethod
    def from_dict(cls, value: Mapping[str, object]) -> ActorGoal:
        goal_id = value.get("goal_id")
        actor_id = value.get("actor_id")
        tier = value.get("tier")
        statement = value.get("statement")
        priority = value.get("priority")
        dependencies = value.get("dependencies", [])
        deadline = value.get("deadline_ticks")
        provenance = value.get("provenance")
        status = value.get("status", "active")
        created = value.get("created_at_ticks", 0)
        updated = value.get("updated_at_ticks", created)
        if not all(isinstance(item, str) for item in (goal_id, actor_id, tier, statement, status)):
            raise ContractError("invalid actor goal serialization")
        goal_id_text = cast(str, goal_id)
        actor_id_text = cast(str, actor_id)
        tier_text = cast(str, tier)
        statement_text = cast(str, statement)
        status_text = cast(str, status)
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise ContractError("serialized goal priority must be an integer")
        if not isinstance(dependencies, list):
            raise ContractError("serialized goal dependencies must be text ids")
        dependency_values: list[str] = []
        for item in cast(list[object], dependencies):
            if not isinstance(item, str):
                raise ContractError("serialized goal dependencies must be text ids")
            dependency_values.append(item)
        if deadline is not None and (not isinstance(deadline, int) or isinstance(deadline, bool)):
            raise ContractError("serialized goal deadline must be an integer or null")
        if not isinstance(provenance, Mapping):
            raise ContractError("serialized goal provenance is required")
        provenance_mapping = cast(Mapping[str, object], provenance)
        if not isinstance(created, int) or isinstance(created, bool):
            raise ContractError("serialized goal creation time must be an integer")
        if not isinstance(updated, int) or isinstance(updated, bool):
            raise ContractError("serialized goal update time must be an integer")
        return cls(
            goal_id=EntityId(goal_id_text),
            actor_id=EntityId(actor_id_text),
            tier=tier_text,  # type: ignore[arg-type]
            statement=statement_text,
            priority=priority,
            dependencies=tuple(EntityId(item) for item in dependency_values),
            deadline_ticks=deadline,
            provenance=GoalProvenance.from_dict(provenance_mapping),
            status=status_text,  # type: ignore[arg-type]
            created_at_ticks=created,
            updated_at_ticks=updated,
        )


# Named tier aliases keep the product vocabulary explicit while retaining one
# validated goal representation and one serialization contract.
LifeMotive = ActorGoal
LongTermGoal = ActorGoal
MediumTermGoal = ActorGoal
ShortTermGoal = ActorGoal
Intent = ActorGoal


@dataclass(frozen=True, slots=True)
class GoalRevisionEvent:
    """Replayable actor-projection revision, not a canonical world event."""

    event_ref: str
    actor_id: EntityId
    goal_id: EntityId
    sequence: int
    kind: GoalRevisionKind
    at_ticks: int
    reason: str
    after: ActorGoal
    before: ActorGoal | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.event_ref.strip() or not self.reason.strip():
            raise ContractError("goal revision requires event_ref and reason")
        if self.sequence < 1 or self.at_ticks < 0:
            raise ContractError("goal revision sequence/time is invalid")
        if self.kind not in GoalRevisionKindValues:
            raise ContractError(f"invalid goal revision kind {self.kind!r}")
        if self.after.actor_id != self.actor_id or self.after.goal_id != self.goal_id:
            raise ContractError("goal revision target does not match after goal")
        if self.before is not None and (
            self.before.actor_id != self.actor_id or self.before.goal_id != self.goal_id
        ):
            raise ContractError("goal revision target does not match before goal")
        if self.kind == "created" and self.before is not None:
            raise ContractError("created goal revision cannot have a before value")
        if self.kind != "created" and self.before is None:
            raise ContractError("non-created goal revision requires a before value")
        _refs(self.evidence_refs, "goal revision evidence")

    @property
    def event_type(self) -> GoalRevisionKind:
        """Compatibility vocabulary for event consumers."""
        return self.kind

    def to_dict(self) -> dict[str, object]:
        return {
            "event_ref": self.event_ref,
            "actor_id": self.actor_id.value,
            "goal_id": self.goal_id.value,
            "sequence": self.sequence,
            "kind": self.kind,
            "at_ticks": self.at_ticks,
            "reason": self.reason,
            "before": self.before.to_dict() if self.before is not None else None,
            "after": self.after.to_dict(),
            "evidence_refs": list(self.evidence_refs),
        }


def to_json(value: Mapping[str, object]) -> str:
    """Canonical JSON helper shared by stack serialization tests."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
