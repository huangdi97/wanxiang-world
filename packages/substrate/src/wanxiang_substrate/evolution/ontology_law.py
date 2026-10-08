"""Ontology / Law multi-scale evolution (G32F).

Ontology and Law candidates are validated against the World Constitution
(which decides which layers are mutable) and against policy (LawCandidate
permissions/scope must never escalate to platform authority). Branch-local
ontology/law commits never pollute the parent worldline.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from wanxiang_domain.constitution import ConstitutionManifest
from wanxiang_domain.errors import PermissionDenied

FORBIDDEN_LAW_PERMISSIONS = ("commit_authority", "platform", "reality_root")


@dataclass(frozen=True, slots=True)
class OntologyCandidate:
    """An ontology (semantic space) change candidate."""

    candidate_id: str
    concept: str
    scope: str = "world"
    stability: float = 1.0
    complexity: float = 0.2
    interpretability: float = 1.0
    evidence_refs: tuple[str, ...] = ()
    evidence_windows: tuple[tuple[int, int], ...] = ()
    norm_refs: tuple[str, ...] = ()
    institution_refs: tuple[str, ...] = ()
    provenance_refs: tuple[str, ...] = ()
    approved: bool = False
    reviewed_by: str | None = None

    def __post_init__(self) -> None:
        for name, value in (
            ("stability", self.stability),
            ("complexity", self.complexity),
            ("interpretability", self.interpretability),
        ):
            if not math.isfinite(value) or not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0,1]")
        for name, refs in (
            ("evidence", self.evidence_refs),
            ("norm", self.norm_refs),
            ("institution", self.institution_refs),
            ("provenance", self.provenance_refs),
        ):
            if len(set(refs)) != len(refs) or any(not ref.strip() for ref in refs):
                raise ValueError(f"ontology {name} refs must be unique and non-empty")
        for start, end in self.evidence_windows:
            if isinstance(start, bool) or isinstance(end, bool) or start < 0 or end <= start:
                raise ValueError("ontology evidence windows must be non-empty")
        if len(set(self.evidence_windows)) != len(self.evidence_windows):
            raise ValueError("ontology evidence windows must be unique")
        if self.reviewed_by is not None and not self.reviewed_by.strip():
            raise ValueError("ontology reviewer must be non-empty")

    def to_dict(self) -> dict[str, object]:
        """Expose candidate evidence without turning it into world truth."""
        return {
            "candidate_id": self.candidate_id,
            "concept": self.concept,
            "scope": self.scope,
            "stability": self.stability,
            "complexity": self.complexity,
            "interpretability": self.interpretability,
            "evidence_refs": list(self.evidence_refs),
            "evidence_windows": [list(window) for window in self.evidence_windows],
            "norm_refs": list(self.norm_refs),
            "institution_refs": list(self.institution_refs),
            "provenance_refs": list(self.provenance_refs),
            "approved": self.approved,
            "reviewed_by": self.reviewed_by,
        }


@dataclass(frozen=True, slots=True)
class LawCandidate:
    """A law (rule set) change candidate with permission + scope."""

    candidate_id: str
    rule: str
    permission: str = "world"
    scope: str = "world"

    def __post_init__(self) -> None:
        if not self.rule:
            raise ValueError("law candidate requires a rule")


class OntologyLawEvolution:
    """Validates ontology/law candidates against a constitution and policy."""

    @staticmethod
    def validate_ontology(candidate: OntologyCandidate, constitution: ConstitutionManifest) -> bool:
        """Ontology evolution requires the ontology layer to be mutable."""
        if candidate.evidence_refs and (not candidate.approved or not candidate.reviewed_by):
            raise PermissionDenied("evidence-backed ontology candidate requires explicit review")
        if "ontology" not in constitution.mutable_law_layers:
            raise PermissionDenied(
                "constitution does not allow ontology evolution (immutable layer)"
            )
        if candidate.scope == "root":
            raise PermissionDenied("root ontology rules are immutable")
        return True

    @staticmethod
    def validate_law(candidate: LawCandidate, constitution: ConstitutionManifest) -> bool:
        """Law evolution requires the law layer to be mutable and never escalates."""
        if "law" not in constitution.mutable_law_layers:
            raise PermissionDenied("constitution does not allow law evolution (immutable layer)")
        if candidate.permission in FORBIDDEN_LAW_PERMISSIONS:
            raise PermissionDenied(
                f"law candidate permission {candidate.permission!r} is forbidden"
            )
        if candidate.scope == "platform":
            raise PermissionDenied("a world law cannot target the platform scope")
        return True
