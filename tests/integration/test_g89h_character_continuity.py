"""G89H: source-created multi-actor seven-day continuity qualification."""

from __future__ import annotations

from typing import cast

import pytest
from scripts.reference_runtime import build_reference_runtime
from wanxiang_domain.ids import EntityId, WorldInstanceId
from wanxiang_substrate.actor_continuity import (
    ContinuityQualificationSeed,
    SevenDayContinuityQualification,
)
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def source() -> SourceRecord:
    content = (
        "# Chapter One\nCharacter: Alice\nCharacter: Bob\n"
        "Alice kept watch at the gate.\nBob carried the letter.\n"
        "relationship: Alice -> Bob\nrule: witnesses remember shared events\n"
    )
    return SourceRecord(
        source_id="g89h_literary_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g89h_literary_source",
        stage="E3",
        rights=RightsEnvelope(owner="qualification", usage="qualification", approved=True),
        payload=content,
        provenance="synthetic:g89h",
        access="private",
    )


@pytest.mark.integration
def test_source_created_multi_actor_seven_day_leave_reenter_replay() -> None:
    authored = OneClickAuthoring().run("job_g89h_continuity", (source(),), profile="book")
    runtime = build_reference_runtime()
    playable = PlayableService(runtime)
    profile = playable.register_package(authored.package, owner_id="owner_g89h")
    alice = playable.entry.create_character(
        "owner_g89h",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_alice",
    )
    bob = playable.entry.create_character(
        "owner_g89h",
        "Bob",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="ent_bob",
    )
    entered_alice = playable.enter(
        profile.profile_id,
        viewer_id="owner_g89h",
        mode="embodiment",
        session_id="g89h_alice_session",
        character_id=alice.character_id,
    )
    entered_bob = playable.enter(
        profile.profile_id,
        viewer_id="owner_g89h",
        mode="embodiment",
        session_id="g89h_bob_session",
        character_id=bob.character_id,
    )
    alice_state = cast(dict[str, object], entered_alice["state"])
    assert len(cast(list[object], alice_state["entities"])) >= 2
    assert profile.world_package_ref == authored.package.package_id
    alice_instance = str(cast(dict[str, object], entered_alice["instance"])["instance_id"])
    bob_instance = str(cast(dict[str, object], entered_bob["instance"])["instance_id"])
    left = playable.leave(alice_instance, viewer_id="owner_g89h")
    continued = playable.continue_instance(alice_instance, viewer_id="owner_g89h")
    assert left["status"] == "left"
    assert cast(dict[str, object], continued["instance"])["instance_id"] == alice_instance

    qualification = SevenDayContinuityQualification(
        ContinuityQualificationSeed(
            source_package_ref=profile.world_package_ref,
            world_instance_refs=(alice_instance, bob_instance),
            actor_ids=(EntityId(alice.character_id), EntityId(bob.character_id)),
            days=7,
            ticks_per_day=24,
            seed=89,
        )
    )
    result = qualification.run()
    assert result.days_completed >= 7
    assert len(result.actor_ids) == 2
    assert len(result.world_instance_refs) == 2
    assert result.memory_count >= result.days_completed * len(result.actor_ids)
    assert result.goal_revision_count >= result.days_completed * len(result.actor_ids)
    assert result.belief_revision_count >= result.days_completed * len(result.actor_ids)
    assert result.relationship_revision_count >= result.days_completed
    assert result.replay_equal
    assert result.leave_reenter_equal
    assert result.final_digest == result.to_dict()["final_digest"]
    assert WorldInstanceId(alice_instance).value.startswith("prv_")
