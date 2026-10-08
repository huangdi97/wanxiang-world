"""G94G: promotion controls leave the real canonical runtime unchanged."""

from __future__ import annotations

import pathlib

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.evolution.platform_feedback import PlatformFeedbackLab
from wanxiang_substrate.evolution.promotion import (
    PromotionEvidence,
    PromotionPolicy,
    validate_promotion,
)
from wanxiang_substrate.evolution.promotion.control import PromotionControlLedger, PromotionRecord


@pytest.mark.integration
def test_promotion_sandbox_and_rollback_do_not_mutate_sqlite_world(
    persist_db_path: pathlib.Path,
) -> None:
    runtime = make_world_runtime(persist_db_path)
    created = runtime.create_world()
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("cmd_g94g_anchor"),
            instance_id=created.instance_id,
            branch_id=created.root_branch_id,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "g94g_anchor", "count": 1},
            world_time=WorldTime(1),
        )
    )
    before = runtime.current_state(created.instance_id, created.root_branch_id)
    before_events = runtime.events(created.instance_id, created.root_branch_id)

    lab = PlatformFeedbackLab()
    report = lab.run_sandbox(
        "candidate_g94g",
        {"quality": 0.96},
        invariants_ok=True,
        security_ok=True,
        cost=1.0,
        deterministic=True,
    )
    approved = lab.approve(report, "platform_policy")
    release = lab.release(
        approved,
        kind="runtime",
        name="candidate-g94g",
        version="1.0.0",
        release_id="release_g94g_runtime",
    )
    rolled_back = lab.rollback(release)
    validate_promotion(
        PromotionEvidence(
            current_level="L4",
            target_level="L5",
            evidence_count=5,
            stability=0.92,
            cross_scenario=True,
            approved=True,
            world_count=3,
            benchmark_score=approved.benchmark["quality"],
            sandbox_passed=approved.approved,
            rollback_ready=rolled_back.status == "rolled_back",
            policy_version=PromotionPolicy().version,
        )
    )
    ledger = PromotionControlLedger()
    ledger.record(
        PromotionRecord(
            record_id="promotion_g94g",
            derived_definition_id="definition_g94g",
            source_worldline_ref=created.root_branch_id.value,
            parent_definition_ref=created.instance_id.value,
        )
    )
    withdrawn = ledger.withdraw("promotion_g94g", rationale="rollback qualification")
    assert withdrawn.status == "withdrawn"
    assert rolled_back.status == "rolled_back"
    assert (
        runtime.current_state(created.instance_id, created.root_branch_id).semantic_hash()
        == before.semantic_hash()
    )
    assert runtime.events(created.instance_id, created.root_branch_id) == before_events
    assert (
        runtime.restore_and_replay(
            created.instance_id, created.root_branch_id
        ).state.semantic_hash()
        == before.semantic_hash()
    )
