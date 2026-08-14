"""Ontology / Law multi-scale evolution (G32F).

Ontology and Law candidates are validated against the World Constitution
(which decides which layers are mutable) and against policy (LawCandidate
permissions/scope must never escalate to platform authority). Branch-local
ontology/law commits never pollute the parent worldline.
"""

from __future__ import annotations

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

    def __post_init__(self) -> None:
        if self.stability < 0 or self.stability > 1:
            raise ValueError("stability must be in [0,1]")
        if self.complexity < 0 or self.complexity > 1:
            raise ValueError("complexity must be in [0,1]")


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
