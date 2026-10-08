"""G91F: Quest is a committed-evidence projection, not truth."""

from __future__ import annotations

import pytest
from wanxiang_substrate.reality.challenge import Opportunity
from wanxiang_substrate.reality.quest import (
    CommittedStateEvidence,
    QuestObjective,
    QuestProjectionAdapter,
    QuestProjectionError,
)


def _opportunity() -> Opportunity:
    return Opportunity(
        opportunity_id="opp_bridge",
        kind="challenge",
        condition="bridge_open",
        score=0.7,
        at_ticks=1,
        evidence_refs=("event:bridge_opened",),
        world_state_refs=("state:bridge",),
    )


def test_quest_progress_comes_from_committed_refs_and_optional_objectives() -> None:
    projection = QuestProjectionAdapter().project(
        _opportunity(),
        CommittedStateEvidence(event_refs=("event:bridge_opened",)),
        optional_objectives=(
            QuestObjective("optional:report", "Write report", "event:report_saved", optional=True),
        ),
    )
    assert projection.progress == 1.0
    assert projection.status == "ready"
    assert projection.objectives[0].completed is True
    assert projection.objectives[1].completed is False
    assert projection.projection_only is True


def test_narrative_text_cannot_fake_progress() -> None:
    adapter = QuestProjectionAdapter()
    with pytest.raises(QuestProjectionError):
        adapter.project(
            _opportunity(),
            CommittedStateEvidence(),
            narrative_text="The bridge is open, therefore complete.",
        )
    empty = adapter.from_opportunity(_opportunity())
    assert empty.progress == 0.0
    assert empty.status == "active"


def test_ignored_opportunity_stays_ignored_in_projection() -> None:
    from wanxiang_substrate.reality.challenge import OpportunityLifecycle

    lifecycle = OpportunityLifecycle()
    eligible = lifecycle.mark_eligible(_opportunity(), actor_id="alice", at_ticks=1)
    ignored = lifecycle.ignore(eligible, decision_ref="decision:ignored")
    projection = QuestProjectionAdapter().from_opportunity(
        ignored, committed_event_refs=("event:bridge_opened",)
    )
    assert projection.status == "ignored"
    assert not hasattr(projection, "commit")
