"""Family semantic world: persons, kinship, life events, claims (G09B).

Kinship validity is time-scoped and validated (no self-loops, no child ==
parent). Imported facts are Claim sets with evidence links, never unconditional
truth. Lineage queries are deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_substrate.genealogy.errors import InvalidKinship

KinshipRole = Literal["parent", "child", "spouse"]


@dataclass(frozen=True, slots=True)
class Person:
    person_id: str
    name: str
    birth_year: int | None = None
    death_year: int | None = None
    living: bool = False

    def __post_init__(self) -> None:
        if not self.person_id or not self.name:
            raise InvalidKinship("person requires id and name")


@dataclass(frozen=True, slots=True)
class Kinship:
    """A time-scoped relationship between two persons."""

    relation_id: str
    source: str
    target: str
    role: KinshipRole
    start_year: int = 0
    end_year: int | None = None

    def __post_init__(self) -> None:
        if self.source == self.target:
            raise InvalidKinship("a person cannot be their own relation target")
        if self.end_year is not None and self.end_year < self.start_year:
            raise InvalidKinship("kinship end year before start year")


@dataclass(frozen=True, slots=True)
class LifeEvent:
    event_id: str
    person_id: str
    kind: str
    year: int
    place: str = ""


@dataclass(frozen=True, slots=True)
class FamilyClaim:
    """A claim about a person/fact with evidence links (not truth)."""

    claim_id: str
    person_id: str
    proposition: str
    value: str
    source_refs: tuple[str, ...] = ()


class FamilyWorld:
    """In-memory family world with validated kinship and lineage queries."""

    def __init__(self) -> None:
        self._persons: dict[str, Person] = {}
        self._kinships: dict[str, Kinship] = {}
        self._events: dict[str, LifeEvent] = {}
        self._claims: dict[str, FamilyClaim] = {}

    def add_person(self, person: Person) -> Person:
        self._persons[person.person_id] = person
        return person

    def add_kinship(self, kinship: Kinship) -> Kinship:
        if kinship.source not in self._persons or kinship.target not in self._persons:
            raise InvalidKinship("kinship references unknown persons")
        if kinship.role == "parent" and self._descendant(kinship.target, kinship.source):
            raise InvalidKinship("kinship would create a cycle")
        self._kinships[kinship.relation_id] = kinship
        return kinship

    def add_event(self, event: LifeEvent) -> LifeEvent:
        if event.person_id not in self._persons:
            raise InvalidKinship("event references unknown person")
        self._events[event.event_id] = event
        return event

    def add_claim(self, claim: FamilyClaim) -> FamilyClaim:
        if claim.person_id not in self._persons:
            raise InvalidKinship("claim references unknown person")
        self._claims[claim.claim_id] = claim
        return claim

    def parents(self, person_id: str) -> tuple[Person, ...]:
        result: list[Person] = []
        for kinship in self._kinships.values():
            if kinship.role == "parent" and kinship.target == person_id:
                parent = self._persons.get(kinship.source)
                if parent is not None:
                    result.append(parent)
        return tuple(sorted(result, key=lambda p: p.person_id))

    def children(self, person_id: str) -> tuple[Person, ...]:
        result: list[Person] = []
        for kinship in self._kinships.values():
            if kinship.role == "parent" and kinship.source == person_id:
                child = self._persons.get(kinship.target)
                if child is not None:
                    result.append(child)
        return tuple(sorted(result, key=lambda p: p.person_id))

    def claims_for(self, person_id: str) -> tuple[FamilyClaim, ...]:
        return tuple(
            sorted(
                (c for c in self._claims.values() if c.person_id == person_id),
                key=lambda c: c.claim_id,
            )
        )

    def _descendant(self, ancestor: str, candidate: str) -> bool:
        """True if candidate is a descendant of ancestor (cycle guard)."""
        frontier = [ancestor]
        seen: set[str] = set()
        while frontier:
            current = frontier.pop()
            if current == candidate:
                return True
            if current in seen:
                continue
            seen.add(current)
            frontier.extend(child.person_id for child in self.children(current))
        return False
