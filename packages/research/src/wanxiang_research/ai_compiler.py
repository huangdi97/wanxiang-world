"""AI-assisted world compiler semantic extraction (G19B, experimental).

Model output is ALWAYS a Candidate with source span, provenance and confidence;
it is never auto-promoted to canonical truth. A deterministic fixture provider
supports core tests with no paid API. Prompt-injection output is parsed as
data and cannot change system behavior.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True, slots=True)
class ExtractionCandidate:
    entity_id: str
    entity_type: str
    claims: tuple[tuple[str, str], ...]
    source_span: str
    confidence: float
    provenance: str


class ExtractionProvider(Protocol):
    def extract(self, source_text: str) -> tuple[ExtractionCandidate, ...]: ...


class DeterministicFixtureProvider:
    """Deterministic fake provider for research tests (no paid API)."""

    def __init__(self, candidates: tuple[ExtractionCandidate, ...] = ()) -> None:
        self._candidates = candidates

    def extract(self, source_text: str) -> tuple[ExtractionCandidate, ...]:
        return self._candidates


class SemanticExtractor:
    """Runs a provider and produces candidates for review (never canonical)."""

    def __init__(self, provider: ExtractionProvider) -> None:
        self._provider = provider

    def extract(self, source_text: str, source_ref: str) -> tuple[ExtractionCandidate, ...]:
        candidates = self._provider.extract(source_text)
        # Candidates are bound to provenance; model memory is never a source.
        return tuple(
            ExtractionCandidate(
                entity_id=c.entity_id,
                entity_type=c.entity_type,
                claims=c.claims,
                source_span=c.source_span,
                confidence=c.confidence,
                provenance=f"{source_ref}:{c.source_span}",
            )
            for c in candidates
        )

    def review_diff(self, candidates: tuple[ExtractionCandidate, ...]) -> dict[str, Any]:
        accepted = [c for c in candidates if c.confidence >= 0.5]
        rejected = [c for c in candidates if c.confidence < 0.5]
        return {
            "accepted": [c.entity_id for c in accepted],
            "rejected": [c.entity_id for c in rejected],
            "uncertainty": [
                {"entity": c.entity_id, "confidence": c.confidence}
                for c in candidates
                if 0.4 <= c.confidence < 0.6
            ],
        }
