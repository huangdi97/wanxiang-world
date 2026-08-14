"""Relation/Group social pattern distillation (G32D).

Repeated behavior history is distilled into relation/group/norm CANDIDATES ?
never directly into Canon. Windowed pattern detection with a policy-controlled
stability threshold; every candidate carries origin + provenance.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

PatternType = Literal["relation", "group", "norm"]


@dataclass(frozen=True, slots=True)
class BehaviorRecord:
    """One observed behavior in a window."""

    behavior: str
    actor_id: str
    window: int


@dataclass(frozen=True, slots=True)
class CandidateEnvelope:
    """A distillation candidate (never Canon until reviewed/promoted)."""

    candidate_id: str
    pattern_type: PatternType
    key: str
    observed_count: int
    windows_seen: int
    threshold: int
    origin_ref: str
    provenance: tuple[str, ...]

    @property
    def meets_threshold(self) -> bool:
        return self.windows_seen >= self.threshold


class SocialPatternDistiller:
    """Windowed pattern detection over repeated behavior history."""

    def __init__(self, threshold: int = 2) -> None:
        if threshold < 1:
            raise ValueError("threshold must be >= 1")
        self._threshold = threshold
        self._windows: dict[int, list[BehaviorRecord]] = {}
        self._next_candidate = 0

    def observe(self, record: BehaviorRecord) -> None:
        self._windows.setdefault(record.window, []).append(record)

    def observe_batch(self, records: list[BehaviorRecord]) -> None:
        for record in records:
            self.observe(record)

    def distill(self, threshold: int | None = None) -> tuple[CandidateEnvelope, ...]:
        """Detect patterns stable across windows; single behaviors never qualify."""
        threshold = threshold or self._threshold
        counts: dict[tuple[str, str], tuple[int, set[int]]] = {}
        for window, records in self._windows.items():
            seen_in_window: set[tuple[str, str]] = set()
            for record in records:
                key = (record.behavior, record.actor_id)
                if key in seen_in_window:
                    continue  # count a pattern once per window
                seen_in_window.add(key)
                entry = counts.setdefault(key, (0, set()))
                counts[key] = (entry[0] + 1, entry[1] | {window})
        candidates: list[CandidateEnvelope] = []
        for (behavior, actor), (total, windows_seen) in sorted(counts.items()):
            pattern_type: PatternType
            if behavior.startswith("norm:"):
                pattern_type = "norm"
            elif behavior.startswith("group:"):
                pattern_type = "group"
            else:
                pattern_type = "relation"
            self._next_candidate += 1
            envelope = CandidateEnvelope(
                candidate_id=f"cand_social_{self._next_candidate}",
                pattern_type=pattern_type,
                key=behavior,
                observed_count=total,
                windows_seen=len(windows_seen),
                threshold=threshold,
                origin_ref=f"distill://{actor}",
                provenance=tuple(sorted(f"win:{w}" for w in windows_seen)),
            )
            if envelope.meets_threshold:
                candidates.append(envelope)
        return tuple(candidates)
