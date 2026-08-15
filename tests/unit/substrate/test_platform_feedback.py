"""G33E: platform feedback sandbox/benchmark/approval."""

from __future__ import annotations

import pytest
from tests.helpers.replay_fixture import RULES, SCHEMA, build_fixture_events
from wanxiang_domain.errors import PermissionDenied
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.evolution.platform_feedback import PlatformFeedbackLab


@pytest.mark.unit
def test_world_instance_does_not_own_platform_approval() -> None:
    lab = PlatformFeedbackLab()
    report = lab.run_sandbox(
        "cand_xw_1",
        {"accuracy": 0.9, "latency": 12.0},
        invariants_ok=True,
        security_ok=True,
        cost=3.0,
        deterministic=True,
    )
    # A world instance (or any non-platform approver) cannot approve.
    with pytest.raises(PermissionDenied):
        lab.approve(report, "world_instance")
    # Platform reviewer can approve.
    approved = lab.approve(report, "platform_reviewer")
    assert approved.approved is True


@pytest.mark.unit
def test_sandbox_gate_blocks_approval() -> None:
    lab = PlatformFeedbackLab()
    report = lab.run_sandbox(
        "cand_xw_2",
        {"accuracy": 0.5},
        invariants_ok=False,  # invariant failure
        security_ok=True,
        cost=1.0,
        deterministic=True,
    )
    with pytest.raises(PermissionDenied):
        lab.approve(report, "platform_reviewer")
    with pytest.raises(PermissionDenied):
        lab.release(report, kind="domain", name="household", version="2.0.0", release_id="rel_1")


@pytest.mark.unit
def test_versioned_release_and_rollback_do_not_rewrite_world_events() -> None:
    lab = PlatformFeedbackLab()
    report = lab.run_sandbox(
        "cand_xw_3",
        {"determinism": 1.0},
        invariants_ok=True,
        security_ok=True,
        cost=2.0,
        deterministic=True,
    )
    approved = lab.approve(report, "platform_policy")
    release = lab.release(
        approved, kind="runtime", name="wanxiang-runtime", version="2.1.0", release_id="rel_rt_1"
    )
    assert release.status == "active"

    # Past world events replay identically before and after release/rollback.
    before = ReplayEngine(RULES, SCHEMA).replay(build_fixture_events()).semantic_hash()
    rolled = lab.rollback(release)
    assert rolled.status == "rolled_back"
    after = ReplayEngine(RULES, SCHEMA).replay(build_fixture_events()).semantic_hash()
    assert after == before
    assert after == "7d17aba7b9b76f04174f28a05ed7139505ab1784d0377ebe1966f7ef8d69fd00"
