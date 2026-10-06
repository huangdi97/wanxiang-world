"""R7 closure: four reference slices and Gate H shared-reality Experience proof.

These tests deliberately compose existing production contracts instead of creating
four parallel demo stacks. Every world mutation still goes through WorldRuntime /
CommitAuthority; Foundry/Execution/Harness outputs remain proposal-side.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import pytest
from wanxiang_api.experience_player_service import ExperiencePlayerService
from wanxiang_application.observer_experience import ObserverExperienceService
from wanxiang_domain.errors import ValidationRejected
from wanxiang_domain.ids import WorldInstanceId
from wanxiang_execution import ExecutionClass, ExecutionPolicy
from wanxiang_foundry import (
    ArtifactKind,
    ArtifactRef,
    CapabilityPackage,
    CapabilityRequest,
    CaseKind,
    KnowledgeLevel,
    OutputClass,
    PromotionLevel,
    ProvenanceLayer,
    ProvenanceRecord,
    RuleBasedFoundryProvider,
    RuntimeRequirement,
    Validity,
    VerificationCase,
    VerifiedCapabilityRegistry,
    WorldEffect,
    canonical_sha256,
    invoke,
    run_cases,
    verify,
)
from wanxiang_runtime.r7_agent_harness import (
    HarnessConsequence,
    JsonRpcAgentHarnessProvider,
    WorldObservation,
)
from wanxiang_substrate.ledger.ledger import CompletionLedger
from wanxiang_substrate.ledger.model import ContentItem, ReviewDecision
from wanxiang_substrate.sources.gate import SourceGate
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash

from scripts.reference_runtime import build_reference_runtime

ROOT = Path(__file__).resolve().parents[2]
HARNESS = ROOT / "scripts" / "r7_reference_harness.py"
SCIENCE_CAPABILITY = ROOT / "reference_worlds" / "r7" / "science" / "double_capability.py"


def _digest(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@pytest.mark.integration
def test_original_world_two_experiences_share_one_canonical_reality() -> None:
    """Original/Fiction + Gate H: Player writes, Observer reads the same truth."""
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_r7_original"))
    player = ExperiencePlayerService(runtime)
    observer = ObserverExperienceService(runtime)
    branch = player.start_session(world.instance_id)

    created = player.act(
        world.instance_id,
        branch,
        expected_revision=0,
        action_type="create_entity",
        payload={"entity_id": "ent_hero", "count": 3},
        actor_id="act_hero",
        command_id="cmd_r7_original_create",
    )
    view_after_create = observer.observe(world.instance_id, branch)
    assert created["revision"] == 1
    assert view_after_create.revision == 1
    assert view_after_create.state_hash == created["state_hash"]
    assert view_after_create.event_count == 1

    changed = player.act(
        world.instance_id,
        branch,
        expected_revision=1,
        action_type="set_status",
        payload={"entity_id": "ent_hero", "status": "awake"},
        actor_id="act_hero",
        command_id="cmd_r7_original_status",
    )
    view_after_change = observer.observe(world.instance_id, branch)
    assert changed["revision"] == 2
    assert view_after_change.state_hash == changed["state_hash"]

    # A rejected proposal cannot advance canonical reality.
    with pytest.raises(ValidationRejected):
        player.act(
            world.instance_id,
            branch,
            expected_revision=2,
            action_type="transfer_resource",
            payload={"source_id": "ent_hero", "target_id": "ent_hero", "amount": 999},
            actor_id="act_hero",
            command_id="cmd_r7_original_rejected",
        )
    assert observer.observe(world.instance_id, branch).revision == 2

    # A child branch starts from the same committed baseline but is isolated.
    child = runtime.create_branch(world.instance_id, branch)
    child_result = player.act(
        world.instance_id,
        child.branch_id,
        expected_revision=2,
        action_type="set_status",
        payload={"entity_id": "ent_hero", "status": "branch-exploring"},
        actor_id="act_hero",
        command_id="cmd_r7_original_child",
    )
    assert child_result["revision"] == 3
    assert observer.observe(world.instance_id, branch).revision == 2
    assert observer.observe(world.instance_id, child.branch_id).revision == 3

    # The Observer Experience is structurally read-only: it owns no mutation API.
    assert not hasattr(observer, "act")
    assert not hasattr(observer, "commit")


@pytest.mark.integration
def test_heritage_world_requires_rights_evidence_and_keeps_reconstruction_distinct() -> None:
    """Heritage slice: evidence/rights are gates, reconstruction is not canon."""
    approved = SourceRecord(
        source_id="src_r7_heritage",
        kind="catalogue",
        content_hash=payload_hash("bronze vessel catalogue entry"),
        content_ref="ref://heritage/catalogue/1",
        stage="E3",
        rights=RightsEnvelope(
            owner="reference-museum",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
        ),
        payload="bronze vessel catalogue entry",
        provenance="reference:r7:heritage",
        access="private",
    )
    denied = SourceRecord(
        source_id="src_r7_heritage_denied",
        kind="catalogue",
        content_hash=payload_hash("restricted catalogue entry"),
        content_ref="ref://heritage/catalogue/denied",
        stage="E3",
        rights=RightsEnvelope(
            owner="reference-museum",
            usage="qualification",
            approved=False,
            package_inclusion_allowed=False,
        ),
        payload="restricted catalogue entry",
        provenance="reference:r7:heritage",
        access="restricted",
    )
    gate = SourceGate()
    assert gate.decide(approved).ok is True
    assert gate.decide(denied).ok is False

    ledger = CompletionLedger()
    source_backed = ledger.submit(
        ContentItem(
            item_id="heritage-source-claim",
            label="source_backed",
            source_refs=(approved.content_ref,),
            rights_approved=True,
        )
    )
    reconstruction = ledger.submit(
        ContentItem(
            item_id="heritage-reconstruction",
            label="reconstruction",
            source_refs=(),
            rights_approved=True,
        )
    )
    assert source_backed.label == "source_backed"
    assert reconstruction.label == "reconstruction"

    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_r7_heritage"))
    player = ExperiencePlayerService(runtime)
    branch = player.start_session(world.instance_id)
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_artifact", "count": 0},
        "act_curator",
        "cmd_r7_heritage_create",
    )
    event_count_before_review = len(runtime.events(world.instance_id, branch))

    # Submitting generated reconstruction changes no World history by itself.
    assert ledger.require("heritage-reconstruction").label == "reconstruction"
    assert len(runtime.events(world.instance_id, branch)) == event_count_before_review

    canon = ledger.review(
        ReviewDecision(
            decision_id="review_r7_heritage",
            item_id="heritage-source-claim",
            from_label="source_backed",
            to_label="canon",
            reviewer="reference-curator",
            rationale="approved source and evidence were checked",
            review_version=1,
            evidence_refs=("ref://heritage/evidence/1",),
        )
    )
    assert canon.label == "canon"
    assert canon.source_refs == (approved.content_ref,)
    assert ledger.require("heritage-reconstruction").label == "reconstruction"

    committed = player.act(
        world.instance_id,
        branch,
        1,
        "set_status",
        {"entity_id": "ent_artifact", "status": "source-backed-canon"},
        "act_curator",
        "cmd_r7_heritage_commit",
    )
    assert committed["revision"] == 2
    assert len(runtime.events(world.instance_id, branch)) == event_count_before_review + 1


@pytest.mark.integration
def test_agent_world_reference_harness_is_proposal_only_and_gets_consequences() -> None:
    """Agent slice: cross-process harness proposes; world alone commits/rejects."""
    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_r7_agent"))
    player = ExperiencePlayerService(runtime)
    branch = player.start_session(world.instance_id)
    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_agent", "count": 0},
        "act_agent",
        "cmd_r7_agent_create",
    )

    provider = JsonRpcAgentHarnessProvider(
        [sys.executable, str(HARNESS)],
        cwd=ROOT,
        request_timeout_seconds=30.0,
    )
    try:
        info = provider.info()
        assert info.official_dsh is False
        assert info.kind == "reference-rule-harness"

        state = runtime.current_state(world.instance_id, branch)
        events = runtime.events(world.instance_id, branch)
        decision = provider.decide(
            WorldObservation(
                worldline_id=branch.value,
                revision=state.revision.value,
                state_hash=state.semantic_hash(),
                allowed_history=tuple(event.event_id.value for event in events),
                allowed_context={"targetRevision": "3", "pendingAction": "set_status"},
                goal_hint="advance only by proposing",
            )
        )
        assert decision.status == "proposed"
        assert decision.proposal is not None
        assert decision.proposal.action == "set_status"
        # A decision alone has no effect.
        assert runtime.current_state(world.instance_id, branch).revision.value == 1

        result = player.act(
            world.instance_id,
            branch,
            1,
            decision.proposal.action,
            {"entity_id": "ent_agent", "status": "harness-proposal-accepted"},
            "act_agent",
            "cmd_r7_agent_accepted",
        )
        assert provider.deliver_consequence(
            HarnessConsequence(
                worldline_id=branch.value,
                proposal_id=decision.proposal.proposal_id,
                status="committed",
                revision=int(result["revision"]),
                state_hash=str(result["state_hash"]),
                reason="accepted by Wanxiang authority",
            )
        )

        # Exercise the rejection consequence without changing the world.
        state2 = runtime.current_state(world.instance_id, branch)
        second = provider.decide(
            WorldObservation(
                worldline_id=branch.value,
                revision=state2.revision.value,
                state_hash=state2.semantic_hash(),
                allowed_context={"targetRevision": "3", "pendingAction": "set_status"},
            )
        )
        assert second.status == "proposed"
        assert second.proposal is not None
        assert provider.deliver_consequence(
            HarnessConsequence(
                worldline_id=branch.value,
                proposal_id=second.proposal.proposal_id,
                status="rejected",
                revision=None,
                state_hash=None,
                reason="reference policy rejection",
            )
        )
        assert runtime.current_state(world.instance_id, branch).revision.value == 2
    finally:
        provider.close()


@pytest.mark.integration
def test_science_capability_real_artifact_verifies_executes_then_requires_authority(
    tmp_path: Path,
) -> None:
    """Science slice: real Artifact -> C3 capability -> proposal -> separate Commit."""
    artifact_bytes = SCIENCE_CAPABILITY.read_bytes()
    artifact_digest = hashlib.sha256(artifact_bytes).hexdigest()
    artifact = ArtifactRef(
        kind=ArtifactKind.REPO,
        uri="repo:reference_worlds/r7/science/double_capability.py",
        digest=artifact_digest,
        rights_basis="repository qualification fixture; project license applies",
    )
    provider = RuleBasedFoundryProvider()
    candidate = provider.propose(
        artifact,
        {
            "capability_id": "cap.r7.double",
            "proposed_version": "1.0.0",
            "inputs": ["non-negative integer"],
            "outputs": ["doubled integer"],
            "environment": {"python": "3.12+"},
            "requested_side_effects": ["none"],
        },
    )

    cases = (
        VerificationCase(
            "golden-double-6",
            CaseKind.GOLDEN,
            (sys.executable, str(SCIENCE_CAPABILITY), "6"),
            _digest("12\n"),
            0,
        ),
        VerificationCase(
            "negative-refuses-minus-one",
            CaseKind.NEGATIVE,
            (sys.executable, str(SCIENCE_CAPABILITY), "-1"),
            _digest(""),
            2,
        ),
        VerificationCase(
            "boundary-zero",
            CaseKind.BOUNDARY,
            (sys.executable, str(SCIENCE_CAPABILITY), "0"),
            _digest("0\n"),
            0,
        ),
        VerificationCase(
            "security-no-secret-dependency",
            CaseKind.SECURITY,
            (sys.executable, str(SCIENCE_CAPABILITY), "--security"),
            _digest("safe\n"),
            0,
        ),
    )
    policy = ExecutionPolicy.default_untrusted()
    observed = run_cases(cases, policy, tmp_path / "verification")
    report = verify(cases, observed)
    assert report.grants_k3 is True
    assert report.grants_c3 is True
    assert report.failed_case_ids == ()
    assert report.missing_case_ids == ()

    provenance = (
        ProvenanceRecord(
            ProvenanceLayer.SOURCE_METHOD,
            artifact.uri,
            artifact.digest,
            "tracked source method used by the reference slice",
        ),
        ProvenanceRecord(
            ProvenanceLayer.GENERATED_WRAPPER,
            candidate.candidate_id,
            candidate.candidate_digest(),
            "deterministic rule-based Artifact2Capability candidate",
        ),
        ProvenanceRecord(
            ProvenanceLayer.VALIDATION_FIXTURE,
            "verification:r7-reference-worlds",
            report.evidence_digest,
            "golden/negative/boundary/security execution evidence",
        ),
        ProvenanceRecord(
            ProvenanceLayer.RUNTIME_ADAPTER,
            "execution:local-process@1.0.0",
            canonical_sha256({"provider": "execution-local-process", "version": "1.0.0"}),
            "process-boundary reference Execution Fabric provider",
        ),
    )
    policy_fingerprint = canonical_sha256(
        {
            "trust": policy.trust.value,
            "execution_class": policy.execution_class.value,
            "filesystem": policy.filesystem.value,
            "network": policy.network.value,
            "secrets": policy.secrets.value,
            "side_effects": policy.side_effects.value,
            "wall_seconds_limit": policy.wall_seconds_limit,
        }
    )
    package = CapabilityPackage(
        capability_id=candidate.capability_id,
        version=candidate.proposed_version,
        artifact_digest=artifact.digest,
        interface_digest=canonical_sha256(dict(candidate.proposed_interface)),
        provenance=provenance,
        validity=Validity(
            supported_inputs=("non-negative integer",),
            known_limitations=("reference arithmetic only", "PROCESS is not a hostile-code sandbox"),
            environment_hash=canonical_sha256(
                {
                    "python": f"{sys.version_info.major}.{sys.version_info.minor}",
                    "execution_class": policy.execution_class.value,
                }
            ),
        ),
        runtime=RuntimeRequirement(
            execution_class=ExecutionClass.PROCESS,
            policy_fingerprint=policy_fingerprint,
        ),
        world_effect=WorldEffect(allowed_output_class=OutputClass.OBSERVATION),
        knowledge_level=KnowledgeLevel.K3_VERIFIED_ENVIRONMENTAL,
        promotion_level=PromotionLevel.C3_VERIFIED,
        verification_digest=report.evidence_digest,
    )
    registry = VerifiedCapabilityRegistry()
    registry.admit(package, report)

    runtime = build_reference_runtime()
    world = runtime.create_world(instance_id=WorldInstanceId("wld_r7_science"))
    player = ExperiencePlayerService(runtime)
    branch = player.start_session(world.instance_id)
    assert runtime.events(world.instance_id, branch) == ()

    outcome = invoke(
        registry,
        package,
        CapabilityRequest(
            execution_id="r7-science-invoke",
            command=(sys.executable, str(SCIENCE_CAPABILITY), "5"),
        ),
        policy,
        tmp_path / "invocation",
    )
    assert outcome.observation["proposal_only"] is True
    assert outcome.proposal["proposal_only"] is True
    assert len(outcome.execution_digest) == 64
    # Execution succeeded, but canonical reality is still untouched.
    assert runtime.events(world.instance_id, branch) == ()

    player.act(
        world.instance_id,
        branch,
        0,
        "create_entity",
        {"entity_id": "ent_science", "count": 0},
        "act_scientist",
        "cmd_r7_science_create",
    )
    committed = player.act(
        world.instance_id,
        branch,
        1,
        "set_status",
        {"entity_id": "ent_science", "status": "capability-observation-reviewed"},
        "act_scientist",
        "cmd_r7_science_commit",
    )
    assert committed["revision"] == 2
    assert len(runtime.events(world.instance_id, branch)) == 2
