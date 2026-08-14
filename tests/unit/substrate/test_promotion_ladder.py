"""G33A: unified abstraction ladder (L0-L8 promotion)."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import PermissionDenied
from wanxiang_substrate.evolution.promotion import (
    APPROVAL_LEVELS,
    PROMOTION_LEVELS,
    PromotionEvidence,
    PromotionPolicy,
    validate_promotion,
)


@pytest.mark.unit
def test_level_skipping_is_rejected() -> None:
    with pytest.raises(PermissionDenied):
        validate_promotion(
            PromotionEvidence(
                current_level="L0",
                target_level="L2",
                evidence_count=10,
                stability=1.0,
                cross_scenario=True,
            )
        )
    # One step at a time is allowed when evidence suffices.
    validate_promotion(
        PromotionEvidence(
            current_level="L0",
            target_level="L1",
            evidence_count=1,
            stability=0.5,
            cross_scenario=False,
        )
    )


@pytest.mark.unit
def test_l7_l8_require_explicit_approval() -> None:
    assert APPROVAL_LEVELS == ("L7", "L8")
    with pytest.raises(PermissionDenied):
        validate_promotion(
            PromotionEvidence(
                current_level="L6",
                target_level="L7",
                evidence_count=8,
                stability=0.95,
                cross_scenario=True,
                approved=False,
            )
        )
    # With explicit approval the step passes.
    validate_promotion(
        PromotionEvidence(
            current_level="L6",
            target_level="L7",
            evidence_count=8,
            stability=0.95,
            cross_scenario=True,
            approved=True,
        )
    )


@pytest.mark.unit
def test_evidence_and_stability_requirements_enforced() -> None:
    with pytest.raises(PermissionDenied):
        validate_promotion(
            PromotionEvidence(
                current_level="L0",
                target_level="L1",
                evidence_count=0,
                stability=0.5,
                cross_scenario=False,
            )
        )
    with pytest.raises(PermissionDenied):
        validate_promotion(
            PromotionEvidence(
                current_level="L3",
                target_level="L4",
                evidence_count=4,
                stability=0.75,
                cross_scenario=False,
            )
        )


@pytest.mark.unit
def test_policy_is_versioned() -> None:
    p1 = PromotionPolicy(version=1)
    p2 = PromotionPolicy(version=2)
    assert p1.version == 1 and p2.version == 2
    assert PROMOTION_LEVELS == ("L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8")
