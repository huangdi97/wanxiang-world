"""Time-scoped relationship dimensions and revision records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError
from wanxiang_domain.ids import EntityId

RelationshipVisibility = Literal["public", "participants", "source"]
VisibilityValues = ("public", "participants", "source")


@dataclass(frozen=True, slots=True)
class RelationshipDimensions:
    """Bounded social dimensions; none is a canonical world fact by itself."""

    trust: float = 0.0
    affection: float = 0.0
    hostility: float = 0.0
    debt: float = 0.0
    loyalty: float = 0.0
    dependency: float = 0.0
    authority: float = 0.0
    reputation: float = 0.0

    def __post_init__(self) -> None:
        values = (
            self.trust,
            self.affection,
            self.hostility,
            self.debt,
            self.loyalty,
            self.dependency,
            self.authority,
            self.reputation,
        )
        if any(not -1.0 <= value <= 1.0 for value in values):
            raise ContractError("relationship dimensions must be in [-1, 1]")

    def to_dict(self) -> dict[str, float]:
        return {
            "trust": self.trust,
            "affection": self.affection,
            "hostility": self.hostility,
            "debt": self.debt,
            "loyalty": self.loyalty,
            "dependency": self.dependency,
            "authority": self.authority,
            "reputation": self.reputation,
        }


@dataclass(frozen=True, slots=True)
class RelationshipState:
    """One actor-to-actor relation view with temporal and event provenance."""

    relationship_id: str
    source_actor_id: EntityId
    target_actor_id: EntityId
    relation_type: str
    dimensions: RelationshipDimensions
    valid_from: int
    valid_to: int | None = None
    event_refs: tuple[str, ...] = ()
    visibility: RelationshipVisibility = "participants"

    def __post_init__(self) -> None:
        if not self.relationship_id.strip() or not self.relation_type.strip():
            raise ContractError("relationship requires id and type")
        if self.source_actor_id == self.target_actor_id:
            raise ContractError("relationship cannot target the same actor")
        if self.valid_from < 0 or (self.valid_to is not None and self.valid_to < self.valid_from):
            raise ContractError("relationship validity interval is invalid")
        if any(not ref.strip() for ref in self.event_refs):
            raise ContractError("relationship event refs cannot be blank")
        if len(set(self.event_refs)) != len(self.event_refs):
            raise ContractError("relationship event refs must be unique")
        if self.visibility not in VisibilityValues:
            raise ContractError(f"invalid relationship visibility {self.visibility!r}")

    def visible_to(self, viewer_actor_id: EntityId, *, admin: bool = False) -> bool:
        if admin or self.visibility == "public":
            return True
        if self.visibility == "source":
            return viewer_actor_id == self.source_actor_id
        return viewer_actor_id in (self.source_actor_id, self.target_actor_id)

    def active_at(self, at_ticks: int) -> bool:
        return self.valid_from <= at_ticks and (self.valid_to is None or at_ticks <= self.valid_to)


Relationship = RelationshipState
