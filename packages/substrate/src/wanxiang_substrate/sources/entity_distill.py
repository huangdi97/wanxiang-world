"""Place/object/organization/path source distillation (G35D).

M32: turn approved source text into source-bound CANDIDATES for places,
paths, objects and organizations (gardens, public paths, letters, medicine,
gifts, households) plus topology candidates (connections), routing details
that cannot be directly verified into Completion instead of presenting them
as source evidence. Reuses G35B locators + the shared evidence review rules;
introduces no second registry/engine.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.sources.evidence import AUTHORIZED_REVIEWERS, evidence_ok
from wanxiang_substrate.sources.locator import SourceLocator, segment_source, source_slice

EntityKind = Literal["place", "path", "object", "organization"]
VALID_ENTITY_KINDS = ("place", "path", "object", "organization")
EdgeKind = Literal["portal", "path", "custody", "containment", "membership"]
VALID_EDGE_KINDS = ("portal", "path", "custody", "containment", "membership")
EntityStatus = Literal["pending", "eligible", "rejected"]
VALID_ENTITY_STATUSES = ("pending", "eligible", "rejected")


@dataclass(frozen=True, slots=True)
class EntityMention:
    """A source-bound mention of a place/object/organization candidate."""

    key: str
    kind: EntityKind
    display_name: str
    locators: tuple[SourceLocator, ...]

    def __post_init__(self) -> None:
        if not self.key or not self.display_name:
            raise ContractError("entity mention requires key and display name")
        if self.kind not in VALID_ENTITY_KINDS:
            raise ContractError(f"invalid entity kind {self.kind!r}")
        if not self.locators:
            raise ContractError("entity mention requires at least one evidence locator")

    @property
    def has_evidence(self) -> bool:
        return bool(self.locators)


@dataclass(frozen=True, slots=True)
class EntityConnection:
    """A source-bound topology edge between two entity candidates."""

    connection_id: str
    source_key: str
    target_key: str
    label: str
    kind: EdgeKind
    locators: tuple[SourceLocator, ...]

    def __post_init__(self) -> None:
        if not self.source_key or not self.target_key or not self.label:
            raise ContractError("connection requires source, target and label")
        if self.kind not in VALID_EDGE_KINDS:
            raise ContractError(f"invalid edge kind {self.kind!r}")
        if not self.locators:
            raise ContractError("connection requires at least one evidence locator")


@dataclass(frozen=True, slots=True)
class EntityCandidate:
    """A distilled place/object/organization candidate; never Canon until review.

    completion_notes carry details that could not be directly verified in the
    source; they are strings, never evidence, and never satisfy the review gate.
    """

    candidate_id: str
    kind: EntityKind
    key: str
    display_name: str
    mentions: tuple[EntityMention, ...]
    completion_notes: tuple[str, ...] = ()
    provenance: tuple[str, ...] = ()
    status: EntityStatus = "pending"

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.key or not self.display_name:
            raise ContractError("entity candidate requires id, key and display name")
        if self.kind not in VALID_ENTITY_KINDS:
            raise ContractError(f"invalid entity kind {self.kind!r}")
        if self.status not in VALID_ENTITY_STATUSES:
            raise ContractError(f"invalid entity status {self.status!r}")
        if not self.mentions:
            raise ContractError("entity candidate requires at least one mention")

    @property
    def evidence_locators(self) -> tuple[SourceLocator, ...]:
        return tuple(
            sorted(
                (loc for mention in self.mentions for loc in mention.locators),
                key=lambda loc: loc.locator,
            )
        )

    def with_status(self, status: EntityStatus) -> EntityCandidate:
        return EntityCandidate(
            candidate_id=self.candidate_id,
            kind=self.kind,
            key=self.key,
            display_name=self.display_name,
            mentions=self.mentions,
            completion_notes=self.completion_notes,
            provenance=self.provenance,
            status=status,
        )


@dataclass(frozen=True, slots=True)
class EntityReviewDecision:
    candidate_id: str
    approved: bool
    reason: str
    reviewer: str

    def __post_init__(self) -> None:
        if not self.reason:
            raise ContractError("review decision requires a reason")


@dataclass(frozen=True, slots=True)
class DistilledEntities:
    """Result of distillation: source-bound candidates + topology edges."""

    candidates: tuple[EntityCandidate, ...]
    connections: tuple[EntityConnection, ...]

    @property
    def unresolved_targets(self) -> tuple[str, ...]:
        """Connection targets with no distilled candidate -> Completion."""
        keys = {c.key for c in self.candidates}
        return tuple(sorted({c.target_key for c in self.connections} - keys))


class EntityDistiller:
    """Deterministic place/object/organization + topology distillation.

    Pure: reads source text, produces candidates and connections. Rules
    (extract_entities / extract_connections) are caller-supplied so the
    mechanism is edition-agnostic. Source eligibility is enforced by the
    existing SourceGate before this class is used; no write path exists here.
    """

    def __init__(
        self,
        *,
        extract_entities: Callable[[str], tuple[tuple[str, EntityKind, str], ...]],
        extract_connections: Callable[[str], tuple[tuple[str, str, str, EdgeKind], ...]],
    ) -> None:
        self._extract_entities = extract_entities
        self._extract_connections = extract_connections

    def distill(self, source_id: str, text: str) -> DistilledEntities:
        """Distill candidates and topology; re-running on same text is identical."""
        mentions_by: dict[tuple[str, EntityKind], set[SourceLocator]] = {}
        mention_names: dict[tuple[str, EntityKind], str] = {}
        edges_by: dict[tuple[str, str, str, EdgeKind], set[SourceLocator]] = {}
        for locator in segment_source(source_id, text):
            segment = source_slice(text, locator)
            for key, kind, display in self._extract_entities(segment):
                mentions_by.setdefault((key, kind), set()).add(locator)
                mention_names[(key, kind)] = display
            for source_key, target_key, label, edge_kind in self._extract_connections(segment):
                edges_by.setdefault((source_key, target_key, label, edge_kind), set()).add(locator)
        candidates: list[EntityCandidate] = []
        for index, ((key, kind), locators) in enumerate(sorted(mentions_by.items()), start=1):
            display = mention_names[(key, kind)]
            sorted_locators = tuple(sorted(locators, key=lambda loc: loc.locator))
            provenance = (source_id,) + tuple(loc.locator for loc in sorted_locators)
            candidates.append(
                EntityCandidate(
                    candidate_id=f"ent_{index:04d}",
                    kind=kind,
                    key=key,
                    display_name=display,
                    mentions=(
                        EntityMention(
                            key=key,
                            kind=kind,
                            display_name=display,
                            locators=sorted_locators,
                        ),
                    ),
                    provenance=provenance,
                )
            )
        connections: list[EntityConnection] = []
        for index, ((source_key, target_key, label, edge_kind), locators) in enumerate(
            sorted(edges_by.items()), start=1
        ):
            connections.append(
                EntityConnection(
                    connection_id=f"conn_{index:04d}",
                    source_key=source_key,
                    target_key=target_key,
                    label=label,
                    kind=edge_kind,
                    locators=tuple(sorted(locators, key=lambda loc: loc.locator)),
                )
            )
        return DistilledEntities(
            candidates=tuple(candidates),
            connections=tuple(connections),
        )


class EntityReviewGate:
    """Human/rule review gate: only evidence-backed candidates become eligible.

    Completion notes never count as evidence: eligibility requires resolvable
    source locators on every mention (and on every claimed connection).
    """

    def __init__(self, *, min_evidence_locators: int = 1) -> None:
        if min_evidence_locators < 1:
            raise ValueError("min_evidence_locators must be >= 1")
        self._min_evidence_locators = min_evidence_locators

    def review(
        self,
        candidate: EntityCandidate,
        *,
        source_text: str,
        reviewer: str,
        connections: tuple[EntityConnection, ...] = (),
    ) -> EntityReviewDecision:
        if reviewer not in AUTHORIZED_REVIEWERS:
            return EntityReviewDecision(
                candidate.candidate_id,
                False,
                f"reviewer {reviewer!r} is not authorized",
                reviewer,
            )
        claim_locators = [mention.locators for mention in candidate.mentions]
        claim_locators += [
            conn.locators for conn in connections if conn.source_key == candidate.key
        ]
        ok, reason = evidence_ok(
            locators_per_claim=tuple(claim_locators),
            source_text=source_text,
            min_evidence_locators=self._min_evidence_locators,
        )
        if not ok:
            return EntityReviewDecision(candidate.candidate_id, False, reason, reviewer)
        return EntityReviewDecision(
            candidate.candidate_id,
            True,
            "evidence-backed entity approved",
            reviewer,
        )
