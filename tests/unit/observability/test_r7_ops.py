"""R7 observability is useful but never canonical truth."""

from __future__ import annotations

import pytest
from wanxiang_observability.r7_ops import R7OpsView, r7_readiness


def test_ops_view_contains_required_r7_dimensions_and_is_non_canonical() -> None:
    view = R7OpsView(
        world_id="world-1",
        worldline_id="wl-1",
        revision=12,
        runtime_lock_hash="lock-hash",
        reality_profile_ref="reality.reference@1.0.0",
        world_profile_ref="world.reference@1.0.0",
        provider_graph_hash="graph-hash",
        proposal_count=8,
        commit_count=5,
        reject_count=3,
        history_append_latency_ms=2.5,
        replay_duration_ms=9.0,
        actor_calls=4,
        model_calls=2,
        execution_jobs=3,
        token_count=100,
        cost_microunits=17,
        resource_units=4,
        migration_status="idle",
        outbox_pending=1,
        outbox_retries=2,
    )

    payload = view.to_dict()
    assert payload["canonical"] is False
    assert payload["revision"] == 12
    assert payload["runtime_lock_hash"] == "lock-hash"
    assert payload["proposal_count"] == 8
    assert payload["outbox_retries"] == 2
    assert "secret" not in payload
    assert "api_key" not in payload


def test_readiness_is_derived_and_cannot_claim_ready_with_a_blocker() -> None:
    ready = r7_readiness(world_host="ready", providers="ready", migration="ready")
    blocked = r7_readiness(
        world_host="ready",
        providers="degraded",
        migration="ready",
        blockers=("official-dsh-live-not-qualified",),
    )

    assert ready.ready is True
    assert ready.to_dict()["canonical"] is False
    assert blocked.ready is False
    assert blocked.blockers == ("official-dsh-live-not-qualified",)


def test_ops_view_rejects_negative_counters() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        R7OpsView(
            world_id="world-1",
            worldline_id="wl-1",
            revision=-1,
            runtime_lock_hash="lock",
            reality_profile_ref="reality@1",
            world_profile_ref="world@1",
            provider_graph_hash="graph",
        )
