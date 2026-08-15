"""Timeline + Canon graph records (M36, split for file-size budget)."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from wanxiang_substrate.sources.locator import SourceLocator

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
