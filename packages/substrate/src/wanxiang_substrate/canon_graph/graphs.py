"""Full Corpus -> Canon Graph (M36).

Composes the M32 source/distillation machinery into runnable graphs:
- SceneCandidate (time/place/participant cues; cross-segment/chapter policy),
- CharacterGraph (identity/alias/role/life-stage),
- SourceGraph (place containment/connectivity, item custody, org membership),
- TimelineGraph (event before/after/uncertain + participants/place/evidence),
- CanonGraph (categories, edition views, contradictory claims preserved).
Pure and deterministic; real《红楼梦》canon remains EXTERNAL_BLOCKED.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.sources.locator import SourceLocator


# ---------------------------------------------------------------- scenes
@dataclass(frozen=True, slots=True)
class SceneCandidate:
    """A scene candidate from time/place/participant cues (cross-chapter ok)."""

    scene_id: str
    chapter_range: tuple[int, int]
    place_keys: tuple[str, ...]
    participant_keys: tuple[str, ...]
    cues: tuple[str, ...]
    locators: tuple[SourceLocator, ...]

    def __post_init__(self) -> None:
        if not self.scene_id:
            raise ContractError("scene requires an id")
        if self.chapter_range[0] > self.chapter_range[1]:
            raise ContractError("scene chapter_range must be ordered")


def detect_scenes(
    locators: tuple[SourceLocator, ...],
    *,
    chapter_of: tuple[tuple[SourceLocator, str], ...],
    place_of: tuple[tuple[SourceLocator, str], ...],
    participant_of: tuple[tuple[SourceLocator, str], ...],
) -> tuple[SceneCandidate, ...]:
    """Group source slices into scene candidates by shared cues.

    Caller-supplied cue maps (locator -> chapter/place/participant) keep the
    mechanism edition-agnostic.
    """
    scenes: list[SceneCandidate] = []
    seen: set[str] = set()
    for locator, chapter in chapter_of:
        place_keys = tuple(sorted(p for loc, p in place_of if loc.locator == locator.locator))
        participants = tuple(
            sorted(p for loc, p in participant_of if loc.locator == locator.locator)
        )
        scene_id = f"scene_{chapter}_{'_'.join(place_keys) or 'nowhere'}"
        if scene_id in seen:
            continue
        seen.add(scene_id)
        chapter_range = (int(chapter), int(chapter))
        scenes.append(
            SceneCandidate(
                scene_id=scene_id,
                chapter_range=chapter_range,
                place_keys=place_keys,
                participant_keys=participants,
                cues=("time", "place", "participant"),
                locators=(locator,),
            )
        )
    return tuple(sorted(scenes, key=lambda s: s.scene_id))


# ---------------------------------------------------------------- character graph
@dataclass(frozen=True, slots=True)
class CharacterNode:
    """A character with aliases, role and life-stage evidence."""

    character_key: str
    display_name: str
    aliases: tuple[str, ...]
    role: str
    life_stage: str
    evidence: tuple[SourceLocator, ...]


@dataclass(frozen=True, slots=True)
class CharacterEdge:
    """A relation between two characters."""

    source_key: str
    target_key: str
    relation_type: str
    valid_from: int | None = None
    valid_to: int | None = None


@dataclass(frozen=True, slots=True)
class CharacterGraph:
    """Identity/Alias/Role graph."""

    nodes: tuple[CharacterNode, ...]
    edges: tuple[CharacterEdge, ...]

    def node(self, key: str) -> CharacterNode | None:
        for node in self.nodes:
            if node.character_key == key:
                return node
        return None


def build_character_graph(
    *,
    identities: tuple[tuple[str, str, tuple[str, ...], str, str], ...],
    relations: tuple[tuple[str, str, str, int | None, int | None], ...],
) -> CharacterGraph:
    """Build the character graph from distilled identity + relation claims."""
    nodes = tuple(
        CharacterNode(
            character_key=key,
            display_name=display,
            aliases=aliases,
            role=role,
            life_stage=life_stage,
            evidence=(),
        )
        for key, display, aliases, role, life_stage in identities
    )
    edges = tuple(
        CharacterEdge(source_key=s, target_key=t, relation_type=r, valid_from=v1, valid_to=v2)
        for s, t, r, v1, v2 in relations
    )
    return CharacterGraph(nodes=nodes, edges=edges)


# ---------------------------------------------------------------- source graph
@dataclass(frozen=True, slots=True)
class SourceGraph:
    """Place containment/connectivity, item custody, org membership claims."""

    place_connectivity: tuple[tuple[str, str, str], ...]  # (a, b, via)
    place_containment: tuple[tuple[str, str], ...]  # (container, contained)
    item_custody: tuple[tuple[str, str], ...]  # (item, custodian)
    org_membership: tuple[tuple[str, str], ...]  # (actor, org)


def build_source_graph(
    *,
    connectivity: tuple[tuple[str, str, str], ...] = (),
    containment: tuple[tuple[str, str], ...] = (),
    custody: tuple[tuple[str, str], ...] = (),
    membership: tuple[tuple[str, str], ...] = (),
) -> SourceGraph:
    return SourceGraph(
        place_connectivity=tuple(sorted(connectivity)),
        place_containment=tuple(sorted(containment)),
        item_custody=tuple(sorted(custody)),
        org_membership=tuple(sorted(membership)),
    )


# ---------------------------------------------------------------- timeline
EventOrder = str  # "before" | "after" | "uncertain"


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    """An event with ordering, participants, place and evidence."""

    event_id: str
    label: str
    order: EventOrder
    participants: tuple[str, ...]
    place_key: str
    evidence: tuple[SourceLocator, ...] = ()


@dataclass(frozen=True, slots=True)
class TimelineGraph:
    """Event ordering graph (before/after/uncertain)."""

    events: tuple[TimelineEvent, ...]
    order_edges: tuple[tuple[str, str, EventOrder], ...]

    def before(self, a: str, b: str) -> bool:
        return (a, b, "before") in self.order_edges


def build_timeline(
    *,
    events: tuple[tuple[str, str, EventOrder, tuple[str, ...], str], ...],
) -> TimelineGraph:
    """Build the timeline from (id, label, order, participants, place) events."""
    timeline_events = tuple(
        TimelineEvent(event_id=eid, label=label, order=order, participants=parts, place_key=place)
        for eid, label, order, parts, place in events
    )
    order_edges: list[tuple[str, str, EventOrder]] = []
    ids = [e.event_id for e in timeline_events]
    for index, event in enumerate(timeline_events):
        if event.order == "before" and index + 1 < len(ids):
            order_edges.append((event.event_id, ids[index + 1], "before"))
    return TimelineGraph(events=timeline_events, order_edges=tuple(sorted(order_edges)))


# ---------------------------------------------------------------- canon graph
@dataclass(frozen=True, slots=True)
class CanonClaim:
    """A canon claim with a category and optional edition scope."""

    claim_id: str
    proposition: str
    category: str  # e.g. character/relation/event/place/item
    edition: str  # e.g. "edition_a" / "shared"
    evidence: tuple[str, ...] = ()
    contradicted_by: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class CanonGraph:
    """Canon categories, edition views and preserved contradictions."""

    claims: tuple[CanonClaim, ...]

    def edition_view(self, edition: str) -> tuple[CanonClaim, ...]:
        return tuple(c for c in self.claims if c.edition == edition or c.edition == "shared")

    def contradictions(self) -> tuple[tuple[str, str], ...]:
        pairs: list[tuple[str, str]] = []
        for claim in self.claims:
            for other_id in claim.contradicted_by:
                if claim.claim_id < other_id:
                    pairs.append((claim.claim_id, other_id))
        return tuple(sorted(set(pairs)))


def build_canon_graph(
    *,
    claims: tuple[tuple[str, str, str, str, tuple[str, ...]], ...],
    contradictions: tuple[tuple[str, str], ...] = (),
) -> CanonGraph:
    """Build the canon graph; contradictory claims are never dropped."""
    contradicted: dict[str, tuple[str, ...]] = {}
    for left, right in contradictions:
        contradicted[left] = contradicted.get(left, ()) + (right,)
        contradicted[right] = contradicted.get(right, ()) + (left,)
    return CanonGraph(
        claims=tuple(
            CanonClaim(
                claim_id=cid,
                proposition=prop,
                category=cat,
                edition=edition,
                evidence=evidence,
                contradicted_by=contradicted.get(cid, ()),
            )
            for cid, prop, cat, edition, evidence in claims
        )
    )


# ---------------------------------------------------------------- coverage
@dataclass(frozen=True, slots=True)
class CoverageReport:
    """Source -> claim traceability + resume/retry summary."""

    source_segments: int
    scenes: int
    characters: int
    places: int
    items: int
    organizations: int
    events: int
    claims: int
    resumed_from_cache: bool
    retried: int
    source_to_claim_traceable: bool

    def summary(self) -> dict[str, object]:
        return {
            "source_segments": self.source_segments,
            "scenes": self.scenes,
            "characters": self.characters,
            "places": self.places,
            "items": self.items,
            "organizations": self.organizations,
            "events": self.events,
            "claims": self.claims,
            "resumed_from_cache": self.resumed_from_cache,
            "retried": self.retried,
            "source_to_claim_traceable": self.source_to_claim_traceable,
        }

    def to_hash(self) -> str:
        return hashlib.sha256(
            json.dumps(self.summary(), sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
