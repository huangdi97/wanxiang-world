"""Character relation / knowledge-boundary distillation (G35G).

M32: per-character runnable model, not personality labels: source-backed
life-stage/persona/relation/world facts with public/private scope, a
knowledge boundary (private facts of others stay hidden unless granted), and
future facts visible only on the control plane. Completion (unverifiable) and
Interpretive (persona) are kept separate from factual canon. Reuses G35B
locators + G35E scenario/temporal classification; anonymized keys make the
mechanism identity-agnostic.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.sources.canon import ScenarioPoint, Temporal
from wanxiang_substrate.sources.locator import SourceLocator, segment_source, source_slice

FactScope = Literal["public", "private"]
VALID_FACT_SCOPES = ("public", "private")
FactKind = Literal["life_stage", "persona", "relation", "world"]
VALID_FACT_KINDS = ("life_stage", "persona", "relation", "world")


@dataclass(frozen=True, slots=True)
class CharacterFact:
    """A source-backed fact about a character with scope and kind."""

    fact_id: str
    character_key: str
    proposition: str
    scope: FactScope
    kind: FactKind
    temporal: Temporal
    locators: tuple[SourceLocator, ...]
    status: Literal["pending", "eligible", "rejected"] = "pending"

    def __post_init__(self) -> None:
        if not self.fact_id or not self.character_key or not self.proposition:
            raise ContractError("fact requires id, character key and proposition")
        if self.scope not in VALID_FACT_SCOPES:
            raise ContractError(f"invalid fact scope {self.scope!r}")
        if self.kind not in VALID_FACT_KINDS:
            raise ContractError(f"invalid fact kind {self.kind!r}")
        if not self.locators:
            raise ContractError("fact requires at least one evidence locator")

    @property
    def is_runtime_visible(self) -> bool:
        return self.temporal != "future"


@dataclass(frozen=True, slots=True)
class RelationClaim:
    """A source-backed relation claim between two character keys."""

    relation_id: str
    source_key: str
    target_key: str
    relation_type: str
    scope: FactScope
    locators: tuple[SourceLocator, ...]

    def __post_init__(self) -> None:
        if not self.relation_id or not self.source_key or not self.target_key:
            raise ContractError("relation requires id, source and target")
        if not self.relation_type:
            raise ContractError("relation requires a type")
        if self.scope not in VALID_FACT_SCOPES:
            raise ContractError(f"invalid relation scope {self.scope!r}")
        if not self.locators:
            raise ContractError("relation requires at least one evidence locator")


@dataclass(frozen=True, slots=True)
class KnowledgeBoundary:
    """What each character knows: private facts of others stay hidden.

    grants are (observer_key, fact_id) pairs that lift the boundary for a
    specific private fact. Public facts and a character's own facts are always
    known; future facts are never known at runtime.
    """

    grants: tuple[tuple[str, str], ...] = ()

    def knows(self, observer_key: str, fact: CharacterFact) -> bool:
        if fact.temporal == "future":
            return False
        if fact.scope == "public":
            return True
        if fact.character_key == observer_key:
            return True
        return (observer_key, fact.fact_id) in self.grants


@dataclass(frozen=True, slots=True)
class CharacterCanon:
    """Compiled per-character canon with a knowledge boundary."""

    facts: tuple[CharacterFact, ...]
    relations: tuple[RelationClaim, ...]
    boundary: KnowledgeBoundary
    completion_notes: tuple[str, ...] = ()

    @property
    def runtime_facts(self) -> tuple[CharacterFact, ...]:
        """Facts the running world may see (never future)."""
        return tuple(fact for fact in self.facts if fact.is_runtime_visible)

    def visible_to(self, observer_key: str) -> tuple[CharacterFact, ...]:
        """Facts an observer may see, respecting the knowledge boundary."""
        return tuple(fact for fact in self.runtime_facts if self.boundary.knows(observer_key, fact))

    def facts_for(self, character_key: str) -> tuple[CharacterFact, ...]:
        return tuple(fact for fact in self.facts if fact.character_key == character_key)

    def facts_of_kind(self, kind: FactKind) -> tuple[CharacterFact, ...]:
        return tuple(fact for fact in self.facts if fact.kind == kind)

    def relations_for(self, character_key: str) -> tuple[RelationClaim, ...]:
        return tuple(
            rel
            for rel in self.relations
            if rel.source_key == character_key or rel.target_key == character_key
        )


def _no_private_knowers(_key: str) -> frozenset[str]:
    return frozenset()


class CharacterDistiller:
    """Deterministic character fact/relation + knowledge-boundary distillation.

    Pure: reads source text + caller-supplied rules; produces CharacterCanon.
    Source eligibility is enforced by the existing SourceGate before use.
    """

    def __init__(
        self,
        *,
        extract_facts: Callable[[str], tuple[tuple[str, str, FactKind, FactScope], ...]],
        extract_relations: Callable[[str], tuple[tuple[str, str, str, FactScope], ...]],
        private_knowers: Callable[[str], frozenset[str]] | None = None,
    ) -> None:
        """private_knowers(character_key) -> observer keys granted that
        character's private facts; empty by default (no cross-character leak)."""
        self._extract_facts = extract_facts
        self._extract_relations = extract_relations
        self._private_knowers = private_knowers or _no_private_knowers

    def distill(
        self,
        *,
        scenario: ScenarioPoint,
        source_id: str,
        text: str,
        completion_notes: tuple[str, ...] = (),
    ) -> CharacterCanon:
        """Distill character canon; re-running on same inputs is identical."""
        locators = segment_source(source_id, text)
        index_by_locator = {loc.locator: index for index, loc in enumerate(locators)}
        if scenario.locator.locator not in index_by_locator:
            raise ContractError("scenario locator is not a segment of the source")
        scenario_index = index_by_locator[scenario.locator.locator]
        facts: list[CharacterFact] = []
        relations: list[RelationClaim] = []
        fact_index = 0
        relation_index = 0
        for locator in locators:
            segment_index = index_by_locator[locator.locator]
            if segment_index < scenario_index:
                temporal: Temporal = "past"
            elif segment_index == scenario_index:
                temporal = "present"
            else:
                temporal = "future"
            segment = source_slice(text, locator)
            for proposition, character_key, kind, scope in self._extract_facts(segment):
                fact_index += 1
                facts.append(
                    CharacterFact(
                        fact_id=f"fact_{fact_index:04d}",
                        character_key=character_key,
                        proposition=proposition,
                        scope=scope,
                        kind=kind,
                        temporal=temporal,
                        locators=(locator,),
                    )
                )
            for source_key, target_key, relation_type, scope in self._extract_relations(segment):
                relation_index += 1
                relations.append(
                    RelationClaim(
                        relation_id=f"rel_{relation_index:04d}",
                        source_key=source_key,
                        target_key=target_key,
                        relation_type=relation_type,
                        scope=scope,
                        locators=(locator,),
                    )
                )
        grants: list[tuple[str, str]] = []
        for fact in facts:
            if fact.scope == "private":
                grants.extend(
                    (observer, fact.fact_id)
                    for observer in sorted(self._private_knowers(fact.character_key))
                )
        return CharacterCanon(
            facts=tuple(facts),
            relations=tuple(relations),
            boundary=KnowledgeBoundary(grants=tuple(sorted(set(grants)))),
            completion_notes=completion_notes,
        )
