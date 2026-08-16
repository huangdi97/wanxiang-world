"""Candidate <-> evidence binding (G58A).

Bidirectional tracking: candidate -> source locators/evidence links, and
evidence -> candidates (reverse index). Supports and contradicts are both
preserved; no last-write-wins anywhere.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.parsing.segment import StableLocator

EvidenceRole = Literal["supports", "contradicts"]
VALID_ROLES = ("supports", "contradicts")


@dataclass(frozen=True, slots=True)
class EvidenceLink:
    """One evidence edge between a candidate and a source locator."""

    link_id: str
    candidate_id: str
    locator: StableLocator
    role: EvidenceRole
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not self.link_id or not self.candidate_id:
            raise ContractError("evidence link requires ids")
        if self.role not in VALID_ROLES:
            raise ContractError(f"invalid evidence role {self.role!r}")
        if not (0.0 <= self.weight <= 1.0):
            raise ContractError("weight must be within [0,1]")


class EvidenceBindings:
    """Bidirectional candidate<->evidence index (append-only)."""

    def __init__(self) -> None:
        self._links: dict[str, EvidenceLink] = {}
        self._by_candidate: dict[str, tuple[EvidenceLink, ...]] = {}
        self._by_locator: dict[str, tuple[EvidenceLink, ...]] = {}

    def add(self, link: EvidenceLink) -> EvidenceLink:
        if link.link_id in self._links:
            return self._links[link.link_id]  # idempotent
        self._links[link.link_id] = link
        self._by_candidate[link.candidate_id] = self._by_candidate.get(link.candidate_id, ()) + (
            link,
        )
        key = link.locator.to_string()
        self._by_locator[key] = self._by_locator.get(key, ()) + (link,)
        return link

    def links_for_candidate(self, candidate_id: str) -> tuple[EvidenceLink, ...]:
        return self._by_candidate.get(candidate_id, ())

    def candidates_for_locator(self, locator: StableLocator) -> tuple[str, ...]:
        return tuple(link.candidate_id for link in self._by_locator.get(locator.to_string(), ()))

    def supporting(self, candidate_id: str) -> tuple[EvidenceLink, ...]:
        return tuple(
            link for link in self.links_for_candidate(candidate_id) if link.role == "supports"
        )

    def contradicting(self, candidate_id: str) -> tuple[EvidenceLink, ...]:
        return tuple(
            link for link in self.links_for_candidate(candidate_id) if link.role == "contradicts"
        )

    def all_links(self) -> tuple[EvidenceLink, ...]:
        return tuple(self._links.values())
