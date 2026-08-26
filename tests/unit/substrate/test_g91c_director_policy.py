"""G91C: director modes are explicit proposal policies, not authority."""

from __future__ import annotations

from wanxiang_substrate.reality.director import DirectorPolicy, DirectorProposal


def test_modes_have_explicit_proposal_contracts() -> None:
    canon = DirectorPolicy.for_mode("CANON")
    living = DirectorPolicy.for_mode("LIVING")
    experiment = DirectorPolicy.for_mode("EXPERIMENT")
    assert canon.allows("canon_attractor")
    assert not canon.allows("intervention")
    assert living.can_emit("relationship")
    assert experiment.can_emit("intervention")
    assert set(canon.allowed_proposal_types) != set(living.allowed_proposal_types)


def test_policy_evaluates_proposals_and_emits_audit_only() -> None:
    policy = DirectorPolicy.for_mode("CANON")
    allowed = policy.evaluate(DirectorProposal("p1", "world", "opportunity"), at_ticks=4)
    rejected = policy.evaluate(DirectorProposal("p2", "world", "intervention"), at_ticks=4)
    assert allowed.allowed is True
    assert rejected.allowed is False
    assert rejected.audit.event_type == "proposal_evaluated"
    assert not hasattr(policy, "commit")


def test_mode_transition_is_immutable_and_auditable() -> None:
    original = DirectorPolicy.for_mode("DIRECTED", policy_version=3)
    transition = original.transition("EXPERIMENT", at_ticks=9, reason="controlled trial")
    assert original.mode == "DIRECTED"
    assert transition.policy.mode == "EXPERIMENT"
    assert transition.policy.policy_version == 3
    assert transition.audit.previous_mode == "DIRECTED"
    assert transition.audit.next_mode == "EXPERIMENT"
    assert transition.audit.event_type == "mode_transition"
