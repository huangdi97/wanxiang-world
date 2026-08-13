"""G03G: capability & learning through the authoritative path.

Covers bounded practice/assessment -> CapabilityDelta, evidence linkage,
skill-prerequisite integration, negative gates and replay determinism.
"""

from __future__ import annotations

import pathlib
from collections.abc import Iterator, Mapping

import pytest
from tests.conftest import cleanup_db_file, fresh_db_path, make_world_runtime
from wanxiang_application.world_runtime import CreateWorldResult, WorldRuntime
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.delta import EntityCreate, ProposedWorldDelta
from wanxiang_domain.entity import FieldValue
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import BranchId, CommandId, EntityId, WorldInstanceId
from wanxiang_domain.time import WorldTime
from wanxiang_domain.versions import RuntimeVersion, SchemaVersion
from wanxiang_runtime.replay import ReplayEngine
from wanxiang_substrate.capability.errors import UnsupportedAssessment
from wanxiang_substrate.capability.model import (
    CAPABILITY_MAX_LEVEL,
    CapabilityState,
    LearnerState,
)
from wanxiang_substrate.capability.policy import LearningPolicy
from wanxiang_substrate.capability.query import CapabilityQuery
from wanxiang_substrate.capability.resolver import register_capability_resolvers
from wanxiang_substrate.skills.errors import InvalidSkillStep
from wanxiang_substrate.skills.model import SkillDefinition, SkillStep
from wanxiang_substrate.skills.registry import SkillRegistry
from wanxiang_substrate.skills.resolver import register_skill_resolvers
from wanxiang_substrate.skills.runtime import SkillRuntime

INSTANCE = WorldInstanceId("wld_g03g")
ACTOR = EntityId("alice")
OTHER = EntityId("bob")
CAP = "delivery"
PROBE_ENTITY = EntityId("probe_p1")


def make_cap_runtime(path: pathlib.Path) -> WorldRuntime:
    from wanxiang_runtime.resolver import ResolverRegistry

    def register(registry: ResolverRegistry) -> None:
        register_capability_resolvers(registry)
        register_skill_resolvers(registry)
        registry.register("g03g.probe", _probe)

    return make_world_runtime(path, extra_resolvers=register)


def _probe(command: CommandEnvelope, state: object) -> ProposedWorldDelta:
    probe_id = str(command.payload.get("probe_id") or "p1")
    return ProposedWorldDelta(
        operations=(
            EntityCreate(
                entity_id=EntityId(f"probe_{probe_id}"),
                entity_type="g03g.probe",
                components=(),
            ),
        )
    )


def cmd(
    branch: BranchId,
    revision: int,
    action: str,
    payload: Mapping[str, FieldValue],
    command_id: str,
) -> CommandEnvelope:
    return CommandEnvelope(
        command_id=CommandId(command_id),
        instance_id=INSTANCE,
        branch_id=branch,
        expected_revision=BranchRevision(revision),
        action_type=action,
        payload=payload,
        world_time=WorldTime(revision + 1),
    )


@pytest.fixture
def cap_world() -> Iterator[tuple[WorldRuntime, CreateWorldResult]]:
    path = fresh_db_path()
    runtime = make_cap_runtime(path)
    w = runtime.create_world(instance_id=INSTANCE)
    yield runtime, w
    cleanup_db_file(path)


def _practice(
    runtime: WorldRuntime,
    branch: BranchId,
    revision: int,
    record_id: str,
    count: int,
    evidence_ref: str,
) -> int:
    runtime.submit_command(
        cmd(
            branch,
            revision,
            "capability.record_practice",
            {
                "record_id": record_id,
                "actor_id": ACTOR.value,
                "capability": CAP,
                "practice_count": count,
                "evidence_ref": evidence_ref,
            },
            f"cmd_p_{record_id}",
        )
    )
    return revision + 1


def _assess(
    runtime: WorldRuntime,
    branch: BranchId,
    revision: int,
    assessment_id: str,
    outcome: str,
    evidence_ref: str,
    assessment_type: str = "practical",
) -> int:
    runtime.submit_command(
        cmd(
            branch,
            revision,
            "capability.record_assessment",
            {
                "assessment_id": assessment_id,
                "actor_id": ACTOR.value,
                "capability": CAP,
                "assessment_type": assessment_type,
                "outcome": outcome,
                "evidence_ref": evidence_ref,
            },
            f"cmd_a_{assessment_id}",
        )
    )
    return revision + 1


