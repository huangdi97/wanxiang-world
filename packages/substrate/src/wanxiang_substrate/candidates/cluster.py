"""Candidate clustering: merge/split suggestions (G57H).

Suggestions are reversible PROPOSALS: nothing is merged or split destructively.
A decision log records approve/reject reversibly so clustering can be undone.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import ContractError

from wanxiang_substrate.candidates.envelope import CandidateEnvelope

SuggestionKind = Literal["merge", "split"]
VALID_SUGGESTION_KINDS = ("merge", "split")
DecisionKind = Literal["approve", "reject"]
VALID_DECISION_KINDS = ("approve", "reject")


@dataclass(frozen=True, slots=True)
class ClusterSuggestion:
    """A reversible merge/split proposal (never a mutation)."""

    suggestion_id: str
    kind: SuggestionKind
    candidate_ids: tuple[str, ...]
    basis: str
    reversible: bool = True

    def __post_init__(self) -> None:
        if not self.suggestion_id:
            raise ContractError("suggestion requires an id")
        if self.kind not in VALID_SUGGESTION_KINDS:
            raise ContractError(f"invalid suggestion kind {self.kind!r}")
        if len(self.candidate_ids) < 2 and self.kind == "merge":
            raise ContractError("merge suggestion requires >= 2 candidates")
        if self.reversible is not True:
            raise ContractError("suggestions must be reversible")


@dataclass(frozen=True, slots=True)
class ClusterDecision:
    """A reversible review decision on a clustering suggestion."""

    decision_id: str
    suggestion_id: str
    decision: DecisionKind
    reviewer: str
    rationale: str

    def __post_init__(self) -> None:
        if not self.decision_id or not self.suggestion_id or not self.reviewer:
            raise ContractError("decision requires ids and reviewer")
        if self.decision not in VALID_DECISION_KINDS:
            raise ContractError(f"invalid decision {self.decision!r}")
        if not self.rationale:
            raise ContractError("decision requires a rationale")


class CandidateClusterer:
    """Suggests reversible merges/splits; logs reversible decisions."""

    def __init__(self) -> None:
        self._decisions: dict[str, ClusterDecision] = {}

    def suggest_merges(
        self,
        candidates: tuple[CandidateEnvelope, ...],
    ) -> tuple[ClusterSuggestion, ...]:
        """Merge candidates sharing the same identity key (same kind + key)."""
        groups: dict[str, list[CandidateEnvelope]] = {}
        for candidate in candidates:
            key = dict(candidate.payload).get("identity_key") or dict(candidate.payload).get("key")
            if key:
                groups.setdefault(f"{candidate.kind}:{key}", []).append(candidate)
        suggestions: list[ClusterSuggestion] = []
        for group_key, group in sorted(groups.items()):
            ids = tuple(c.candidate_id for c in sorted(group, key=lambda c: c.candidate_id))
            if len(ids) > 1:
                suggestions.append(
                    ClusterSuggestion(
                        suggestion_id=_digest(f"merge:{group_key}"),
                        kind="merge",
                        candidate_ids=ids,
                        basis=f"shared {group_key}",
                    )
                )
        return tuple(suggestions)

    def suggest_splits(
        self,
        candidates: tuple[CandidateEnvelope, ...],
    ) -> tuple[ClusterSuggestion, ...]:
        """Split candidates carrying conflicting values for the same field."""
        suggestions: list[ClusterSuggestion] = []
        for candidate in candidates:
            fields = dict(candidate.payload)
            for key in ("display_name", "name"):
                if key not in fields:
                    continue
                parts = [part for part in fields[key].split("|") if part]
                if len(parts) > 1:
                    suggestions.append(
                        ClusterSuggestion(
                            suggestion_id=_digest(f"split:{candidate.candidate_id}:{key}"),
                            kind="split",
                            candidate_ids=(candidate.candidate_id,),
                            basis=f"conflicting {key} values",
                        )
                    )
        return tuple(suggestions)

    def decide(self, decision: ClusterDecision) -> None:
        if decision.suggestion_id not in self._decisions:
            self._decisions[decision.suggestion_id] = decision
        # Re-deciding the same suggestion overwrites (reversible), appending a
        # new decision is disallowed to keep the log unambiguous.
        self._decisions[decision.suggestion_id] = decision

    def decision_for(self, suggestion_id: str) -> ClusterDecision | None:
        return self._decisions.get(suggestion_id)


def _digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
