"""G32D: relation/group social pattern distillation."""

from __future__ import annotations

import pytest
from wanxiang_substrate.evolution.distillation import (
    BehaviorRecord,
    CandidateEnvelope,
    SocialPatternDistiller,
)


@pytest.mark.unit
def test_single_behavior_cannot_upgrade_institution() -> None:
    distiller = SocialPatternDistiller(threshold=2)
    distiller.observe(BehaviorRecord(behavior="gift alice->bob", actor_id="alice", window=1))
    candidates = distiller.distill()
    assert candidates == ()  # a single window never forms a candidate


@pytest.mark.unit
def test_multi_window_stable_pattern_forms_candidate() -> None:
    distiller = SocialPatternDistiller(threshold=2)
    for window in (1, 2, 3):
        distiller.observe_batch(
            [
                BehaviorRecord("gift alice->bob", "alice", window),
                BehaviorRecord("visit alice->xiaoxiang", "alice", window),
            ]
        )
    candidates = distiller.distill()
    assert len(candidates) == 2
    by_key = {c.key: c for c in candidates}
    gift = by_key["gift alice->bob"]
    assert gift.pattern_type == "relation"
    assert gift.windows_seen == 3
    assert gift.meets_threshold
    assert gift.provenance == ("win:1", "win:2", "win:3")
    assert gift.origin_ref == "distill://alice"


@pytest.mark.unit
def test_threshold_is_policy_controlled() -> None:
    distiller = SocialPatternDistiller(threshold=3)
    for window in (1, 2):
        distiller.observe(BehaviorRecord("norm:quiet_after_curfew", "lin", window))
    assert distiller.distill() == ()  # 2 windows < threshold 3
    distiller.observe(BehaviorRecord("norm:quiet_after_curfew", "lin", 3))
    candidates = distiller.distill()
    assert len(candidates) == 1
    assert candidates[0].pattern_type == "norm"
    assert candidates[0].meets_threshold


@pytest.mark.unit
def test_candidates_are_envelopes_never_canon() -> None:
    distiller = SocialPatternDistiller(threshold=2)
    distiller.observe_batch(
        [
            BehaviorRecord("group:poetry_salon", "daiyu", 1),
            BehaviorRecord("group:poetry_salon", "daiyu", 2),
        ]
    )
    candidates = distiller.distill()
    assert len(candidates) == 1
    assert isinstance(candidates[0], CandidateEnvelope)
    assert candidates[0].pattern_type == "group"
    # Candidates are not canon: no truth label, no promotion.
    assert not hasattr(candidates[0], "label")
