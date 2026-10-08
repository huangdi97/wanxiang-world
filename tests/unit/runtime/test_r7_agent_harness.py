"""Tests for the R7 agent-harness JSON-RPC bridge (reference harness only)."""

from __future__ import annotations

import re
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest
from wanxiang_runtime.r7_agent_harness import (
    AgentDecision,
    AgentProposal,
    HarnessConsequence,
    HarnessProtocolError,
    HarnessUnavailable,
    JsonRpcAgentHarnessProvider,
    WorldObservation,
    parse_decision,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
HARNESS_SCRIPT = REPO_ROOT / "scripts" / "r7_reference_harness.py"
WORLDLINE = "wl_harness"


@pytest.fixture(name="provider")
def provider_fixture() -> Iterator[JsonRpcAgentHarnessProvider]:
    provider = JsonRpcAgentHarnessProvider(
        [sys.executable, str(HARNESS_SCRIPT), "--stdio"],
        cwd=REPO_ROOT,
        request_timeout_seconds=30.0,
    )
    try:
        yield provider
    finally:
        provider.close()


def observation(revision: int, *, target: int = 3) -> WorldObservation:
    return WorldObservation(
        worldline_id=WORLDLINE,
        revision=revision,
        state_hash=f"hash-{revision}",
        allowed_history=(f"{WORLDLINE}:evt:{revision}",),
        allowed_context={"targetRevision": str(target), "pendingAction": "set_status"},
        goal_hint="advance the world",
    )


def test_reference_harness_identifies_itself_as_non_official(
    provider: JsonRpcAgentHarnessProvider,
) -> None:
    info = provider.info()

    assert info.harness_id == "wanxiang-reference-rule-harness"
    assert info.kind == "reference-rule-harness"
    assert info.official_dsh is False
    assert provider.provider_id == "agent-harness-rpc"


def test_harness_proposes_before_the_target_revision(provider: JsonRpcAgentHarnessProvider) -> None:
    decision = provider.decide(observation(0))

    assert decision.status == "proposed"
    assert decision.proposal is not None
    assert decision.proposal.action == "set_status"
    assert decision.proposal.proposal_id == f"prop_{WORLDLINE}_1"
    assert re.fullmatch(r"[0-9a-f]{64}", decision.proposal.payload_digest)


def test_harness_proposal_is_deterministic_for_the_same_observation(
    provider: JsonRpcAgentHarnessProvider,
) -> None:
    first = provider.decide(observation(1))
    second = provider.decide(observation(1))

    assert first.proposal == second.proposal


def test_harness_abstains_once_the_target_revision_is_reached(
    provider: JsonRpcAgentHarnessProvider,
) -> None:
    decision = provider.decide(observation(3))

    assert decision.status == "abstained"
    assert decision.proposal is None
    assert "target 3" in decision.reason


def test_harness_accepts_a_committed_consequence(provider: JsonRpcAgentHarnessProvider) -> None:
    acknowledged = provider.deliver_consequence(
        HarnessConsequence(
            worldline_id=WORLDLINE,
            proposal_id=f"prop_{WORLDLINE}_1",
            status="committed",
            revision=1,
            state_hash="hash-1",
            reason="committed",
        )
    )

    assert acknowledged is True


def test_harness_accepts_a_rejected_consequence(provider: JsonRpcAgentHarnessProvider) -> None:
    acknowledged = provider.deliver_consequence(
        HarnessConsequence(
            worldline_id=WORLDLINE,
            proposal_id=f"prop_{WORLDLINE}_1",
            status="rejected",
            revision=None,
            state_hash=None,
            reason="policy.cross-worldline-guard",
        )
    )

    assert acknowledged is True


def test_missing_harness_executable_is_reported_as_unavailable() -> None:
    provider = JsonRpcAgentHarnessProvider(
        ["definitely-not-a-real-binary-xyz"],
        cwd=REPO_ROOT,
    )
    try:
        with pytest.raises(HarnessUnavailable):
            provider.info()
    finally:
        provider.close()


def test_garbage_harness_answer_is_a_protocol_error() -> None:
    provider = JsonRpcAgentHarnessProvider(
        [sys.executable, "-c", "import sys; sys.stdout.write('not json\\n'); sys.stdout.flush()"],
        cwd=REPO_ROOT,
    )
    try:
        with pytest.raises(HarnessProtocolError):
            provider.info()
    finally:
        provider.close()


def test_silent_harness_is_reported_as_unavailable() -> None:
    provider = JsonRpcAgentHarnessProvider(
        [sys.executable, "-c", "import sys; sys.stdin.read()"],
        cwd=REPO_ROOT,
        request_timeout_seconds=5.0,
    )
    try:
        with pytest.raises(HarnessUnavailable):
            provider.info()
    finally:
        provider.close()


def test_proposed_decision_must_carry_a_proposal() -> None:
    with pytest.raises(HarnessProtocolError, match="must carry a proposal"):
        AgentDecision(status="proposed", proposal=None, reason="oops")


def test_abstained_decision_must_not_carry_a_proposal() -> None:
    proposal = AgentProposal(
        proposal_id="p1",
        action="set_status",
        rationale_ref="r",
        payload_digest="d",
    )
    with pytest.raises(HarnessProtocolError, match="must not carry a proposal"):
        AgentDecision(status="abstained", proposal=proposal, reason="no")


def test_unknown_consequence_status_is_rejected_locally() -> None:
    with pytest.raises(HarnessProtocolError, match="unknown consequence status"):
        HarnessConsequence(
            worldline_id=WORLDLINE,
            proposal_id="p1",
            status="maybe",
            revision=None,
            state_hash=None,
            reason="",
        )


def test_parse_decision_rejects_missing_status_and_broken_proposal() -> None:
    with pytest.raises(HarnessProtocolError, match="missing 'status'"):
        parse_decision({"proposal": None})
    with pytest.raises(HarnessProtocolError, match="missing required fields"):
        parse_decision({"status": "proposed", "proposal": {"proposalId": "p1"}})
    with pytest.raises(HarnessProtocolError, match="must be an object"):
        parse_decision({"status": "proposed", "proposal": "p1"})


def test_bridge_module_holds_no_commit_path() -> None:
    source = (
        REPO_ROOT / "packages" / "runtime" / "src" / "wanxiang_runtime" / "r7_agent_harness.py"
    ).read_text(encoding="utf-8")

    assert "append(" not in source
    assert "CommitCapability" not in source
    for forbidden in (
        "wanxiang_runtime.authority",
        "wanxiang_runtime.isa_pipeline",
        "wanxiang_substrate",
    ):
        assert forbidden not in source, f"harness bridge must not import {forbidden}"
