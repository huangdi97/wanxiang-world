"""Domain recommender (G59B).

Deterministic, explainable recommendation from source/candidate features:
each recommendation carries a score and the concrete features that drove it.
No model required; providers can be plugged in later behind the same surface.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_substrate.candidates.envelope import CandidateEnvelope
from wanxiang_substrate.domains.capability import DomainCapability, DomainRegistry


@dataclass(frozen=True, slots=True)
class Recommendation:
    domain_id: str
    score: float
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not self.domain_id:
            raise ContractError("recommendation requires a domain id")
        if not (0.0 <= self.score <= 1.0):
            raise ContractError("score must be within [0,1]")


from wanxiang_domain.errors import ContractError  # noqa: E402


class DomainRecommender:
    """Feature-driven domain recommendation (explainable, deterministic)."""

    def recommend(
        self,
        registry: DomainRegistry,
        *,
        source_kind: str,
        candidates: tuple[CandidateEnvelope, ...],
    ) -> tuple[Recommendation, ...]:
        features = self._features(source_kind, candidates)
        recommendations: list[Recommendation] = []
        for domain in registry.all():
            score, reasons = self._score(domain, features)
            if score > 0.0:
                recommendations.append(Recommendation(domain.domain_id, score, tuple(reasons)))
        return tuple(sorted(recommendations, key=lambda r: (-r.score, r.domain_id)))

    def _features(
        self,
        source_kind: str,
        candidates: tuple[CandidateEnvelope, ...],
    ) -> set[str]:
        kinds = {c.kind for c in candidates}
        payloads = " ".join(" ".join(c.fields.values()) for c in candidates).lower()
        features: set[str] = set()
        if source_kind == "gedcom":
            features.add("family")
        if "identity" in kinds and "relation" in kinds:
            features.add("social")
        if "event" in kinds and "time" in kinds:
            features.add("temporal")
        if "place" in kinds:
            features.add("spatial")
        if "organization" in kinds or "role" in kinds:
            features.add("institutional")
        if any(word in payloads for word in ("rule", "norm", "ritual", "礼")):
            features.add("norms")
        if any(word in payloads for word in ("secret", "believe", "knows")):
            features.add("epistemic")
        return features

    def _score(
        self,
        domain: DomainCapability,
        features: set[str],
    ) -> tuple[float, tuple[str, ...]]:
        reasons: list[str] = []
        score = 0.0
        for provided in domain.provides:
            key = provided.lower()
            if key in ("family", "genealogy") and "family" in features:
                score += 0.4
                reasons.append("family source features")
            if key in ("social", "relation") and "social" in features:
                score += 0.3
                reasons.append("identity+relation candidates")
            if key in ("temporal", "timeline") and "temporal" in features:
                score += 0.3
                reasons.append("event+time candidates")
            if key in ("spatial", "place", "topology") and "spatial" in features:
                score += 0.2
                reasons.append("place candidates")
            if key in ("institution", "organization") and "institutional" in features:
                score += 0.2
                reasons.append("organization/role candidates")
            if key in ("norm", "rule", "ritual") and "norms" in features:
                score += 0.2
                reasons.append("norm/rule markers")
            if key in ("epistemic", "knowledge") and "epistemic" in features:
                score += 0.2
                reasons.append("secret/belief markers")
        return min(score, 1.0), tuple(reasons)
