"""Unified Abstraction Ladder (G33A).

Candidate promotion moves one level at a time from L0 (event) to L8 (platform
improvement). L0-L3 may be more automatic; L7-L8 always require explicit
approval. Every level has minimum evidence / stability / cross-scenario /
approval requirements defined by a versioned promotion policy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from wanxiang_domain.errors import PermissionDenied

PromotionLevel = Literal["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8"]

PROMOTION_LEVELS: tuple[str, ...] = (
    "L0",
    "L1",
    "L2",
    "L3",
    "L4",
    "L5",
    "L6",
    "L7",
    "L8",
)

# Levels that always require explicit approval.
APPROVAL_LEVELS: tuple[str, ...] = ("L7", "L8")


@dataclass(frozen=True, slots=True)
class LevelRequirement:
    """Minimum requirements to promote INTO a level."""

    level: PromotionLevel
    min_evidence: int
    min_stability: float
    cross_scenario: bool
    approval_required: bool


@dataclass(frozen=True, slots=True)
class PromotionPolicy:
    """Versioned promotion policy (L0..L8 requirements)."""

    version: int = 1
    requirements: tuple[LevelRequirement, ...] = (
        LevelRequirement("L0", 0, 0.0, False, False),
        LevelRequirement("L1", 1, 0.3, False, False),
        LevelRequirement("L2", 2, 0.5, False, False),
        LevelRequirement("L3", 3, 0.6, False, False),
        LevelRequirement("L4", 4, 0.7, True, False),
        LevelRequirement("L5", 5, 0.8, True, False),
        LevelRequirement("L6", 6, 0.85, True, False),
        LevelRequirement("L7", 8, 0.9, True, True),
        LevelRequirement("L8", 10, 0.95, True, True),
    )

    def requirement(self, level: PromotionLevel) -> LevelRequirement:
        for req in self.requirements:
            if req.level == level:
                return req
        raise ValueError(f"unknown promotion level {level!r}")


@dataclass(frozen=True, slots=True)
class PromotionEvidence:
    """Evidence provided for a promotion step."""

    current_level: PromotionLevel
    target_level: PromotionLevel
    evidence_count: int
    stability: float
    cross_scenario: bool
    approved: bool = False


def validate_promotion(evidence: PromotionEvidence, policy: PromotionPolicy | None = None) -> None:
    """Validate one promotion step (no level skipping; L7-L8 need approval)."""
    policy = policy or PromotionPolicy()
    current_index = PROMOTION_LEVELS.index(evidence.current_level)
    target_index = PROMOTION_LEVELS.index(evidence.target_level)
    if target_index != current_index + 1:
        raise PermissionDenied(
            f"level-skipping promotion rejected: "
            f"{evidence.current_level} -> {evidence.target_level} "
            f"(must advance one level at a time)"
        )
    req = policy.requirement(evidence.target_level)
    if evidence.evidence_count < req.min_evidence:
        raise PermissionDenied(
            f"insufficient evidence for {evidence.target_level}: "
            f"{evidence.evidence_count} < {req.min_evidence}"
        )
    if evidence.stability < req.min_stability:
        raise PermissionDenied(
            f"insufficient stability for {evidence.target_level}: "
            f"{evidence.stability} < {req.min_stability}"
        )
    if req.cross_scenario and not evidence.cross_scenario:
        raise PermissionDenied(f"{evidence.target_level} requires cross-scenario evidence")
    if req.approval_required and not evidence.approved:
        raise PermissionDenied(f"{evidence.target_level} requires explicit approval")
