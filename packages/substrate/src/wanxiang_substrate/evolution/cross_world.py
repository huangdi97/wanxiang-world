"""Cross-world distillation (G33D).

Forms Domain/Runtime candidates from MULTIPLE authorized world histories. It
reads only the authorized cross-world dataset (opt-in consent + rights/retention
per G32G), discovers patterns across worlds as candidates, preserves world
origins (anonymized: world-level only, never actor identity), and never lets a
candidate activate directly ? activation requires explicit approval.
"""

from __future__ import annotations

from dataclasses import dataclass

from wanxiang_domain.errors import PermissionDenied

from wanxiang_substrate.evolution.telemetry import CrossWorldDataset


@dataclass(frozen=True, slots=True)
class CrossWorldCandidate:
    """A cross-world pattern candidate (never auto-activated)."""

    candidate_id: str
    pattern: str
    world_origins: tuple[str, ...]
    window_coverage: int
    threshold: int
    approved: bool = False

    @property
    def meets_threshold(self) -> bool:
        return self.window_coverage >= self.threshold


class CrossWorldDistiller:
    """Cross-world pattern discovery over authorized telemetry only."""

    def __init__(self, dataset: CrossWorldDataset, threshold: int = 2) -> None:
        if threshold < 1:
            raise ValueError("threshold must be >= 1")
        self._dataset = dataset
        self._threshold = threshold
        self._next = 0

    def distill(self) -> tuple[CrossWorldCandidate, ...]:
        """Discover patterns across worlds; only authorized entries are visible."""
        by_pattern: dict[str, set[str]] = {}
        for envelope in self._dataset.entries():
            # Only telemetry kinds carrying cross-world signal are considered;
            # trajectories are excluded from cross-world candidates (privacy).
            if envelope.kind == "trajectory":
                continue
            by_pattern.setdefault(envelope.metric, set()).add(envelope.world_ref)
        candidates: list[CrossWorldCandidate] = []
        for pattern, worlds in sorted(by_pattern.items()):
            if len(worlds) < self._threshold:
                continue
            self._next += 1
            candidates.append(
                CrossWorldCandidate(
                    candidate_id=f"cand_xw_{self._next}",
                    pattern=pattern,
                    world_origins=tuple(sorted(worlds)),
                    window_coverage=len(worlds),
                    threshold=self._threshold,
                )
            )
        return tuple(candidates)

    def activate(self, candidate: CrossWorldCandidate, approver: str = "") -> None:
        """Candidates never activate directly; explicit approval required."""
        if not candidate.meets_threshold:
            raise PermissionDenied("candidate below threshold; cannot activate")
        if not candidate.approved or approver not in ("reviewer", "policy"):
            raise PermissionDenied("cross-world candidate requires explicit approval to activate")
