"""Source-derived identity & alias distillation (G35C).

M32: turn approved source text into character identity CANDIDATES with
evidence-backed alias claims. Candidates are never Canon: a human/rule review
gate must approve each candidate (every alias needs a resolvable source
locator) before it may enter Canon compilation (G35E). Reuses G35B
SourceLocator/segment_source/source_slice and the G04B ClaimCandidate/
EvidenceLink claim model; introduces no second state/registry/engine.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.sources.evidence import AUTHORIZED_REVIEWERS, evidence_ok
from wanxiang_substrate.sources.locator import (
    SourceLocator,
    segment_source,
    source_slice,
)
from wanxiang_substrate.sources.model import ClaimCandidate, EvidenceLink

IdentityStatus = Literal["pending", "eligible", "rejected"]
VALID_IDENTITY_STATUSES = ("pending", "eligible", "rejected")


@dataclass(frozen=True, slots=True)
class AliasClaim:
    """One alias of an identity, backed by evidence locators (G35C)."""

    alias: str
    identity_key: str
    locators: tuple[SourceLocator, ...]
    role: Literal["alias"] = "alias"
    reviewed: bool = False

    def __post_init__(self) -> None:
        if not self.alias or not self.identity_key:
            raise ContractError("alias claim requires alias and identity_key")
        if self.role != "alias":
            raise ContractError(f"invalid alias role {self.role!r}")
        if not self.locators:
            raise ContractError("alias claim requires at least one evidence locator")

    @property
    def has_evidence(self) -> bool:
        return bool(self.locators)


@dataclass(frozen=True, slots=True)
class IdentityCandidate:
    """A distilled identity candidate; never Canon until review approves."""

    candidate_id: str
    identity_key: str
    display_name: str
    aliases: tuple[AliasClaim, ...]
    provenance: tuple[str, ...] = ()
    status: IdentityStatus = "pending"

    def __post_init__(self) -> None:
        if not self.candidate_id or not self.identity_key or not self.display_name:
            raise ContractError("identity candidate requires id, key and display name")
        if self.status not in VALID_IDENTITY_STATUSES:
            raise ContractError(f"invalid identity status {self.status!r}")

    @property
    def all_aliases_have_evidence(self) -> bool:
        return bool(self.aliases) and all(claim.has_evidence for claim in self.aliases)

    def with_status(self, status: IdentityStatus) -> IdentityCandidate:
        return IdentityCandidate(
            candidate_id=self.candidate_id,
            identity_key=self.identity_key,
            display_name=self.display_name,
            aliases=self.aliases,
            provenance=self.provenance,
            status=status,
        )


@dataclass(frozen=True, slots=True)
class IdentityReviewDecision:
    candidate_id: str
    approved: bool
    reason: str
    reviewer: str

    def __post_init__(self) -> None:
        if not self.reason:
            raise ContractError("review decision requires a reason")


class IdentityDistiller:
    """Deterministic identity/alias distillation from approved source text.

    The distiller is pure: it only reads the source text and produces
    candidates. Source eligibility (rights/stage/injection) is enforced by the
    existing SourceGate before this class is used; no write path exists here.
    """

    def __init__(
        self,
        *,
        extract_mentions: Callable[[str], tuple[str, ...]],
        resolve_identity: Callable[[str], str | None],
    ) -> None:
        self._extract_mentions = extract_mentions
        self._resolve_identity = resolve_identity

    def distill(self, source_id: str, text: str) -> tuple[IdentityCandidate, ...]:
        """Distill identity candidates; re-running on same text is identical."""
        by_identity: dict[str, dict[str, set[SourceLocator]]] = {}
        for locator in segment_source(source_id, text):
            for mention in self._extract_mentions(source_slice(text, locator)):
                identity_key = self._resolve_identity(mention)
                if identity_key is None:
                    continue  # mention does not resolve to a known identity
                by_identity.setdefault(identity_key, {}).setdefault(mention, set()).add(locator)
        candidates: list[IdentityCandidate] = []
        for index, (identity_key, alias_map) in enumerate(sorted(by_identity.items()), start=1):
            aliases = tuple(
                AliasClaim(
                    alias=alias,
                    identity_key=identity_key,
                    locators=tuple(sorted(locators, key=lambda loc: loc.locator)),
                )
                for alias, locators in sorted(alias_map.items())
            )
            all_locators = tuple(
                sorted(
                    (loc for claim in aliases for loc in claim.locators),
                    key=lambda loc: loc.locator,
                )
            )
            provenance = (source_id,) + tuple(loc.locator for loc in all_locators)
            candidates.append(
                IdentityCandidate(
                    candidate_id=f"ident_{index:04d}",
                    identity_key=identity_key,
                    display_name=identity_key,
                    aliases=aliases,
                    provenance=provenance,
                )
            )
        return tuple(candidates)


class IdentityReviewGate:
    """Human/rule review gate: only evidence-backed candidates become eligible."""

    def __init__(self, *, min_evidence_locators: int = 1) -> None:
        if min_evidence_locators < 1:
            raise ValueError("min_evidence_locators must be >= 1")
        self._min_evidence_locators = min_evidence_locators

    def review(
        self,
        candidate: IdentityCandidate,
        *,
        source_text: str,
        reviewer: str,
    ) -> IdentityReviewDecision:
        if reviewer not in AUTHORIZED_REVIEWERS:
            return IdentityReviewDecision(
                candidate.candidate_id,
                False,
                f"reviewer {reviewer!r} is not authorized",
                reviewer,
            )
        ok, reason = evidence_ok(
            locators_per_claim=tuple(claim.locators for claim in candidate.aliases),
            source_text=source_text,
            min_evidence_locators=self._min_evidence_locators,
        )
        if not ok:
            return IdentityReviewDecision(candidate.candidate_id, False, reason, reviewer)
        return IdentityReviewDecision(
            candidate.candidate_id,
            True,
            "evidence-backed identity approved",
            reviewer,
        )


def identity_to_claim(candidate: IdentityCandidate) -> ClaimCandidate:
    """Convert an approved identity candidate into the shared claim model.

    Every alias evidence locator becomes a supporting EvidenceLink so the
    existing claim pipeline (G04D completion ledger / G35E canon compilation)
    can consume identity candidates without a second claim abstraction.
    """
    links = tuple(
        EvidenceLink(
            claim_id=candidate.identity_key,
            source_id=locator.source_id,
            role="supports",
            weight=1.0,
        )
        for claim in candidate.aliases
        for locator in claim.locators
    )
    source_ids = tuple(
        sorted({locator.source_id for claim in candidate.aliases for locator in claim.locators})
    )
    return ClaimCandidate(
        claim_id=f"identity:{candidate.candidate_id}",
        proposition=(
            f"identity:{candidate.identity_key} has aliases "
            + ", ".join(claim.alias for claim in candidate.aliases)
        ),
        source_ids=source_ids,
        status="eligible" if candidate.status == "eligible" else "pending",
        evidence_links=links,
    )
