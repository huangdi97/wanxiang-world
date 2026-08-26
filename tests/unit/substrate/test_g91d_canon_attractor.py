"""G91D: canon guidance measures and recommends without forcing choice."""

from __future__ import annotations

from wanxiang_substrate.reality.canon_attractor import (
    CanonAttractorPolicy,
    CanonConstraint,
)


def test_soft_and_hard_constraints_produce_distance_metrics() -> None:
    policy = CanonAttractorPolicy(
        (
            CanonConstraint("soft_duty", "duty", 0.8, tolerance=0.1, weight=0.5),
            CanonConstraint("hard_place", "place", 1.0, kind="hard", tolerance=0.0),
        ),
        major_divergence_threshold=0.6,
    )
    distance = policy.measure({"duty": 0.4, "place": 0.0})
    assert set(distance.metrics) == {"soft_duty", "hard_place"}
    assert distance.soft_violations == ("soft_duty",)
    assert distance.hard_violations == ("hard_place",)
    assert distance.major is True


def test_major_divergence_recommends_branch_but_preserves_choice() -> None:
    policy = CanonAttractorPolicy((CanonConstraint("hard_duty", "duty", 1.0, kind="hard"),))
    assessment = policy.assess("choice:leave", {"duty": 0.0}, at_ticks=7)
    assert assessment.branch_recommended is True
    assert assessment.proposal.recommendation == "fork_worldline"
    assert assessment.choice_ref == "choice:leave"
    assert assessment.proposal.observed_choice == "choice:leave"
    assert assessment.choice_preserved is True
    assert not hasattr(policy, "commit")


def test_small_divergence_stays_on_worldline_without_rewriting_choice() -> None:
    policy = CanonAttractorPolicy((CanonConstraint("soft_duty", "duty", 0.8, tolerance=0.3),))
    assessment = policy.assess("choice:help", {"duty": 0.7}, at_ticks=2)
    assert assessment.branch_recommended is False
    assert assessment.proposal.recommendation == "continue_worldline"
    assert assessment.proposal.free_will_preserved is True
