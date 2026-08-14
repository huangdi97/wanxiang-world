"""G32C: Actor capability / persona evolution separation."""

from __future__ import annotations

import pytest
from wanxiang_domain.ids import EntityId
from wanxiang_substrate.capability.model import CapabilityDelta
from wanxiang_substrate.evolution.actor_evolution import (
    ActorEvolutionTracker,
    PersonaDelta,
)

ACTOR = EntityId("actor_lin")


@pytest.mark.unit
def test_skill_gain_does_not_change_persona_hash() -> None:
    tracker = ActorEvolutionTracker(ACTOR)
    tracker.apply_persona(
        PersonaDelta(
            actor_id=ACTOR, trait="temperament", to_value="melancholic", rationale="baseline"
        )
    )
    persona_before = tracker.state.persona_hash()
    tracker.apply_capability(
        CapabilityDelta(
            actor_id=ACTOR,
            capability="calligraphy",
            level_delta=1,
            mastery_delta=0.2,
            confidence_delta=0.1,
            reason="practiced",
            evidence_refs=("ref://practice",),
        )
    )
    # Skill gain changes capability but never the persona.
    assert tracker.state.persona_hash() == persona_before
    assert tracker.state.capability_hash() != ""
    assert tracker.state.trait("temperament") == "melancholic"


@pytest.mark.unit
def test_explicit_persona_delta_changes_persona() -> None:
    tracker = ActorEvolutionTracker(ACTOR)
    before = tracker.state.persona_hash()
    tracker.apply_persona(
        PersonaDelta(actor_id=ACTOR, trait="resolve", to_value="steadfast", rationale="after trial")
    )
    assert tracker.state.persona_hash() != before
    assert tracker.state.trait("resolve") == "steadfast"


@pytest.mark.unit
def test_long_term_persona_change_has_event_chain() -> None:
    tracker = ActorEvolutionTracker(ACTOR)
    for i, value in enumerate(("cautious", "reserved", "guarded"), start=1):
        tracker.apply_persona(
            PersonaDelta(actor_id=ACTOR, trait="trust", to_value=value, rationale=f"event {i}"),
            provenance_ref=f"persona://event_{i}",
        )
    kinds = [e.kind for e in tracker.state.trajectory]
    assert kinds == ["persona", "persona", "persona"]
    assert [e.provenance_ref for e in tracker.state.trajectory] == [
        "persona://event_1",
        "persona://event_2",
        "persona://event_3",
    ]
    assert tracker.state.trait("trust") == "guarded"


@pytest.mark.unit
def test_trajectory_provenance_mixes_capability_and_persona() -> None:
    tracker = ActorEvolutionTracker(ACTOR)
    tracker.apply_capability(
        CapabilityDelta(
            actor_id=ACTOR,
            capability="calligraphy",
            level_delta=1,
            mastery_delta=0.1,
            confidence_delta=0.1,
            reason="practice",
        ),
        provenance_ref="cap://practice_1",
    )
    tracker.apply_persona(
        PersonaDelta(
            actor_id=ACTOR, trait="temperament", to_value="melancholic", rationale="baseline"
        ),
        provenance_ref="persona://baseline",
    )
    assert [e.kind for e in tracker.state.trajectory] == ["capability", "persona"]
    assert tracker.state.trajectory[0].provenance_ref == "cap://practice_1"
    assert tracker.state.trajectory[1].provenance_ref == "persona://baseline"