@pytest.mark.unit
def test_practice_bounded_level_and_evidence(
    cap_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = cap_world
    rev = 0
    rev = _practice(runtime, w.root_branch_id, rev, "pr1", 3, "evid://p1")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    cap = CapabilityQuery(state).capability(ACTOR, CAP)
    assert cap is not None and cap.level == 1
    assert cap.evidence_refs == ("evid://p1",)
    # More practice crosses the next level boundary and accumulates evidence.
    rev = _practice(runtime, w.root_branch_id, rev, "pr2", 3, "evid://p2")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    cap = CapabilityQuery(state).capability(ACTOR, CAP)
    assert cap is not None and cap.level == 2
    assert cap.evidence_refs == ("evid://p1", "evid://p2")


@pytest.mark.unit
def test_assessment_pass_increases_mastery_but_not_level(
    cap_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = cap_world
    rev = _practice(runtime, w.root_branch_id, 0, "pr1", 3, "evid://p1")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    before = CapabilityQuery(state).capability(ACTOR, CAP)
    assert before is not None
    rev = _assess(runtime, w.root_branch_id, rev, "as1", "pass", "evid://a1")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    after = CapabilityQuery(state).capability(ACTOR, CAP)
    assert after is not None
    assert after.level == before.level
    assert after.mastery > before.mastery
    assert after.confidence > before.confidence


@pytest.mark.unit
def test_unsupported_assessment_cannot_create_mastery(
    cap_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = cap_world
    before = runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash()
    with pytest.raises(UnsupportedAssessment):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                0,
                "capability.record_assessment",
                {
                    "assessment_id": "as_bad",
                    "actor_id": ACTOR.value,
                    "capability": CAP,
                    "assessment_type": "astrology",
                    "outcome": "pass",
                    "evidence_ref": "evid://bad",
                },
                "cmd_a_bad",
            )
        )
    after = runtime.current_state(w.instance_id, w.root_branch_id).semantic_hash()
    assert after == before  # rejected command changed nothing


@pytest.mark.unit
def test_direct_delta_requires_evidence(
    cap_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = cap_world
    from wanxiang_substrate.capability.errors import EvidenceRequired

    with pytest.raises(EvidenceRequired):
        runtime.submit_command(
            cmd(
                w.root_branch_id,
                0,
                "capability.apply_delta",
                {
                    "actor_id": ACTOR.value,
                    "capability": CAP,
                    "level_delta": 1,
                    "mastery_delta": 0.0,
                    "confidence_delta": 0.0,
                    "reason": "claim without evidence",
                    "evidence_refs": "[]",
                },
                "cmd_delta_no_evid",
            )
        )


@pytest.mark.unit
def test_learner_state_and_biography(
    cap_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = cap_world
    rev = _practice(runtime, w.root_branch_id, 0, "pr1", 3, "evid://p1")
    rev = _assess(runtime, w.root_branch_id, rev, "as1", "pass", "evid://a1")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    learner: LearnerState = CapabilityQuery(state).learner_state(ACTOR)
    assert learner.practice_records == 1
    assert learner.assessment_records == 1
    assert learner.biography == ("evid://p1", "evid://a1")
    assert learner.capability(CAP) is not None
    # Another actor never learns about Alice's capability without evidence.
    assert CapabilityQuery(state).capability(OTHER, CAP) is None


@pytest.mark.unit
def test_capability_stays_bounded(
    cap_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = cap_world
    rev = 0
    for i in range(60):
        rev = _practice(runtime, w.root_branch_id, rev, f"prb{i}", 3, f"evid://p{i}")
        rev = _assess(runtime, w.root_branch_id, rev, f"asb{i}", "pass", f"evid://a{i}")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    cap = CapabilityQuery(state).capability(ACTOR, CAP)
    assert cap is not None
    assert 0 <= cap.level <= CAPABILITY_MAX_LEVEL
    assert 0.0 <= cap.mastery <= 1.0
    assert 0.0 <= cap.confidence <= 1.0


@pytest.mark.integration
def test_learning_biography_reconstructs(
    cap_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = cap_world
    rev = 0
    rev = _practice(runtime, w.root_branch_id, rev, "pr1", 6, "evid://p1")
    rev = _assess(runtime, w.root_branch_id, rev, "as1", "fail", "evid://a1")
    rev = _assess(runtime, w.root_branch_id, rev, "as2", "pass", "evid://a2")
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    events = runtime.events(w.instance_id, w.root_branch_id)
    replayed = ReplayEngine(RuntimeVersion(1), SchemaVersion(1)).replay(events)
    assert replayed.semantic_hash() == state.semantic_hash()
    original = CapabilityQuery(state).capability(ACTOR, CAP)
    rebuilt = CapabilityQuery(replayed).capability(ACTOR, CAP)
    assert original is not None and rebuilt is not None
    assert original.level == rebuilt.level
    assert original.mastery == rebuilt.mastery
    assert original.evidence_refs == rebuilt.evidence_refs


@pytest.mark.integration
def test_skill_step_requires_capability(
    cap_world: tuple[WorldRuntime, CreateWorldResult],
) -> None:
    runtime, w = cap_world
    registry = SkillRegistry()
    registry.register(
        SkillDefinition(
            skill_id=EntityId("skill_probe"),
            version=1,
            name="probe",
            steps=(
                SkillStep(
                    "probe",
                    "g03g.probe",
                    {"probe_id": "p1"},
                    requires_capability="delivery:2",
                ),
            ),
        )
    )
    skill = SkillRuntime(runtime, registry, INSTANCE, w.root_branch_id)
    # No capability yet -> step is rejected and the skill is marked failed.
    with pytest.raises(InvalidSkillStep):
        skill.execute(EntityId("skill_inst_1"), EntityId("skill_probe"), ACTOR)
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(PROBE_ENTITY) is None
    # Practice to level 2, then the same skill executes.
    revision = state.revision.value
    _practice(runtime, w.root_branch_id, revision, "pr1", 6, "evid://p1")
    completed = skill.execute(EntityId("skill_inst_2"), EntityId("skill_probe"), ACTOR)
    assert completed == ["probe"]
    state = runtime.current_state(w.instance_id, w.root_branch_id)
    assert state.entity(PROBE_ENTITY) is not None


@pytest.mark.unit
def test_policy_apply_clamps_regression() -> None:

    from wanxiang_substrate.capability.model import CapabilityDelta

    # A huge negative delta cannot push below zero.
    current = CapabilityState(actor_id=ACTOR, capability=CAP, level=1, mastery=0.5, confidence=0.5)
    delta = CapabilityDelta(
        actor_id=ACTOR,
        capability=CAP,
        level_delta=-100,
        mastery_delta=-1.0,
        confidence_delta=-1.0,
        reason="test regression",
        evidence_refs=("evid://r",),
    )
    updated = LearningPolicy.apply(delta, current)
    assert updated.level == 0
    assert updated.mastery == 0.0
    assert updated.confidence == 0.0
    assert "evid://r" in updated.evidence_refs
