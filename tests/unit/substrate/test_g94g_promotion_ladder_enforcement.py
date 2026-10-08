"""G94G: higher ladder levels require evidence, worlds, sandbox, and rollback."""

from __future__ import annotations

import pytest
from wanxiang_domain.errors import PermissionDenied
from wanxiang_substrate.evolution.platform_feedback import PlatformFeedbackLab
from wanxiang_substrate.evolution.promotion import (
    PromotionEvidence,
    PromotionLevel,
    PromotionPolicy,
    validate_promotion,
)


@pytest.mark.unit
def test_m91_l0_to_l5_require_increasing_evidence_and_worlds() -> None:
    policy = PromotionPolicy()
    levels: tuple[PromotionLevel, ...] = ("L0", "L1", "L2", "L3", "L4", "L5")
    requirements = [policy.requirement(level) for level in levels]
    assert [item.min_evidence for item in requirements] == [0, 1, 2, 3, 4, 5]
    assert [item.min_worlds for item in requirements] == [1, 1, 1, 1, 2, 3]
    assert requirements[4].sandbox_required is True
    assert requirements[5].rollback_required is True
    assert requirements[5].review_required is True

    validate_promotion(
        PromotionEvidence(
            current_level="L3",
            target_level="L4",
            evidence_count=4,
            stability=0.8,
            cross_scenario=True,
            world_count=2,
            benchmark_score=0.8,
            sandbox_passed=True,
        ),
        policy,
    )
    with pytest.raises(PermissionDenied, match="world evidence"):
        validate_promotion(
            PromotionEvidence(
                current_level="L4",
                target_level="L5",
                evidence_count=5,
                stability=0.9,
                cross_scenario=True,
                benchmark_score=0.95,
                sandbox_passed=True,
                rollback_ready=True,
                approved=True,
            ),
            policy,
        )


@pytest.mark.unit
def test_l5_requires_approved_sandbox_benchmark_and_rollback() -> None:
    policy = PromotionPolicy(version=7)
    lab = PlatformFeedbackLab()
    report = lab.run_sandbox(
        "ontology_g94g",
        {"quality": 0.95},
        invariants_ok=True,
        security_ok=True,
        cost=2.0,
        deterministic=True,
    )
    with pytest.raises(PermissionDenied, match="high-level review"):
        validate_promotion(
            PromotionEvidence(
                current_level="L4",
                target_level="L5",
                evidence_count=5,
                stability=0.9,
                cross_scenario=True,
                world_count=3,
                benchmark_score=0.95,
                sandbox_passed=True,
                rollback_ready=True,
                policy_version=7,
            ),
            policy,
        )
    approved = lab.approve(report, "platform_reviewer")
    release = lab.release(
        approved,
        kind="domain",
        name="ontology-candidate",
        version="1.0.0",
        release_id="release_g94g",
    )
    rolled_back = lab.rollback(release)
    validate_promotion(
        PromotionEvidence(
            current_level="L4",
            target_level="L5",
            evidence_count=5,
            stability=0.9,
            cross_scenario=True,
            approved=True,
            world_count=3,
            benchmark_score=approved.benchmark["quality"],
            sandbox_passed=approved.approved,
            rollback_ready=rolled_back.status == "rolled_back",
            policy_version=7,
        ),
        policy,
    )
    with pytest.raises(PermissionDenied, match="policy version"):
        validate_promotion(
            PromotionEvidence(
                current_level="L4",
                target_level="L5",
                evidence_count=5,
                stability=0.9,
                cross_scenario=True,
                approved=True,
                world_count=3,
                benchmark_score=0.95,
                sandbox_passed=True,
                rollback_ready=True,
                policy_version=6,
            ),
            policy,
        )
