"""G94B: repeated detection reads the actual playable committed stream."""

from __future__ import annotations

import pathlib
from typing import cast

import pytest
from tests.conftest import make_world_runtime
from wanxiang_domain.ids import BranchId, EntityId, WorldInstanceId
from wanxiang_runtime.resolver import ResolverRegistry
from wanxiang_runtime.state import InMemoryCanonicalState
from wanxiang_substrate.authoring.one_click import OneClickAuthoring
from wanxiang_substrate.evolution.pattern_detector import RepeatedPatternDetector
from wanxiang_substrate.evolution.pattern_detector_model import RepeatedPatternPolicy
from wanxiang_substrate.evolution.pattern_observation import PatternObservationStore
from wanxiang_substrate.playable import PlayableService
from wanxiang_substrate.preview.runtime import register_preview_resolvers
from wanxiang_substrate.sources.model import RightsEnvelope, SourceRecord, payload_hash


def _source() -> SourceRecord:
    content = (
        "# G94B Detector Town\nCharacter: Alice\nCharacter: Bob\n"
        "Alice keeps watch at the gate. Bob carries the letter.\n"
        "relationship: Alice -> Bob\nrule: repeated duties are observable\n"
    )
    return SourceRecord(
        source_id="g94b_detector_source",
        kind="text",
        content_hash=payload_hash(content),
        content_ref="memory://g94b_detector_source",
        stage="E3",
        rights=RightsEnvelope(
            owner="qualification",
            usage="qualification",
            approved=True,
            package_inclusion_allowed=True,
            public_export_allowed=True,
            training_allowed=False,
        ),
        payload=content,
        provenance="synthetic:g94b",
        access="private",
    )


def _register(registry: ResolverRegistry) -> None:
    register_preview_resolvers(registry)


def _actor_ids(state: InMemoryCanonicalState) -> dict[str, str]:
    found: dict[str, str] = {}
    for entity in state.entities():
        for component in entity.components.values():
            if component.component_type == "profile":
                value = component.fields.get("display_name")
                if isinstance(value, str):
                    found[value] = entity.entity_id.value
    return found


@pytest.mark.integration
def test_detector_uses_real_committed_events_without_mutating_runtime(
    persist_db_path: pathlib.Path,
) -> None:
    source = _source()
    package = OneClickAuthoring().run("job_g94b_detector", (source,), profile="book").package
    assert package.evidence_coverage > 0.0
    runtime = make_world_runtime(persist_db_path, extra_resolvers=_register)
    playable = PlayableService(runtime)
    profile = playable.register_package(package, owner_id="g94b_owner", visibility="private")
    character = playable.entry.create_character(
        "g94b_owner",
        "Alice",
        compatible_profile_ids=(profile.experience_package_ref,),
        character_id="character_g94b_alice",
    )
    entered = playable.enter(
        profile.profile_id,
        viewer_id="g94b_owner",
        mode="embodiment",
        session_id="session_g94b_alice",
        character_id=character.character_id,
    )
    instance = WorldInstanceId(str(cast(dict[str, object], entered["instance"])["instance_id"]))
    branch = BranchId(playable.store.get_instance(instance.value).branch_id)
    alice = EntityId(_actor_ids(runtime.current_state(instance, branch))["Alice"])
    for status in ("watching", "watching", "watching"):
        playable.action(
            instance.value,
            viewer_id="g94b_owner",
            action_type="set_status",
            payload={"entity_id": alice.value, "status": status},
        )

    before = runtime.current_state(instance, branch)
    events = runtime.events(instance, branch)
    store = PatternObservationStore.rebuild(events, window_size=100)
    policy = RepeatedPatternPolicy(
        minimum_occurrences=3,
        minimum_windows=1,
        minimum_support=1.0,
        maximum_counterexample_rate=0.0,
        minimum_confidence=0.8,
    )
    detections = RepeatedPatternDetector(policy).detect(store)
    status_detection = next(item for item in detections if item.key == "entity.update:status")
    assert status_detection.qualified is True
    assert set(status_detection.event_refs).issubset({event.event_id.value for event in events})
    assert runtime.current_state(instance, branch).semantic_hash() == before.semantic_hash()
    assert (
        runtime.restore_and_replay(instance, branch).state.semantic_hash() == before.semantic_hash()
    )
