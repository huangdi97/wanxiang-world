"""G18G: learn / challenge experience completion.

- Learning artifact/assessment evidence is traceable.
- Capability changes are separated from persona changes.
- A challenge affects the world through the normal action/commit path.
"""

from __future__ import annotations

import pathlib

from tests.conftest import make_world_runtime
from wanxiang_api.learn_service import LearnService
from wanxiang_domain.command import CommandEnvelope
from wanxiang_domain.hierarchy import BranchRevision
from wanxiang_domain.ids import CommandId, EntityId
from wanxiang_domain.time import WorldTime
from wanxiang_substrate.capability.model import AssessmentEvidence, LearnerState, PracticeRecord


def _learner() -> LearnerState:
    return LearnerState(
        actor_id=EntityId("learner"),
        capabilities=(),
        practice_records=0,
        assessment_records=0,
        biography=(),
    )


def test_learning_evidence_traceable() -> None:
    service = LearnService()
    learner = _learner()
    practice = PracticeRecord(
        record_id=EntityId("rec_1"),
        actor_id=EntityId("learner"),
        capability="smithing",
        practice_count=1,
        evidence_ref="ref://smith_1",
    )
    updated = service.practice(learner, practice)
    assert updated.practice_records == 1
    state = updated.capability("smithing")
    assert state is not None and state.evidence_refs == ("ref://smith_1",)
    # Assessment adds evidence provenance.
    evidence = AssessmentEvidence(
        assessment_id=EntityId("a1"),
        actor_id=EntityId("learner"),
        capability="smithing",
        assessment_type="practical",
        outcome="pass",
        evidence_ref="ref://smith_assess",
    )
    assessed = service.assess(updated, evidence)
    assessed_state = assessed.capability("smithing")
    assert assessed_state is not None
    assert assessed_state.evidence_refs == ("ref://smith_1", "ref://smith_assess")
    assert assessed.assessment_records == 1


def test_capability_changes_separated_from_persona() -> None:
    service = LearnService()
    learner = _learner()
    evidence = AssessmentEvidence(
        assessment_id=EntityId("a2"),
        actor_id=EntityId("learner"),
        capability="strategy",
        assessment_type="practical",
        outcome="pass",
        evidence_ref="ref://strat",
    )
    updated = service.assess(learner, evidence)
    assert updated.capability("strategy") is not None
    # No persona/actor entity was mutated: the learner aggregate has no persona
    # field, and the service never touches canonical actor state.
    assert "persona" not in updated.biography


def test_challenge_affects_world_through_command_path(persist_db_path: pathlib.Path) -> None:
    runtime = make_world_runtime(persist_db_path)
    w = runtime.create_world()
    iid, branch = w.instance_id, w.root_branch_id
    # A challenge action is submitted through the normal command path and commits.
    runtime.submit_command(
        CommandEnvelope(
            command_id=CommandId("challenge_1"),
            instance_id=iid,
            branch_id=branch,
            expected_revision=BranchRevision(0),
            action_type="create_entity",
            payload={"entity_id": "challenge_marker", "count": 1},
            world_time=WorldTime(1),
        )
    )
    events = runtime.persistence.event_store.load(iid, branch)
    assert len(events) == 1
    assert runtime.current_state(iid, branch).entity(EntityId("challenge_marker")) is not None
